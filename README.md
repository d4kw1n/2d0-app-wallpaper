# 2Do - Task Desktop App

Ứng dụng quản lý công việc cá nhân, trực quan, đa nền tảng (Windows/Linux), hỗ trợ theme, đa ngôn ngữ, tự động đặt hình nền, chạy nền system tray.

## 🚀 Tính năng nổi bật
- Thêm/xóa/đánh dấu hoàn thành task, mục tiêu tháng, mục tiêu dài hạn
- Tự động tạo hình ảnh danh sách task và đặt làm hình nền
- Chạy nền system tray, hỗ trợ ẩn/hiện, menu chuột phải
- Tùy chọn theme (Dark/Light), đa ngôn ngữ (Tiếng Việt/English)
- Tùy chọn tự động xóa task hôm nay khi sang ngày mới
- Hỗ trợ portable (chạy trực tiếp) và bản cài đặt (installer)

## 📦 Download & Release
- **Tải bản portable hoặc bản cài đặt mới nhất tại:**
  [👉 Trang Release trên GitHub](https://github.com/d4kw1n/2d0-app-wallpaper/releases)
- **Donate ủng hộ tác giả:**
  [☕ Buy Me a Coffee](https://www.buymeacoffee.com/shr3wd)

## 🖥️ Hướng dẫn cài đặt & sử dụng

### 1. Yêu cầu
- Python 3.8+
- pip
- (Windows) Đã cài Visual C++ Build Tools nếu gặp lỗi khi cài Pillow

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng (dev)
```bash
python main.py
```

### 4. Build bản portable (Windows)
```bash
pyinstaller --onefile --windowed --icon=assets/logo.ico --add-data "assets;assets" --name 2Do main.py
```
- File exe sẽ nằm ở `dist/2Do.exe`. Chạy trực tiếp không cần cài đặt.

### 5. Build bản portable (Linux)
```bash
pyinstaller --onefile --windowed --icon=assets/logo.png --add-data "assets:assets" --name 2Do main.py
```
- File exe sẽ nằm ở `dist/2Do`. Chạy trực tiếp không cần cài đặt.

### 6. Tạo bản cài đặt (Windows)
- Cài [Inno Setup](https://jrsoftware.org/isinfo.php)
- Sử dụng file script mẫu `installer.iss` (xem trong repo)
- Build xong sẽ có file `2DoSetup.exe` cho phép chọn thư mục cài đặt, tạo shortcut Start Menu/Desktop

### 7. Tạo shortcut trên Linux
- Tạo file `2Do.desktop` như hướng dẫn trong README, copy vào `~/.local/share/applications/`

## 📝 Lưu ý
- Đảm bảo file icon/logo/font đều nằm trong thư mục `assets/`
- Nếu build bản portable, chỉ cần gửi file exe và thư mục assets cho người dùng
- Nếu build bản cài đặt, chỉ cần gửi file setup

## 💡 Đóng góp & Liên hệ
- Đóng góp code, báo lỗi, góp ý: tạo issue hoặc pull request trên GitHub
- Donate ủng hộ tác giả: [☕ Buy Me a Coffee](https://www.buymeacoffee.com/shr3wd)

---

## License
MIT 