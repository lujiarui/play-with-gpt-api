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
    
    parser.add_argument("--instruction", type=str, default="Fix the spelling or grammar mistakes", help="The instruction to edit the input text")
    parser.add_argument("--model", type=str, default="text-davinci-edit-001", help="The model to use for edit (default: text-davinci-edit-001)")
    
    parser.add_argument("--temperature", type=float, default=1.0, help="The temperature of the model (higher means more creative)")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output from response")
    return parser


if __name__ == "__main__":
    # Parse the command line arguments
    args = get_argparser().parse_args()
    
    args.model = args.model.lower().strip()
    assert args.model in model_config.EDITS, f"Edit model must be one of {model_config.EDITS}"
    logging.info(f"Calling streaming edits with instruction: {args.instruction} (Ctrl+C to exit)")
    
    args = args.__dict__    # as kwargs
    while True:
        user_msg = input(">>> [User] ")
        response, extra = util.text_edit(input=user_msg, **args)
        
        print(f"\n>>> [bot] {response}")
        if extra != {}:
            print(f">>> [sys] {extra}")   
            
    
    


