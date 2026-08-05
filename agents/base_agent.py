from abc import ABC,abstractmethod

from core.action import Action
from core.observation import Observation 

class BaseAgent (ABC):
    """
    Base class for every agent

    """    
    @abstractmethod
    def act(self,observation:Observation) -> Action:
        """
        Return the next Action

        """    
        raise NotImplementedError    