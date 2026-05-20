import time
import requests

while True:
    try:
        requests.post("http://localhost:7860/predict", json={"text": "Live architecture test."})
    except:
        pass
    time.sleep(0.1)
