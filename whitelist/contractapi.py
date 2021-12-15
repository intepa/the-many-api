import json
import os
from web3 import Web3
from pathlib import Path
from configobj import ConfigObj
from web3.middleware import geth_poa_middleware

BASE_DIR = Path(__file__).resolve().parent.parent

if os.environ.get("PROJECT_ENV") == "PRODUCTION":
    appID = os.environ.get("INFURA_APP_ID")
    owner = os.environ.get("OWNER_ADDRESS")
    private_key = os.environ.get("OWNER_PRIVATE_KEY")
    contract_address = os.environ.get("REGULATOR_SERVICE_CONTRACT_ADDRESS")

else:
    config = ConfigObj(f'{BASE_DIR}/settings.conf')
    appID = config['INFURA_APP_ID']
    owner = config['OWNER_ADDRESS']
    private_key = config['OWNER_PRIVATE_KEY']
    contract_address = config['REGULATOR_SERVICE_CONTRACT_ADDRESS']


w3 = Web3(Web3.HTTPProvider(
    f"https://polygon-mumbai.infura.io/v3/{appID}"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

RegulatorServiceContract = f'{BASE_DIR}/contracts/RegulatorService.json'

with open(RegulatorServiceContract, 'r') as f:
    truffleFile = json.load(f)

ABI = truffleFile['abi']

regServiceContract = w3.eth.contract(
    address=contract_address, abi=ABI)


def setPermissions(address, send=True, receive=True):
    trans = regServiceContract.functions.setPermissions(address, send, receive).buildTransaction(
        {'gas': 70000, 'gasPrice': w3.toWei('1.5', 'gwei'), 'nonce': w3.eth.getTransactionCount(owner), 'from': owner})
    signed_txn = w3.eth.account.signTransaction(trans, private_key=private_key)
    return w3.eth.sendRawTransaction(signed_txn.rawTransaction)
