# Multi-Agent Obsidian Vault System

A distributed multi-agent system for collaborative learning within your Obsidian vault, powered by Claude and other AI models.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│         Obsidian Vault (SIE-Flashcard-Set)         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  Research    │  │  Synthesis   │  │  Review  │ │
│  │    Agent     │  │    Agent     │  │  Agent   │ │
│  │  (Opus 5.5)  │  │ (Sonnet 5.5) │  │ (Haiku)  │ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
│         │                  │                │     │
│         └──────────────────┼──────────────┘     │
│                            │                    │
│         ┌──────────────────▼──────────────────┐ │
│         │   Task Orchestrator (Central)       │ │
│         │  - Queue Management                │ │
│         │  - Permission Control              │ │
│         │  - Coordination                    │ │
│         └──────────────────┬──────────────────┘ │
│                            │                    │
│  ┌────────────┬────────────┼────────────┬──────┬┘
│  │            │            │            │      │
│  ▼            ▼            ▼            ▼      │
│ Tasks    Messages      Logs         Vault    │
│        Message-Queue                Files     │
│                                              │
└─────────────────────────────────────────────┘
        ▲                                
        │ Agent Workspace
        │ (read/write)
        │
    ┌───┴─────────────────┐
    │   Agent Interfaces  │
    │  - Read Notes       │
    │  - Write Notes      │
    │  - Create Flashcards│
    │  - Search Notes     │
    │  - Message Agents   │
    │  - Log Activity     │
    └─────────────────────┘
```

## Components

### 1. **agents.config.json**
Central configuration file defining all agents, their capabilities, and permissions.

```json
{
  "agents": [
    {
      "id": "claude-research",
      "model": "claude-opus-5-5",
      "role": "Research & Content Creation",
      "permissions": {
        "read": ["Core-Ops", "Command-Center"],
        "write": ["Core-Ops/research-agent"]
      }
    }
  ]
}
```

### 2. **agent_orchestrator.py**
Central orchestrator managing task flow, permissions, and agent coordination.

**Key Methods:**
- `submit_task()` - Add a task to the queue
- `update_task_status()` - Update task status (pending → in_progress → completed)
- `read_vault_file()` - Read from vault with permission checks
- `write_vault_file()` - Write to vault with agent attribution
- `list_tasks()` - List tasks with optional filtering

### 3. **agent_interface.py**
Interface that individual agents use to interact with the vault.

**Key Methods:**
- `read_note()` - Read a note from vault
- `write_note()` - Write a note with metadata
- `create_flashcard()` - Create study flashcards
- `search_notes()` - Full-text search
- `send_message_to_agent()` - Inter-agent communication
- `log_activity()` - Log agent actions

## Agent Types

### Claude Research Agent (Opus 5.5)
- **Role**: Research & Content Creation
- **Capabilities**: Web search, comprehensive notes, flashcard generation
- **Write Access**: `Core-Ops/research-agent/`

### Claude Synthesis Agent (Sonnet 5.5)
- **Role**: Knowledge Synthesis & Pattern Recognition
- **Capabilities**: Cross-document analysis, summaries, relationship mapping
- **Write Access**: `Core-Ops/synthesis-agent/`

### Claude Review Agent (Haiku 4.5)
- **Role**: Quality Assurance
- **Capabilities**: Content review, error detection, consistency checking
- **Write Access**: `Core-Ops/review-agent/`

## Directory Structure

```
Multi-Agent-System/
├── agents.config.json           # Agent definitions
├── agent_orchestrator.py        # Central orchestrator
├── agent_interface.py           # Agent API interface
├── message-queue/               # Inter-agent messages
├── tasks/                       # Task definitions & status
├── logs/                        # Activity logs
├── agent-workspace-*/           # Individual agent workspaces
└── README.md                    # This file
```

## Usage Examples

### 1. Submit a Task

```bash
python3 Multi-Agent-System/agent_orchestrator.py submit-task \
  "research" \
  "claude-research" \
  "Research SIE exam topics" \
  '{"topic": "Securities Industry", "depth": "comprehensive"}'
```

### 2. Check Task Status

```bash
python3 Multi-Agent-System/agent_orchestrator.py get-status task_20261019_160000_123456
```

### 3. List All Tasks

```bash
python3 Multi-Agent-System/agent_orchestrator.py list-tasks
```

### 4. List Tasks for Specific Agent

```bash
python3 Multi-Agent-System/agent_orchestrator.py list-tasks claude-research
```

### 5. Agent Creates Content

```python
from agent_interface import AgentVaultInterface

agent = AgentVaultInterface("claude-research")

# Create a flashcard
agent.create_flashcard(
    front="What are the main SIE topics?",
    back="Investment products, markets, and regulations",
    deck="sie-fundamentals",
    tags=["sie", "exam"]
)

# Write a research note
agent.write_note(
    "Core-Ops/research-agent/securities-101.md",
    "# Securities Industry Basics\n\n...",
    tags=["research", "securities"]
)

# Search for related content
results = agent.search_notes("securities", "Core-Ops")
```

## Workflow Example: Study Material Creation

```
1. User submits task: "Create flashcards for Options Trading"
   ↓
2. Orchestrator assigns to Claude Research Agent
   ↓
3. Research Agent:
   - Searches existing notes
   - Generates comprehensive content
   - Creates flashcards
   - Writes to Core-Ops/research-agent/
   ↓
4. Sends message to Synthesis Agent
   ↓
5. Synthesis Agent:
   - Reviews content
   - Identifies gaps
   - Creates summary connections
   ↓
6. Sends message to Review Agent
   ↓
7. Review Agent:
   - Checks accuracy
   - Verifies consistency
   - Provides feedback
   ↓
8. Final content ready in Core-Ops/
```

## Inter-Agent Communication

Agents can communicate via the message queue:

```python
# Agent A sends to Agent B
agent_a.send_message_to_agent("claude-synthesis", {
    "type": "content-ready",
    "content_path": "Core-Ops/research-agent/new-notes.md",
    "message": "Research complete, ready for synthesis"
})

# Agent B reads from message queue
import json
queue_dir = Path("Multi-Agent-System/message-queue")
for msg_file in queue_dir.glob("msg_*.json"):
    with open(msg_file) as f:
        msg = json.load(f)
        if msg["to"] == "claude-synthesis":
            # Process message
            pass
```

## Permissions Model

Each agent has restricted read/write access:

```json
{
  "permissions": {
    "read": ["Core-Ops", "Command-Center"],    // Can read from these dirs
    "write": ["Core-Ops/research-agent"],      // Can only write here
    "execute": false                            // Cannot run commands
  }
}
```

## Activity Logging

All agent actions are logged in `Multi-Agent-System/logs/<agent_id>.jsonl`:

```json
{
  "timestamp": "2026-10-19T16:00:00.000000",
  "agent_id": "claude-research",
  "activity": "flashcard_created",
  "details": {
    "deck": "sie-fundamentals",
    "count": 5
  }
}
```

## Task Status Flow

```
PENDING → IN_PROGRESS → COMPLETED
           ↓
         FAILED (with error message)
```

## Integration with Claude

### Via Claude Code Session

```bash
# In Claude Code, agents can be driven by Claude directly
claude-code-session --run-agent claude-research --task "research_task_id"
```

### Via API Calls

Each agent can call Claude's API directly when implementing task logic:

```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Research SIE topics and create notes"}
    ]
)
```

## Best Practices

1. **Task Granularity**: Keep tasks focused (one agent, one responsibility)
2. **Permissions**: Follow principle of least privilege - agents only access what they need
3. **Monitoring**: Check `Multi-Agent-System/logs/` to monitor agent activity
4. **Messages**: Use message queue for agent-to-agent coordination
5. **Error Handling**: Check task status for failures, review error messages

## Troubleshooting

### Task Stuck in PENDING
- Check if agent_id is correct: `python3 agent_orchestrator.py agent-info <agent_id>`
- Verify permissions in agents.config.json

### Agent Cannot Write File
- Check write permissions in agents.config.json
- Ensure directory path matches permission pattern

### Messages Not Being Delivered
- Verify target agent_id exists
- Check message queue directory exists

## Future Enhancements

- [ ] Web UI for task management
- [ ] Real-time agent status dashboard
- [ ] Advanced scheduling and workflows
- [ ] Agent collaboration templates
- [ ] Performance metrics and analytics
- [ ] Webhook integrations for external triggers
