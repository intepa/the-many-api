from web3 import Web3
from . import contractapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.

@api_view(['POST'])
def whitelistAddress(request, address):
    try:
        if Web3.isAddress(address):
            contractapi.setPermissions(address)
            api_response = "Pending"
        else:
            api_response = "The provided address is not valid!"
        return Response({"response": api_response})
    except Exception as e:
        return Response({"response": e})


@api_view(['GET'])
def getContract(request):
    RegulatorServiceContract = f'{BASE_DIR}/contracts/RegulatorService.json'

    with open(RegulatorServiceContract, 'r') as f:
        truffleFile = json.load(f)

    return Response(truffleFile)
