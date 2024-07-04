terraform import azurerm_app_configuration.app_configuration /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.AppConfiguration/configurationStores/xledger-syncronizer-state-dev

terraform import azurerm_storage_account.app_storage_account /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Storage/storageAccounts/syncronizerstoragedev

terraform import azurerm_service_plan.service_plan /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Web/serverFarms/xledeger-syncronizer-asp-dev

terraform import azurerm_application_insights.application_insights /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Insights/components/xledger-syncronizer-ai-dev

terraform import azurerm_linux_function_app.function_app /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.Web/sites/xledger-syncronizer-dev

terraform import azurerm_role_assignment.storage_container_access /subscriptions/a42468e7-3510-409f-849a-111d4574481d/providers/Microsoft.Authorization/roleDefinitions/ba92f5b4-2d11-453d-a403-e96b0029c9fe

terraform import azurerm_role_assignment.app_configuration_access /subscriptions/a42468e7-3510-409f-849a-111d4574481d/resourceGroups/DDBI-ResourceGroup/providers/Microsoft.AppConfiguration/configurationStores/xledger-syncronizer-state-dev/providers/Microsoft.Authorization/roleAssignments/a9f8a22a-415c-9f2b-dd91-5cb452fd8334
