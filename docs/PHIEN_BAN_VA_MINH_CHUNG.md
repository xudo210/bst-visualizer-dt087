# Đối chiếu phiên bản mã nguồn và minh chứng DT087

**Ngày đóng gói:** 01/11/2026.  
**Repository công khai:** https://github.com/xudo210/bst-visualizer-dt087  
**Phiên bản GitHub đã chụp minh chứng (Commit C):** `ef3be7982a911e3340021beb7fcb56990fe26fb3`  
**Website công khai:** https://bst-visualizer-dt087.onrender.com/

## Hai phiên bản có khác nhau

- **C**: mã nguồn trên GitHub tại SHA nêu trên. Ảnh A09 chứng minh 12/12 ca CLI và khảo sát 5/20/50 nút; A10 chứng minh 44 unittest OK trên bản clone GitHub; A11 là ảnh repository Public/commit.
- **S-ZIP (bản đóng gói tích hợp):** mã nguồn đầy đủ đặt trong ZIP nộp kèm Word/PDF/TXT. Bản này có thêm kiểm thử, thực nghiệm 29 lượt, ảnh minh chứng, tài liệu và các thay đổi code so với C; **không trùng GitHub SHA C**.
- **Commit S trên GitHub:** hiện **chưa có SHA xác nhận cho bản S-ZIP**. Chỉ có thể điền SHA S mới sau khi đưa bản S-ZIP lên GitHub và xác nhận đúng tree mã nguồn. Không được ghi SHA C thành SHA S của ZIP vì mã nguồn khác nhau.
- **Định danh S-ZIP:** SHA-256 của chính file ZIP được ghi trong `*_ThongTinNop.txt` bên ngoài ZIP. File ZIP không tự chứa mã băm của chính nó để tránh vòng lặp tham chiếu.

## Kiểm tra thực tế trên bản S-ZIP

- `python -m test.runtests`: 12/12 PASS.
- `python -m unittest discover -s test -p "test_*.py" -v`: 52 ca được phát hiện; 36 OK, 16 skipped vì môi trường kiểm tra không có Flask. Các ca skipped **không được coi là PASS**.
- `python -m experiments.benchmark`: 29/29 PASS.
- Để kiểm toàn bộ endpoint HTTP, chạy lại trên máy có Flask: `python -m pip install -r requirements-web.txt` rồi chạy unittest.

## Minh chứng và tính trung thực

- A01–A08: ảnh CLI giai đoạn trước, kết quả từng trường hợp đã đối chiếu logic BST.
- A09: ảnh chạy 12/12 ca CLI trên bản clone C và khảo sát 5/20/50.
- A10: ảnh 44 unittest trên bản clone C; ảnh remote/SHA/clean.
- A11: ảnh GitHub Public, main, commit C `ef3be79`.
- W01–W04: minh họa giao diện/thuật toán từ website.

Các minh chứng A09–A11 xác nhận **C**; chúng không tự động chứng minh toàn bộ mã mới trong S-ZIP đã được push lên GitHub.
