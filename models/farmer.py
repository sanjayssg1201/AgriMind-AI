from dataclasses import dataclass 

@dataclass

class Worker:
    """Represents the farmer or a hired farm hand."""

    worker_id:int
    x:int 
    y:int 
    busy:bool