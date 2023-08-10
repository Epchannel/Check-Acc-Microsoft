import requests
import csv

url = "https://khoatoantin.com/ajax/office365_api"
data = {
    "username": "trogiup24h",
    "password": "PHO"
}

# Đọc dữ liệu từ tệp CSV
csv_file = "accounts.csv"

with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    accounts = []
    for row in reader:
        account = f"{row['username']}:{row['password']}"
        accounts.append(account)

data["accounts"] = "\n".join(accounts)

# Gửi yêu cầu POST
response = requests.post(url, data=data)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.status_code)
