import nmap
import os
import multiprocessing

def callback(target, result, SERVICES_DICT):
    #print(result)
    try:
        elap = result['nmap']['scanstats']['elapsed']
        targetInfo = result['scan'][target]
    except:
        print('\n[-] Host may not reachable,Use ping to check the connection.')
        exit('\nTarget seems down!')
        
    print(f"Done! in {elap}s")
    targetOS = targetInfo.get('osmatch')[0]['name'] if targetInfo.get('osmatch') else 'Unknow'
    print(f"[  Target: {target}       OS:{targetOS} ]")
    
    template = "{:<5} {:<10} {:<12} {:<40} {:<35}"
    print(template.format("proto","Port", "Service", "Description", "Version"))
    print("-----"*16)
    
    servicesTcp = targetInfo.get('tcp')
    if servicesTcp:
        for port,service in servicesTcp.items():
            if service.get('script') and service.get('script').get('ssl-cert'):    #patch here. cuz the Author of python-nmap forget "tunnel"
                service['name'] = 'ssl/' + service['name']
            print(template.format("tcp", port, service['name'], service['product'], service['version']))
            insertService('tcp', port, service, SERVICES_DICT)
            
    servicesUdp = targetInfo.get('udp')
    if servicesUdp:
        for port,service in servicesUdp.items():
            if service['state'] == 'open':
                print(template.format("udp", port, service['name'], service['product'], service['version'])) 
                insertService('udp', port, service, SERVICES_DICT)
    print('')

def insertService(protocol, port, service, SERVICES_DICT):
    SERVICES_DICT[(protocol,port)] = {
        'protocol':protocol,
        'port': port,
        'name':service['name'],
        'product': service['product'],
        'version': service['version'],
        'details':[],
        'reconState':'N'    #N: None, D: Done, R: Running
    }
    
def run(target, arguments, SERVICES_DICT):
    nm = nmap.PortScannerAsync()
    print("[*] Nmap Scanning...",end='',flush=True)
    nm.scan(target, arguments=arguments,sudo=True, callback=lambda x,y:callback(x,y,SERVICES_DICT))

    while nm.still_scanning():
        print('.',end='',flush=True)
        nm.wait(2)
        
    return SERVICES_DICT
