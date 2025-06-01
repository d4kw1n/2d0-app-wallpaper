# Task Manager Desktop App

Ứng dụng quản lý công việc cho phép tạo danh sách task và hiển thị chúng dưới dạng hình nền desktop.

## Tính năng

- Thêm và quản lý các task công việc
- Chạy nền (system tray)
- Tạo hình ảnh trực quan từ danh sách task
- Tự động đặt hình ảnh làm hình nền desktop

## Cài đặt

1. Cài đặt Python 3.8 trở lên
2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Chạy ứng dụng:
```bash
python main.py
```

2. Nhập các task vào ô input và nhấn "Thêm"
3. Nhấn "Tạo hình ảnh" để tạo hình ảnh từ danh sách task
4. Nhấn "Đặt làm hình nền" để đặt hình ảnh làm hình nền desktop

## Lưu ý

- Ứng dụng sẽ chạy trong system tray khi đóng cửa sổ chính
- Hình ảnh được lưu trong thư mục "images"
- Cần thêm file icon.png vào thư mục gốc để hiển thị icon trong system tray 