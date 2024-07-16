# Xledger Syncronizer

## Overview
Data Ductus is migrating from Brilliant to Xledger as a business system. The data stored with Xledger is needed for internal business analytics. This app will fetch the necessary business data from Xledger's GraphQL API and write the data to a Data Lake as .parquet files. This raw data will be transformed and loaded into a structure more suitable for business analytics, but that is not within the scope of this application. The scope of this application is to produce and keep the raw data synchronized in the Data Lake. The application is built on Azure serverless infrastructure.

## Architecture

The app is developed as a function app in Azure (Figure 1). It consist of several Azure functions and associated triggers. Each function will be responsible for fetching and keeping a particular type of data synchronized in the Data Lake. For example, one function will be responsible for timesheets data, and another one for projects data. An App Configuration component will be used to store the state of the synchronization. All data will be written to ddbistorage account.

![Azure architecture](https://dev.azure.com/dataductusddbi/ddbi/_apis/git/repositories/xledger/items?path=/architecture/azure_architecture.png&api-version=6.0&resolveLfs=true)

*Figure 1: High-level architecture showing the flow of data from timers to Azure Functions and the Data Lake. The illustration only shows one function, but the function app will have a timer and function for each type of business data.*

## Features

### Data Extraction and Synchronization

#### Timesheets
Performs a full load of all timesheets data using the *timesheets* endpoint. After a full data load, only new data is retrieved using a combination of the *timesheet_deltas* endpoint and *timesheets* endpoint. The data includes time reported by Data Ductus employees.

#### Projects
Performs a full load of all projects data using the *projects* endpoint. After a full data load, only new data is retrieved using a combination of the *project_deltas* endpoint and *projects* endpoint. The data includes information on ongoing projects for Data Ductus.

#### Employees
Performs a full load of all employee data using the *employees* endpoint. After a full data load, only new data is retrieved using a combination of the *employee_deltas* endpoint and *employees* endpoint. The data includes information on all Data Ductus employees such as contact information, employment type, salary group, etc.

#### Customers
Performs a full load of all customers data using the *customers* endpoint. After a full data load, only new data is retrieved using a combination of the *customer_deltas* endpoint and *customers* endpoint. The data includes information on all Data Ductus customers such as company name, contact information, etc.

#### Suppliers
Performs a full load of all suppliers data using the *suppliers* endpoint. After a full data load, only new data is retrieved using a combination of the *supplier_deltas* endpoint and *suppliers* endpoint. The data includes information on all Data Ductus suppliers such as company name, contact information, etc.

#### Transactions
Performs a full load of all transactions data using the *transactions* endpoint. After a full data load, only new data is retrieved using a combination of the *transaction_deltas* endpoint and *transactions* endpoint. The data includes all invoices, both incoming and outgoing, for Data Ductus. It corresponds to "Huvudbokstransaktioner" in Xledger.

#### ArTransactions (Accounts Receivable Transactions)
Performs a full load of all artransactions data using the *arTransactions* endpoint. After a full data load, only new data is retrieved using a combination of the *arTransaction_deltas* endpoint and *arTransactions* endpoint. These transactions are invoices sent from Data Ductus to external entities (e.g. invoices to customers). 

#### ApTransactions (Accounts Payable Transactions)
Performs a full load of all aptransactions data using the *apTransactions* endpoint. After a full data load, only new data is retrieved using a combination of the *apTransaction_deltas* endpoint and *apTransactions* endpoint. These transactions are invoices sent to Data Ductus (e.g., invoices from suppliers or travel expenses from employees).

## Adding support for more data
Go to Xledger and look for the right endpoint for your data (*https://demo.xledger.net/GraphQL*). 
If your data has endpoints that has support for deltas (e.g. timesheet_deltas, employee_deltas), then you can do both full syncronizations and syncronize changes over time. Otherwise you can only do a full syncronization every time the function is triggered. Once you have a query you are happy with on Xledger, just copy the node fields and create a new function that follows the same template as the existing functions in the function folder. You can copy almost all the code.

## Api Keys
API keys for dev and prod environments are generated in an Xledger account. Administrator access is needed. Api keys are stored within variable groups in the azure devops pipeline and deployed within the pipeline. Upon expiry these keys will need to be changed to keep the app upp and running.

## Data output
The files are written to a Datalake in ddbistorage account. Depending on which environment is used, the data will be written to the container xledger-dev or xledger-prod. There will be two types of files; either full_sync or sync_changes. The full_sync files contain a full syncronization. Sync_changes only fetch the items that have changed since the last full syncronization. The files will be organized in containers (folders), one folder for each busniess data type. 

Below is an illustration of the files format and file structure.
```
`timesheets/full_sync-20240711_21_17_09-timesheets.parquet`
`timesheets/sync_changes-20240712_21_17_09-timesheets.parquet`
`projects/full_sync-20240711_21_17_09-projects.parquet`
`projects/sync_changes-20240712_21_17_09-projects.parquet`
```
    
## Deployment

### Infrastructure
The infrastructure is defined in terraform. It's deployed as part of the azure devops pipeline. To deploy it manually:

```bash
# Cd into either the infrastructure.
cd ./infrastructure/dev

# Initialize the Terraform working directory.
terraform init

# Apply the Terraform configuration
terraform apply
```

### Function App
The function app is also deployed as part of the azure devops pipeline.

## KEEP?
## Deployment
1. Configure terraform backend.
Terraform stores the state in a storage account. This has to be configured manually. Decide where you want the statefiles. Create a storage account with a container for both dev and prod. Then configure the backend.tf files in both infrastructure/dev and infrastructure/prod.
2. Configure Service Principal.
The infrastructure is deployed via a service principal. Make sure it is set up and make sure all the needed enviroment variables are imported into the deployment pipeline.
3. Configure API-keys.
API-keys are fetched in the deployment pipeline from variable groups. Make sure they are present.
4. Configure 
