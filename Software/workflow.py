from dataclasses import dataclass
from typing import List, Dict, Any

## Example workflow for a chemical synthesis

@dataclass
class ProcedureStep:
    timestamp: float
    action: str
    parameters: Dict[str, Any] = None

@dataclass
class ReactionStep:
    reaction: str
    conditions: Dict[str, Any]
    time: str
    procedure: List[ProcedureStep]

steps = [
    ReactionStep(
        reaction="2 * C1=CC=CC=C1C=O -> C6H5CHOHCOC6H5",
        conditions={
            "catalyst": "Thiamine",
            "solvent": "Ethanol",
            "base": "NaOH",
            "duration": "1 hours",
            "state": "Anhydrous"
        },
        time="24 hours",
        procedure=[
            ProcedureStep(timestamp=0, action="select", parameters={"vial": "1"}),
            ProcedureStep(timestamp=0, action="add", parameters={"vial": "123", "vol": "1", "rate": "1"}),
            ProcedureStep(timestamp=5, action="add", parameters={"vial": "456", "vol": "1", "rate": "1"}),
            ProcedureStep(timestamp=10, action="temp", parameters={"vial": "789", "val": "100", "rate": "1"}),
            ProcedureStep(timestamp=10, action="add", parameters={"vial": "777", "vol": "1" ,"rate": "1"}),
            ProcedureStep(timestamp=60, action="seal", parameters={"vail": "1", "storage": "flash_queue"})
        ]
    )
]