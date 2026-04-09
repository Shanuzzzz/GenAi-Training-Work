import requests

url = "http://127.0.0.1:8000/upload"
file_path = "sample.csv"

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response JSON:")
print(response.json())