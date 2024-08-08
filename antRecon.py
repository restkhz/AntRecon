import argparse
import ipaddress
import socket
import multiprocessing
from _utils import nmapHandler
from _utils import toolsLoader 
from _utils import report
from time import sleep
import os

RPT_DIR = os.getcwd()

script_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_path)


SERVICES_DICT = multiprocessing.Manager().dict()

def isValidTarget(target):
    try:
        ipaddress.ip_address(target)
        return target
    except ValueError:
        pass
    
    try:
        socket.gethostbyname(target)
        return target
    except:
        print("Invalid target.")
        exit(1)
        

def main():
    global SERVICES_DICT
    parser = argparse.ArgumentParser(description="""
    Automated reconnaissance tools for OSCP and HTB(root required)
    Automated single target reconnaissance and Markdown report generation.
    Only [ONE] target at a time.
    
    Hope it could save your OSCP and HTB some time.
    """,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('target', type=isValidTarget, help="Target should be a IP or a domain.")
    args = parser.parse_args()
    target = args.target
    print('''
        
 █████╗ ███╗   ██╗████████╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
███████║██╔██╗ ██║   ██║   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██║██║╚██╗██║   ██║   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║██║ ╚████║   ██║   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
''')
    print("----------------------------------------------")
    print(f"AntRecon Scanning: {target}")
    print("----------------------------------------------")
    
    
    results = recon(target)
    report.firstRecon(target, SERVICES_DICT, results, RPT_DIR)
    
    sleep(3)
    nmapRecon(target)
    report.nmapRecon(target, RPT_DIR)
    
def recon(target):
    global SERVICES_DICT
    print('[*] First Recon: Scanning All TCP ports and 53,161,1194 on UDP. It will probably take about 1-7 minutes, then the tools will be kicked in and a report will be generated , so be patient.')
    #targetDict = nmapHandler.run(target, f'-T4 -sS -sU -p U:53,161,1194,T:1-65535 -sV -O --script "(default or auth or vuln) and not http-enum" --script-args mincvss=5.0 -oN ./tempOutput/nmap_{target}', SERVICES_DICT)
    targetDict = nmapHandler.run(target, f'-T4 -sS -sU -p U:53,161,1194,T:1-65535 -sV --allports -O --script ssl-cert -oN ./tempOutput/nmap_{target}', SERVICES_DICT)
    
    #print(targetDict)
    
    SERVICES_DICT = targetDict.copy()
    results = toolsLoader.deepRecon(target, SERVICES_DICT)
    tempDict = SERVICES_DICT.copy()
    for resultOfTool in results:
        for result in resultOfTool:
            for key in result:
                tempDict[key]['details'].append(result[key])
    SERVICES_DICT.update(tempDict)
    print(f'[*] First Recon done.')
    return results

def nmapRecon(target):
    print('[*] Full Nmap recon: Scanning with many scripts. It may take about 3-15 minutes and generate you a FULL nmap report, so be patient.')
    nmapHandler.run(target, f'-T4 -sS -sU -p U:53,161,1194,T:1-65535 -sV -O --script "(default or auth or vuln or discovery) and not (http-enum or TLS-*)" --script-args mincvss=5.0 --script-timeout 240s -oN ./tempOutput/nmap_{target}',SERVICES_DICT)
    print(f'[*] Full Nmap recon done. ')
    
if __name__ == "__main__":
    main()
    print('[*] Everything done, good luck! AntRecon exit.')
