import subprocess
from _utils._utils import runProcess

def searchExp(product, version):
    return runProcess('searchsploit', ['searchsploit', f'{product} {version}'])

def run(target, SERVICES_DICT):
    print('[*] Querying Searchsploit...')
    results = []
    serviceDict = SERVICES_DICT.copy()
    for key in serviceDict:
        if serviceDict[key]['product']:
            product = serviceDict[key]['product'] 
        else:
            continue
        
        
        version = serviceDict[key]['version'].split()[0] if serviceDict[key]['version'] else ''
          
        print(f"Searching exploits for {product} version {version}...\n")
        if product == 'Microsoft Windows RPC':
            exploits = "[Microsoft Windows RPC]: It's usually unlikely to be vulnerable. Please search manually in consideration of the OS VERSION. NOT recommended to waste time here."
        else:
            exploits = searchExp(product, version)
        #if exploits == 'Exploits: No Results\nShellcodes: No Results\n':
        #    exploits = 'No exploit was found.'
        #print(exploits)
        resultStr = f'Exploits for {product} version {version}...\n{exploits}\nThis result may not always accurate. Sometimes you need to find the keyword yourself and search again.'
        results.append({key:{'name':'SearchSploit', 'output':resultStr}})
    return results

if __name__ == '__main__':
    debugList = {('tcp', 53): {'protocol': 'tcp', 'port': 53, 'product': 'dnsmasq', 'version': '2.50', 'details': [], 'reconState': 'N'}, ('tcp', 631): {'protocol': 'tcp', 'port': 631, 'product': 'CUPS', 'version': '1.1', 'details': [], 'reconState': 'N'}}

    run(debugList)
