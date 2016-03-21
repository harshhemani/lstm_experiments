import os
import shutil
import requests

lines = open('image_links.txt', 'r').readlines()

for i, url in enumerate(lines):
    path = 'output/'  + url.split('/')[-1][:-1]
    if os.path.exists(path):
        continue
    url = 'http://tate.org.uk'+url.strip()
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    del r
