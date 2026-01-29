# import time
# from core.redis_client import get_redis

# redis_client=get_redis()

# def process_queue():
#     while True:
#         t_now=time.ctime()
#         split=t_now.split(' ')
#         current_time=split[3]
#         current_date=split[2] + split[1] + split[4]
#         current_time_hour_minute=current_time.split(':')[0]+':' +current_time.split(':')[1]
#         queue_name = f"api_limiter_{current_time_hour_minute}_{current_date}"

