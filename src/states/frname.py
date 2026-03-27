from src.tools import get_logits
from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np


def run_fr_name(
    model_ins: Small_LLM_Model,
    encoded_prompt: list[int],
    closing_tokens: list[int],
    output_list: list[int],
    needed_chars: list[int],
):
    runnable: bool = True
    while runnable:
        logits = get_logits(model_ins, encoded_prompt)
        token = int(np.argmax(logits))

        encoded_prompt.append(token)
        output_list.append(token)

        if token in closing_tokens:
            runnable = False


# this will 100% work
