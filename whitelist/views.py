import time
from web3 import Web3
from . import contractapi
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['POST'])
def whitelistAddress(request, address):
    time.sleep(4)
    try:
        if Web3.isAddress(address):
            contractapi.setPermissions(address)
            api_response = "Pending"
        else:
            api_response = "The provided address is not valid!"
        return Response({"response": api_response})
    except Exception as e:
        return Response({"response": e})
