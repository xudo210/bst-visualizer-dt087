# DT087 — BST Visualizer (Flask + Python gốc)

## 1. Yêu cầu
- Python 3.10 trở lên
- Kết nối Internet **chỉ khi cài Flask lần đầu**; sau đó chạy web trên máy không cần Internet (font sẽ dùng dự phòng nếu offline).

## 2. Cài đặt và chạy
Mở Terminal/PowerShell trong thư mục `DT087_LeAnhTuan`:

```powershell
python -m pip install -r requirements-web.txt
python web_app.py
```

Mở trình duyệt: **http://127.0.0.1:5000**

Trên Windows nếu lệnh `python` không chạy, thử `py` thay cho `python`.

## 3. Cách dùng
1. Nhập dãy khóa nguyên phân biệt (tối đa 100 khóa).
2. Nhập khóa cần xóa.
3. Nhấn **Tạo cây & mô phỏng**.
4. Dùng **Phát / Tạm dừng**, nút tiến/lùi hoặc thanh trượt để xem các bước.
5. Quan sát Inorder trước/sau, gốc mới, số nút, chiều cao, số phép so sánh và nút kế vị.

Các nút ví dụ bên trái cho phép thử ngay: xóa nút lá, một con, hai con, cây rỗng, kế vị nằm sâu.

## 4. Cấu trúc và tính đúng
- `src/bst.py`: **giữ nguyên** mã thuật toán BST của bài gốc.
- `web_trace.py`: phân tích đường tìm kiếm, tạo khung hình minh họa và **gọi trực tiếp `src.bst.xoa()` để tính kết quả cuối**.
- `web_app.py`: Flask HTTP API và trang chủ.
- `templates/index.html`, `static/style.css`, `static/app.js`: giao diện.
- `test/runtests.py`: bộ kiểm thử cũ.
- `test/test_web.py`: kiểm thử bổ sung cho API web.

**Lưu ý kỹ thuật:** Các khung hình trước bước cuối mô tả quá trình tìm và chọn kế vị; khung hình cuối là kết quả thực thi hàm xóa gốc. Đây không phải trình gỡ lỗi ghi lại từng thay đổi con trỏ bên trong `src.bst.xoa`.

## 5. Kiểm thử
```powershell
python -m test.runtests
python -m unittest test.test_web -v
```

## 6. Khi nộp và bảo vệ
- Chạy cả 2 ví dụ bắt buộc.
- Chạy thêm xóa lá, xóa một con, xóa khóa không tồn tại, cây rỗng.
- Chụp ảnh giao diện web để đưa vào mục mở rộng của báo cáo (nếu được phép).
- Nhấn mạnh kết quả được tính từ **mã Python gốc**, không phải thuật toán viết lại trên JavaScript.
- Không đưa web lên Internet công khai nếu chưa cấu hình bảo mật và máy chủ production; Flask ở đây chỉ chạy cục bộ.
