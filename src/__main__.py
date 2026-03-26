from src.engine import send_prompt
from src.layers import model_instantiate, load_available_funcs, load_prompts
import traceback
import sys


def main():
    model_ins = model_instantiate()
    av_funcs = load_available_funcs()
    # prompts = load_prompts()
    # test_n = 1
    ret = send_prompt(
        model_ins,
        "you are a function calling ai assistant, your job is to always return function that needs to be called with the needed arguments, following the structure below"
        + "{'prompt': <exact prompt given (ex. 'What is the sum of 2 and 3?)>,'name':<function name (ex. 'fn_add_numbers)>,'parameters': <parameters with they're values in json (ex. {'a': 2.0, 'b': 3.0}>}"
        + ".don't ever output anything except the given json."
        f"available function are {av_funcs}"
        + f"here is your first job: what is the sum of 5 and 10"
        + "the last thing you should print is always that closing brace."
        + "it should be brought as a single token",
    )
    print(ret)
    # for pr in prompts:
    #     print("*" * 45)
    #     print(f"test {test_n} prompt: {pr["prompt"]}\n")
    #     print("*" * 45)
    #     ret = send_prompt(
    #         model_ins,
    #         "you are a function calling ai assistant, your job is to always return function that needs to be called with the needed arguments, following the structure below"
    #         + "{'prompt': <exact prompt given (ex. 'What is the sum of 2 and 3?)>,'name':<function name (ex. 'fn_add_numbers)>,'parameters': <parameters with they're values in json (ex. {'a': 2.0, 'b': 3.0}>}"
    #         + ".don't ever output anything except the given json."
    #         f"available function are {av_funcs}"
    #         + f"here is your first job: {pr["prompt"]}"
    #         + "the last thing you should print is always that closing brace."
    #         + "it should be brought as a single token",
    #     )
    #     print(f"final output for test {test_n} is : \n{ret}\n")
    #     test_n += 1


try:
    main()
except (Exception, KeyboardInterrupt) as e:
    print(f"catched a {type(e).__name__}\n{e}")
    print(
        f"traceback:\n{traceback.print_exc()}"
    )  # we print traceback to know which file exactly the error happened
