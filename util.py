import time
import logging

import openai

logging.basicConfig(level=logging.INFO)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = "\033[2m"
    ITALICS = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK  = '\033[5m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE  = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKCYAN = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD = ''
        self.ITALICS = ''
        self.UNDERLINE = ''
        self.BLINK = ''
        self.BLACK = ''
        self.RED = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.BLUE  = ''
        self.MAGENTA = ''
        self.CYAN = ''

    

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{bcolors.DIM}Elapsed time ({func.__name__}): {elapsed_time:.2f} sec{bcolors.ENDC}")
        return result
    return wrapper

def parse_response(raw_response, mode='completion', verbose=0):
    """Extract the generated text from the response.
        currently only support single response (n=1)
    """
    if mode in ('completion', 'edit'):
        response = [item.text.strip() for item in raw_response.choices][0] # ordered by score
    elif mode == 'chat':
        response = [msg.message.content.strip() for msg in raw_response.choices][0]
    else:
        raise ValueError(f"mode must be one of ('completion', 'chat', 'edit')")
    
    extra = {}
    
    if verbose > 1:
        extra.update({
            "model": raw_response.model,
            "completion_tokens": raw_response.usage.completion_tokens,
            "prompt_tokens": raw_response.usage.prompt_tokens,
        })
    if verbose > 0:
        extra.update({
            "total_tokens": raw_response.usage.total_tokens,
        })
    
    return response, extra
    
def _format_chat_message(user_msg,
                    system_msg,
                    history_msg,
):
    assert isinstance(user_msg, str), f"user_msg must be a string: {user_msg}"
    assert system_msg is None or isinstance(system_msg, str), f"system_msg must be a string or None: {system_msg}"
    assert history_msg is None or isinstance(history_msg, list), "history_msg must be a list or None"
    
    messages = []
    # configure system_msg
    if system_msg is None or system_msg == '':
        system_msg = "You are a helpful assistant with very brief answer." # by default
    system_msg = system_msg.strip()
    messages.append(
        {"role": "system", "content": system_msg}
    )
    # configure history_msg
    if history_msg is not None and history_msg != []:
        if isinstance(history_msg[0], dict):
            if history_msg[0]["role"] != "user":
                logging.warning("history_msg must start with user's message. The first message will be ignored.")
                while history_msg[0]["role"] != "user":
                    history_msg.pop(0)
            if history_msg[-1]["role"] != "assistant":
                logging.warning("history_msg must end with assistant's message. The last message will be ignored.")
                while history_msg[-1]["role"] != "assistant":
                    history_msg.pop(-1)
            messages.extend(history_msg)
        elif isinstance(history_msg[0], str):   # in a few-shot setting
            if len(history_msg) % 2 != 0:
                logging.warning("history_msg must be a list of even length. The last message will be ignored.")
                history_msg.pop(-1)
            for i, _msg in enumerate(history_msg):
                _msg = _msg.strip()
                if i % 2 == 0:  # user
                    messages.append(
                        {"role": "user", "name":"example_user", "content": _msg}
                    )
                else:   # gpt's response
                    messages.append(
                        {"role": "assistant", "name":"example_assistant", "content": _msg}
                    )
        else:
            raise TypeError(f"history_msg must be a list of dict or str: {history_msg}")
    user_msg = user_msg.strip()
    
    messages.append(
            {"role": "user", "content": user_msg}
    )
    return messages
    
@timer
def text_completion(prompt,
                    model="text-davinci-003",
                    *, 
                    temperature=0.7, 
                    max_tokens=256, 
                    top_p=1, 
                    best_of=1,
                    n=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    verbose=0,
    ):
    """
    Per official API: https://beta.openai.com/docs/api-reference/completions/create
    Args:
        prompt (str): input to the model
        length (int, optional): the maximum number of tokens to generate. Defaults to 100.
        temperature (float, optional): control randomness. Defaults to 0.5.
        top_p (float, optional): control diversity. Defaults to 1.
        n (int, optional): the number of choices to return. Defaults to 1.
        best_of (int, optional): Generates best_of completions server-side and returns only the "best". Defaults to 1.
        frequency_penalty (float, optional): penalize new tokens based on their existing frequency in the text so far. Defaults to 0.
        presence_penalty (float, optional): penalize new tokens based on whether they appear in the text so far. Defaults to 0.
    Returns:
        _type_: _description_
    """
    
    prompt = prompt.strip()
    
    if best_of > 1:
        logging.warning("set 'best_of' to >1 is encouraged! Force to be 1 (may consume too much quota)")
        best_of = 1
    if n > 1:
        logging.warning("set 'n' to >1 is encouraged! Force to be 1 (may consume too much quota)")
        n = 1
    
    response_dict = openai.Completion.create(
                    model=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    best_of=best_of,
                    n=n,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
    )
    response, extra = parse_response(response_dict, 'completion', verbose=verbose)
    return response, extra

@timer
def chat(user_msg,
        model="gpt-3.5-turbo",
        *,
        temperature=0.7, 
        max_tokens=256, 
        top_p=1, 
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        system_msg=None,
        history_msg=[],
        verbose=0
):
    """_summary_

    Args:
        user_msg (_type_): _description_
        model (str, optional): _description_. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): _description_. Defaults to 0.7.
        max_tokens (int, optional): _description_. Defaults to 256.
        top_p (int, optional): _description_. Defaults to 1.
        n (int, optional): _description_. Defaults to 1.
        frequency_penalty (int, optional): _description_. Defaults to 0.
        presence_penalty (int, optional): _description_. Defaults to 0.
        system_msg (_type_, optional): _description_. Defaults to None.
        history_msg (list, optional): all previous message without system message. Defaults to [].
        verbose (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """    
    messages = _format_chat_message(user_msg=user_msg, system_msg=system_msg, history_msg=history_msg)
    
    if n > 1:
        logging.warning("set 'n' to >1 is encouraged! Force to be 1 (may consume too much quota)")
        n = 1

    response_dict = openai.ChatCompletion.create(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        n=n,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    response, extra = parse_response(response_dict, 'chat', verbose=verbose)
    updated_history_msg = messages[1:] + [{"role": "assistant", "content": response}]
    
    return response, updated_history_msg, extra

@timer
def text_edit(input,
        instruction,
        model="text-davinci-edit-001",
        *,
        temperature=0.7, 
        top_p=1, 
        n=1,
        verbose=0
):
    if n > 1:
        logging.warning("set 'n' to >1 is encouraged! Force to be 1 (may consume too much quota)")
        n = 1

    response_dict = openai.Edit.create(
        input=input,
        instruction=instruction,
        model=model,
        temperature=temperature,
        top_p=top_p,
        n=n,
    )

    response, extra = parse_response(response_dict, 'edit', verbose=verbose)
    return response, extra