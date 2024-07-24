from dataclasses import dataclass
from typing import List, Dict, Any

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
            "temperature": "Room temperature",
            "duration": "24 hours",
            "state": "Anhydrous"
        },
        time="24 hours",
        procedure=[
            ProcedureStep(timestamp=0, action="add", parameters={"compound": "thiamine", "solvent": "ethanol"}),
            ProcedureStep(timestamp=5, action="add_dropwise", parameters={"compound": "NaOH", "cooling": True}),
            ProcedureStep(timestamp=10, action="add", parameters={"compound": "benzaldehyde", "swirl": True}),
            ProcedureStep(timestamp=15, action="seal", parameters={"method": "Parafilm", "storage": "room temperature"})
        ]
    ),
    ReactionStep(
        reaction="C6H5CHOHCOC6H5 + HNO3 -> C6H5COCOC6H5",
        conditions={
            "reagent": "Concentrated nitric acid",
            "temperature": "Steam bath",
            "duration": "30 minutes",
            "state": "Fume hood"
        },
        time="30 minutes",
        procedure=[
            ProcedureStep(timestamp=0, action="transfer", parameters={"compound": "benzoin", "mols": 2.0, "transferrate": "slow"}),
            ProcedureStep(timestamp=5, action="heat", parameters={"method": "steam bath", "swirl": True}),
            ProcedureStep(timestamp=30, action="cool", parameters={"method": "tap water", "cover": "plastic seal"}),
            ProcedureStep(timestamp=35, action="filter", parameters={"method": "suction", "wash": "cool water"})
        ]
    ),
    ReactionStep(
        reaction="C6H5COCOC6H5 + C6H5CH2COC6H5 -> (C6H5)4C4H2O",
        conditions={
            "reagent": "KOH",
            "solvent": "Ethanol",
            "temperature": "Reflux",
            "duration": "15 minutes",
            "state": "Anhydrous"
        },
        time="15 minutes",
        procedure=[
            ProcedureStep(timestamp=0, action="add", parameters={"compounds": ["benzil", "dibenzyl ketone"], "solvent": "ethanol"}),
            ProcedureStep(timestamp=5, action="attach", parameters={"equipment": "reflux condenser", "heat": "steam bath"}),
            ProcedureStep(timestamp=10, action="add_dropwise", parameters={"compound": "KOH solution"}),
            ProcedureStep(timestamp=15, action="cool", parameters={"method": "ice bath", "filter": "product"})
        ]
    ),
    ReactionStep(
        reaction="C6H5COCOC6H5 + NaBH4 -> C6H5CHOHCH(OH)C6H5",
        conditions={
            "reagent": "NaBH4",
            "solvent": "Ethanol",
            "temperature": "Room temperature",
            "duration": "10 minutes",
            "state": "Aqueous"
        },
        time="10 minutes",
        procedure=[
            ProcedureStep(timestamp=0, action="dissolve", parameters={"compound": "benzil", "solvent": "ethanol"}),
            ProcedureStep(timestamp=2, action="cool", parameters={"method": "water bath"}),
            ProcedureStep(timestamp=5, action="add", parameters={"compound": "NaBH4"}),
            ProcedureStep(timestamp=10, action="heat", parameters={"method": "boiling"})
        ]
    ),
    ReactionStep(
        reaction="(C6H5)4C4H2O + C6H4(CO2CH3)2 -> (C6H5)4C6H4(CO2CH3)2",
        conditions={
            "reagent": "Dimethyl acetylenedicarboxylate",
            "solvent": "Triethylene glycol",
            "temperature": "Microwave",
            "duration": "5 minutes",
            "state": "Heated"
        },
        time="5 minutes",
        procedure=[
            ProcedureStep(timestamp=0, action="mix", parameters={"compounds": ["tetraphenylcyclopentadienone", "dimethyl acetylenedicarboxylate"], "solvent": "triethylene glycol"}),
            ProcedureStep(timestamp=1, action="microwave", parameters={"power_level": 6}),
            ProcedureStep(timestamp=6, action="cool", parameters={"method": "room temperature"}),
            ProcedureStep(timestamp=10, action="filter", parameters={"method": "micro Hirsch funnel", "wash": "cold ethanol"})
        ]
    )
]