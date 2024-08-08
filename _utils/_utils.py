import re
import subprocess

def removeColor(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text) 

def runProcess(name, command):
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True
            #check = True
        )
        print(f"[+] {name} output:")
        print(result.stdout)
        if result.stderr:
            print(f"[-] {name} err:")
            print(result.stderr)
            result = result.stdout + '\n[-] err:\n' + result.stderr
        else:
            result = result.stdout
            
    except FileNotFoundError:
        msg = f'[-] {name} not found in your system. Skip.'
        print(msg)
        result = msg
    except Exception as e:
        msg = f"[-] An error occurred with {name}:\n {str(e)}"
        result = msg
        print(result)
    return result
