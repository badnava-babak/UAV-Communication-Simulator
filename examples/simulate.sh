#!/bin/bash
sim_vehicle.py --custom-location=38.95209759531131,-95.26429358856721,0,0 --vehicle ArduCopter --mavproxy-args --out=tcpin:127.0.0.1:6760 --map -M --console --instance=1
sim_vehicle.py --custom-location=38.95209759531131,-95.26429358856721,0,0 --vehicle ArduCopter --mavproxy-args --out=tcpin:127.0.0.1:6770 --map -M --console --instance=2

sim_vehicle.py --custom-location=38.95209759531131,-95.26429358856721,0,0 --vehicle ArduCopter --mavproxy-args --out=tcpin:127.0.0.1:6760 --instance=1 --sysid=1
sim_vehicle.py --custom-location=38.95209759531131,-95.26429358856721,0,0 --vehicle ArduCopter --mavproxy-args --out=tcpin:127.0.0.1:6770 --instance=2 --sysid=2
sim_vehicle.py --custom-location=38.95209759531131,-95.26429358856721,0,0 --vehicle ArduCopter --mavproxy-args --out=tcpin:127.0.0.1:6780 --instance=3 --sysid=3
