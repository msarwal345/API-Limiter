from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .redis_client import get_redis
import time,copy,json


# Create your views here.
@api_view(['GET'])
def health_check(request):
    return Response({"status:'ok"})

@api_view(['POST'])
def api_limiter_route(request):
    redis_client = get_redis()
    t_now=time.ctime()
    split=t_now.split(' ')
    current_time=split[3]
    current_date=split[2] + split[1] + split[4]
    current_time_hour_minute=current_time.split(':')[0]+':' +current_time.split(':')[1]
    queue_name = f"api_limiter_{current_time_hour_minute}_{current_date}"
    payload=request_maker_for_queue(request)
    print(payload,queue_name,redis_client,'hello')
    redis_client.lpush(queue_name, json.dumps(payload))
    return Response({"message":"Queued"})

def request_maker_for_queue(request):
    payload={
        'url':'http://127.0.0.1:8000/api_limiter/',
        'method':'POST',
        'body':request.data,
        'headers':{
            "Authorization":request.headers.get("Authorization")
        }
    }
    return payload

