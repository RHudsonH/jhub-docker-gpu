import requests, subprocess, sys

def get_gpus():
    result = subprocess.run(['/usr/bin/nvidia-smi',  '--query-gpu=uuid', '--format=csv,noheader'], capture_output=True, text=True)
    uuids = result.stdout.strip().split('\n')
    return uuids

device_list = get_gpus()



url = 'http://hwalloc:5000/api/v1/devices/batch-create'

r = requests.post(url, json={'devices': device_list})

if r.status_code == 200:
    print('Sucessfully populated database', r.json())
    sys.exit(0)
else:
    print('Operation failed:', r.text)
    sys.exit(-1)
