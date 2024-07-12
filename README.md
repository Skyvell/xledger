## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Running the Application](#running-the-application)
5. [Usage](#usage)
    - [API Endpoints](#api-endpoints)
    - [GraphQL Queries](#graphql-queries)
    - [File Outputs](#file-outputs)
6. [Deployment](#deployment)
    - [Development Environment](#development-environment)
    - [Production Environment](#production-environment)
7. [Infrastructure](#infrastructure)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact](#contact)


## Overview
Data Ductus is migrating from Brilliant to Xledger as a business system. The data stored with Xledger is needed for internal business analytics. This app will fetch the necessary business data from Xledger's GraphQL API and write the data to a Data Lake as .parquet files. This raw data will be transformed and loaded into a structure more suitable for business analytics, but that is not within the scope of this application. The scope of this application is to produce and keep the raw data synchronized in the Data Lake. The application is built on Azure serverless infrastructure.

## Features
- **Timesheets**: Perform a full load of all timesheets data and keep it synchronized.
Time reported by Data Ductus employees.

- **Projects**: Perform a full load of all projects data and keep it synchronized.
All information about ongoing projects. 

- **Employees**: Perform a full load of all employees' data and keep it synchronized.
Employee information such as general information about each employee etc.

- **Customers**: Perform a full load of all customers' data and keep it synchronized.
Information about all Data Ductus customers. General information, contact information etc.

- **ap_transactions**:
Short for "accounts payable transactions". These are invoices that sent to Data Ductus.
The transactions consists of travel invoices for Data Ductus employees and invoices from suppliers.

- **ar_transactions**:
Short for "accounts recievable transactions". Consists of invoices sent to Data Ductus customers.

- **transactions**: Perform a full load of all customers' data and keep it synchronized.
Corresponds to "huvudbokstransaktioner" in Xledger.

## Architecture

The app is developed as a function app in Azure (Figure 1). It will consist of several Azure functions and associated triggers. Each function will be responsible for fetching and keeping a particular type of data synchronized in the Data Lake. For example, one function will be responsible for timesheets data, and another one for projects data. An App Configuration component will be used to store the state of the synchronization.

![Azure architecture](https://dev.azure.com/dataductusddbi/ddbi/_apis/git/repositories/xledger/items?path=/architecture/azure_architecture.png&api-version=6.0&resolveLfs=true)

*Figure 1: High-level architecture showing the flow of data from timers to Azure Functions and the Data Lake. The illustration only shows one function, but the function app will have a timer and function for each type of business data.*

## Adding support for new business data
Depending on which queries are available the procedure will vary a bit. If the query has a deltas query, no custom code will need to be written.

1. Go to the Xledger GraphQL API.
2. Construct the queries needed for getting the data.

## Usage

### Endpoint

### GraphQL queries

### File outputs
The files are written to a Datalake. When performing a full load of all the data, all data is written to one file. Next time when data is syncronized, changes will be in a new file. Files are named in a standardised nammed. Here are a few examples:
<pre>
<code>
`20240610_11_47_40_employees.parquet`
`20240610_15_39_09_employees.parquet`
`20240610_15_40_22_employees.parquet`
`20240610_11_47_34_customers.parquet`
`20240610_15_40_38_customers.parquet`
`20240611_13_27_39_customers.parquet`
</code>
</pre>

Question/thought: Maybe full load files should be named differently. Maybe syncronization or full_load should be prefixed.

## Deployment
1. Configure terraform backend.
Terraform stores the state in a storage account. This has to be configured manually. Decide where you want the statefiles. Create a storage account with a container for both dev and prod. Then configure the backend.tf files in both infrastructure/dev and infrastructure/prod.
2. Configure Service Principal.
The infrastructure is deployed via a service principal. Make sure it is set up and make sure all the needed enviroment variables are imported into the deployment pipeline.
3. Configure API-keys.
API-keys are fetched in the deployment pipeline from variable groups. Make sure they are present.
4. Configure 
    


### Development

### Production

## Infrastructure
The infrastructure is defined in terraform. It's deployed as part of the azure devops pipeline. But it you need to deploy it manually:

```bash
# Cd into either the infrastructure.
cd ./infrastructure/dev

# Initialize the Terraform working directory.
terraform init

# Apply the Terraform configuration
terraform apply
```


## Testing

## License

## Contacts
