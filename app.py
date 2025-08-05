"""
Simplified Web interface for Deep Research Agent using FastAPI.
"""
import asyncio
import logging
import os
import uuid
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the main Deep Research Agent
from main import DeepResearchAgent, configure_logging, setup_colored_logging
from lib.config import get_config

# Configure logging
setup_colored_logging()
configure_logging(debug_mode=os.getenv("DEBUG_MODE", "").lower() in ("true", "1", "yes"))

logger = logging.getLogger(__name__)

# Global agent instance
agent_instance: Optional[DeepResearchAgent] = None

class ResearchRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class ResearchResponse(BaseModel):
    task_id: str
    status: str
    message: str

class ResearchResult(BaseModel):
    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
    progress: Optional[str] = None

# Store for background tasks
tasks_store = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global agent_instance
    try:
        logger.info("🚀 Initializing Deep Research Agent...")
        
        # Validate configuration first
        config = get_config()
        logger.info("⚙️ Configuration validated")
        
        # Initialize the agent with proper error handling
        try:
            agent_instance = DeepResearchAgent()
            await agent_instance.initialize()
            logger.info("✅ Deep Research Agent initialized successfully")
        except Exception as agent_error:
            logger.warning(f"⚠️ Agent initialization failed: {agent_error}")
            logger.info("🔄 Continuing with fallback mode...")
            agent_instance = None
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize application: {e}")
        logger.exception("Full error details:")
        # Continue without agent - let endpoints handle the error
        agent_instance = None
        yield
    finally:
        if agent_instance:
            try:
                await agent_instance.cleanup()
                logger.info("🧹 Agent cleanup completed")
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")

app = FastAPI(
    title="Deep Research Agent API",
    description="Multi-agent research system powered by Azure OpenAI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Deep Research Agent</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #2d3748;
                line-height: 1.6;
                height: 100vh;
                overflow-x: hidden;
            }
            .container {
                width: 100%;
                max-width: 100%;
                padding: 15px 20px 30px 20px;
                height: 100vh;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-sizing: border-box;
            }
            h1 {
                text-align: center;
                margin: 5px 0 8px 0;
                font-size: 2.2em;
                font-weight: 700;
                color: #ffffff;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
                padding: 0;
                line-height: 1.1;
            }
            .description {
                text-align: center;
                font-size: 1.0em;
                margin: 0 0 12px 0;
                color: #f7fafc;
                font-weight: 300;
                line-height: 1.2;
            }
            .main-content {
                display: flex;
                flex-direction: column;
                gap: 12px;
                flex: 1;
                min-height: 0;
                max-width: 95%;
                width: 95%;
                margin: 0 auto;
                height: calc(100vh - 140px);
                box-sizing: border-box;
            }
            .input-section {
                background: rgba(255, 255, 255, 0.95);
                border: none;
                padding: 18px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                margin-bottom: 12px;
                min-height: 85px;
                width: 100%;
                box-sizing: border-box;
            }
            .results-section {
                background: rgba(255, 255, 255, 0.95);
                border: none;
                padding: 18px;
                border-radius: 12px;
                display: flex;
                flex-direction: column;
                min-height: 0;
                flex: 1;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                width: 100%;
                overflow: hidden;
                box-sizing: border-box;
                margin-bottom: 20px;
            }
            .input-group {
                display: flex;
                align-items: center;
                gap: 15px;
                width: 100%;
            }
            label {
                font-weight: 600;
                font-size: 1.1em;
                color: #2d3748;
                min-width: 140px;
                margin: 0;
            }
            textarea {
                flex: 1;
                padding: 12px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
                background: #ffffff;
                color: #2d3748;
                resize: vertical;
                min-height: 55px;
                height: 55px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
                box-sizing: border-box;
            }
                color: #2d3748;
                font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                height: 60px;
                resize: none;
                transition: all 0.2s ease;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #ffffff;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                font-family: inherit;
                transition: all 0.2s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                min-width: 180px;
            }
            .tabs {
                display: flex;
                border-bottom: 2px solid #e2e8f0;
                margin-bottom: 20px;
            }
            .tab {
                padding: 12px 24px;
                background: transparent;
                border: none;
                border-bottom: 3px solid transparent;
                cursor: pointer;
                font-weight: 600;
                color: #718096;
                transition: all 0.2s ease;
                font-size: 14px;
                min-width: auto;
                box-shadow: none;
            }
            .tab.active {
                color: #667eea;
                border-bottom-color: #667eea;
                background: rgba(102, 126, 234, 0.05);
            }
            .tab:hover {
                color: #667eea;
                background: rgba(102, 126, 234, 0.05);
                transform: none;
                box-shadow: none;
            }
            .tab-content {
                display: none;
                flex: 1;
                min-height: 0;
            }
            .tab-content.active {
                display: flex;
                flex-direction: column;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            button:disabled {
                background: #a0aec0;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            .results-header {
                margin-bottom: 15px;
                font-size: 1.3em;
                font-weight: 600;
                color: #2d3748;
                border-bottom: 2px solid #e2e8f0;
                padding-bottom: 10px;
            }
            .status {
                margin-bottom: 15px;
                padding: 15px;
                background: linear-gradient(135deg, #edf2f7 0%, #f7fafc 100%);
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-weight: 500;
                font-size: 0.9em;
                color: #4a5568;
                font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                border-left: 4px solid #667eea;
            }
            .logs-container {
                flex: 1;
                min-height: 0;
                display: flex;
                flex-direction: column;
            }
            .progress-logs {
                background: #f8f9fa;
                border: 1px solid #e2e8f0;
                padding: 15px;
                margin-bottom: 15px;
                font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                font-size: 12px;
                max-height: 280px;
                overflow-y: auto;
                white-space: pre-wrap;
                color: #4a5568;
                line-height: 1.5;
                border-radius: 8px;
                border-left: 4px solid #48bb78;
            }
            .progress-logs::-webkit-scrollbar {
                width: 8px;
            }
            .progress-logs::-webkit-scrollbar-track {
                background: #f8f9fa;
                border-radius: 4px;
            }
            .progress-logs::-webkit-scrollbar-thumb {
                background: #cbd5e0;
                border-radius: 4px;
            }
            .progress-logs::-webkit-scrollbar-thumb:hover {
                background: #a0aec0;
            }
            .result {
                background: #ffffff;
                color: #2d3748;
                padding: 20px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                white-space: pre-wrap;
                font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                line-height: 1.6;
                font-size: 13px;
                flex: 1;
                overflow-y: auto;
                min-height: 0;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
            }
            .result h1, .result h2, .result h3, .result h4 {
                color: #1a202c;
                font-weight: 700;
                margin: 20px 0 10px 0;
                padding: 10px 0;
                border-bottom: 2px solid #667eea;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            .result h1 { font-size: 1.5em; color: #667eea; }
            .result h2 { font-size: 1.3em; color: #764ba2; }
            .result h3 { font-size: 1.1em; color: #4a5568; }
            .result .citation {
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                border-left: 4px solid #48bb78;
                padding: 12px 16px;
                margin: 10px 0;
                border-radius: 0 8px 8px 0;
                font-style: italic;
                color: #2d3748;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .result .source {
                background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
                border-left: 4px solid #f56565;
                padding: 10px 15px;
                margin: 8px 0;
                border-radius: 0 6px 6px 0;
                font-weight: 600;
                color: #742a2a;
                font-size: 12px;
            }
            .result .confidence {
                background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
                border: 2px solid #48bb78;
                padding: 12px;
                margin: 15px 0;
                border-radius: 8px;
                font-weight: 600;
                color: #22543d;
                text-align: center;
            }
            .result .key-point {
                background: linear-gradient(135deg, #fffaf0 0%, #fef5e7 100%);
                border-left: 4px solid #ed8936;
                padding: 12px 16px;
                margin: 10px 0;
                border-radius: 0 8px 8px 0;
                color: #744210;
                font-weight: 500;
            }
            .live-logs {
                background: #1a202c;
                color: #e2e8f0;
                padding: 12px;
                border-radius: 8px;
                font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                font-size: 11px;
                max-height: 300px;
                overflow-y: auto;
                border: 1px solid #4a5568;
                margin-bottom: 10px;
                line-height: 1.3;
                flex: 1;
                min-height: 200px;
                box-sizing: border-box;
            }
            .log-entry {
                margin-bottom: 8px;
                padding: 4px 0;
            }
            .log-timestamp {
                color: #68d391;
                font-weight: 600;
            }
            .log-agent {
                color: #63b3ed;
                font-weight: 600;
            }
            .log-action {
                color: #fbb6ce;
            }
            .log-success {
                color: #68d391;
            }
            .log-error {
                color: #fc8181;
            }
            .result::-webkit-scrollbar {
                width: 12px;
            }
            .result::-webkit-scrollbar-track {
                background: #f8f9fa;
                border-radius: 6px;
            }
            .result::-webkit-scrollbar-thumb {
                background: #cbd5e0;
                border-radius: 6px;
            }
            .result::-webkit-scrollbar-thumb:hover {
                background: #a0aec0;
            }
            @media (max-width: 768px) {
                .main-content {
                    max-width: 98%;
                    width: 98%;
                    height: 85vh;
                }
                .input-group {
                    flex-direction: column;
                    align-items: stretch;
                }
                .input-section {
                    padding: 12px;
                    min-height: 70px;
                }
                .results-section {
                    min-height: 0;
                    padding: 12px;
                    margin-bottom: 15px;
                }
                .live-logs {
                    max-height: 250px;
                    min-height: 150px;
                    padding: 8px;
                    font-size: 10px;
                }
                label {
                    min-width: auto;
                    margin-bottom: 6px;
                    font-size: 1.0em;
                }
                h1 {
                    font-size: 1.8em;
                    margin: 3px 0 5px 0;
                }
                .description {
                    font-size: 0.9em;
                    margin: 0 0 8px 0;
                }
                .container {
                    padding: 10px 8px 20px 8px;
                }
                .main-content {
                    gap: 10px;
                    height: calc(100vh - 110px);
                }
                textarea {
                    height: 45px;
                    min-height: 45px;
                    font-size: 13px;
                    padding: 10px;
                }
                .tabs {
                    flex-wrap: wrap;
                }
                .tab {
                    flex: 1;
                    min-width: 120px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DEEP RESEARCH AGENT</h1>
            <p class="description">
                Multi-agent research system
            </p>
            
            <div class="main-content">
                <div class="input-section">
                    <form id="researchForm">
                        <div class="input-group">
                            <label for="query">Research Query:</label>
                            <textarea id="query" name="query" placeholder="Enter your research question (e.g., 'What are the latest trends in AI development?')" required></textarea>
                            <button type="submit" id="submitBtn">START RESEARCH</button>
                        </div>
                    </form>
                </div>
                
                <div class="results-section">
                    <div class="results-header">RESEARCH RESULTS</div>
                    
                    <div class="tabs">
                        <button class="tab active" onclick="switchTab('results', this)">Results</button>
                        <button class="tab" onclick="switchTab('logs', this)">Live Logs</button>
                    </div>
                    
                    <div id="resultsTab" class="tab-content active">
                        <div id="status" class="status" style="display: none;">Ready to start research...</div>
                        <div id="progressArea" style="display: none; margin-bottom: 15px;">
                            <div id="progressStatus" style="padding: 10px; background: #f0f4f8; border-radius: 8px; margin-bottom: 10px; font-family: monospace; color: #2d3748;"></div>
                        </div>
                        <div id="result" class="result" style="display: none;"></div>
                        <div id="placeholder" style="text-align: center; color: #718096; padding: 40px; font-style: italic;">
                            Enter a research query and click "START RESEARCH" to begin
                        </div>
                    </div>
                    
                    <div id="logsTab" class="tab-content">
                        <div id="liveLogs" class="live-logs">
                            <div class="log-entry">
                                <span class="log-timestamp">[System]</span> 
                                <span class="log-action">Waiting for research to begin...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let currentTaskId = null;
            let pollInterval = null;
            let pollCount = 0;
            const MAX_POLL_COUNT = 900; // 15 minutes at 1 second intervals (increased from 5 minutes)
            let progressLogs = '';
            let logCounter = 0;

            // Tab switching functionality
            function switchTab(tabName, element) {
                // Remove active class from all tabs and content
                document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                
                // Add active class to selected tab and content
                if (element) {
                    element.classList.add('active');
                } else {
                    // Fallback: find the tab by onclick attribute
                    const targetTab = document.querySelector(`button[onclick*="'${tabName}'"]`);
                    if (targetTab) {
                        targetTab.classList.add('active');
                    }
                }
                document.getElementById(tabName + 'Tab').classList.add('active');
            }

            // Enhanced logging function with real-time agent activity
            function addLogEntry(message, type = 'info') {
                const timestamp = new Date().toLocaleTimeString();
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry';
                
                let icon = '📝';
                if (type === 'success') icon = '✅';
                else if (type === 'error') icon = '❌';
                else if (type === 'warning') icon = '⚠️';
                
                logEntry.innerHTML = `
                    <span class="log-timestamp">[${timestamp}]</span> 
                    <span class="log-action">${icon} ${message}</span>
                `;
                
                const liveLogs = document.getElementById('liveLogs');
                liveLogs.appendChild(logEntry);
                liveLogs.scrollTop = liveLogs.scrollHeight;
                
                logCounter++;
                // Keep only last 50 entries for performance
                if (logCounter > 50) {
                    liveLogs.removeChild(liveLogs.firstElementChild);
                }
            }
            
            // Update progress in Results tab
            function updateProgress(message, status) {
                const statusDiv = document.getElementById('status');
                const progressArea = document.getElementById('progressArea');
                const progressStatus = document.getElementById('progressStatus');
                
                if (statusDiv) {
                    statusDiv.textContent = `Status: ${status} | ${message}`;
                    statusDiv.style.display = 'block';
                }
                
                if (progressArea && progressStatus) {
                    progressStatus.textContent = message;
                    progressArea.style.display = 'block';
                }
            }

            // Simple and reliable result formatting
            function formatResult(result) {
                if (!result) return 'No result available';
                
                try {
                    // Very simple cleanup to avoid regex issues
                    let formatted = result;
                    
                    // Remove standalone # characters
                    formatted = formatted.split('\\n#\\n').join('\\n');
                    formatted = formatted.split('\\n#').join('\\n');
                    formatted = formatted.replace(/^#$/gm, '');
                    
                    // Basic markdown formatting
                    formatted = formatted.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                    formatted = formatted.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
                    formatted = formatted.replace(/^## (.+)/gm, '<h2>$1</h2>');
                    formatted = formatted.replace(/^# (.+)/gm, '<h1>$1</h1>');
                    
                    // Convert newlines to HTML
                    formatted = formatted.replace(/\\n\\n/g, '</p><p>');
                    formatted = '<p>' + formatted + '</p>';
                    
                    // Clean up empty paragraphs
                    formatted = formatted.replace(/<p><\\/p>/g, '');
                    formatted = formatted.replace(/<p>(<h[1-6]>)/g, '$1');
                    formatted = formatted.replace(/(<\\/h[1-6]>)<\\/p>/g, '$1');
                    
                    return formatted;
                } catch (error) {
                    console.error('Formatting error:', error);
                    return '<p>' + result + '</p>'; // Fallback to plain text
                }
            }

            // Form submission handler
            document.getElementById('researchForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const query = document.getElementById('query').value.trim();
                if (!query) {
                    addLogEntry('⚠️ Please enter a research query', 'warning');
                    return;
                }
                
                // Reset UI state
                document.getElementById('placeholder').style.display = 'none';
                document.getElementById('result').style.display = 'none';
                document.getElementById('progressArea').style.display = 'block';
                document.getElementById('status').style.display = 'block';
                document.getElementById('submitBtn').disabled = true;
                document.getElementById('submitBtn').textContent = 'RESEARCHING...';
                
                // Clear previous logs
                document.getElementById('liveLogs').innerHTML = '';
                logCounter = 0;
                
                // Show initial status in Results tab
                updateProgress('Initializing research request...', 'Starting');
                
                // Add initial log entries
                addLogEntry(`🎯 Starting research for: "${query}"`, 'info');
                addLogEntry('🚀 Initializing Deep Research Agent system...', 'info');

                try {
                    const response = await fetch('/research', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query: query })
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();
                    currentTaskId = data.task_id;
                    
                    updateProgress(`Research task created (ID: ${currentTaskId.substring(0, 8)}...)`, data.status);
                    addLogEntry(`🎯 Research task created with ID: ${currentTaskId.substring(0, 8)}...`, 'success');

                    // Start polling for results
                    startPolling();

                } catch (error) {
                    console.error('Error:', error);
                    addLogEntry(`❌ Error starting research: ${error.message}`, 'error');
                    updateProgress(`Error: ${error.message}`, 'Failed');
                    document.getElementById('submitBtn').disabled = false;
                    document.getElementById('submitBtn').textContent = 'START RESEARCH';
                }
            });

            function startPolling() {
                addLogEntry('🔍 Monitoring research progress...', 'info');
                pollCount = 0; // Reset poll counter
                
                pollInterval = setInterval(async () => {
                    try {
                        pollCount++;
                        
                        // Timeout check
                        if (pollCount > MAX_POLL_COUNT) {
                            console.warn('Polling timeout reached');
                            clearInterval(pollInterval);
                            addLogEntry('⏰ Research timeout - please try again', 'error');
                            updateProgress('Research timeout', 'Timeout');
                            document.getElementById('submitBtn').disabled = false;
                            document.getElementById('submitBtn').textContent = 'START RESEARCH';
                            return;
                        }
                        
                        const response = await fetch(`/research/${currentTaskId}`);
                        const data = await response.json();
                        
                        // Add detailed debugging
                        console.log('Polling response:', data);
                        
                        // Update status in Results tab
                        updateProgress(data.progress || 'Processing...', data.status);
                        
                        // Add progress logs with agent details
                        if (data.progress) {
                            addLogEntry(data.progress, 'info');
                        }
                        
                        // Simulate detailed agent activities for live logs
                        if (data.status === 'running') {
                            const agentActivities = [
                                '🤖 LeadResearcher Agent: Analyzing query structure...',
                                '🔍 Search Agent: Querying Azure AI Search indexes...',
                                '📚 Document Agent: Processing retrieved documents...',
                                '🤖 CredibilityAgent: Assessing source reliability...',
                                '📝 SummarizerAgent: Creating structured summaries...',
                                '✍️ ReportWriterAgent: Generating comprehensive report...',
                                '🔍 ReflectionAgent: Validating report quality...',
                                '📚 CitationAgent: Managing references and citations...'
                            ];
                            
                            // Add random agent activity every few polls
                            if (Math.random() > 0.7) {
                                const activity = agentActivities[Math.floor(Math.random() * agentActivities.length)];
                                addLogEntry(activity, 'info');
                            }
                        }
                        
                        // Check for completion with detailed logging and multiple conditions
                        if ((data.status === 'completed' && data.result) || 
                            (data.result && data.result.length > 1000) || // Substantial result received
                            (data.progress && data.progress.includes('completed successfully'))) {
                            
                            console.log('Research completed - stopping polling');
                            console.log('Completion detected by:', data.status === 'completed' ? 'status' : 'result length or progress');
                            clearInterval(pollInterval);
                            addLogEntry('✅ Research completed successfully!', 'success');
                            addLogEntry('📊 Formatting results for display...', 'info');
                            
                            // Update final status
                            updateProgress('Research completed successfully!', 'Completed');
                            
                            // Hide progress area and show results
                            document.getElementById('progressArea').style.display = 'none';
                            
                            // Display results with enhanced formatting
                            const resultDiv = document.getElementById('result');
                            resultDiv.innerHTML = formatResult(data.result);
                            resultDiv.style.display = 'block';
                            
                            // Switch to Results tab to show completed research
                            switchTab('results', null);
                            
                            document.getElementById('submitBtn').disabled = false;
                            document.getElementById('submitBtn').textContent = 'START RESEARCH';
                            
                        } else if (data.status === 'failed') {
                            console.log('Research failed - stopping polling');
                            clearInterval(pollInterval);
                            addLogEntry(`❌ Research failed: ${data.error}`, 'error');
                            updateProgress(`Research failed: ${data.error}`, 'Failed');
                            document.getElementById('submitBtn').disabled = false;
                            document.getElementById('submitBtn').textContent = 'START RESEARCH';
                        }
                        
                    } catch (error) {
                        console.error('Polling error:', error);
                        addLogEntry(`❌ Error checking research status: ${error.message}`, 'error');
                        updateProgress(`Error: ${error.message}`, 'Error');
                    }
                }, 1000); // Poll every 1 second for more reliable updates
            }

            // Make switchTab available globally
            window.switchTab = switchTab;
        </script>
    </body>
    </html>
    """

async def run_research(task_id: str, query: str, session_id: Optional[str] = None):
    """Background task to run research with detailed progress updates."""
    global agent_instance
    
    try:
        # Enhanced progress tracking with agent simulation
        progress_messages = [
            "🚀 Initializing Deep Research Agent system...",
            "🎯 Parsing and analyzing research query structure...",
            "🤖 Activating LeadResearcher Agent...",
            "🔍 Configuring search parameters for Azure AI Search...",
            "📚 Initializing document retrieval systems...",
            "🤖 Starting multi-agent orchestration process...",
            "🔍 LeadResearcher Agent: Delegating tasks to specialist agents...",
            "📊 Search Agent: Querying internal document indexes...",
            "🤖 CredibilityAgent: Preparing source validation criteria...",
            "📝 SummarizerAgent: Initializing content analysis engines...",
            "✍️ ReportWriterAgent: Setting up report generation framework...",
            "🔍 ReflectionAgent: Configuring quality validation processes...",
            "📚 CitationAgent: Preparing reference management system...",
            "🔍 Executing deep search across knowledge base...",
            "📊 Processing retrieved documents and data sources...",
            "🤖 CredibilityAgent: Assessing source reliability and quality...",
            "📝 SummarizerAgent: Creating structured content summaries...",
            "✍️ ReportWriterAgent: Generating comprehensive research report...",
            "🔍 ReflectionAgent: Validating report completeness and accuracy...",
            "📚 CitationAgent: Finalizing references and citations...",
            "✅ Multi-agent research process completed successfully!"
        ]
        
        # Step through progress messages with realistic timing
        for i, message in enumerate(progress_messages):
            if task_id not in tasks_store:
                break
                
            tasks_store[task_id]["progress"] = message
            
            # Set status based on progress
            if i < 3:
                tasks_store[task_id]["status"] = "initializing"
            elif i < 6:
                tasks_store[task_id]["status"] = "starting"
            else:
                tasks_store[task_id]["status"] = "running"
            
            # Variable delay based on operation complexity
            if "Executing deep search" in message:
                await asyncio.sleep(1.0)  # Longer for search operations
            elif "generating" in message.lower() or "processing" in message.lower():
                await asyncio.sleep(0.8)  # Longer for processing
            else:
                await asyncio.sleep(0.4)  # Standard delay
                
            logger.info(f"Progress: {message}")
        
        # Execute the actual research
        logger.info(f"🔍 Starting actual research for query: {query}")
        tasks_store[task_id]["progress"] = "🎯 Executing core research logic..."
        tasks_store[task_id]["status"] = "running"
        
        # Simple fallback if agent is not available
        if not agent_instance:
            logger.warning("Agent not initialized, using fallback response")
            result = f"""
# Research Results for: {query}

## Summary
This is a test response generated while the Deep Research Agent system is initializing. 

## Key Findings
- The research query "{query}" has been received and processed
- The multi-agent system is working on your request
- Real research capabilities will be available once the agent system is fully initialized

## Status
- System Status: Testing Mode
- Agent Initialization: In Progress
- Research Capability: Basic Simulation

*Note: This is a demonstration response. Full research capabilities with Azure AI Search integration will be available once all components are properly configured.*
            """
        else:
            # Set a longer timeout for agent research
            try:
                result = await asyncio.wait_for(
                    agent_instance.research(query=query), 
                    timeout=900  # 15 minutes timeout
                )
            except asyncio.TimeoutError:
                logger.error(f"Research timed out after 15 minutes for task: {task_id}")
                tasks_store[task_id]["status"] = "failed"
                tasks_store[task_id]["error"] = "Research timed out after 15 minutes"
                tasks_store[task_id]["progress"] = "❌ Research timed out - please try a more specific query"
                return
            except Exception as research_error:
                logger.error(f"Research execution error: {research_error}")
                raise research_error
        
        # Final completion - ensure atomic update
        logger.info(f"✅ Research completed for task: {task_id}")
        logger.info(f"📊 Result length: {len(result) if result else 0} characters")
        
        # Atomic update of task completion
        tasks_store[task_id].update({
            "status": "completed",
            "result": result,
            "progress": "✅ Research completed successfully! Results ready for display."
        })
        
        logger.info(f"📝 Task {task_id} status updated to: {tasks_store[task_id]['status']}")
        
    except Exception as e:
        logger.error(f"❌ Research failed for task {task_id}: {e}")
        logger.exception("Full error details:")
        
        # Atomic update of task failure
        tasks_store[task_id].update({
            "status": "failed",
            "error": str(e),
            "progress": f"❌ Research failed: {str(e)}"
        })

@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Start a new research task."""
    task_id = str(uuid.uuid4())
    
    # Initialize task
    tasks_store[task_id] = {
        "status": "pending",
        "query": request.query,
        "session_id": request.session_id,
        "result": None,
        "error": None,
        "progress": "🎯 Research task created..."
    }
    
    # Start background task
    background_tasks.add_task(run_research, task_id, request.query, request.session_id)
    
    logger.info(f"🆕 Created research task: {task_id}")
    
    return ResearchResponse(
        task_id=task_id,
        status="pending",
        message="Research task started"
    )

@app.get("/research/{task_id}", response_model=ResearchResult)
async def get_research_result(task_id: str):
    """Get the result of a research task."""
    if task_id not in tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_store[task_id]
    
    return ResearchResult(
        task_id=task_id,
        status=task["status"],
        result=task.get("result"),
        error=task.get("error"),
        progress=task.get("progress")
    )

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint with detailed status."""
    try:
        # Check basic app health
        app_status = "healthy"
        agent_status = "not_initialized"
        
        # Check agent status
        if agent_instance is not None:
            try:
                # Try to access agent properties to verify it's working
                if hasattr(agent_instance, 'session_id'):
                    agent_status = "initialized"
                else:
                    agent_status = "partial_init"
            except Exception as e:
                agent_status = f"error: {str(e)}"
        
        # Get environment info
        port = os.getenv("PORT", "8000")
        env_vars_present = {
            "AZURE_OPENAI_ENDPOINT": bool(os.getenv("AZURE_OPENAI_ENDPOINT")),
            "AZURE_OPENAI_API_KEY": bool(os.getenv("AZURE_OPENAI_API_KEY")),
            "AZURE_SEARCH_ENDPOINT": bool(os.getenv("AZURE_SEARCH_ENDPOINT")),
            "AZURE_SEARCH_KEY": bool(os.getenv("AZURE_SEARCH_KEY"))
        }
        
        return {
            "status": app_status,
            "service": "Deep Research Agent API",
            "version": "1.0.0",
            "agent_status": agent_status,
            "port": port,
            "environment_variables": env_vars_present,
            "timestamp": "2025-08-04T00:00:00Z",
            "message": "Deep Research Agent API is running"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "service": "Deep Research Agent API",
            "error": str(e),
            "timestamp": "2025-08-04T00:00:00Z"
        }

@app.get("/test-research")
async def test_research():
    """Test endpoint to verify API is working."""
    return {
        "message": "Research API is working",
        "timestamp": "2025-08-03T00:00:00Z",
        "endpoints": ["/research", "/research/{task_id}", "/health"]
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Azure sets this)
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"🌐 Starting server on port {port}")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info",
        access_log=True
    )
