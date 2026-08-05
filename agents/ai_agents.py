from agents.base_agents import BaseAgent
from core.action import Action
from core.observation import observation

class AIAgent(BaseAgent):
    """
    Main AI Agent 
    
    """    
    def act(self,observation:Observation)->Action:
        return Action(action_type = "PASS")