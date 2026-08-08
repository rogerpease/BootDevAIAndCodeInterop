import os
import json
from dotenv import load_dotenv
from prompts import system_prompt 
from call_function import call_function 
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
parser.add_argument('--verbose',action="store_true",default=False)           


args=parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
prompt_messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt },
]

iteration = 0 
for iteration in range(20): 
   response = client.chat.completions.create(
             model="openrouter/free",
             messages=prompt_messages,
             tools=available_functions)

   response_message = response.choices[0].message
   if response_message.tool_calls is None:
      print(response_message.content)
      exit(0) 

   for tool_call in response_message.tool_calls:
      function_args = json.loads(tool_call.function.arguments or "{}")
      print(f"Calling function: {tool_call.function.name}({function_args})")
      result_message = call_function(tool_call,verbose=args.verbose)
      print(f"-> {result_message['content']}")

   prompt_messages.append(response_message)
   prompt_messages.append(result_message)

#   print(response_message.content)

print("ERROR") 
exit(1) 
