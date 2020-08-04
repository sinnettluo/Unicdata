# VEZGajROREVOV0JQcXZiQ1lRS2dvWjR2NWYzcGJ0cEJPRDJrR2g3NkVMT3B3Rjkrd1BPMkhYdWw0Z1FRcnIvYkxWL2wzTERKYVF5bVJNckY2RlF2QkNveW1ZMWFzSDFYWmJBT1IrYldBaDRJVWl3Y1R3ei92a3dtTTRTRlZqQ2RZMlhob2VXc1NSY3NXckFUNkZzdU5BdlNiT3hCZCtvQlNIWXlKaUp1VnI4QVVKTVZLOXRDRXEyMzB5cCttaEVsYjNLell1T0VrY3pWcUFPc0VuUnFJd2VHUFp2TzlseUl5VHRBR01oZWhNU0cyQjBoOU5UeXh5b2ZJeXRFVEcycC0tamdNVmVXUHo2aEVRNDR3b3JMdy9Cdz09--7550d324f9f63e25e49e95269d0b9df2d59ba4ec
import re

from redis import Redis

redis_cli = Redis(host="127.0.0.1", port=6379, db=2)
# redis_cli.sadd("niuniu_cookie","VEZGajROREVOV0JQcXZiQ1lRS2dvWjR2NWYzcGJ0cEJPRDJrR2g3NkVMT3B3Rjkrd1BPMkhYdWw0Z1FRcnIvYkxWL2wzTERKYVF5bVJNckY2RlF2QkNveW1ZMWFzSDFYWmJBT1IrYldBaDRJVWl3Y1R3ei92a3dtTTRTRlZqQ2RZMlhob2VXc1NSY3NXckFUNkZzdU5BdlNiT3hCZCtvQlNIWXlKaUp1VnI4QVVKTVZLOXRDRXEyMzB5cCttaEVsYjNLell1T0VrY3pWcUFPc0VuUnFJd2VHUFp2TzlseUl5VHRBR01oZWhNU0cyQjBoOU5UeXh5b2ZJeXRFVEcycC0tamdNVmVXUHo2aEVRNDR3b3JMdy9Cdz09--7550d324f9f63e25e49e95269d0b9df2d59ba4ec")
b = []
a = redis_cli.smembers('niuniu_cookie')
for i in a:
    if "[" in str(i):
        f = re.findall("'_niu_niu_session', 'path': '/', 'secure': False, 'value': '(.*)'}, ", str(i))[0]
        b.append(f)
    else:
        b.append(i)
print(b)
print(len(b))
