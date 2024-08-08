import importlib
import multiprocessing
from _utils.toolsList import toolsList
from _utils.toolsList import genericTools

def loadAndRun(tool, target, service):
    module = importlib.import_module('_utils.' + tool + 'Handler')
    result = module.run(target, service)
    return result

def deepRecon(target, SERVICES_DICT):
    tasks = []
    
    for tool in genericTools:
        tasks.append((tool, target, SERVICES_DICT))
        
    for key in SERVICES_DICT:
        if toolsList:
            for tool in toolsList:
                if tool['service'] in SERVICES_DICT[key]['name']:
                    tasks.append((tool['name'], target, SERVICES_DICT[key]))
                    
    with multiprocessing.Pool() as pool:
        results = pool.starmap(loadAndRun, tasks)
        
    return results
