@description('The name of the App Service Plan')
param name string

@description('The location into which the resources should be deployed')
param location string

@description('The SKU of the App Service Plan')
param sku object = {
  name: 'B1'
  tier: 'Basic'
}

@description('Tags to apply to the App Service Plan')
param tags object = {}

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: name
  location: location
  tags: tags
  sku: sku
  properties: {
    reserved: true // Set to true for Linux plans
  }
}

output id string = appServicePlan.id
output name string = appServicePlan.name
