import os
import json
from dotenv import load_dotenv
from prompts import system_prompt 
import argparse 

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

from openai import OpenAI
from calls import available_functions 

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('user_prompt')           # positional argument


args=parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
prompt_messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt },
]

response = client.chat.completions.create(
          model="openrouter/free",
          messages=prompt_messages,
          tools=available_functions)

response_message = response.choices[0].message
for tool_call in response_message.tool_calls:
    function_args = json.loads(tool_call.function.arguments or "{}")
    print(f"Calling function: {tool_call.function.name}({function_args})")
print(response_message.content)


