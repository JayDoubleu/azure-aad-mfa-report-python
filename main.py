import sys
import asyncio
from datetime import datetime
import logging
from helpers import (
    set_headers,
    get_tenant,
    get_azure_credentials,
    get_aad_users,
    get_auth_user_details,
    xlsx_dict_prep,
    generate_xlsx,
    handle_custom_ssl,
)

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT = "https://graph.microsoft.com"


def main():
    # Handle custom SSL CA injection to certifi in venv
    handle_custom_ssl()
    # Set authentication headers using Azure CLI profile.
    logger.info("Authenticating using azure cli ..")
    headers = set_headers(get_azure_credentials(DEFAULT_ENDPOINT))
    tenant = get_tenant(headers)
    logger.info(f'Tenant ID: {tenant["id"]}')
    logger.info(f'Tenant Name: {tenant["displayName"]}\n')

    # Get mfa user registration report.
    logger.info("Retrieving user authentication registration report ...")
    auth_user_details = {
        user["id"]: user
        for user in get_auth_user_details(
            # graph.microsoft.com requires additional permissions
            # using graph.windows.net instead.
            headers,
            "https://graph.windows.net",
            api_version="beta",
        )
    }
    logger.info(
        f"Retrieved {len(auth_user_details)} "
        "user authentication registration records ...\n"
    )

    # Parallel query (Azure AD) user account details with minimal $select query.
    # https://docs.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-beta#properties
    logger.info("Retrieving user details ...")
    user_query_details = [
        "signInActivity",
        "accountEnabled",
        "onPremisesSyncEnabled",
        "creationType",
        "userType",
        "externalUserState",
        "externalUserStateChangeDateTime",
    ]
    # Handle asyncio on win32 systems.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    aad_users_details = {
        user["id"]: user
        for user in asyncio.run(
            get_aad_users(
                headers,
                DEFAULT_ENDPOINT,
                list(auth_user_details.keys()),
                user_query_details,
                api_version="beta",
            )
        )
    }
    logger.info(f"Retrieved {len(aad_users_details)} user details records ...\n")

    # Merge mfa user registration details with user account details.
    user_details_merged = [
        {**auth_user_details[user_id], **aad_users_details[user_id]}
        for user_id in auth_user_details.keys()
    ]

    # Prepare dictionary for XLSX converstion.
    xlsx_data = xlsx_dict_prep(user_details_merged)

    # Convert data to XLSX.
    timestamp = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    tenant_name = tenant["displayName"].replace(" ", "_").lower()
    filename = f"mfa_report_{tenant_name}_{timestamp}.xlsx"
    logger.info(f"Generating XLSX report file {filename }...")
    generate_xlsx(xlsx_data, "MFA Report", "TableStyleMedium9", filename)
    logger.info("Done.")


if __name__ == "__main__":
    main()
