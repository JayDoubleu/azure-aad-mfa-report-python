# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Azure AD MFA Report generator written in Python. It uses Azure CLI authentication to connect to Azure AD/Microsoft Graph API and generates an Excel report showing MFA registration status for all users in a tenant.

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies (requires Poetry)
poetry install --no-dev

# Install development dependencies 
poetry install

# Select Python version if multiple installed
poetry env use python3.9
```

### Running the Application
```bash
# Login to Azure CLI first
az login

# Run the MFA report generator
poetry run mfa_report
```

### Code Quality Tools
```bash
# Format code with Black
poetry run fmt

# Run linting with flake8
poetry run flake8

# Type checking with mypy
poetry run mypy .

# Run tests
poetry run pytest
```

## Architecture Overview

### Core Components

1. **main.py** - Entry point that orchestrates the entire MFA report generation:
   - Handles SSL certificate configuration
   - Authenticates using Azure CLI credentials
   - Retrieves MFA registration details from graph.windows.net
   - Fetches user account details from graph.microsoft.com
   - Merges data and generates Excel report

2. **helpers.py** - Contains all utility functions:
   - `handle_custom_ssl()` - Injects custom CA certificates for SSL proxy environments
   - `get_azure_credentials()` - Gets Azure CLI credentials
   - `get_auth_user_details()` - Fetches MFA registration data
   - `get_aad_users()` - Async parallel fetching of user details
   - `xlsx_dict_prep()` - Prepares data for Excel export
   - `generate_xlsx()` - Creates the Excel report file

### Key Technical Details

- Uses two different Microsoft Graph endpoints:
  - `graph.windows.net` (beta API) for MFA registration details
  - `graph.microsoft.com` (beta API) for user account details
- Implements async/parallel requests using aiohttp for performance
- Handles Windows AD vs Azure AD accounts differently
- Supports custom SSL certificates via certificate.pem file
- Generates timestamped Excel reports with formatted tables

### Dependencies

- Azure CLI authentication via `azure-cli-core`
- Async HTTP requests with `aiohttp`
- Excel generation using `openpyxl`
- SSL certificate handling through `certifi`