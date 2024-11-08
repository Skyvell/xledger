# Xledger Synchronizer

## Overview
Data Ductus is migrating from Brilliant to Xledger as a business system. The data stored in Xledger is needed for internal business analytics. This app will fetch the necessary business data from Xledger's GraphQL API and write the data to a Data Lake as .parquet files. This raw data will be transformed and loaded into a structure more suitable for business analytics, but that is outside the scope of this application. The focus of this application is to produce and keep the raw data synchronized in the Data Lake. The application is built on Azure serverless infrastructure.

## Architecture

The app is developed as a function app in Azure (Figure 1). It consists of several Azure functions and associated triggers. Each function is responsible for fetching and keeping a particular type of data synchronized in the Data Lake. For example, one function handles timesheet data, while another handles project data. An App Configuration component is used to store the state of the synchronization. All data is written to the ddbistorage account.

![Azure architecture](https://dev.azure.com/dataductusddbi/ddbi/_apis/git/repositories/xledger/items?path=/architecture/azure_architecture.png&api-version=6.0&resolveLfs=true)

*Figure 1: High-level architecture showing the flow of data from timers to Azure Functions and the Data Lake. The illustration only shows one function, but the function app will have a timer and function for each type of business data.*

## Features

### Data Extraction and Synchronization

#### Timesheets
Performs a full load of all timesheet data using the *timesheets* endpoint. After a full data load, only new data is retrieved using a combination of the *timesheet_deltas* and *timesheets* endpoints. The data includes time reported by Data Ductus employees.

#### Projects
Performs a full load of all project data using the *projects* endpoint. After a full data load, only new data is retrieved using a combination of the *project_deltas* and *projects* endpoints. The data includes information on ongoing projects for Data Ductus.

#### Employees
Performs a full load of all employee data using the *employees* endpoint. After a full data load, only new data is retrieved using a combination of the *employee_deltas* and *employees* endpoints. The data includes information on all Data Ductus employees, such as contact information, employment type, salary group, etc.

#### Customers
Performs a full load of all customer data using the *customers* endpoint. After a full data load, only new data is retrieved using a combination of the *customer_deltas* and *customers* endpoints. The data includes information on all Data Ductus customers, such as company name and contact information.

#### Suppliers
Performs a full load of all supplier data using the *suppliers* endpoint. After a full data load, only new data is retrieved using a combination of the *supplier_deltas* and *suppliers* endpoints. The data includes information on all Data Ductus suppliers, such as company name and contact information.

#### Transactions
Performs a full load of all transaction data using the *transactions* endpoint. After a full data load, only new data is retrieved using a combination of the *transaction_deltas* and *transactions* endpoints. The data includes all invoices, both incoming and outgoing, for Data Ductus. It corresponds to "Huvudbokstransaktioner" in Xledger.

#### ArTransactions (Accounts Receivable Transactions)
Performs a full load of all accounts receivable transaction data using the *arTransactions* endpoint. After a full data load, only new data is retrieved using a combination of the *arTransaction_deltas* and *arTransactions* endpoints. These transactions are invoices sent from Data Ductus to external entities (e.g., invoices to customers).

#### ApTransactions (Accounts Payable Transactions)
Performs a full load of all accounts payable transaction data using the *apTransactions* endpoint. After a full data load, only new data is retrieved using a combination of the *apTransaction_deltas* and *apTransactions* endpoints. These transactions are invoices sent to Data Ductus (e.g., invoices from suppliers or travel expenses from employees).

#### Employee Groups
Fetches a table of Employee Groups from Xledger using a Flexlink and writes it to the Data lake.

#### Employment Types
Fetches a table of Employment Types from Xledger using a Flexlink and writes it to the Data lake.

#### Cost Categories
Fetches a table of cost category data from Xledger using a Flexlink and writes it to the Data Lake.

#### Project Cost Setups
Fetches a table of project cost setup data from Xledger using a Flexlink and writes it to the Data Lake.

#### Cost Element Per Time Type
Fetches a table of cost element data per time type using a Flexlink and writes it to the Data Lake.

## Adding Support for More Data in Xledger

### Xledger API Data
Go to Xledger and look for the correct endpoint for your data (*https://demo.xledger.net/GraphQL*). 
If your data has endpoints that support deltas (e.g., timesheet_deltas, employee_deltas), you can perform both full synchronizations and synchronize changes over time. Otherwise, you can only perform a full synchronization each time the function is triggered. Once you have a query you are satisfied with in Xledger, copy the node fields and create a new function following the same template as the existing functions in the function folder. You can reuse most of the code.

### Xledger FlexLink Data Export Guide

#### Steps:

1. **Identify Table**: Select the table in Xledger to export.
2. **Create Export Link**: Click "Create Export Link" and choose Excel format (no parameter refinement needed).
3. **Store FlexLink**: Copy the FlexLink and securely save it in the Azure Pipeline Variable Group:
   - Use separate groups for Dev and Prod.
4. **Add Variable**: Add the variable to `./infrastructure/[dev|prod]/variables.tf`.
5. **Update Configuration**:
   - In `./infrastructure/[dev|prod]/main.tf`, include the variable in `app_settings`.
   - In `./shared/environment_config`, load the variable from the environment.
6. **Deploy Update**: Modify `./templates/deploy_infrastructure.yml` to deploy the app with the new variable.
7. **Write the Function**: Use `./function/employee_groups` as a template to write the function:
   - Copy and adjust the function code as needed.
   - Create a `settings.py` file with the required configuration.

## Xledger authentication
API keys for the dev and prod environments are generated in an Xledger account. Administrator access is required. The demo API keys expire after 2 weeks, so the prod API key is used for both xledger-dev and xledger-prod. API keys are stored within variable groups in the Azure DevOps pipeline and are deployed as environment variable of the function app in the pipeline. Upon expiry, these keys will need to be updated to keep the app running.

## Data Output
The files are written to a Data Lake in the ddbistorage account. Depending on the environment, the data is written to either the xledger-dev or xledger-prod container. There are two types of files: full_sync or sync_changes. Full_sync files contain a complete data synchronization, while sync_changes files contain only the items that have changed since the last full synchronization. The files are organized in containers (folders), one folder per business data type.

Below is an example of the file format and structure:
```
`timesheets/full_sync-20240711_21_17_09-timesheets.parquet`
`timesheets/sync_changes-20240712_21_17_09-timesheets.parquet`
`projects/full_sync-20240711_21_17_09-projects.parquet`
`projects/sync_changes-20240712_21_17_09-projects.parquet`
```

## Deployment

### Authentication
A service connection called "xledger" has been configured in Azure DevOps, pointing to an app registration inside Azure Portal. It was configured using the automated approach in Azure DevOps. Service principal properties are stored in a variable group within the pipeline and are loaded into the pipeline for authentication.

### Infrastructure
The infrastructure is defined in Terraform. An Azure storage account is used as the backend for the state. All deployment variables, backend settings, provider settings, and components can be found in:

`infrastructure/dev` or `infrastructure/prod`.

### Function App
The function app is also deployed as part of the Azure DevOps pipeline.