# Deep Research Agent - Azure Deployment Guide

## 🚀 Quick Deployment Commands

### Force Stop All Deployments
```powershell
# Stop all Azure processes
Get-Process | Where-Object {$_.ProcessName -like "*azd*" -or $_.ProcessName -like "*azure*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Force kill any remaining processes
taskkill /f /im azd.exe /t 2>$null; taskkill /f /im az.exe /t 2>$null
```

### Deploy Application
```powershell
# Deploy with Azure Developer CLI
azd deploy --no-prompt

# Alternative: Manual deployment if azd fails
az webapp restart --name [APP-NAME] --resource-group [RG-NAME]
az webapp deployment source config-zip --resource-group [RG-NAME] --name [APP-NAME] --src deploy.zip
```

## 📋 Prerequisites

### 1. Required Tools
- Azure CLI (`az --version`)
- Azure Developer CLI (`azd version`)
- PowerShell (Windows) or Bash (Linux/Mac)

### 2. Environment Setup
```powershell
# Login to Azure
az login
azd auth login

# Set subscription (if multiple)
az account set --subscription "YOUR-SUBSCRIPTION-ID"
```

### 3. Environment Variables
Ensure these are set in your `.env` file:
```env
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
TAVILY_API_KEY=your-tavily-key
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_KEY=your-search-key
```

## 🔧 Deployment Steps

### Step 1: Prepare Environment
```powershell
# Navigate to project directory
cd "C:\Users\kapildhanger\OneDrive - Microsoft\Microsoft_Kapil\Azure_learning\git-repos\Deep-Research-Agents"

# Verify configuration
azd env list
azd env get-values
```

### Step 2: Force Clean Previous Deployments
```powershell
# Stop all running processes
Get-Process | Where-Object {$_.ProcessName -like "*azd*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Clear deployment cache
Remove-Item -Path ".azure\*" -Recurse -Force -ErrorAction SilentlyContinue
```

### Step 3: Initialize Environment (if needed)
```powershell
# Only run if environment doesn't exist
azd env new dpr
azd env select dpr
```

### Step 4: Deploy Infrastructure and Application
```powershell
# Full deployment (infrastructure + app)
azd up --no-prompt

# OR deploy only application (if infrastructure exists)
azd deploy --no-prompt
```

### Step 5: Verify Deployment
```powershell
# Check health endpoint
curl -s https://[APP-NAME].azurewebsites.net/health

# Check application logs
az webapp log tail --name [APP-NAME] --resource-group [RG-NAME]
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Deployment Conflict (409 Error)
```powershell
# Solution: Restart the web app
az webapp restart --name [APP-NAME] --resource-group [RG-NAME]

# Wait and retry
Start-Sleep -Seconds 30
azd deploy --no-prompt
```

#### 2. Build Process Failed
```powershell
# Check startup.txt configuration
Get-Content startup.txt

# Should contain:
# gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:$PORT --timeout 300
```

#### 3. Application Not Starting
```powershell
# Check environment variables in Azure
az webapp config appsettings list --name [APP-NAME] --resource-group [RG-NAME]

# Update if needed
az webapp config appsettings set --name [APP-NAME] --resource-group [RG-NAME] --settings "KEY=VALUE"
```

#### 4. Memory/Performance Issues
```powershell
# Scale up the app service plan
az appservice plan update --name [PLAN-NAME] --resource-group [RG-NAME] --sku B2
```

## 📊 Current Deployment Configuration

### Application Details
- **Name**: Deep Research Agent
- **Type**: Azure App Service (Linux)
- **Runtime**: Python 3.12
- **Framework**: FastAPI + Gunicorn + Uvicorn
- **Port**: Dynamic ($PORT environment variable)

### Resource Group
- **Name**: rgdpr
- **Location**: East US (or configured region)

### Key Features Deployed
- ✅ Multi-agent research system
- ✅ Real-time progress tracking (1.5s polling)
- ✅ Enhanced UI with two-column layout
- ✅ Background task processing
- ✅ Health monitoring endpoints
- ✅ Comprehensive error handling

### Startup Configuration
```txt
gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:$PORT --timeout 300
```

## 🎯 Success Verification

### 1. Health Check
```powershell
curl -s https://[APP-NAME].azurewebsites.net/health
# Expected: {"status":"healthy","service":"Deep Research Agent API","version":"1.0.0"}
```

### 2. Web Interface
- Navigate to: `https://[APP-NAME].azurewebsites.net/`
- Should show: Clean two-column layout with research form and results area

### 3. Functionality Test
- Enter a research query
- Verify real-time progress updates
- Confirm research results display properly

## 📝 Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service endpoint | `https://your-openai.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Authentication key | `abc123...` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | `gpt-4o` |
| `TAVILY_API_KEY` | Web search API key | `tvly-...` |
| `AZURE_SEARCH_ENDPOINT` | Azure Cognitive Search endpoint | `https://your-search.search.windows.net` |
| `AZURE_SEARCH_KEY` | Search service key | `xyz789...` |
| `PORT` | Application port (auto-set by Azure) | `8000` (local), dynamic (Azure) |

## 🔄 Redeployment Process

### Quick Update (Code Changes Only)
```powershell
# Make your code changes, then:
azd deploy --no-prompt
```

### Full Redeployment (Infrastructure + Code)
```powershell
# Warning: This will recreate resources
azd down --purge
azd up --no-prompt
```

### Manual Deployment (Alternative)
```powershell
# Create deployment package
Compress-Archive -Path . -DestinationPath deploy.zip -Force -CompressionLevel Fastest

# Deploy via Azure CLI
az webapp deployment source config-zip --resource-group rgdpr --name [APP-NAME] --src deploy.zip
```

## 📞 Support Commands

### Get Application URL
```powershell
azd env get-values | Select-String "SERVICE_WEB_ENDPOINT_URL"
```

### View Application Logs
```powershell
az webapp log tail --name [APP-NAME] --resource-group rgdpr --provider filesystem
```

### Check Resource Status
```powershell
az resource list --resource-group rgdpr --output table
```

---

## 🏆 Deployment Success Criteria

- [x] Health endpoint returns 200 OK
- [x] Web interface loads correctly
- [x] Real-time progress updates work
- [x] Research functionality completes end-to-end
- [x] No deployment conflicts or errors
- [x] Application starts within expected timeframe

**Last Updated**: August 3, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
