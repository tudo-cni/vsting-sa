#!/usr/bin/python3
from yaml import load, dump, CLoader as Loader, CDumper as Dumper
from typing import List
from os import listdir, path
from sys import argv
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def getAvailableNetworkInterfaces() -> List[str]:
    ifaces = listdir(path.join('/', 'sys', 'class', 'net'))
    return ifaces

def configureApi(interfaces: List[str]):
    '''
        Generates a suitable config for the vSTING API
            interface: list of interfaces. The interface leading to the robot must be specified first.
        Example:
            interfaces:     ['enps30', 'enp4s0']
    '''
    with open(path.join('..', 'configs', 'api-config-base.yml'), 'r') as file:
        config = load(file, Loader=Loader)

    config['interfaces']['robot'] = interfaces[0]
    config['interfaces']['operator'] = interfaces[1]
    config['combox']['cli']['working_directory'] = path.join(Path.home(), *'vsting/combox_monitor/dist/cli'.split('/'))
    # Write generated config to file
    with open(path.join(Path.home(), 'vsting', 'api','api-config.yml'), 'w') as file:
        file.write(dump(config, Dumper=Dumper, sort_keys=False))
        logger.info("updated api config.")

def configureCombox(interfaces: List[str]):
    '''
        Generates a suitable config for the combox monitor daemon
            interface: list of interfaces. The interface leading to the robot must be specified first.
        Example:
            interfaces:     ['enps30', 'enp4s0']
    '''
    # Read base yml config
    with open(path.join('..', 'configs', 'combox-config-base.yml'), 'r') as file:
        config = load(file, Loader=Loader)
    # Generate interface_tags configuration
    iface_tags = {'vsting-br': {'technology': 'Bridge'}}
    iface_tags = {
        **iface_tags,  
        **{
            iface: {'technology': 'Robot' if idx == 0 else 'Operator'}
            for idx, iface in enumerate(interfaces)
        }
    }
    # Generate traffic interfaces configuration
    traffic_ifaces = interfaces   
    # Set generated args in config
    config["interface_tags"] = iface_tags
    config["traffic"]["interfaces"] = traffic_ifaces
    # Write generated config to file
    with open(path.join(Path.home(), 'vsting', 'combox_monitor','combox-config-vsting.yml'), 'w') as file:
        file.write(dump(config, Dumper=Dumper, sort_keys=False))
        logger.info("updated config with interface monitoring configuration.")

def updateConfigs(interfaces: List[str]):

    logger.info('updating configuration files ...')
    if len(interfaces) != 2:
        logger.fatal(f'two network interfaces must be provided for configuration')
        exit(1)
    
    available_ifaces = getAvailableNetworkInterfaces()

    # check if all passed in interfaces exist.
    iface_check = [ iface in available_ifaces for iface in interfaces]
    if not all(iface_check):
        unavailable_ifaces = [interfaces[idx] for idx, check in enumerate(iface_check) if check is False]
        logger.fatal(f'{" and ".join(unavailable_ifaces)} {"are" if len(unavailable_ifaces) > 1 else "is"} not available')
        exit(1)
    
    # generate api config
    configureApi(interfaces)
    
    # generate combox config
    configureCombox(interfaces)

    logger.info('update of configuration files completed.')
    

if __name__ == '__main__':
    updateConfigs(argv[1:])