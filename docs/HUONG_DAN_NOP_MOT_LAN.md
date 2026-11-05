# Quy trình nộp và cập nhật website MỘT LẦN

1. Không xóa repository hay hoàn tác commit cũ khi website đang chạy. Giữ nguyên backup local.
2. Chạy toàn bộ test từ bản cuối; xem `README.md`.
3. Thử trên `http://127.0.0.1:5000/`: ví dụ 01–08, đặc biệt 06/07/08; tải nhật ký TXT.
4. Upload **các file và thư mục con của bản cuối** lên repository `xudo210/bst-visualizer-dt087`, thay đúng những file trùng tên. **Không tải nguyên ZIP**.
5. Đảm bảo `requirements-web.txt` có cả Flask và gunicorn.
6. Render → Deploy latest commit (nếu Auto Deploy chưa kích hoạt); chờ Live.
7. Mở trang công khai trong tab ẩn danh; kiểm ví dụ 06 và nút tải TXT.
8. Ghi SHA commit cuối, chụp hình GitHub/Render/kiểm thử/bảng thực nghiệm để bổ sung báo cáo Word.

Website này và chương trình dòng lệnh dùng chung `src/bst.py`. Không cần tạo thêm một repo cho mã nguồn chỉ vì `src/` nằm trong repo web.
