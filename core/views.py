from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .redis_client import get_redis
import time,json,requests


# Create your views here.
@api_view(['GET'])
def health_check(request):
    return Response({"status:'ok"})

@api_view(['GET'])
def api_limiter_ip(request):
    ip=request.META.get('REMOTE_ADDR')
    redis_client = get_redis()
    current_time=int(time.time())
    key=f"api_limit_{ip}_{current_time}"
    count=redis_client.get(key)
    print(count,key,"count---keyvalue")
    if count is not None and int(count)>10:
        return Response({"message":"Too many requests"},status=429)
    else:
        redis_client.incr(key)
        redis_client.expire(key,10)
        requests.get('http://127.0.0.1:8000/health/')
        return Response({"message":"ok"})

@api_view(['POST'])
def api_limiter_route(request):
    redis_client = get_redis()
    t_now=time.ctime()
    split=t_now.split(' ')
    current_time=split[3]
    current_date=split[2] + split[1] + split[4]
    current_time_hour_minute=current_time.split(':')[0]+':' +current_time.split(':')[1]
    queue_name = f"api_limiter_{current_time_hour_minute}_{current_date}"
    payload=payload_maker_for_queue(request)
    redis_client.lpush(queue_name, json.dumps(payload))
    return Response({"message":"Queued"})

def payload_maker_for_queue(request):
    payload={
        'url':'http://127.0.0.1:8000/health/',
        'method':'GET',
        'body':request.data,
        'headers':{
            "Authorization":request.headers.get("Authorization")
        }
    }
    return payload

