# DT087 – Bản web và mã nguồn CUỐI CÙNG

**Đề tài:** Xóa nút trên cây tìm kiếm nhị phân (BST): nút lá, một con, hai con, dùng nút kế vị (successor).  
**Học phần:** Cấu trúc dữ liệu và Giải thuật – INT13185.  
**Sinh viên:** Lê Anh Tuấn – N24DCDT105.  
**Website:** https://bst-visualizer-dt087.onrender.com/  
**Repository:** https://github.com/xudo210/bst-visualizer-dt087

## Chức năng đã tích hợp trong một bản duy nhất

1. Tạo BST với tối đa 100 khóa nguyên phân biệt, kiểm tra dữ liệu sai/trùng.
2. Xóa lá, một con, hai con dùng successor, xóa khóa không tồn tại, cây rỗng.
3. **Xóa nhiều khóa liên tiếp**: tối đa 20 khóa trên cây cập nhật sau lần trước.
4. Mô phỏng SVG từng sự kiện từ callback của chính `src/bst.py` (không dựng lại thuật toán JS).
5. 8 ví dụ nhanh, gồm kế vị sâu và kế vị có cây con phải.
6. Bộ đếm theo từng bước: xét nút khi tìm khóa, xét nút/bước trái tìm kế vị, xét nút khi xóa bản sao.
7. Inorder trước/sau, gốc, số nút, chiều cao và trạng thái hợp lệ BST.
8. Sao chép kết quả và **tải nhật ký từng bước dạng `.txt`**; favicon riêng; giao diện co giãn.
9. 12 ca kiểm thử chuẩn, bộ kiểm thử mở rộng, bộ kiểm thử web, và 29 lượt thực nghiệm 5/20/50 nút.

**Chú ý:** Các ô gốc, số nút, chiều cao là **kết quả cuối của lần xóa**, còn hình cây và bộ đếm là **trạng thái của bước đang xem**. Bước sao chép khóa successor có thể tạm thời hiện hai khóa trùng; BST chỉ được kiểm tra ở cuối thao tác.

## Chạy trên Windows

Mở CMD **ngay tại thư mục chứa `web_app.py`**, chạy:

```powershell
python -m pip install -r requirements-web.txt
python -m test.runtests
python -m unittest discover -s test -p "test_*.py" -v
python -m experiments.benchmark
python web_app.py
```

Sau đó mở http://127.0.0.1:5000/ . Nếu Flask đang chạy ở cửa sổ CMD khác, dùng `Ctrl+C` để dừng bản cũ trước khi khởi động bản mới.

## Kiểm tra nhanh trước khi đưa lên GitHub

1. Ví dụ 06: chèn `5,3,7,2,4,6,8`; xóa `5,3,99,6`; gốc sau từng lần `6,6,6,7`; inorder cuối `[2,4,7,8]`.
2. Ví dụ 07: kế vị sâu; bộ đếm khi kết thúc tìm khóa `1`, xét kế vị `4`, bước trái `3`, xét xóa bản sao `4`, tổng lượt xét `9`.
3. Ví dụ 08: nút kế vị có con phải; kiểm tra inorder giữ nguyên tất cả khóa trừ khóa xóa.
4. Nút **Tải nhật ký từng bước (.txt)** tải được file và ghi đủ các lần xóa.
5. Chạy lại toàn bộ test, sau đó chạy website ở localhost; cuối cùng cập nhật GitHub đúng **một lần** và kiểm tra Render Live.

## Triển khai Render

- Build Command: `pip install -r requirements-web.txt`
- Start Command: `gunicorn web_app:app`
- Root Directory: để trống
- Instance Type: Free (nếu sử dụng gói miễn phí)
- Repository: `xudo210/bst-visualizer-dt087`, branch `main`.

Chỉ tải **nội dung của thư mục này** lên thư mục gốc repository. Không cần đẩy ZIP; bỏ qua `__pycache__`, `.venv`, `*.pyc`. Không ghi đè một phiên bản đã chạy ổn mà chưa kiểm thử.

## Sơ đồ mã nguồn

- `src/bst.py`: BST cốt lõi, duyệt inorder O(n), chèn/xóa/tìm kế vị và bộ đếm.
- `web_trace.py`: chuyển các sự kiện xóa thành khung mô phỏng.
- `web_app.py`: Flask và các endpoint JSON.
- `templates/index.html`, `static/app.js`, `static/style.css`: website.
- `demo.py`: CLI và hai ví dụ bắt buộc.
- `test/`: kiểm thử gốc, nâng cao, bộ đếm, website và hồi quy giao diện.
- `experiments/`: 29 lượt thực nghiệm, CSV và bảng Markdown phục vụ báo cáo.
- `docs/anh_ket_qua/`: ảnh minh chứng từ phiên bản trước; ảnh GitHub, kiểm thử và website công khai cần được chụp lại theo phiên bản cuối.

## Phiên bản nộp và ảnh minh chứng

Gói tích hợp này đã được kiểm thử trực tiếp với các lệnh trong mục "Chạy trên Windows". Mã nguồn ZIP đầy đủ **khác** commit GitHub C được chụp trong A10–A11. Xem `docs/PHIEN_BAN_VA_MINH_CHUNG.md` và mã SHA-256 ZIP trong file TXT thuộc bộ hồ sơ nộp.

Các ảnh A01–A08 là hình chạy CLI từ giai đoạn trước; A09–A11 minh chứng cho commit C trên GitHub. Các hình W01–W04 dùng minh họa chức năng web. Người nộp cần hiểu được cách nối liên kết và thay successor khi trình bày.

Mã nguồn có sự hỗ trợ biên soạn từ công cụ AI; người nộp chịu trách nhiệm rà soát, kiểm thử và trình bày trung thực.
