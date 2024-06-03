from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes
from integration import serializers
import aiohttp
import asyncio
import base64


@authentication_classes([BasicAuthentication])
class BasicLoginView(APIView):
    serializer_class = serializers.EmployeeSerializer
    url = "http://176.192.70.122:90/fitnes_t_nfc_mobile/hs/nfc_mobile/v1"
    data = {
        "Request_id": "e1477272-88d1-4acc-8e03-7008cdedc81e",
        "ClubId": "59115d1e-9052-11eb-810c-6eae8b56243b",
        "Method": "GetSpecialistList",
        "Parameters": {
            "ServiceId": ""
        }
    }
    auth_str = "FitnessKit:vY0xodyg"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/json'
    }
    permission_classes = [AllowAny,]

    async def get(self, request):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, json=self.data, headers=self.headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    data = []
                    for i in response_data:
                        a = {
                            'id': i['id'],
                            "name": i['first_name'],
                            "last_name": i['last_name'],
                            "phone": i['phone'],
                            "image_url": i['image_url'],
                        }
                        data.append(a)
                    serializer = self.get_serializers(data=a, many=True)
                    serializer.is_valid()
                    return JsonResponse(serializer.data, safe=False)
                else:
                    error_message = await response.text()
                    return {'error': error_message}
