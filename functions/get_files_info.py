import os 


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
      
   try: 
       working_dir_abs = os.path.abspath(working_directory)
       target_dir      = os.path.normpath(os.path.join(working_dir_abs,directory))

       valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

       result = "Result for "  
       result += "current" if directory == '.' else "'"+directory+"'"
       result += " directory:\n"

       if not valid_target_dir:
          return result + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
       if not os.path.isdir(target_dir): 
          return result + f'    Error: "{target_dir}" is not a directory'
       
       for file in os.listdir(target_dir):
          fullpath = os.path.join(target_dir,file)
          result += "   - "+file+":"  
          result += " file_size="+str(os.path.getsize(fullpath))+ " bytes,"
          result += " is_dir="
          result +=  "True" if os.path.isdir(fullpath) else "False"
          result += "\n"
    
       return result
   except Exception as e:
       return f'    Error: Excepted out because {e}'


