#!/usr/bin/env python3
"""
Agent Interface for Multi-Agent Obsidian System
Provides API for agents to interact with the vault
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import hashlib


class AgentVaultInterface:
    """Interface for agents to interact with the Obsidian vault"""

    def __init__(self, agent_id: str, vault_root: str = "/home/user/SIE-Flashcard-Set-2026"):
        self.agent_id = agent_id
        self.vault_root = Path(vault_root)
        self.agent_workspace = self.vault_root / "Multi-Agent-System" / f"agent-workspace-{agent_id}"
        self.agent_workspace.mkdir(parents=True, exist_ok=True)

    def read_note(self, file_path: str) -> Optional[str]:
        """Read a note from the vault"""
        full_path = self.vault_root / file_path
        if full_path.exists() and full_path.is_file():
            with open(full_path) as f:
                return f.read()
        return None

    def write_note(self, file_path: str, content: str, tags: Optional[List[str]] = None) -> bool:
        """Write a note to the vault with agent metadata"""
        full_path = self.vault_root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        metadata = {
            "agent": self.agent_id,
            "created": datetime.now().isoformat(),
            "tags": tags or []
        }

        header = f"""---
agent: {self.agent_id}
created: {metadata['created']}
tags: {json.dumps(tags or [])}
---

"""
        try:
            with open(full_path, "w") as f:
                f.write(header + content)
            return True
        except Exception as e:
            print(f"Error writing note: {e}")
            return False

    def list_notes(self, directory: str = "Core-Ops") -> List[str]:
        """List all notes in a directory"""
        target_dir = self.vault_root / directory
        notes = []
        if target_dir.exists():
            for md_file in target_dir.rglob("*.md"):
                rel_path = md_file.relative_to(self.vault_root)
                notes.append(str(rel_path))
        return notes

    def search_notes(self, query: str, directory: str = "Core-Ops") -> List[Dict[str, Any]]:
        """Search for notes containing a query string"""
        results = []
        target_dir = self.vault_root / directory

        if not target_dir.exists():
            return results

        for md_file in target_dir.rglob("*.md"):
            try:
                with open(md_file) as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        rel_path = str(md_file.relative_to(self.vault_root))
                        # Extract first 200 chars of context
                        lines = content.split("\n")
                        matching_lines = [l for l in lines if query.lower() in l.lower()]
                        results.append({
                            "file": rel_path,
                            "matches": len(matching_lines),
                            "context": matching_lines[:3]
                        })
            except Exception as e:
                print(f"Error searching {md_file}: {e}")

        return sorted(results, key=lambda x: x["matches"], reverse=True)

    def create_flashcard(self, front: str, back: str, deck: str = "default", tags: Optional[List[str]] = None) -> bool:
        """Create a flashcard note"""
        card_id = hashlib.md5(f"{front}{back}".encode()).hexdigest()[:8]
        deck_dir = self.vault_root / "Flashcards" / deck
        deck_dir.mkdir(parents=True, exist_ok=True)

        card_content = f"""# {front}

## Answer
{back}

## Deck
{deck}

## Created by
Agent: {self.agent_id}
Timestamp: {datetime.now().isoformat()}
"""

        card_file = deck_dir / f"card_{card_id}.md"
        try:
            with open(card_file, "w") as f:
                f.write(card_content)
            return True
        except Exception as e:
            print(f"Error creating flashcard: {e}")
            return False

    def update_task(self, task_id: str, status: str, result: Optional[Dict] = None) -> bool:
        """Update a task status (for orchestrator integration)"""
        tasks_dir = self.vault_root / "Multi-Agent-System" / "tasks"
        task_file = tasks_dir / f"{task_id}.json"

        if task_file.exists():
            try:
                with open(task_file) as f:
                    task_data = json.load(f)

                task_data["status"] = status
                task_data["completed_at"] = datetime.now().isoformat()
                if result:
                    task_data["result"] = result

                with open(task_file, "w") as f:
                    json.dump(task_data, f, indent=2)
                return True
            except Exception as e:
                print(f"Error updating task: {e}")
                return False
        return False

    def send_message_to_agent(self, target_agent_id: str, message: Dict[str, Any]) -> bool:
        """Send a message to another agent"""
        queue_dir = self.vault_root / "Multi-Agent-System" / "message-queue"
        queue_dir.mkdir(parents=True, exist_ok=True)

        message_data = {
            "from": self.agent_id,
            "to": target_agent_id,
            "timestamp": datetime.now().isoformat(),
            "payload": message
        }

        msg_id = hashlib.md5(
            f"{self.agent_id}{target_agent_id}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:8]

        msg_file = queue_dir / f"msg_{msg_id}.json"
        try:
            with open(msg_file, "w") as f:
                json.dump(message_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def get_agent_workspace_info(self) -> Dict[str, Any]:
        """Get information about this agent's workspace"""
        files = list(self.agent_workspace.glob("*"))
        return {
            "agent_id": self.agent_id,
            "workspace_path": str(self.agent_workspace),
            "files_count": len(files),
            "files": [f.name for f in files]
        }

    def log_activity(self, activity_type: str, details: Dict[str, Any]) -> bool:
        """Log agent activity"""
        log_dir = self.vault_root / "Multi-Agent-System" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{self.agent_id}.jsonl"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "activity": activity_type,
            "details": details
        }

        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False


def main():
    """Example usage"""
    interface = AgentVaultInterface("claude-research")

    # Create a sample flashcard
    interface.create_flashcard(
        "What is the SIE exam?",
        "The Securities Industry Essentials (SIE) exam is a test for entry-level securities professionals.",
        deck="financial-basics"
    )

    # Log activity
    interface.log_activity("flashcard_created", {
        "deck": "financial-basics",
        "count": 1
    })

    print(json.dumps(interface.get_agent_workspace_info(), indent=2))


if __name__ == "__main__":
    main()
