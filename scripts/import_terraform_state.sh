#!/bin/bash

# Import App Configuration.
terraform import azurerm_app_configuration.app_configuration /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.AppConfiguration/configurationStores/xledger-syncronizer-state-dev

# Import Storage Account for the function app.
terraform import azurerm_storage_account.app_storage_account /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Storage/storageAccounts/syncronizerstoragedev

# Import Service Plan for funciton app.
terraform import azurerm_service_plan.service_plan /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Web/serverFarms/xledeger-syncronizer-asp-dev

# Import Application Insights for function app.
terraform import azurerm_application_insights.application_insights /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Insights/components/xledger-syncronizer-ai-dev

# Import Linux Function App.
terraform import azurerm_linux_function_app.function_app /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Web/sites/xledger-syncronizer-dev

# Import Role Assignment for DDBI Storage Container Access.
terraform import azurerm_role_assignment.storage_container_access /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Storage/storageAccounts/ddbistorage/blobServices/default/containers/xledger-dev/providers/Microsoft.Authorization/roleAssignments/ab285942-f789-019f-e3c1-b1dadd1c0d38

# Import Role Assignment for App Configuration Access.
terraform import azurerm_role_assignment.app_configuration_access /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.AppConfiguration/configurationStores/xledger-syncronizer-state-dev/providers/Microsoft.Authorization/roleAssignments/a9f8a22a-415c-9f2b-dd91-5cb452fd8334
