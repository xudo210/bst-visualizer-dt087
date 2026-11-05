# DT087 — Nang cap 03: Kiem thu va thuc nghiem (31/10/2026)

## Muc dich

Bo sung bang thuc nghiem co the tai lap cho ba quy mo **5, 20, 50 nut**, va hai ca dac biet ve **tim ke vi**. Khong thay doi `src/bst.py`, giao dien, API, du lieu web, hoac ket qua mo phong.

## Cach chay (Windows CMD tai thu muc goc)

```powershell
python -m test.runtests
python -m unittest discover -s test -p "test_*.py" -v
python -m experiments.benchmark
```

Luu y: khi test HTTP, can cai Flask truoc: `python -m pip install -r requirements-web.txt`.

## Dau ra

- `experiments/ket_qua.csv`: moi hang mot phep xoa **doc lap**, chua danh sach chen, goc/chieu cao/so nut/inorder truoc va sau, cac bo dem va PASS.
- `experiments/BANG_KET_QUA.md`: bang tom tat 5/20/50 nut, co the tham khao khi viet Chuong 4 (khong gan nhan la so lieu cua may khac).
- `test/test_thuc_nghiem.py`: kiem tra bao toan BST, dung so nut, tinh tai lap, CSV va test xoa theo cac day ngau nhien co seed co dinh.

## Quy uoc quan trong

- **Tim khoa:** so nut da xet trong qua trinh tim khoa can xoa (khong phai so lan thuc hien toan tu so sanh).
- **Tim ke vi:** so nut duoc xet khi di sang trai tu goc cay con phai; so buoc trai = so nut xet - 1.
- **Xoa ban sao:** so nut xet khi xoa nut ke vi cu.
- **Tong = tim khoa + tim ke vi + xoa ban sao**; khong cong lai so canh trai de tranh dem trung.
- **Chieu cao:** rong 0, la 1; `xoa` O(h), duyet inorder de kiem chung O(n) tinh rieng.
- **Kieu chia giua:** du lieu chen trung vi truoc de tao cay gan can doi. Khong phai AVL va khong co phep quay.
- **Kieu tron co dinh:** random.Random(87000 + n), xao tron dung mot lan voi moi n.
- Khong dung so luot xet nut nhu thoi gian thuc thi (ms).
- Vi du `tang_dan + xoa_goc` co the chi xet 1 nut, do nut goc co mot con; de cho thay xau nhat, dung `tang_dan + xoa_lon_nhat`.

## Anh minh chung

1. Sau khi chay lai **ban ma nguon cuoi**, chup A09: `python -m test.runtests` hien `12/12 PASS`.
2. Chup bo kiem thu mo rong: `python -m unittest discover -s test -p "test_*.py" -v` (khong bao gom bo `runtests.py` do ten file khac quy tac discover).
3. Chup CMD `python -m experiments.benchmark` hien tong ca PASS va duong dan file CSV; co the kem anh bang CSV trong phu luc.
4. A10 va A11 (clone + GitHub commit) CHI chup lai sau khi day code cuoi len GitHub.
5. Anh cay/xoa truoc day chi can chup lai neu khong con trung voi code/ket qua moi.

## Khuyen nghi bao cao

Bo sung muc **4.x Thuc nghiem va doi chieu**: mo ta thiet ke 3 dang chen (tang, chia giua, tron), 3 tinh huong xoa, bai toan 5/20/50 nut, dinh nghia bo dem, bang so lieu, phan tich xu huong theo chieu cao. Phan biet ro bang thuc nghiem voi do phuc tap ly thuyet va so lieu do tren may cua ban.
