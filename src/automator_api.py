import os
import argparse
import openai
import logging

import config as config
import util

logging.basicConfig(level=logging.CRITICAL)
# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
    
    
# receives a list of arguments and returns a dictionary of arguments
def get_argparser():
    # Set up the command line arguments
    parser = argparse.ArgumentParser(description="Generate text using the OpenAI GPT API")
    parser.add_argument("prompt",  type=str, help="The base prompt to start the generated text")
    
    parser.add_argument("--usage", type=str, default="explain", help="The usage of the chatbot (default: explain)")
    parser.add_argument("--tone", type=str, default="neutral", help="The tone of the chatbot (default: neutral)")
    
    parser.add_argument("--model", type=str, default="gpt-4-0314", help="The model to use for chat (default: gpt-4-0314)")
    parser.add_argument("--max_tokens", type=int, default=128, help="The length of the generated text in tokens")
    parser.add_argument("--temperature", type=float, default=1.0, help="The temperature of the model (higher means more creative)")
    parser.add_argument("--verbose", type=int, default=0, help="Verbose level of output info (e.g., token usage) from response (default: 0)")
    
    return parser


if __name__ == "__main__":
    # Parse the command line arguments
    args = get_argparser().parse_args()
    
    args.model = args.model.lower().strip()
    assert args.model in config.CHAT_COMPLETIONS, f"Completions model must be one of {config.COMPLETIONS}"
    
    args = args.__dict__    # as kwargs
    
    usage = args.pop("usage")
    
    user_msg = config.PREFIX_LIBRARY[usage] + args.pop("prompt")
    system_msg = config.SYSTEM_MESSAGE_LIBRARY[args.pop("tone")]
    
    response, _, _, _ = util.chat(user_msg=user_msg, 
                                system_msg=system_msg, 
                                **args)
    
    if usage in ('explain', 'joke'):  # output response directly
        print(response.strip())
    elif usage == 'polish': # output original prompt with refined response 
        print(">>> Original text >>>")
        print(user_msg.strip())
        print(f">>> Refined version from {args['model']} >>>")
        print(response.strip())
    elif usage == 'grammar_check':
        print(">>> Original text >>>")
        print(user_msg.strip())
        print(f">>> Potential grammar/spelling error(s) >>>")
        print(response.strip())
    elif usage == 'translate':
        print(">>> Original text >>>")
        print(user_msg.strip())
        print(f">>> Translated (En) >>>")
        print(response.strip())
    elif usage == 'writing':
        print(">>> Prompt text >>>")
        print(user_msg.strip())
        print(f">>> Composed paragraph >>>")
        print(response.strip())
    else:
        raise NotImplementedError

