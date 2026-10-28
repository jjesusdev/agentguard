from __future__ import annotations
import yaml
from pathlib import Path
from typing import List, Dict, Any
from .events import AgentEvent

class Rule:
    def __init__(self, id_: str, match: dict, action: str):
        self.id = id_
        self.match = match
        self.action = action

    def matches(self, event: AgentEvent) -> bool:
        m = self.match
        if m.get("tool_name") and event.tool_name != m["tool_name"]:
            return False
        if m.get("path_contains"):
            if not event.path or m["path_contains"] not in event.path:
                return False
        if m.get("args_contains"):
            # simple contains check on digest placeholder
            if not event.args_digest or m["args_contains"] not in event.args_digest:
                return False
        return True

class Detector:
    def __init__(self, rules_path: Path):
        self.rules = self._load(rules_path)

    def _load(self, path: Path) -> List[Rule]:
        if not path.exists():
            return []
        data = yaml.safe_load(path.read_text()) or []
        if not isinstance(data, list):
            raise ValueError("rules file must contain a list")
        rules = []
        for i, r in enumerate(data):
            if not isinstance(r, dict):
                raise ValueError(f"rule #{i} must be a dict")
            if "id" not in r or "match" not in r or "action" not in r:
                raise ValueError(f"rule #{i} missing required fields id/match/action")
            if not isinstance(r["match"], dict):
                raise ValueError(f"rule #{i} match must be dict")
            rules.append(Rule(r["id"], r["match"], r["action"]))
        return rules

    def check(self, event: AgentEvent) -> List[Dict[str, Any]]:
        hits = []
        for rule in self.rules:
            if rule.matches(event):
                hits.append({"rule_id": rule.id, "action": rule.action, "event": event.model_dump()})
        return hits
