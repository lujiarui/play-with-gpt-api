import os
import argparse
import readline
import logging

import openai

import util
import config as model_config

logging.basicConfig(level=logging.INFO)
# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# receives a list of arguments and returns a dictionary of arguments
def get_argparser():
    # Set up the command line arguments
    parser = argparse.ArgumentParser(description="Generate text using the OpenAI GPT API")
    parser.add_argument("--system_msg", type=str, default="You are a helpful assistant with very brief answer", help="The base prompt to start the generated text")
    
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="The model to use for chat (default: gpt-3.5-turbo)")
    
    parser.add_argument("--feed_previous", action="store_true", help="Feed the previous response back into the model (can consume a lot of quota)")
    
    parser.add_argument("--max_tokens", type=int, default=128, help="The length of the generated text in tokens")
    parser.add_argument("--temperature", type=float, default=1.0, help="The temperature of the model (higher means more creative)")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output from response")
    return parser


if __name__ == "__main__":
    # Parse the command line arguments
    args = get_argparser().parse_args()
    args.model = args.model.lower().strip()
    assert args.model in model_config.CHAT_COMPLETIONS, f"Chat model must be one of {model_config.CHAT_COMPLETIONS}"
    
    args = args.__dict__    # as kwargs

    feed_previous = args.pop("feed_previous")
    logging.info(f"Entering chat mode... (Ctrl+C to exit)")
    
    while True:
        if not feed_previous: 
            history_msg = []
        else:
            print('{util.bcolors.ITALICS}history: {util.bcolors.ENDC}', history_msg)
            
        user_msg = input(f"{util.bcolors.BOLD}>>> The user puts:\n{util.bcolors.ENDC}")
        response, history_msg, extra = util.chat(user_msg, history_msg=history_msg, **args)
        
        print(f"{util.bcolors.BOLD}>>> The bot answers:{util.bcolors.ENDC}")
        print(f"{util.bcolors.HEADER}{response}{util.bcolors.ENDC}")
        if extra != {}:
            print(f"{util.bcolors.RED}>>> info: {extra}{util.bcolors.ENDC}")   

        
    


