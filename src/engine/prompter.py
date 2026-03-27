from src.layers import get_vocabulary
from src.tools import encode, decode
from llm_sdk.llm_sdk import Small_LLM_Model
from src.states.foprompt import run_fo_prompt
from src.states.frprompt import run_fr_prompt
from src.states.foname import run_fo_name
from src.states.frname import run_fr_name
from src.states.foparam import run_fo_param
from src.states.frparam import run_fr_param


def send_prompt(
    model_ins: Small_LLM_Model, task: str, av_funcs: list, **kwargs
) -> str:
    output_list = []
    encoded_prompt = encode(
        model_ins,
        f"Available functions: {av_funcs}\n\nTask: {task}\n\nOutput the JSON function call:",
    )
    vocab = get_vocabulary(model_ins)
    closings = []
    closing_brace = []
    for key, v in vocab.items():
        closings.append(v) if '"' in key else None
        (
            closing_brace.append(v) if "}" in key else None
        )
    run_fo_prompt(
        model_ins,
        encoded_prompt,
        [
            vocab["{"],
            vocab['"'],
            vocab["prompt"],
            vocab['":'],
            vocab['Ġ"'],
        ],
        output_list,
    )
    run_fr_prompt(
        model_ins,
        task,
        encoded_prompt,
        output_list,
        [vocab['",'], vocab['Ġ"']],
    )
    run_fo_name(
        model_ins,
        encoded_prompt,
        [
            vocab["name"],
            vocab['":'],
            vocab['Ġ"'],
        ],
        output_list,
    )
    run_fr_name(
        model_ins,
        encoded_prompt,
        closings,
        output_list,
        [vocab['",'], vocab['Ġ"']],
    )
    run_fo_param(
        model_ins,
        encoded_prompt,
        [
            vocab['"'],
            vocab["parameters"],
            vocab['":'],
            vocab['Ġ{"'],
        ],
        output_list,
    )
    run_fr_param(
        model_ins,
        encoded_prompt,
        closing_brace,
        output_list,
        [vocab["}"], vocab["}"]],
        vocab,
    )
    return decode(model_ins, output_list)
