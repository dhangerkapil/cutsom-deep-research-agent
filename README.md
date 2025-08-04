# 🔬 Deep Research Agent

Enterprise-grade AI research platform for automated document analysis and intelligent reporting

## 🎯 Overview
The Deep Research Agent represents an advanced multi-agent artificial intelligence framework powered by **Microsoft Semantic Kernel**. Utilizing sophisticated **MagenticOrchestration** technology, this system coordinates multiple AI specialists to autonomously produce comprehensive research outputs from organizational knowledge bases. The platform seamlessly integrates document discovery through Azure AI Search and Semantic Kernel Memory with advanced quality validation to deliver end-to-end enterprise research automation.

### 🌟 Core Capabilities

- **🤖 Intelligent Agent Coordination**: Advanced orchestration using cutting-edge Semantic Kernel technology
- **🔍 Enterprise Document Discovery**: Seamless integration with Azure AI Search and Semantic Kernel Memory
- **🌐 Hybrid Search Technology**: Combines internal knowledge bases with external web research capabilities
- **🧠 Persistent Knowledge Management**: Continuous context preservation via Semantic Kernel Memory integration
- **🛡️ Comprehensive Quality Assurance**: Advanced confidence scoring and multi-tier source validation
- **📝 Professional Report Creation**: Automated generation of evidence-backed reports with complete citation tracking
- **🌐 Cross-Language Support**: Advanced translation capabilities with domain-specific terminology handling
- **⚡ Adaptive Quality Control**: Intelligent monitoring and continuous improvement mechanisms

## 🏗️ System Architecture

The Deep Research Agent leverages a sophisticated multi-agent architecture built on **Microsoft Semantic Kernel** with **MagenticOrchestration** at its core. This design enables complete automation of enterprise research workflows, from document discovery through final report delivery.

### 🎭 Architecture Overview

```
                         ┌─────────────────────────────────┐
                         │   MagenticOrchestration Hub     │
                         │ (StandardMagenticManager Core)  │
                         │    + Enterprise Logic Layer     │
                         └──────────┬──────────────────────┘
                                    │ Intelligent Coordination
                                    ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │                   Multi-Agent Intelligence Network              │
   │                  (Semantic Kernel Foundation)                   │
   │                                                                 │
   │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐    │
   │  │ Research Team   │ │ Quality Control │ │  Knowledge      │    │
   │  │    Leader       │ │    Specialist   │ │  Synthesizer    │    │
   │  │ ┌─────────────┐ │ │ (Source        │ │ (Information    │    │
   │  │ │ANALYST_01   │ │ │ Validation)     │ │  Integration)   │    │
   │  │ │ANALYST_02   │ │ │                 │ │                 │    │
   │  │ │ANALYST_03+  │ │ │                 │ │                 │    │
   │  │ └─────────────┘ │ │                 │ │                 │    │
   │  └─────────────────┘ └─────────────────┘ └─────────────────┘    │
   │                                                                 │
   │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐    │
   │  │ Documentation   │ │ Quality Review  │ │  Language       │    │
   │  │   Specialist    │ │   Coordinator   │ │ Processing      │    │
   │  │ (Evidence +     │ │ (Standards      │ │ (Professional   │    │
   │  │  Confidence)    │ │  Compliance)    │ │  Translation)   │    │
   │  └─────────────────┘ └─────────────────┘ └─────────────────┘    │
   │                                                                 │
   │  ┌─────────────────┐                                            │
   │  │  Reference      │                                            │
   │  │  Management     │                                            │
   │  │ (Citation       │                                            │
   │  │  Tracking)      │                                            │
   │  └─────────────────┘                                            │
   └─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │                  Infrastructure & Plugin Services               │
   │                                                                 │
   │  ┌─────────────────┐ ┌─────────────────┐                        │
   │  │  Knowledge      │ │ Search Engine   │                        │
   │  │  Repository     │ │   Integration   │                        │
   │  │ (Research       │ │ (Azure AI       │                        │
   │  │  Memory)        │ │  Platform)      │                        │
   │  └─────────────────┘ └─────────────────┘                        │
   └─────────────────────────────────────────────────────────────────┘
```

### 🔬 Enterprise Document Discovery Platform

**Advanced Search Integration** delivers powerful information retrieval capabilities:

The platform features a comprehensive Azure AI Search integration that adapts dynamically to project specifications defined in `config/project_config.yaml`. This unified search interface operates across multiple organizational indexes configured through centralized configuration management.

The search architecture demonstrates remarkable flexibility, accommodating diverse enterprise document structures and index configurations. It achieves superior information discovery through the strategic combination of Vector-based search, Semantic understanding, and traditional Full-text indexing methodologies.

#### 🌐 Hybrid Research Capabilities

**Comprehensive Information Gathering**: The platform incorporates advanced web search capabilities to supplement internal knowledge sources:

- **Primary Information Source**: Internal document discovery via Azure AI Search infrastructure
- **Secondary Research Layer**: Automatic web search activation when internal sources prove insufficient
- **Flexible Configuration**: Complete control over web search features through `project_config.yaml` settings
- **Unified Quality Standards**: All external search results undergo identical reliability validation as internal documents

<details>
<summary>

### 🎭 Intelligent Agent Specialization

</summary>

#### 1. **Research Team Leader** 🎯 *Primary Coordinator*
   - **Primary Function**: Orchestrates and manages multiple specialized research sub-agents
   - **Technical Design**: Coordinates 3+ dedicated research units (ANALYST_01, ANALYST_02, ANALYST_03+)
   - **Advanced Features**: Parallel task distribution and simultaneous query processing capabilities
   - **Technical Implementation**: Leverages `ConcurrentOrchestration` and `ParallelResearchPlugin` for agent management
   - **Core Operations**: 
     - Strategic distribution of research tasks across specialized units
     - Intelligent synthesis and consolidation of multi-agent findings
     - Advanced quality control and result harmonization
     - Dynamic scaling of agent resources based on workload requirements
   - **Knowledge Persistence**: Shared context management through Semantic Kernel Memory across all research units

#### 2. **Quality Control Specialist** 🔍 *Reliability Assessment Expert*
   - **Primary Function**: Comprehensive evaluation of source credibility and information coverage
   - **Assessment Framework**: Source authenticity, information consistency, and evidence robustness
   - **Operational Scope**: Gap identification through supplementary research, credibility scoring algorithms
   - **Deliverables**: Detailed reliability assessments with actionable improvement recommendations

#### 3. **Knowledge Synthesizer** 📋 *Information Integration Expert*
   - **Primary Function**: Advanced summarization of extensive organizational document collections
   - **Domain Expertise**: Enterprise-specific content categorization and priority assessment
   - **Technical Capabilities**: Multi-level summarization, intelligent keyword extraction, relevance scoring
   - **Output Generation**: Structured knowledge summaries with key insight identification

#### 4. **Documentation Specialist** ✍️ *Report Creation Expert*
   - **Primary Function**: Professional report generation with integrated confidence assessment
   - **Technical Framework**: Advanced document structuring, citation management, evidence presentation
   - **Quality Metrics**: Multi-dimensional confidence evaluation covering source quality, consistency, and comprehensiveness
   - **Final Products**: Executive-ready reports with comprehensive reliability indicators

#### 5. **Quality Review Coordinator** 🎯 *Standards Compliance Expert*
   - **Primary Function**: Comprehensive validation of report quality and confidence assessment accuracy
   - **Technical Approach**: Meta-analytical evaluation, logical consistency validation, improvement recommendations
   - **Compliance Standards**: Adherence to enterprise research and development quality protocols
   - **Output Generation**: Quality assurance reports with detailed improvement guidance

#### 6. **Language Processing Specialist** 🌐 *Multilingual Expert*
   - **Primary Function**: Professional-grade translation with specialized terminology preservation
   - **Domain Expertise**: Technical documentation format retention, specialized terminology databases
   - **Quality Assurance**: Translation accuracy evaluation, terminology consistency management

#### 7. **Reference Management Specialist** 📚 *Citation Tracking Expert*
   - **Primary Function**: Comprehensive citation management for internal organizational documents
   - **Technical Capabilities**: Automated citation generation, complete source traceability
   - **Validation Process**: Citation accuracy verification, source availability confirmation
   - **Final Deliverables**: Comprehensive citation databases with complete metadata tracking

</details>

## 🚀 Getting Started

### System Requirements

To deploy the Deep Research Agent platform, verify these prerequisites are available:

- **Python Environment** (Version 3.12 or higher recommended: 3.12.10+)
- **Azure OpenAI Services** with appropriate model access:
  - Advanced language models (GPT-4.1, GPT-4.1-mini, o3, or comparable alternatives)
  - Text embedding capabilities (text-embedding-3-small, text-embedding-3-large, and similar)
- **Azure AI Search Infrastructure** configured with:
  - Semantic search functionality activated
  - Vector search capabilities enabled
  - Pre-populated search indexes containing organizational documents
- **External Search API** (optional enhancement for web research):
  - Tavily API credentials
  - Note: Current implementation supports Tavily exclusively; additional search providers require custom implementation

### 📦 Platform Installation

Complete these sequential steps to establish your Deep Research Agent environment:

#### Step 1: Repository Acquisition
```powershell
git clone https://github.com/dhangerkapil/deep-research-agent.git
cd deep-research-agent
```

#### Step 2: Python Environment Preparation
```powershell
# Establish isolated Python environment
python -m venv deepresearchagent

# Environment activation
.\deepresearchagent\Scripts\Activate.ps1

# Environment verification (should display virtual environment path)
where python
```

#### Step 3: Dependency Installation
```powershell
pip install -r requirements.txt
```

#### Step 4: Configuration File Generation

**4.1 Environment Configuration Setup**
```powershell
# Generate environment configuration from template
Copy-Item .env.example .env
```
*Customize with your specific Azure and API credentials*

**4.2 Project Configuration Establishment**
```powershell
# Initialize project configuration from template
Copy-Item config\project_config_templates.yaml config\project_config.yaml
```
*Configure according to your organizational requirements*

**Essential configuration elements in `config/project_config.yaml`:**
- Organizational details (system.company)
- **Azure AI Search index specifications (data_sources.document_types)**
- External search configuration (data_sources.web_search)
- Agent behavioral parameters (agents)

#### Step 5: Platform Activation
```powershell
# Initialize the research platform
python main.py --query "Could you summarize the latest update on Azure OpenAI in 2025?"
```

### 🛠️ Configuration Architecture

#### Template Organization Structure

The platform utilizes a template-based configuration system requiring customization:

```
Enterprise-Research-Platform/
├── config/
│   ├── project_config_templates.yaml # Configuration template foundation
│   └── project_config.yaml           # Customized configuration (user-generated)
├── .env.example                      # Environment template foundation
└── .env                              # Environment configuration (user-generated)
```

## 🌐 Azure Cloud Integration

### Azure Deployment Prerequisites

Before deploying to Azure, ensure you have:

- **Azure CLI** installed and configured (`az --version`)
- **Azure Developer CLI** installed (`azd version`)
- **Active Azure subscription** with appropriate permissions
- **Python 3.12** runtime support in Azure App Service

### Step 1: Install Azure Tools
```powershell
# Install Azure CLI (if not already installed)
# Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Install Azure Developer CLI
# Download from: https://docs.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd

# Verify installations
az --version
azd version
```

### Step 2: Azure Authentication
```powershell
# Login to Azure CLI
az login

# Login to Azure Developer CLI
azd auth login

# Set your subscription (if you have multiple)
az account set --subscription "YOUR-SUBSCRIPTION-ID"
```

### Step 3: Environment Configuration
Ensure your `.env` file contains all required Azure service endpoints:
```env
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
TAVILY_API_KEY=your-tavily-key
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_KEY=your-search-key
```

### Step 4: Initialize Azure Project
```powershell
# Initialize the Azure project (first time only)
azd init

# Follow the prompts to:
# - Select Python as the language
# - Choose App Service as the hosting option
# - Set environment name (e.g., 'production', 'dev')
# - Select Azure region (e.g., 'East US', 'West Europe')
```

### Step 5: Deploy to Azure
```powershell
# Deploy infrastructure and application
azd up

# This command will:
# 1. Provision Azure resources (App Service, Resource Group)
# 2. Build the application
# 3. Deploy to Azure App Service
# 4. Configure environment variables
```

### Step 6: Update Deployment (After Changes)

For **quick application-only deployments** (recommended for code changes):
```powershell
# Deploy only application code (fastest option)
azd deploy --no-prompt

# This command will:
# 1. Package your application code
# 2. Upload to Azure App Service
# 3. Restart the application
# 4. Preserve existing infrastructure and settings
```

For **full infrastructure and application deployment**:
```powershell
# Full deployment with infrastructure updates
azd up --no-prompt

# Use this when you've changed:
# - Azure resource configurations
# - Environment variables
# - Infrastructure settings
```

### Step 7: Verify Deployment

After deployment, test your application:
```powershell
# Get the deployment URL
azd show

# Test the health endpoint
curl "https://[your-app-name].azurewebsites.net/health"

# Test the main interface
# Open https://[your-app-name].azurewebsites.net/ in your browser
```

## 🚀 Automated Deployment (Optional)

### GitHub Actions CI/CD Pipeline

The repository includes a GitHub Actions workflow (`.github/workflows/azure-dev.yml`) for automated deployments. This is **optional** but recommended for:

- **Automatic deployments** when code is pushed to main branch
- **Team collaboration** with consistent deployment process
- **Continuous integration** with automated testing

#### Setting Up GitHub Actions (Optional)

If you want automated deployments, configure these GitHub repository secrets:

1. **Repository Variables** (Settings → Secrets and variables → Actions → Variables):
   ```
   AZURE_CLIENT_ID: [your-service-principal-client-id]
   AZURE_TENANT_ID: [your-azure-tenant-id]
   AZURE_SUBSCRIPTION_ID: [your-azure-subscription-id]
   AZURE_ENV_NAME: [your-azd-environment-name]
   AZURE_LOCATION: [your-azure-region]
   ```

2. **Repository Secrets** (Settings → Secrets and variables → Actions → Secrets):
   ```
   AZURE_OPENAI_API_KEY: [your-azure-openai-key]
   AZURE_SEARCH_API_KEY: [your-azure-search-key]
   TAVILY_API_KEY: [your-tavily-api-key]
   ```

#### Manual vs Automated Deployment

**Manual Deployment (Current Method)**:
```powershell
azd deploy --no-prompt  # Fast, immediate control
```

**Automated Deployment (GitHub Actions)**:
- Triggers automatically on git push to main branch
- Includes automated health checks
- Consistent deployment process
- Requires initial setup of secrets/variables

**Recommendation**: Start with manual deployment, add GitHub Actions later for team environments.

#### Removing GitHub Actions (If Not Needed)

If you prefer manual deployment only, you can remove the workflow:
```powershell
# Remove the GitHub Actions workflow
Remove-Item -Path ".github\workflows\azure-dev.yml" -Force

# Or keep it for future use (recommended)
# The workflow won't run unless you configure the required secrets
```

### Troubleshooting Deployment Issues

#### Common Issues and Solutions

**1. Deployment Conflicts (409 Error)**
```powershell
# Stop all conflicting processes
Get-Process | Where-Object {$_.ProcessName -like "*azd*" -or $_.ProcessName -like "*azure*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Restart the web app
az webapp restart --name [YOUR-APP-NAME] --resource-group [YOUR-RG-NAME]

# Retry deployment
azd deploy --no-prompt
```

**2. Python Runtime Issues**
- Ensure `startup.txt` contains: `gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:$PORT --timeout 300`
- Verify Python 3.12 is specified in Azure configuration
- Check that all dependencies are in `requirements.txt`

**3. Environment Variable Issues**
```powershell
# Set environment variables manually if needed
az webapp config appsettings set --resource-group [RG-NAME] --name [APP-NAME] --settings AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"

# Check current settings
az webapp config appsettings list --resource-group [RG-NAME] --name [APP-NAME]
```

**4. Application Logs**
```powershell
# Stream live application logs
az webapp log tail --name [APP-NAME] --resource-group [RG-NAME]

# Download log files
az webapp log download --resource-group [RG-NAME] --name [APP-NAME]
```

### Production Deployment Checklist

- [ ] All environment variables configured
- [ ] Azure OpenAI endpoints accessible
- [ ] Azure AI Search indexes populated
- [ ] Web search API keys valid (if using web search)
- [ ] Application successfully starts
- [ ] Health check endpoint responds
- [ ] Research functionality tested end-to-end

### Accessing Your Deployed Application

After successful deployment, your application will be available at:
```
https://[your-app-name].azurewebsites.net/
```

The deployment process will display the URL in the terminal output.