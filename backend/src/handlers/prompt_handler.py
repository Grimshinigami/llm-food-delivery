
# Typing hints
from typing import Optional

# Configuration and helpers
from fastapi.encoders import jsonable_encoder
from src.config import CONFIG
from src.prompts.functions import ALL_ALLOWED_FUNCTIONS

# Importing schemas and hints
from src.schemas import ChatRequest

# Utils
import json

from src.prompts.functions.all_functions import all_functions


CFG_PROMPTS = CONFIG["prompts"]
CFG_CHAT = CFG_PROMPTS["chat"]
CFG_FUNCTIONS = CFG_PROMPTS["functions"]


# Utils
from pathlib import Path


## Creating handler
class PromptHandler():
    def __init__(
        self,
    ):
        pass

    def get_messages(self, prompt_request):
        """Gets the chatlog from the user and prepares the prompt for the system"""

        # Gets the system prompt and injects context
        system_prompt = Path(CFG_CHAT["filepath"]).read_text()

        # Retrieves the chat log
        chatlog = jsonable_encoder(prompt_request.query.history)

        # print("chatlog is:",chatlog)

        # Formatting - removes "name" parameter from non-functional inputs
        chatlog = [
            {"role": message["role"], "content": message["content"]}
            if message["role"] != "function"
            else {
                "role": message["role"],
                "content": message["content"],
                "name": message["name"],
            }
            for message in chatlog
        ]

        # Merges all together
        messages = [{"role": "system", "content": system_prompt}] + chatlog

        return messages

    def prepare_response(self, response):
        """Formats the response from the system"""
        response = jsonable_encoder(response)
        # print("response in prepare_response is: ",response)
        # print("tool_calls is:",response["choices"][0]["message"].get('tool_calls',None))
        return {
            "response": response["choices"][0]["message"]["content"],
            # "function_call": response["choices"][0]["message"].get("function_call", None),
            "tool_calls": response["choices"][0]["message"].get('tool_calls',None),
            # "tools_call":response['tools_calls'][0]['function']
        }

    
    def get_functions(self,):
        """Returns the functions signatures"""
        # return ALL_ALLOWED_FUNCTIONS
        return all_functions
