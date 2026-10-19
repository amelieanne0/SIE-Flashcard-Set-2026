#!/usr/bin/env python3
"""
Multi-Agent Orchestrator for Obsidian Vault
Coordinates multiple AI agents working on shared knowledge base
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    type: str
    agent_id: str
    description: str
    input_data: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class AgentOrchestrator:
    def __init__(self, config_path: str = str(Path(__file__).resolve().parent / "agents.config.json")):
        self.config_path = Path(config_path)
        self.vault_root = Path(__file__).resolve().parent.parent
        self.queue_path = self.vault_root / "Multi-Agent-System" / "message-queue"
        self.tasks_path = self.vault_root / "Multi-Agent-System" / "tasks"

        self.queue_path.mkdir(parents=True, exist_ok=True)
        self.tasks_path.mkdir(parents=True, exist_ok=True)

        self.config = self._load_config()
        self.agents = {agent["id"]: agent for agent in self.config.get("agents", [])}
        self.task_queue: List[Task] = []

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path) as f:
            return json.load(f)

    def submit_task(
        self,
        task_type: str,
        agent_id: str,
        description: str,
        input_data: Dict[str, Any],
    ) -> str:
        """Submit a task to the queue"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        task = Task(
            id=task_id,
            type=task_type,
            agent_id=agent_id,
            description=description,
            input_data=input_data,
        )

        self.task_queue.append(task)
        self._save_task(task)
        return task_id

    def _save_task(self, task: Task):
        task_file = self.tasks_path / f"{task.id}.json"
        with open(task_file, "w") as f:
            task_dict = asdict(task)
            task_dict["status"] = task.status.value
            json.dump(task_dict, f, indent=2)

    def update_task_status(self, task_id: str, status: TaskStatus, result: Optional[Dict] = None, error: Optional[str] = None):
        """Update task status"""
        task_file = self.tasks_path / f"{task_id}.json"
        if task_file.exists():
            with open(task_file) as f:
                task_data = json.load(f)

            task_data["status"] = status.value
            task_data["completed_at"] = datetime.now().isoformat()
            if result:
                task_data["result"] = result
            if error:
                task_data["error"] = error

            with open(task_file, "w") as f:
                json.dump(task_data, f, indent=2)

    def read_vault_file(self, file_path: str) -> str:
        """Read a file from the vault"""
        full_path = self.vault_root / file_path
        if full_path.exists() and full_path.is_file():
            with open(full_path) as f:
                return f.read()
        raise FileNotFoundError(f"File not found: {file_path}")

    def write_vault_file(self, file_path: str, content: str, agent_id: str) -> bool:
        """Write a file to the vault with agent attribution"""
        # Check permissions
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_id}")

        write_paths = agent["permissions"].get("write", [])

        # Check if agent has write permission
        allowed = False
        for pattern in write_paths:
            if file_path.startswith(pattern):
                allowed = True
                break

        if not allowed:
            raise PermissionError(f"Agent {agent_id} cannot write to {file_path}")

        full_path = self.vault_root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Add agent attribution
        header = f"\n---\nAgents: [{agent_id}]\nLast-Modified: {datetime.now().isoformat()}\n---\n\n"
        with open(full_path, "w") as f:
            f.write(header + content)

        return True

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task"""
        task_file = self.tasks_path / f"{task_id}.json"
        if task_file.exists():
            with open(task_file) as f:
                return json.load(f)
        return None

    def list_tasks(self, agent_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all tasks, optionally filtered"""
        tasks = []
        for task_file in self.tasks_path.glob("task_*.json"):
            with open(task_file) as f:
                task = json.load(f)

            if agent_id and task.get("agent_id") != agent_id:
                continue
            if status and task.get("status") != status:
                continue

            tasks.append(task)

        return sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)

    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an agent"""
        return self.agents.get(agent_id)


def main():
    orchestrator = AgentOrchestrator()

    if len(sys.argv) < 2:
        print("Usage: agent_orchestrator.py <command> [args]")
        print("Commands:")
        print("  submit-task <type> <agent-id> <description> <input-json>")
        print("  get-status <task-id>")
        print("  list-tasks [agent-id] [status]")
        print("  agent-info <agent-id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "submit-task" and len(sys.argv) >= 5:
        task_type = sys.argv[2]
        agent_id = sys.argv[3]
        description = sys.argv[4]
        input_data = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}

        task_id = orchestrator.submit_task(task_type, agent_id, description, input_data)
        print(json.dumps({"task_id": task_id, "status": "submitted"}))

    elif command == "get-status" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        status = orchestrator.get_task_status(task_id)
        print(json.dumps(status or {"error": "Task not found"}))

    elif command == "list-tasks":
        agent_id = sys.argv[2] if len(sys.argv) > 2 else None
        status = sys.argv[3] if len(sys.argv) > 3 else None
        tasks = orchestrator.list_tasks(agent_id, status)
        print(json.dumps(tasks, indent=2))

    elif command == "agent-info" and len(sys.argv) >= 3:
        agent_id = sys.argv[2]
        info = orchestrator.get_agent_info(agent_id)
        print(json.dumps(info or {"error": "Agent not found"}))


if __name__ == "__main__":
    main()
