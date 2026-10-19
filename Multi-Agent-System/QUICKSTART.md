# Multi-Agent Obsidian System - Quick Start

Get started with the multi-agent system in 5 minutes.

## Prerequisites

- Python 3.8+
- Anthropic API key (set as `ANTHROPIC_API_KEY` environment variable)
- Existing Obsidian vault

## 1. Set Up Environment

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Navigate to vault
cd <path-to-vault>

# Verify structure
ls -la Multi-Agent-System/
```

## 2. Create a Task

### Option A: Using the CLI

```bash
# Create a research task
python3 Multi-Agent-System/agent_orchestrator.py submit-task \
  "research" \
  "claude-research" \
  "Create SIE exam study guide" \
  '{"topic": "Investment Products", "format": "structured-notes"}'
```

### Option B: Using Python API

Create a file `submit_task.py`:

```python
from Multi_Agent_System.agent_orchestrator import AgentOrchestrator
import json

orchestrator = AgentOrchestrator()

task_id = orchestrator.submit_task(
    task_type="research",
    agent_id="claude-research",
    description="Create comprehensive SIE study notes on bonds and fixed income",
    input_data={
        "topic": "Fixed Income Securities",
        "subtopics": ["Bond Types", "Yield Calculations", "Duration"],
        "depth": "comprehensive"
    }
)

print(f"Task submitted: {task_id}")
```

Run it:
```bash
cd <path-to-vault>
python3 submit_task.py
```

## 3. Agent Processes Task

The agent performs the work:

```python
# agent_implementation.py - Run by the agent
from Multi_Agent_System.agent_interface import AgentVaultInterface
import json

agent = AgentVaultInterface("claude-research")

# 1. Search existing content
results = agent.search_notes("Fixed Income")
print(f"Found {len(results)} existing notes")

# 2. Create new flashcards
flashcards = [
    ("What is duration?", "A measure of bond price sensitivity to interest rate changes"),
    ("Types of bonds", "Government, Corporate, Municipal, High-Yield"),
    ("Yield curve", "Graph showing yields for bonds of different maturities"),
]

for front, back in flashcards:
    agent.create_flashcard(front, back, deck="fixed-income", tags=["sie", "bonds"])

# 3. Write comprehensive notes
notes = """# Fixed Income Securities

## Bond Basics
- Fixed income instrument with regular coupon payments
- Principal repaid at maturity
- Lower risk than equities

## Bond Types
1. **Government Bonds**: Backed by government
2. **Corporate Bonds**: Issued by companies
3. **Municipal Bonds**: Issued by states/municipalities
...
"""

agent.write_note(
    "Core-Ops/research-agent/fixed-income-guide.md",
    notes,
    tags=["sie", "bonds", "fixed-income"]
)

# 4. Log the work
agent.log_activity("research_complete", {
    "topic": "Fixed Income Securities",
    "flashcards_created": len(flashcards),
    "notes_written": True
})

print("Research task complete!")
```

## 4. Monitor Task Status

```bash
# Get task status
python3 Multi-Agent-System/agent_orchestrator.py get-status <task_id>

# List all tasks
python3 Multi-Agent-System/agent_orchestrator.py list-tasks

# List tasks for specific agent
python3 Multi-Agent-System/agent_orchestrator.py list-tasks claude-research

# List completed tasks
python3 Multi-Agent-System/agent_orchestrator.py list-tasks "" "completed"
```

## 5. Review Results

### Check Vault Files

```bash
# View created notes
cat Core-Ops/research-agent/fixed-income-guide.md

# View flashcards
ls -la Flashcards/fixed-income/
cat Flashcards/fixed-income/card_*.md
```

### Check Activity Logs

```bash
# View agent activity
tail -20 Multi-Agent-System/logs/claude-research.jsonl | jq .
```

## 6. Multi-Agent Workflow Example

Create a complete workflow with multiple agents:

```python
# workflow.py
from Multi_Agent_System.agent_orchestrator import AgentOrchestrator
from Multi_Agent_System.agent_interface import AgentVaultInterface
import json

orchestrator = AgentOrchestrator()

# Step 1: Research Agent creates content
print("Step 1: Submitting research task...")
task1 = orchestrator.submit_task(
    "research",
    "claude-research",
    "Research options trading strategies",
    {"topic": "Options", "detail": "high"}
)

# (Simulate agent processing)
print("Step 2: Research agent working...")
research_agent = AgentVaultInterface("claude-research")
research_agent.create_flashcard(
    "What is a call option?",
    "Right to buy an asset at a specific price",
    deck="options",
    tags=["derivatives", "options"]
)

# Step 3: Synthesis agent reviews and creates connections
print("Step 3: Submitting synthesis task...")
task2 = orchestrator.submit_task(
    "synthesis",
    "claude-synthesis",
    "Synthesize options trading with other derivatives",
    {"source_topic": "Options", "connect_to": ["Futures", "Swaps"]}
)

synthesis_agent = AgentVaultInterface("claude-synthesis")
synthesis_agent.send_message_to_agent("claude-review", {
    "type": "ready_for_review",
    "content": "Core-Ops/synthesis-agent/options-connections.md"
})

# Step 4: Review agent validates
print("Step 4: Submitting review task...")
task3 = orchestrator.submit_task(
    "review",
    "claude-review",
    "Review all options content for accuracy",
    {"content_paths": ["Core-Ops/research-agent", "Core-Ops/synthesis-agent"]}
)

# Check status
print(f"\nTask statuses:")
print(f"  Research: {orchestrator.get_task_status(task1)['status']}")
print(f"  Synthesis: {orchestrator.get_task_status(task2)['status']}")
print(f"  Review: {orchestrator.get_task_status(task3)['status']}")
```

Run the workflow:
```bash
cd <path-to-vault>
python3 workflow.py
```

## 7. Common Tasks

### Create Study Materials
```bash
python3 Multi-Agent-System/agent_orchestrator.py submit-task \
  "content-creation" \
  "claude-research" \
  "Create comprehensive study guide on municipal bonds" \
  '{"topic": "Municipal Bonds", "format": "guide-with-flashcards"}'
```

### Review for Accuracy
```bash
python3 Multi-Agent-System/agent_orchestrator.py submit-task \
  "review" \
  "claude-review" \
  "Quality check all bond-related content" \
  '{"content_directory": "Core-Ops/research-agent", "focus": "accuracy"}'
```

### Synthesize Multiple Topics
```bash
python3 Multi-Agent-System/agent_orchestrator.py submit-task \
  "synthesis" \
  "claude-synthesis" \
  "Create connections between fixed income and equity markets" \
  '{"topics": ["Fixed Income", "Equities"], "connection_type": "market-relationships"}'
```

## 8. Verify Installation

```bash
# Test orchestrator
python3 Multi-Agent-System/agent_orchestrator.py agent-info claude-research

# Test agent interface
python3 Multi-Agent-System/agent_interface.py

# Check directory structure
tree Multi-Agent-System/ -L 2
# or
find Multi-Agent-System/ -type d | head -20
```

## 9. Next Steps

1. **Customize agents**: Edit `agents.config.json` to adjust agent capabilities
2. **Create workflows**: Build domain-specific workflows for your study needs
3. **Monitor activity**: Check `Multi-Agent-System/logs/` regularly
4. **Integrate with Claude**: Use this in Claude Code sessions for automated task creation
5. **Scale up**: Add more specialized agents as needed

## Troubleshooting

### Import Errors
```bash
# Add to Python path
export PYTHONPATH="<path-to-vault>/Multi-Agent-System:$PYTHONPATH"
```

### Permission Denied
```bash
# Make scripts executable
chmod +x Multi-Agent-System/*.py
```

### API Key Issues
```bash
# Verify API key
echo $ANTHROPIC_API_KEY

# If not set, add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="your-key-here"
```

## Support

For issues or questions:
1. Check `Multi-Agent-System/README.md` for detailed documentation
2. Review task logs: `cat Multi-Agent-System/logs/*.jsonl`
3. Check task status: `python3 agent_orchestrator.py get-status <task_id>`
