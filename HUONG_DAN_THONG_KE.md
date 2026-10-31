# DT087 — NÂNG CẤP SỐ 2: THỐNG KÊ CHI PHÍ THUẬT TOÁN

## Mục tiêu

Bổ sung thống kê theo từng frame lấy trực tiếp từ callback trong `src/bst.py`:

1. **Nút xét khi tìm khóa** (`search_nodes`, tương thích `comparisons` cũ): mỗi nút xét khi tìm khóa mục tiêu tính 1; KHÔNG đồng nghĩa với đếm từng toán tử `<`, `>`, `==`.
2. **Nút xét khi tìm kế vị** (`successor_visits`): đếm nút đầu tiên ở con phải và từng nút trái khi truy tìm khóa nhỏ nhất.
3. **Bước đi trái khi tìm kế vị** (`successor_steps`): đếm số cạnh đi trái; bằng `successor_visits - 1` nếu có kế vị.
4. **Nút xét khi xóa bản sao kế vị** (`cleanup_visits`): đếm lượt xét trên đường đệ quy xóa nút kế vị cũ trong cây con phải.
5. **Tổng lượt xét nút** (`total_visits`): tổng các pha trên; cùng một nút có thể được tính nhiều lần vì thuật toán hiện duyệt lại để xóa bản sao.

**Không** tính chi phí tạo cây, snapshot, vẽ SVG hoặc duyệt inorder vào các bộ đếm này. Các giá trị chỉ là phép đo theo định nghĩa; không phải thời gian chạy, không phải tổng số phép toán CPU. Độ phức tạp thuật toán xóa theo chiều cao cây: `O(h)` thời gian, `O(h)` stack đệ quy.

## Chạy trên máy (Windows)

1. Giải nén ZIP, vào thư mục `DT087_BanNangCap_ThongKeChinhXac` (nơi có `web_app.py`).
2. Mở CMD ngay trong thư mục, chạy:

```bat
python -m pip install -r requirements-web.txt
python -m test.runtests
python -m unittest test.test_nang_cao test.test_web test.test_web_batch test.test_thong_ke -v
python thuc_nghiem_thong_ke.py
python web_app.py
```

3. Vào `http://127.0.0.1:5000/`, bấm `Ctrl + Shift + R` nếu vẫn thấy bản cũ.
4. Chọn **07 · Kế vị nhiều bước**: cây chèn `50,30,80,70,90,60,75,55,65`, xóa `50`. Ở bước cuối phải thấy: tìm khóa 1 nút; tìm kế vị 4 nút, đi trái 3 bước; xóa bản sao 4 nút; tổng 9 lượt thăm; gốc mới `55`.
5. Chọn **08 · Kế vị có con phải**: `50,30,80,60,90,70,65`, xóa `50`. Kế vị `60`, số nút xét kế vị 2, đi trái 1, dọn bản sao 2; gốc mới 60; inorder `[30,60,65,70,80,90]`.
6. Kéo thanh timeline về đầu: mọi bộ đếm = 0. Kéo đến giữa: tăng theo từng sự kiện; đến cuối: bằng kết quả chính thức. Kiểm ví dụ `06 · Xóa nhiều khóa` hoạt động như trước.

## Cập nhật GitHub / Render

Sau khi chạy TEST thành công trên máy, mở repo `xudo210/bst-visualizer-dt087` và cập nhật các file mới (không đưa lên nguyên ZIP):

- `src/bst.py`
- `web_trace.py`
- `templates/index.html`
- `static/app.js`
- `static/style.css`
- `test/test_thong_ke.py` (mới)
- `thuc_nghiem_thong_ke.py` (mới, sinh bảng khảo sát)
- `HUONG_DAN_THONG_KE.md` (mới)

**Không được làm mất `gunicorn` trong `requirements-web.txt`.** Render có thể tự redeploy nếu Auto-Deploy bật. Mở lại URL công khai để kiểm tra mục "THỐNG KÊ THAO TÁC" xuất hiện.

## Minh chứng báo cáo

- Chụp ảnh bộ đếm khi bắt đầu, giữa và kết thúc ví dụ 07.
- Nêu rõ quy ước đếm để tránh gọi nhầm 'phép so sánh' nếu đang đếm số nút được xét.
- Báo cáo thời gian xóa `O(h)` với cây cân đối `O(log n)`, cây suy biến `O(n)`. Phần xây cây, ghi snapshot và duyệt inorder không nằm trong chi phí xóa cơ sở.
