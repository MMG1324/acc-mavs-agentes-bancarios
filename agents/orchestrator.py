# agents/orchestrator.py

from typing import List, Dict, Any

class OrchestratorAgent:
    """
    Very simple placeholder orchestrator.
    For now it just echoes the user.
    Later we'll plug LangChain + sub-agents here.
    """

    def __init__(self):
        pass

    def handle_message(self, user_message: str, history: List[Dict[str, Any]]) -> str:
        # TODO: replace this with intent detection + routing to sub-agents
        return f"Orchestrator: I received your message -> '{user_message}'"
