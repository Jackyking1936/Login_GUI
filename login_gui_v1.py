import sys
import base64
from pathlib import Path
from image_data import login_image_data

from fubon_neo.sdk import FubonSDK

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QMessageBox, QFileDialog
from PySide6.QtGui import QImage, QPixmap, QIcon, QFont
from PySide6.QtCore import Qt
import os
import certifi

class LoginForm(QWidget):
    def __init__(self, fubon_sdk):
        super().__init__()

        my_img_data = login_image_data()
        folder_data = base64.b64decode(my_img_data.folder_data)
        fubon_data = base64.b64decode(my_img_data.fubon_data)

        folder_icon = self.icon_parser(folder_data)
        fubon_icon = self.icon_parser(fubon_data)

        self.sdk = fubon_sdk

        self.setWindowIcon(fubon_icon)
        self.setWindowTitle('新一代API連線測試')
        self.resize(500, 200)
        
        layout_all = QVBoxLayout()

        label_warning = QLabel('本程式僅供新一代API連線測試')
        layout_all.addWidget(label_warning)

        layout = QGridLayout()

        label_your_id = QLabel('身份證字號:')
        label_your_id.setAlignment(Qt.AlignRight)
        self.lineEdit_id = QLineEdit()
        self.lineEdit_id.setPlaceholderText('請輸入身份證字號')
        layout.addWidget(label_your_id, 0, 0)
        layout.addWidget(self.lineEdit_id, 0, 1)

        label_password = QLabel('登入密碼:')
        label_password.setAlignment(Qt.AlignRight)
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('請輸入登入密碼')
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        label_cert_path = QLabel('憑證路徑:')
        label_cert_path.setAlignment(Qt.AlignRight)
        self.lineEdit_cert_path = QLineEdit()
        self.lineEdit_cert_path.setPlaceholderText('請選擇憑證路徑')
        layout.addWidget(label_cert_path, 2, 0)
        layout.addWidget(self.lineEdit_cert_path, 2, 1)
        
        label_cert_pwd = QLabel('憑證密碼:')
        label_cert_pwd.setAlignment(Qt.AlignRight)
        self.lineEdit_cert_pwd = QLineEdit()
        self.lineEdit_cert_pwd.setPlaceholderText('若為預設憑證密碼請留白')
        self.lineEdit_cert_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(label_cert_pwd, 3, 0)
        layout.addWidget(self.lineEdit_cert_pwd, 3, 1)

        folder_btn = QPushButton('')
        folder_btn.setIcon(folder_icon)
        layout.addWidget(folder_btn, 2, 2)

        login_btn = QPushButton('登入測試')
        layout.addWidget(login_btn, 4, 0, 1, 2)

        layout_all.addLayout(layout)
        self.setLayout(layout_all)
        
        os.environ['SSL_CERT_FILE'] = certifi.where()

        login_btn.clicked.connect(self.check_password)
        folder_btn.clicked.connect(self.showDialog)

    def icon_parser(self, image_byte_data):
        qimg = QImage.fromData(image_byte_data, 'PNG')
        qpix = QPixmap.fromImage(qimg)
        my_icon = QIcon(qpix)
        return my_icon

    def showDialog(self):
        # Open the file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, '請選擇您的憑證檔案', 'C:\\', 'All Files (*)')

        if file_path:
            self.lineEdit_cert_path.setText(file_path)
    
    def check_password(self):
        self.active_account = None
        msg = QMessageBox()

        fubon_id = self.lineEdit_id.text()
        fubon_pwd = self.lineEdit_password.text()
        cert_path = self.lineEdit_cert_path.text()
        cert_pwd = self.lineEdit_cert_pwd.text()

        if cert_pwd == "":
            accounts = self.sdk.login(fubon_id, fubon_pwd, Path(cert_path).__str__())
        else:
            accounts = self.sdk.login(fubon_id, fubon_pwd, Path(cert_path).__str__(), cert_pwd)

        if accounts.is_success:                 
            msg.setWindowTitle("登入成功")
            msg.setText("此帳號已完成簽署及連線測試")
            msg.exec()
        else:
            msg.setWindowTitle("測試訊息")
            msg.setText(accounts.message)
            msg.exec()

if __name__ == "__main__":
    try:
        sdk = FubonSDK()
    except ValueError:
        raise ValueError("請確認網路連線")
    active_account = None
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setStyleSheet("QWidget{font-size: 14pt;}")
    font = QFont("Microsoft JhengHei")  # 字體名稱和字體大小
    app.setFont(font)
    form = LoginForm(sdk)
    form.show()
    
    sys.exit(app.exec())