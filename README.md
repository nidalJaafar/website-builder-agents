# Website Builder POC

An AI-powered multi-agent system that automatically builds complete websites from conversational requirements using LangGraph and Google's Gemini AI.

## Overview

This project implements a sophisticated multi-agent workflow that guides users through website creation via a conversational interface. The system gathers requirements, generates development tasks, and executes them autonomously using AI agents powered by LangGraph orchestration.

## Architecture

### Multi-Agent System

The project uses **LangGraph** to orchestrate four specialized AI agents that work sequentially:

1. **Requirements Agent** (`requirements_agent.py`)
   - Conducts interactive conversations to gather website specifications
   - Asks focused questions about business type, purpose, pages, content, design, and contact info
   - Validates completeness before proceeding
   - Uses `exit_tool` to signal requirements are complete

2. **Task Manager Agent** (`task_manager_agent.py`)
   - Converts requirements into detailed, actionable development tasks
   - Generates JSON-formatted task lists with file paths, descriptions, and success criteria
   - Specifies exact implementation details (layouts, colors, spacing, functionality)
   - Creates tasks at `website_project/{session_id}/` path structure

3. **Developer Agent** (`developer_agent.py`)
   - Executes tasks using MCP (Model Context Protocol) filesystem tools
   - Creates multi-page websites with consistent navigation
   - Implements responsive design with accessibility standards
   - Uses online image placeholders (placehold.co, picsum.photos)
   - Handles 1500 character limit per tool call by splitting content strategically

4. **Orchestrator Agent** (`orchestrator_agent.py`)
   - Coordinates the overall workflow between agents
   - Manages state transitions between phases
   - Tracks session data and progress
   - Finalizes and delivers completed projects

### Workflow Graphs

The system implements multiple LangGraph state machines:

- **Orchestrator Graph** (`orchestrator_graph.py`): Main workflow coordinator
  - Flow: START → task_management_phase → development_phase → finalize_project → END

- **Requirements Graph** (`requirements_graph.py`): Single-step conversational processing
  - Flow: START → process_message → END

- **Task Manager Graph** (`task_manager_graph.py`): Task generation pipeline
  - Flow: START → generate_tasks → parse_tasks → END

- **Developer Graph** (`developer_graph.py`): Iterative development execution
  - Flow: START → agent → tools/advance_to_next_task → project_complete → END
  - Includes conditional routing based on tool calls and task completion

### State Models

Typed state definitions in `state_models.py`:

- `RequirementsState`: Manages conversation messages and gathered data
- `TaskManagerState`: Handles requirements and parsed task lists
- `DeveloperState`: Tracks current task, project status, and development context
- `OrchestratorState`: Maintains overall workflow state and session data

## Technology Stack

### AI Model

**Google Gemini 2.5 Pro** (`gemini-2.5-pro`)
- All agents use this model for natural language processing and decision-making
- Configured in: `requirements_agent.py`, `task_manager_agent.py`, `developer_agent.py`, `json_parser_agent.py`, and `crud.py`
- Requires Google API Key for access

### Core Dependencies

- **LangGraph (>=0.6.6)**: Agent orchestration and workflow management
- **LangChain Google GenAI (>=2.1.12)**: Google Gemini AI model integration
- **LangChain MCP Adapters (>=0.1.9)**: Model Context Protocol for filesystem operations
- **FastAPI (>=0.104.0)**: REST API framework
- **SQLAlchemy (>=2.0.43)**: Database ORM for session management
- **Uvicorn (>=0.24.0)**: ASGI server

### Additional Tools

- **Pyppeteer (>=2.0.0)**: Headless browser automation
- **python-dotenv (>=1.1.1)**: Environment configuration
- **json-repair (>=0.52.0)**: JSON parsing and validation
- **nest-asyncio (>=1.6.0)**: Async event loop utilities

## Project Structure

```
website-builder-poc/
├── src/website_builder/
│   ├── agents/              # AI agent implementations
│   │   ├── requirements_agent.py
│   │   ├── task_manager_agent.py
│   │   ├── developer_agent.py
│   │   └── orchestrator_agent.py
│   ├── graphs/              # LangGraph workflow definitions
│   │   ├── requirements_graph.py
│   │   ├── task_manager_graph.py
│   │   ├── developer_graph.py
│   │   └── orchestrator_graph.py
│   ├── models/              # State and data models
│   │   └── state_models.py
│   ├── prompts/             # Agent system prompts
│   │   ├── requirements_prompts.py
│   │   ├── task_manager_prompts.py
│   │   └── developer_prompts.py
│   ├── api/                 # REST API layer
│   │   ├── controller/
│   │   │   └── api.py       # FastAPI endpoints
│   │   └── service/
│   │       ├── message_service.py
│   │       ├── status_service.py
│   │       ├── json_service.py
│   │       └── zip_service.py
│   ├── db/                  # Database layer
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── database_models.py
│   │   └── crud.py          # Database operations
│   ├── mcp/                 # Model Context Protocol tools
│   │   └── file_system.py   # Filesystem MCP client
│   ├── tools/               # Custom LangChain tools
│   │   └── validation_tools.py
│   ├── scripts/             # Utility scripts
│   │   ├── test_graphs.py   # Graph testing utilities
│   │   └── utilities.py     # Setup/cleanup helpers
│   └── config.py            # Configuration
├── Dockerfile               # Container configuration
├── start.sh                 # Startup script
└── pyproject.toml           # Project metadata and dependencies
```

## API Endpoints

### REST API (FastAPI)

The API runs on port 8080 and provides the following endpoints:

- **`GET /health`**: Health check endpoint
- **`POST /chat/start`**: Initialize a new requirements gathering session
  - Request: `{"user_input": "I want to build a website for..."}`
  - Response: `{"session_id": "uuid", "agent_message": "..."}`

- **`POST /chat/message`**: Send message in ongoing conversation
  - Request: `{"session_id": "uuid", "user_input": "..."}`
  - Response: `{"agent_message": "..."}`

- **`GET /poll/{session_id}`**: Poll session status and progress

- **`GET /zip/{session_id}`**: Download completed website as ZIP file

- **`POST /parse`**: Parse JSON data (utility endpoint)

## Quick Start

For experienced developers who want to get started immediately:

```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and navigate
git clone <repository-url> && cd website-builder-agents

# 3. Install dependencies
uv sync

# 4. Set up environment
echo "GOOGLE_API_KEY=your_key_here" > .env

# 5. Run the application
./start.sh
```

## Installation & Setup

### Prerequisites

- **Python 3.11+**: Required for the application
- **UV Package Manager**: Modern Python package manager (replaces pip/poetry)
- **Node.js and npm**: Required for MCP filesystem server
- **Google API Key**: For Gemini 2.5 Pro access

### Step-by-Step Installation

#### 1. Install UV Package Manager

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

#### 2. Install Node.js and npm

```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# On macOS (using Homebrew)
brew install node

# Verify installation
node --version
npm --version
```

#### 3. Clone the Repository

```bash
git clone <repository-url>
cd website-builder-poc
```

#### 4. Install Python Dependencies

```bash
# UV will automatically install Python 3.11+ if needed
uv sync
```

This command:
- Creates a virtual environment
- Installs all dependencies from `pyproject.toml`
- Sets up the project for development

#### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Using your text editor
nano .env

# Or using echo
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

**How to get a Google API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

#### 6. Run the Application

**Option A: Using the startup script (recommended)**
```bash
chmod +x start.sh  # Make script executable (first time only)
./start.sh
```

This script automatically:
1. Cleans the project workspace
2. Sets up the project structure
3. Starts the FastAPI server on port 8080

**Option B: Manual step-by-step**
```bash
# Step 1: Clean previous workspace
uv run clean-project

# Step 2: Initialize project workspace
uv run setup-project

# Step 3: Start the API server
uv run api
```

#### 7. Verify the Server is Running

Open your browser and visit:
- **Health check**: http://localhost:8080/health

You should see a health check response or the interactive API documentation.

### Docker Deployment

Build and run with Docker:

```bash
docker build -t website-builder .
docker run -p 8080:8080 -e GOOGLE_API_KEY=your_key website-builder
```

The Docker container:
- Uses Python 3.11-slim base image
- Installs Node.js/npm for MCP server
- Runs as non-root user (appuser)
- Exposes port 8080

## Usage Example

### Creating a Website via API

Here's a complete example of using the API to build a website:

#### Step 1: Start a Requirements Session

```bash
curl -X POST http://localhost:8080/chat/start \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "I want to build a website for my bakery business"
  }'
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_message": "Great! What are the main sections you need for your bakery website? (For example: Home, About, Menu, Contact, etc.)"
}
```

#### Step 2: Continue the Conversation

```bash
curl -X POST http://localhost:8080/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_input": "I need Home, About Us, Our Products, and Contact pages"
  }'
```

The agent will continue asking questions about:
- Content for each section
- Design preferences and colors
- Contact information
- Any special features needed

#### Step 3: Agent Confirms and Proceeds

Once enough information is gathered:

```json
{
  "agent_message": "Here's what I gathered:\n- Business: Bakery\n- Sections: Home, About Us, Our Products, Contact\n- Design: Warm colors, professional\n- Contact info: Email and phone\n\nIs this complete enough to start building your website?"
}
```

When you confirm, the system automatically:
1. Generates detailed development tasks
2. Executes each task using the developer agent
3. Creates a complete multi-page website
4. Updates session status to "completed"

#### Step 4: Poll for Completion

```bash
curl http://localhost:8080/poll/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "status": "completed",
  "message": "Website creation complete",
  "project_status": "completed"
}
```

#### Step 5: Download the Website

```bash
curl -O http://localhost:8080/zip/550e8400-e29b-41d4-a716-446655440000
```

This downloads a ZIP file containing:
```
website_project/550e8400-e29b-41d4-a716-446655440000/
├── index.html
├── about.html
├── products.html
├── contact.html
├── css/
│   └── styles.css
└── js/
    └── main.js
```

### Testing Individual Agents

You can test each agent in isolation using the provided scripts:

```bash
# Test requirements gathering
uv run test-requirements

# Test task generation
uv run test-tasks

# Test developer execution
uv run test-developer

# Test complete orchestrator flow
uv run test-orchestrator
```

## Available Scripts

Defined in `pyproject.toml`:

### Main Commands
- `uv run api`: Start the FastAPI server

### Testing Commands
- `uv run test-requirements`: Test requirements gathering agent
- `uv run test-tasks`: Test task manager agent
- `uv run test-developer`: Test developer agent
- `uv run test-orchestrator`: Test full orchestrator workflow

### Utility Commands
- `uv run visualize-graphs`: Generate visual diagrams of LangGraph workflows
- `uv run setup-project`: Initialize project workspace
- `uv run clean-project`: Clean project workspace

## Key Features

### Conversational Requirements Gathering
- Natural language interaction to gather website specifications
- Focused, one-question-at-a-time approach
- Validation before proceeding to development

### Intelligent Task Generation
- Converts requirements into detailed development tasks
- Includes exact file paths, content specifications, and design details
- Session-specific project organization

### Autonomous Development
- Uses MCP filesystem tools for file operations
- Implements multi-page websites with consistent navigation
- Handles character limits intelligently by splitting large files
- Applies modern web design standards automatically

### Design Standards (Auto-Applied)
- **Spacing**: 8px units (8, 16, 24, 32, 48, 64px)
- **Typography**: 16px base, responsive headings, 1.5 line-height
- **Colors**: User-specified with 4.5:1 contrast ratio
- **Responsive**: Mobile-first, breakpoints at 768px/1024px
- **Layout**: CSS Grid for pages, Flexbox for components
- **Accessibility**: Semantic HTML5, ARIA labels, focus states
- **Interactions**: 200ms transitions

### Multi-Page Coordination
The developer agent maintains navigation consistency across all pages:
1. First page creates navigation template with all page links
2. Subsequent pages copy existing navigation structure
3. Navigation updates propagate to all existing pages
4. All pages link to shared CSS/JS files

### Session Management
- SQLAlchemy database for session persistence
- Tracks conversation state, requirements, and tasks
- Supports session reactivation for iterative development
- Stores project outputs and status

## Database Schema

### Session Model (`database_models.py`)
- `id`: UUID primary key
- `status`: Current session status (pending/completed)
- `requirement_gatherer_output`: Stored conversation messages
- `task_manager_output`: Generated tasks JSON
- `state`: Serialized graph state

## Development Workflow

1. **Start Session**: User initiates chat with initial website description
2. **Requirements Phase**: Requirements agent asks clarifying questions
3. **Task Generation**: Task manager creates detailed development tasks
4. **Development Phase**: Developer agent executes tasks sequentially
5. **Finalization**: Orchestrator completes session and provides download link

## Logging

Comprehensive logging configured at DEBUG level:
- Request/response tracking
- Agent conversation logging
- Graph execution monitoring
- Error tracking and debugging

Filtered loggers:
- LangChain function utils (ERROR level)
- gRPC cygrpc (INFO level)

## Environment Configuration

- `PROJECT_WORKSPACE`: Base directory for generated websites (default: `./website_project`)
- `GOOGLE_API_KEY`: Required for Gemini AI access
- Database: SQLite (`test.db`) for development

## MCP Integration

Uses LangChain MCP Adapters to provide filesystem capabilities:
- **Server**: `@modelcontextprotocol/server-filesystem`
- **Tools**: write_file, edit_file, read_file, list_files
- **Workspace**: Scoped to `PROJECT_WORKSPACE` directory

## Error Handling

- HTTP 400 for invalid requests (missing fields)
- HTTP 500 for processing errors with detailed messages
- Graceful fallbacks for state deserialization
- Transaction management for database operations

## Future Enhancements

Potential areas for expansion:
- Support for additional LLM providers
- Advanced template library
- Database backend selection (PostgreSQL, MySQL)
- Real-time WebSocket updates
- Preview server integration
- Custom component library
- Version control integration
- Multi-user collaboration
