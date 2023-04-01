import os
import argparse
import openai
import logging

import config as model_config
import util

logging.basicConfig(level=logging.INFO)
# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
    
# receives a list of arguments and returns a dictionary of arguments
def get_argparser():
    # Set up the command line arguments
    parser = argparse.ArgumentParser(description="Generate text using the OpenAI GPT API")
    parser.add_argument("prompt",  type=str, help="The base prompt to start the generated text")
    parser.add_argument("--model", type=str, default="text-davinci-003", help="The model to use for completion (default: text-davinci-003)")
    
    parser.add_argument("--max_tokens", type=int, default=128, help="The length of the generated text in tokens")
    parser.add_argument("--temperature", type=float, default=1.0, help="The temperature of the model (higher means more creative)")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output from response")
    return parser


if __name__ == "__main__":
    # Parse the command line arguments
    args = get_argparser().parse_args()
    
    args.model = args.model.lower().strip()
    assert args.model in model_config.COMPLETIONS, f"Completions model must be one of {model_config.COMPLETIONS}"
    
    logging.info(f"Calling completion script with prompt: {args.prompt}")
    logging.info("Generating text...")
    
    args = args.__dict__    # as kwargs
    response, extra = util.text_completion(**args)
    
    print(f"\n>>> [bot] {response}")
    if extra != {}:
        print(f">>> [sys] {extra}")   
    


