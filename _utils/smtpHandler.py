import subprocess
from _utils._utils import runProcess

wordlist = './_utils/usernames.txt'

def run(target, SERVICE):
    print(f"[*] SMTP: Enum users on {SERVICE['port']} using {wordlist}")

    command = [
        "smtp-user-enum",
        "-M", "VRFY",
        "-U", wordlist,
        "-t", target
        ]

    try:
        result = subprocess.run(command,text=True,
            capture_output=True, check=True)
    except FileNotFoundError:
        try:
            command[0] = "smtp-user-enum.pl"
            result = subprocess.run(command,text=True,
            capture_output=True, check=True)
        except FileNotFoundError:
            result = "[-] smtp-user-enum and smtp-user-enum.pl: command not found."
            return [{(SERVICE['protocol'], SERVICE['port']): {'name':'smtp-user-enum', 'output':resultStr}}]


    print(f"[+] smtp-user-enum output:")
    print(result.stdout)    
    if result.stderr:
        print(f"[-] smtp-user-enum err:")
        print(result.stderr)
        result = result.stdout + '\n[-] err:\n' + result.stderr
    else:
        result = result.stdout
    resultStr = result
    return [{(SERVICE['protocol'], SERVICE['port']): {'name':'smtp-user-enum', 'output':resultStr}}]
 
