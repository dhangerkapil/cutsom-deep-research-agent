@description('The name of the App Service')
param name string

@description('The location into which the resources should be deployed')
param location string

@description('The App Service Plan ID')
param appServicePlanId string

@description('The runtime name')
param runtimeName string

@description('The runtime version')
param runtimeVersion string

@description('Application settings')
param appSettings object = {}

@description('Tags to apply to the App Service')
param tags object = {}

resource appService 'Microsoft.Web/sites@2022-03-01' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlanId
    siteConfig: {
      linuxFxVersion: 'PYTHON|${runtimeVersion}'
      alwaysOn: true
      ftpsState: 'FtpsOnly'
      minTlsVersion: '1.2'
      appSettings: [for setting in items(appSettings): {
        name: setting.key
        value: setting.value
      }]
      cors: {
        allowedOrigins: ['*']
        supportCredentials: false
      }
    }
    httpsOnly: true
    clientAffinityEnabled: false
  }
}

output id string = appService.id
output name string = appService.name
output uri string = 'https://${appService.properties.defaultHostName}'
output identityPrincipalId string = appService.identity.principalId
