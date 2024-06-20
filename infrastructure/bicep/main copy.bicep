//param functionAppName string
//param appConfigName string
//param location string = resourceGroup().location
//param keyVaultName string
//
//resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
//  name: keyVaultName
//}
//
//resource appConfig 'Microsoft.AppConfiguration/configurationStores@2022-05-01' = {
//  name: appConfigName
//  location: location
//  sku: {
//    name: 'Standard'
//  }
//  properties: {
//    publicNetworkAccess: 'Enabled'
//  }
//}
//
//resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
//  name: '${functionAppName}-plan'
//  location: location
//  sku: {
//    name: 'Y1'
//    tier: 'Dynamic'
//  }
//}
//
//resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
//  name: functionAppName
//  location: location
//  kind: 'functionapp'
//  identity: {
//    type: 'SystemAssigned'
//  }
//  properties: {
//    siteConfig: {
//      appSettings: [
//        {
//          name: 'APIKey'
//          value: '@Microsoft.KeyVault(SecretUri=https://<your-key-vault-name>.vault.azure.net/secrets/DevApiKey)'
//        },
//        {
//          name: 'AppConfigurationConnectionString'
//          value: '@Microsoft.KeyVault(SecretUri=https://<your-key-vault-name>.vault.azure.net/secrets/DevAppConfigConnectionString)'
//        },
//        {
//          name: 'FilesystemDatalake'
//          value: '@Microsoft.KeyVault(SecretUri=https://<your-key-vault-name>.vault.azure.net/secrets/FilesystemDatalake)'
//        }
//      ]
//    }
//    clientAffinityEnabled: false
//    httpsOnly: true
//  }
//  dependsOn: [
//    appServicePlan,
//    appConfig
//  ]
//}
//
//output appConfigConnString string = listKeys(appConfig.id, '2022-05-01').primaryConnectionString
