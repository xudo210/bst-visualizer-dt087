# BST Visualizer DT087 - Nâng cấp thuật toán

## Điểm mới

- `src/bst.py`: `xoa(g, x, tk=None, ghi_buoc=None)` giữ tương thích với mã nguồn gốc.
- Callback `ghi_buoc(event, **metadata)` được gọi **ngay trong thuật toán xóa** để ghi nhận quá trình duyệt, lựa chọn kế vị, thay khóa và nối lại nhánh.
- `web_trace.py`: ghi lại ảnh chụp cây tại mỗi sự kiện; không còn chạy thuật toán mô phỏng riêng trước khi gọi `xoa`.
- `test/test_nang_cao.py`: kiểm thử kế vị có con phải, trạng thái mô phỏng và xóa liên tiếp với seed cố định.

## Chạy

Tại thư mục `DT087_LeAnhTuan`:

```powershell
python -m test.runtests
python -m unittest test.test_nang_cao -v
python -m pip install -r requirements-web.txt
python -m unittest test.test_web -v
python web_app.py
```

Mở `http://127.0.0.1:5000`.

## Giải thích để bảo vệ

- Xóa lá: trả về `None` để cha ngắt liên kết.
- Xóa một con: trả về con duy nhất để cha nối lại.
- Xóa hai con: chọn nút nhỏ nhất của cây con phải, sao chép khóa kế vị, xóa nút kế vị cũ rồi cập nhật liên kết.
- Với mỗi nút, đường tìm kiếm giảm dần độ sâu nên kết thúc. Cây cuối cùng vẫn thỏa `trái < gốc < phải`.
- Thời gian `O(h)`, bộ nhớ ngăn xếp `O(h)`; cây cân đối `O(log n)`, cây suy biến `O(n)`.

## Lưu ý kỹ thuật

Ở bước `thay_khoa`, cây **tạm thời có hai nút cùng khóa** (bản sao kế vị chưa xóa). Đây là trạng thái trung gian của thuật toán, không phải BST hoàn chỉnh; chỉ kiểm tra bất biến sau khi kết thúc. Khi xóa nút gốc có 0 hoặc 1 con, snapshot cuối mới phản ánh gốc mới sau khi hàm `xoa` trả về.

Các phép so sánh `so_sanh_tim` giữ đúng quy ước thống kê trước đây, không tính các phép so sánh khi dọn nút kế vị.

## Nộp bài

Không sửa các số liệu và ảnh minh chứng cũ rồi khẳng định đó là kết quả của bản nâng cấp. Chạy lại trên máy, chụp ảnh mới và bổ sung mục 'Mở rộng: ghi vết thực thi trực tiếp trong thuật toán' vào báo cáo.
