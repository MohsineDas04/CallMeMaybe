from src.engine import send_prompt
from src.layers import model_instantiate
import traceback
import sys
from src.layers import load_available_funcs


def main():
    model_ins = model_instantiate()
    av_funcs = load_available_funcs()
    ret = send_prompt(
        model_ins,
        "you are a function calling ai assistant, your job is to always return function that needs to be called with the needed arguments, following the structure below"
        + "{'prompt': <exact prompt given (ex. 'What is the sum of 2 and 3?)>,'name':<function name (ex. 'fn_add_numbers)>,'parameters': <parameters with they're values in json (ex. {'a': 2.0, 'b': 3.0}>}"
        + ".don't ever output anything except the given json."
        f"available function are {av_funcs}"
        + "here is your first job: what is the sum of 5 and 10"
        + "the last thing you should print is always that closing brace."
        + "it should be brought as a single token",
    )
    print(ret)


try:
    main()
except Exception as e:
    print(f"catched a {type(e).__name__}\n{e}")
    print(f"traceback:\n{traceback.print_exc()}")
