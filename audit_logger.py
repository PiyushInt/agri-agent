import sqlite3
import json
import os
from datetime import datetime
from typing import Any, Dict

class AuditLogger:
    """
    Immutable Audit Log System for Compliance
    Logs all steps: User input, thoughts, tool invocations, and guardrail validations.
    """
    def __init__(self, db_path: str = "audit_log.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                event_type TEXT,
                details TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _log(self, session_id: str, event_type: str, details: Dict[str, Any]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO compliance_logs (session_id, timestamp, event_type, details) VALUES (?, ?, ?, ?)",
            (session_id, timestamp, event_type, json.dumps(details))
        )
        conn.commit()
        conn.close()

    def log_user_prompt(self, session_id: str, prompt: str):
        self._log(session_id, "USER_PROMPT", {"prompt": prompt})

    def log_guardrail_check(self, session_id: str, check_type: str, status: str, reason: str = ""):
        self._log(session_id, "GUARDRAIL_CHECK", {
            "check_type": check_type,
            "status": status,
            "reason": reason
        })

    def log_tool_execution(self, session_id: str, tool_name: str, args: Dict[str, Any], output: Any):
        self._log(session_id, "TOOL_EXECUTION", {
            "tool_name": tool_name,
            "inputs": args,
            "output": output
        })

    def log_agent_thought(self, session_id: str, thought: str):
        self._log(session_id, "AGENT_THOUGHT", {"thought": thought})

    def log_final_response(self, session_id: str, response: str):
        self._log(session_id, "FINAL_RESPONSE", {"response": response})

    def get_logs(self, session_id: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if session_id:
            cursor.execute("SELECT timestamp, event_type, details FROM compliance_logs WHERE session_id = ? ORDER BY id ASC", (session_id,))
        else:
            cursor.execute("SELECT timestamp, event_type, details FROM compliance_logs ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for r in rows:
            logs.append({
                "timestamp": r[0],
                "event_type": r[1],
                "details": json.loads(r[2])
            })
        return logs
