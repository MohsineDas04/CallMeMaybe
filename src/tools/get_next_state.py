import json
from typing import Any

with open("src/data/states.json", "r") as stts:
    states = json.load(stts)


def next_state(current_state: str) -> Any:
    if current_state == "OPENING_STATE":
        return states["FORCED_PROMPT_STATE"]
    if current_state == "FORCED_PROMPT_STATE":
        return states["FREE_PROMPT_STATE"]
    if current_state == "FREE_PROMPT_STATE":
        return states["FORCED_NAME_STATE"]
    if current_state == "FORCED_NAME_STATE":
        return states["FREE_NAME_STATE"]
    if current_state == "FREE_NAME_STATE":
        return states["FORCED_PARAMS_STATE"]
    if current_state == "FORCED_PARAMS_STATE":
        return states["FREE_PARAMS_STATE"]
