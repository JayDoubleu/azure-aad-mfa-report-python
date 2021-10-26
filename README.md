# azure-aad-mfa-report-python

## Prerequisites
Make sure you have installed all of the following prerequisites on your machine:
* Git - [Download & Install Git](https://git-scm.com/downloads).
* Python 3.9 or higher - [Download & Install Python](https://www.python.org/downloads/).
* Azure CLI - [Download & Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
* Poetry - [Download & Install Poetry](https://python-poetry.org/docs/#installation).

## Usage:
- Download contents of this repository and navigate to mfa_report script folder: <br>
  ```shell
  $ git clone https://github.com/JayDoubleu/azure-aad-mfa-report-python.git
  $ cd azure-aad-mfa-report-python
  ```
- If you are behind SSL proxy place your custom CA file in PEM format at the root directory of this repository.
  CA needs to be in PEM format and named "certificate.pem" . 
  Script will try to detect this file and add it to certifi CA store within poetry's virtual environment.
  
- If you have multiple versions of python installed instruct poetry to use correct one: <br>
  `$ poetry env use python3.9`
  
- Install poetry dependencies: <br>
  `$ poetry install`

- Navigate to https://portal.azure.com and login to tenant which you want to run MFA report against.
- Make sure your browser session is signed with MFA if one is enabled.
- Activate PIM role if neccesary.


- Login to azure cli: <br>
  `$ az login`

- Run MFA script:<br>
  ```shell
  $ poetry run mfa_report
  2021-10-24 23:55:03 INFO     	 Authenticating using azure cli ..
  2021-10-24 23:55:04 INFO     	 Tenant ID: <Your tenant GUID>
  2021-10-24 23:55:04 INFO     	 Tenant Name: <Your tenant name>

  2021-10-24 23:55:04 INFO     	 Retrieving user authentication registration report ...
  2021-10-24 23:55:04 INFO     	 Retrieved X user authentication registration records ...

  2021-10-24 23:55:04 INFO     	 Retrieving user details ...
  2021-10-24 23:55:05 INFO     	 Retrieved X user details records ...

  2021-10-24 23:55:05 INFO     	 Generating XLSX report file mfa_report_<tenant name>_20211024_23_55_05.xlsx...
  2021-10-24 23:55:05 INFO     	 Done.
  ```

- If everything went fine you should be able to see generated xlsx report in your current directory

<br>
<div align="center">

| :zap:        Please note, this script is using Microsoft's **beta** API's which are subject to change  |
|--------------------------------------------------------------------------------------------------------|
</div>
<br>

## Report columns explained:

| Column name | Details |
|---|---|
| userId | Account object ID |
| isEnabled | Is account enabled<br>Value can be "Yes" only as Azure MFA registration reports only enabled accounts  |
| userDisplayName | Account display name |
| userPrincipalName | Account UPN |
| isExternal | Is account a "Guest"<br>Values can be "Yes" or "N/A" |
| externalDomain | External account domain name<br>Values can be a DNS name of external domain or "N/A" if account type is "Member" |
| externalUserState | State of external account<br>Values can be "PendingAcceptance", "Accepted" or "N/A" |
| externalUserStateLastChangeUTC | Timestamp of external account last change of state<br>Values can be UTC Datetime or "N/A" |
| tenantDomain | Domain name of user account's tenant. |
| methodsRegistered | MFA methods registered by the account<br>Values can be:<br><br>microsoftAuthenticatorPush<br>softwareOneTimePasscode<br>officePhone<br>mobilePhone<br>email<br><br>OR <br><br>No AAD MFA configured<br><br>Please note that this only shows the MFA user state on the Azure AD tenant.<br>User can be configured with MFA at office.com level and it will not be reflected in this report. |
| onPremisesSyncEnabled | Type of user account<br>Values can be:<br>"Yes" - Windows AD account<br>"No"  - Azure AD account |
| lastInteractiveSignInUTC | Last user's interactive sign in date in UTC<br>Values can be UTC Datetime or "N/A" if never signed in via AAD |
| lastNonInteractiveSignInUTC | Last user's non-interactive sign in date in UTC<br>Values can be UTC Datetime or "N/A" if never signed in via AAD |
