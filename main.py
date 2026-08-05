from agents.ai_agents import AIAgent
from core.observation import Observation 

agent_instance = AIAgent()

def agent (observation):

    obs = Observation(raw_data =observation)

    return agent_instance.act(obs)