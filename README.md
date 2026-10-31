# DT087 – Xóa nút cây nhị phân tìm kiếm (BST)

- Sinh viên: Lê Anh Tuấn – N24DCDT105 – D24CQDT01-N
- Học phần INT13185, Nhóm 03; đề DT087.
- Ngôn ngữ: Python 3 (chỉ dùng thư viện chuẩn).
- Thuật toán: `src/bst.py`; ví dụ/nhập liệu: `demo.py`; kiểm thử: `test/runtests.py`.

## Chạy trong VS Code
Mở **Open Folder** tại thư mục dự án chứa `demo.py`.

```powershell
python demo.py --example 1
python demo.py --example 2
python demo.py --interactive
python -m test.runtests
```

Nếu Windows dùng `py`, thay `python` bằng `py`.

## Hợp đồng hàm
- `tao_cay(day)`: tối đa 100 khóa nguyên phân biệt. Trùng khóa hoặc sai loại -> `ValueError`.
- `chen(g,x)` chèn và **trả gốc**.
- `nho_nhat(g)` đi trái đến cuối, xác định successor.
- `xoa(g,x,tk)` xử lý lá/một con/hai con, **trả gốc mới**. Khi hai con, chép khóa successor rồi xóa bản gốc của successor.
- `duyet_giua`, `dem_nut`, `kiem_bst`, `chieu_cao` là các hàm độc lập để kiểm chứng.

Cây rỗng có gốc `None` (tương đương `nothing` trong mẫu Julia), cao 0. Lá cao 1.

## Bằng chứng cần bổ sung bởi sinh viên
Chụp **ảnh chạy thật** cho `VD01`, `VD02`, `TK01`, `TK02`, `BIEN01`, `BIEN02`, `BIEN03`, `LOI01`, tổng kết test, GitHub commit, clone sạch rồi chạy lại = 11 ảnh tối thiểu.

**Lưu ý:** Mã nguồn do trợ lý hỗ trợ soạn dựa theo phiếu DT087. Người nộp cần đọc, tự chạy, kiểm thử, kiểm tra độc lập và trình bày trung thực quá trình thực hiện. Không sử dụng ảnh mẫu BFS làm minh chứng.
