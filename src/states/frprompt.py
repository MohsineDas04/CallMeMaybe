from src.tools import encode, decode, get_logits
from llm_sdk.llm_sdk import Small_LLM_Model


def run_fr_prompt(
    model_ins: Small_LLM_Model,
    task,
    encoded_prompt: list[int],
    output_list: list[int],
    needed_chars: list[int],
) -> None:
    safe_task = task.replace('"', '\\"')
    encoded_task = encode(model_ins, safe_task)
    for token in encoded_task:
        encoded_prompt.append(token)
        output_list.append(token)
    for char in needed_chars:
        encoded_prompt.append(char)
        output_list.append(char)
