import os
import subprocess
import traceback

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:

       working_dir_abs = os.path.abspath(working_directory)
       target_file      = os.path.normpath(os.path.join(working_dir_abs,file_path))

       valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

       if not valid_target_file:
          return f'    Error: Cannot execute "{file_path}" as it is outside the permitted working directory {working_dir_abs}'

       if not os.path.isfile(target_file):
          return f'    Error: "{file_path}" does not exist or is not a file'
   
       if not target_file.endswith(".py"):
          return f'    Error: "{file_path}" is not a Python file'
 
       command = ["python3", target_file]
       if args: 
         command.extend(args)

       resultstr = ""

       result = subprocess.run(command,text=True,
                      timeout=30,
                      cwd=working_dir_abs,
                      capture_output=True)

       if result.returncode != 0: 
          resultstr = "Process exited with code "+str(result.returncode)+"\n"  

       if result.stdout is None and result.stderr is None: 
          resultstr += "No output produced\n" 
       else:
          if result.stdout is not None:
            resultstr += "STDOUT: "+result.stdout +"\n"
          if result.stderr is not None:
            resultstr += "STDERR: "+result.stderr +"\n"

       return resultstr 

    except Exception as e:
       traceback.print_exc()
       return f'Error: Overall Exception {e}' 
  
