from src.layers import get_vocabulary
from src.tools import encode, decode, get_logits
from llm_sdk.llm_sdk import Small_LLM_Model
from src.states.foprompt import run_fo_prompt
from src.states.frprompt import run_fr_prompt
import numpy as np


def send_prompt(
    model_ins: Small_LLM_Model, task: str, av_funcs: list, **kwargs
) -> str:
    output_list = []
    encoded_prompt = encode(
        model_ins,
        "you are a function calling ai assistant, your job is to always return function that needs to be called with the needed arguments, following the structure below"
        + "{'prompt': <exact prompt given (ex. 'What is the sum of 2 and 3?)>,'name':<function name (ex. 'fn_add_numbers)>,'parameters': <parameters with they're values in json (ex. {'a': 2.0, 'b': 3.0}>}"
        + ".don't ever output anything except the given json."
        f"available function are {av_funcs}"
        + f"here is your first job: {task}"
        + "the last thing you should print is always that closing brace."
        + "it should be brought as a single token",
    )
    vocab = get_vocabulary(model_ins)
    # if vocab['?",Ġ"']:
    #     print(f"{decode(model_ins, [vocab['?",Ġ"']])} exists")
    #     print(f"{decode(model_ins, [vocab['"']])} exists")
    #     exit(0)
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

    return decode(model_ins, output_list)
    # openbrace_id = vocab["{"]
    # closingbrace_id = vocab["}"]
    # doubleclosing = vocab["}}"]
    # print(f"id of openbrace: {openbrace_id}")
    # print("=" * 42, f"\nencoded prompt : {encoded_prompt}\n", "=" * 42)
    # logits = get_logits(model_ins, encoded_prompt)
    # openbrace_proba = logits[openbrace_id]
    # print("All logits probs")
    # print("=" * 42)
    # print("=" * 42)
    # print(f"score for openbrace ({{) (likely the highest): {openbrace_proba}")
    # print(f"the highest one is : {logits.max()}\n")
    # print("=" * 42)
    # mask = np.full(logits.shape, -np.inf)
    # mask[openbrace_id] = logits[openbrace_id]
    # forced_token = int(np.argmax(mask))
    # encoded_prompt.append(forced_token)
    # output_list.append(forced_token)
    # output = decode(model_ins, output_list)
    # print("=" * 42)
    # print(f"output {2}: {output}\n")
    # print(f"new token {repr(decode(model_ins, [forced_token]))}\n")
    # print("=" * 42)
    # logits = get_logits(model_ins, encoded_prompt)
    # mask = np.full(logits.shape, -np.inf)
    # mask[vocab['"']] = logits[vocab['"']]
    # forced_token = int(np.argmax(mask))
    # encoded_prompt.append(forced_token)
    # output_list.append(forced_token)
    # output = decode(model_ins, output_list)
    # print("=" * 42)
    # print(f"output {2}: {output}\n")
    # print(f"new token {repr(decode(model_ins, [forced_token]))}\n")
    # print("=" * 42)
    # ############################################################
    # i = 3
    # last_three: str = ""
    # while last_three[:2] != "}}":
    #     logits = get_logits(model_ins, encoded_prompt)
    #     # mask = np.full(logits.shape, -np.inf)
    #     # mask[vocab['"']] = logits[vocab['"']]
    #     forced_token = int(np.argmax(logits))
    #     encoded_prompt.append(forced_token)
    #     output_list.append(forced_token)
    #     output = decode(model_ins, output_list)
    #     last_three = output[-3:]
    #     print("=" * 42)
    #     print(f"output {i}: {output}\n")
    #     print(f"new token {repr(decode(model_ins, [forced_token]))}\n")
    #     print("=" * 42)
    # # output = decode(model_ins, output_list)
    # return output
