targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Azure OpenAI API Key')
@secure()
param azureOpenaiApiKey string

@description('Azure Search Admin Key')
@secure()
param azureSearchAdminKey string

@description('Tavily API Key')
@secure()
param tavilyApiKey string

// Optional parameters
param appServicePlanName string = ''
param appServiceName string = ''
param resourceGroupName string = ''

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

// App Service Plan
module appServicePlan './modules/appServicePlan.bicep' = {
  name: 'appServicePlan'
  scope: rg
  params: {
    name: !empty(appServicePlanName) ? appServicePlanName : '${abbrs.webServerFarms}${resourceToken}'
    location: location
    tags: tags
    sku: {
      name: 'B1'
      tier: 'Basic'
    }
  }
}

// App Service for Deep Research Agent
module appService './modules/appService.bicep' = {
  name: 'appService'
  scope: rg
  params: {
    name: !empty(appServiceName) ? appServiceName : '${abbrs.webSitesAppService}${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': 'web' })
    appServicePlanId: appServicePlan.outputs.id
    runtimeName: 'python'
    runtimeVersion: '3.12'
    appSettings: {
      // Azure OpenAI Configuration from .env
      AZURE_OPENAI_API_KEY: azureOpenaiApiKey
      AZURE_OPENAI_ENDPOINT: 'https://kdeastus2aoai.openai.azure.com/'
      AZURE_OPENAI_API_VERSION: '2025-01-01-preview'
      // Model deployments from .env file
      AZURE_GPT41_DEPLOYMENT: 'gpt-4.1'
      AZURE_GPT41_MINI_DEPLOYMENT: 'gpt-4.1'
      AZURE_O3_DEPLOYMENT: 'o3'
      AZURE_EMBEDDING_DEPLOYMENT: 'text-embedding-3-large'
      // Azure Search Configuration from .env
      AZURE_SEARCH_API_KEY: azureSearchAdminKey
      AZURE_SEARCH_ENDPOINT: 'https://kd-genai-demo.search.windows.net'
      AZURE_SEARCH_INDEX_NAME: 'deep-research1'
      // Tavily API Configuration from .env
      TAVILY_API_KEY: tavilyApiKey
      TAVILY_MAX_RESULTS: '10'
      TAVILY_MAX_RETRIES: '3'
      // Logging Configuration from .env
      LOG_LEVEL: 'INFO'
      DEBUG_MODE: 'false'
      // Azure App Service specific settings
      SCM_DO_BUILD_DURING_DEPLOYMENT: 'true'
      WEBSITE_HTTPLOGGING_RETENTION_DAYS: '7'
    }
  }
}

// App Service outputs
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_SUBSCRIPTION_ID string = subscription().subscriptionId

output AZURE_RESOURCE_GROUP string = rg.name
output SERVICE_WEB_IDENTITY_PRINCIPAL_ID string = appService.outputs.identityPrincipalId
output SERVICE_WEB_NAME string = appService.outputs.name
output SERVICE_WEB_URI string = appService.outputs.uri