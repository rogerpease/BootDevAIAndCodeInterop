import os 

from config import MAX_CHARS


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets contents of file_path (up to "+str(MAX_CHARS)+" characters) in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to get file content from, relative to the working directory",
                    "required": True, 
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
      
   try: 
       working_dir_abs = os.path.abspath(working_directory)
       target_file      = os.path.normpath(os.path.join(working_dir_abs,file_path))

       valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

       if not valid_target_file:
          return f'    Error: Cannot list "{target_file}" as it is outside the permitted working directory {working_dir_abs}'
    
       if not os.path.isfile(target_file): 
          return f'    Error: "{target_file}" is not a file'
       
       with open(target_file,'r') as fp:
           content = fp.read(MAX_CHARS)
           print (len(content))
           if fp.read(1):
               print ("More to read")
               content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
           return content
   except Exception as e:
       return f'    Error: Excepted out because {e}'


