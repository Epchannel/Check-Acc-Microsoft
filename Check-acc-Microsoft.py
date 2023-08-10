import sys
import requests
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QTextEdit

class ServerCheckApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_servers = {
            "1": "Server 1",
            "2": "Server 2"
        }

        self.api_urls = {
            "1": "https://khoatoantin.com/ajax/office365_api",
            "2": "https://pidkey.com/ajax/office365_api"
        }

        self.auth_data = {
            "username": "trogiup24h",
            "password": "PHO"
        }

        self.csv_file = "accounts.csv"
        self.valid_accounts = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Server Check App")
        self.setGeometry(100, 100, 600, 450)

        self.server_label = QLabel("Chọn server API:", self)
        self.server_label.setGeometry(50, 50, 150, 30)

        self.server_combobox = QComboBox(self)
        self.server_combobox.setGeometry(200, 50, 150, 30)
        for key, value in self.api_servers.items():
            self.server_combobox.addItem(f"{key}: {value}")

        self.result_text = QTextEdit(self)
        self.result_text.setGeometry(50, 100, 500, 250)
        self.result_text.setReadOnly(True)

        self.start_button = QPushButton("Bắt đầu kiểm tra", self)
        self.start_button.setGeometry(250, 360, 100, 30)
        self.start_button.clicked.connect(self.start_check)

        self.copy_right_label = QLabel("Copyright (C) 2023 EPCHANNEL", self)
        self.copy_right_label.setGeometry(200, 390, 200, 20)  # Adjust the position here

    def start_check(self):
        selected_api = self.server_combobox.currentText().split(":")[0]
        if selected_api in self.api_urls:
            selected_api_url = self.api_urls[selected_api]

            with open(self.csv_file, "r") as file:
                reader = csv.DictReader(file)
                accounts = []
                for row in reader:
                    account = f"{row['username']}:{row['password']}"
                    accounts.append(account)

                self.auth_data["accounts"] = "\n".join(accounts)

            response = requests.post(selected_api_url, data=self.auth_data)

            if response.status_code == 200:
                data = response.json()
                valid_accounts = []
                for item in data:
                    username = item.get('username', '')
                    password = item.get('password', '')
                    status = item.get('status', '')
                    if status == 'valid':
                        valid_accounts.append(f"{username}:{password} from {self.api_servers[selected_api]}")
                if valid_accounts:
                    self.result_text.setPlainText("\n".join(valid_accounts))
                else:
                    self.result_text.setPlainText("Không có tài khoản hợp lệ.")
            else:
                self.result_text.setPlainText(f"Lỗi từ {self.api_servers[selected_api]}: {response.status_code}")
        else:
            self.result_text.setPlainText("Lựa chọn server API không hợp lệ.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ServerCheckApp()
    mainWin.show()
    sys.exit(app.exec())
