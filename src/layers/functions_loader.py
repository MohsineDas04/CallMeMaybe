from src.models.functions_data import FunctionModel
from typing import List
import json


def load_available_funcs() -> List[FunctionModel]:
    with open("./data/input/functions_definition.json", "r") as func_def:
        funcs_data = json.load(func_def)
    funcs_ins: List[FunctionModel] = []
    for f in funcs_data:
        funcs_ins.append(
            FunctionModel(
                name=f["name"],
                description=f["description"],
                parameters=f["parameters"],
                returns=f["returns"],
            )
        )
    return funcs_ins
