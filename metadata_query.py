import requests
import json
import sys

def get_token():
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
    response = requests.put(url, headers=headers, timeout=2)
    response.raise_for_status()
    return response.text

def get_metadata(key):
    token = get_token()
    url = f"http://169.254.169.254/latest/meta-data/{key}"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers, timeout=2)
    response.raise_for_status()
    return {key: response.text}

def allget_metadata(key=None):
    token = get_token()
    METADATA_URL = f"http://169.254.169.254/latest/meta-data/"
    headers = {"X-aws-ec2-metadata-token": token}

    if key is not None:
        url = METADATA_URL + key
    else:
        url = METADATA_URL

    try:
        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()

        if key:
            print("specific key")
            print(json.dumps({key: response.text}, indent=2))
        else:
            #print(json.dumps(response.text.splitlines(), indent=2))
            keys = response.text.splitlines()
            print(keys)
            for k in keys:
                if k is not None:
                    print(get_metadata(k))

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    #print(get_metadata("instance-id"))
    allget_metadata(sys.argv[1] if len(sys.argv) > 1 else None)
