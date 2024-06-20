// Parameters
param functionAppName string
param appConfigName string
param storageAccountName string
param keyVaultName string
param location string = resourceGroup().location
param sku string = 'Standard_LRS'

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2022-11-01' existing = {
  name: resourceGroup().name
}

// App Configuration
resource appConfig 'Microsoft.AppConfiguration/configurationStores@2022-11-01' = {
  name: appConfigName
  location: location
  sku: {
    name: 'Standard'
  }
}

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: sku
  }
  kind: 'StorageV2'
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2022-11-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    accessPolicies: []
  }
}

// Function App
resource functionApp 'Microsoft.Web/sites@2022-11-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-11-01' = {
  name: '${functionAppName}-plan'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
}

// Role Assignments
resource appConfigRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(appConfig.id, 'AppConfigDataOwner')
  scope: appConfig
  properties: {
    principalId: functionApp.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '516239f1-1b23-4d10-8650-6d7b1d7df88d') // App Configuration Data Owner
  }
}

resource storageAccountRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, 'StorageBlobDataContributor')
  scope: storageAccount
  properties: {
    principalId: functionApp.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor
  }
}

resource keyVaultRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, 'KeyVaultSecretsUser')
  scope: keyVault
  properties: {
    principalId: functionApp.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b86a8fe4-44ce-4948-aee5-eccb2c155cd7') // Key Vault Secrets User
  }
}
