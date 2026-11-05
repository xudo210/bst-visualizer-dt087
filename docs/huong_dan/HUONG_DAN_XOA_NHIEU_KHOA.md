# DT087 — Nâng cấp 1: Xóa nhiều khóa liên tiếp

## Thay đổi
- Nhập một hoặc nhiều khóa cần xóa trong cùng ô, ví dụ `5, 3, 99, 6`.
- Chèn một lần và lần lượt xóa trên *chính cây đã cập nhật*, không dựng lại cây sau mỗi lần.
- Chọn "Lần xóa đang xem" để xem cây, inorder, số nút, gốc, thống kê và 14 bước (hoặc số bước thực tế) của **mỗi** lần xóa.
- Giao diện có ví dụ nhanh `06 · Xóa nhiều khóa`.
- Endpoint `/api/analyze` cũ vẫn giữ nguyên; endpoint mới là `/api/analyze-batch` với `{"values":[5,3,7,2,4,6,8], "targets":[5,3,99,6]}`.

## Những file được thay đổi
- `web_app.py`: thêm API xóa liên tiếp.
- `web_trace.py`: giữ gốc cây giữa các lần, ghi lại snapshot.
- `static/app.js`: xử lý ô nhập dãy xóa và chọn lần xóa.
- `static/style.css`: CSS của thanh chọn lần xóa.
- `templates/index.html`: trường nhập, ví dụ, thanh chọn.
- `requirements-web.txt`: đồng bộ thêm gunicorn như bản trên GitHub.
- `test/test_web_batch.py`: 9 ca mới, trong đó 5 ca API cần Flask.

## Cách chạy trên Windows
1. Giải nén ZIP, mở vào `DT087_BanNangCap_XoaNhieuKhoa`.
2. Bấm thanh địa chỉ File Explorer, gõ `cmd`, Enter.
3. Chạy `python -m pip install -r requirements-web.txt` nếu chưa cài thư viện.
4. Chạy `python -m test.runtests`.
5. Chạy `python -m unittest test.test_nang_cao test.test_web test.test_web_batch -v`.
6. Chạy `python web_app.py`, mở `http://127.0.0.1:5000/`.
7. Nhấn ví dụ `06 · Xóa nhiều khóa`, chọn các lần xóa trong danh sách.

## Kết quả mong đợi
Chèn `5,3,7,2,4,6,8`, xóa liên tiếp `5,3,99,6`:
- Lần 1: `[2,3,4,6,7,8]`, gốc 6.
- Lần 2: `[2,4,6,7,8]`, gốc 6.
- Lần 3: `[2,4,6,7,8]`, gốc 6 (không thấy 99).
- Lần 4: `[2,4,7,8]`, gốc 7.

## Lưu ý cập nhật GitHub và Render
Chỉ sau khi bản local chạy và test ổn, tải những file sửa đổi lên cùng đường dẫn trong repository GitHub `xudo210/bst-visualizer-dt087` và commit. Nếu Render có auto-deploy, nó sẽ cập nhật từ GitHub. Kiểm tra lại link công khai sau khi Render báo Live.

**Không đăng tải file .env, token, mật khẩu hoặc thư mục môi trường ảo.**
