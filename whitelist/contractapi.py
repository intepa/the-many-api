import json
from web3 import Web3
from pathlib import Path
from configobj import ConfigObj
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

BASE_DIR = Path(__file__).resolve().parent.parent
RegulatorServiceContract = f'{BASE_DIR}/contracts/RegulatorService.json'
config = ConfigObj(f'{BASE_DIR}/settings.conf')

with open(RegulatorServiceContract, 'r') as f:
    truffleFile = json.load(f)

ABI = truffleFile['abi']

regServiceContract = w3.eth.contract(
    address=config['REGULATOR_SERVICE_CONTRACT_ADDRESS'], abi=ABI)


def setPermissions(address, send=True, receive=True):
    return regServiceContract.functions.setPermissions(
        address, send, receive).transact({'from': w3.eth.accounts[0]})
