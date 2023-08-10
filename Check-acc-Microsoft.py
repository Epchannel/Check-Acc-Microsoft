import requests
import csv

# Danh sách API cần kiểm tra
api_servers = {
    "1": "Server 1",
    "2": "Server 2"
}

api_urls = {
    "1": "https://khoatoantin.com/ajax/office365_api",
    "2": "https://pidkey.com/ajax/office365_api"
}

# Thông tin xác thực cho API
auth_data = {
    "username": "trogiup24h",
    "password": "PHO"
}

# Đọc dữ liệu từ tệp CSV
csv_file = "accounts.csv"

# Lưu tài khoản hợp lệ
valid_accounts = []

# Lựa chọn server API từ người dùng
print("Chọn server API để kiểm tra:")
for key, value in api_servers.items():
    print(f"{key}: {value}")
selected_api = input("Nhập số tương ứng với server API: ")

if selected_api in api_urls:
    selected_api_url = api_urls[selected_api]

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        accounts = []
        for row in reader:
            account = f"{row['username']}:{row['password']}"
            accounts.append(account)

        auth_data["accounts"] = "\n".join(accounts)

    # Gửi yêu cầu POST đến API
    response = requests.post(selected_api_url, data=auth_data)

    if response.status_code == 200:
        data = response.json()
        for item in data:
            username = item.get('username', '')
            password = item.get('password', '')
            status = item.get('status', '')
            if status == 'valid':
                valid_accounts.append(f"{username}:{password} from {api_servers[selected_api]}")
                print(f"Valid: {username}:{password} from {api_servers[selected_api]}")
    else:
        print(f"Error from {api_servers[selected_api]}:", response.status_code)

    # Ghi các tài khoản hợp lệ vào tệp tin
    valid_accounts_file = "valid_accounts.txt"
    with open(valid_accounts_file, "w") as file:
        for account in valid_accounts:
            file.write(account + "\n")

    print("Đã ghi các tài khoản hợp lệ vào tệp", valid_accounts_file)
else:
    print("Lựa chọn server API không hợp lệ.")
