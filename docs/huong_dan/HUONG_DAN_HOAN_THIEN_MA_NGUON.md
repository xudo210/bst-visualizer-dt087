# DT087 - Hoan thien ma nguon BST (nang cap 03)

## Da sua gi?

1. `src/bst.py`: `duyet_giua` ghi vao mot danh sach duoc tich luy, O(n) thoi gian cho n nut, thay cho viec cong danh sach moi nut co the toi O(n^2) tren cay suy bien. Khong thay doi ket qua inorder.
2. `src/bst.py`: `xoa` goi `nho_nhat` thay vi viet lai vong lap tim successor; `nho_nhat` co tham so tuy chon `ghi_xet` de phat su kien trace va cap nhat hai bo dem ke vi. Khong thay doi thu tu su kien, thong ke, quy tac xoa la/mot con/hai con.
3. `demo.py`: in ro 4 bo dem (nut tim khoa, nut tim ke vi, canh trai, nut xoa ban sao). Khong goi so nut xet la "so phep so sanh toan tu".
4. `test/test_cai_tien_bst.py`: 10 ca bo sung ve inorder, successor, callback, thong ke va xoa lien tiep.

## Cach chay

Tren Windows: mo CMD tai thu muc co `demo.py`, roi chay:

```bat
python -m pip install -r requirements-web.txt
python -m test.runtests
python -m unittest test.test_nang_cao test.test_thong_ke test.test_web_batch test.test_cai_tien_bst -v
python -m unittest test.test_web -v
python demo.py --example 1
python demo.py --example 2
python thuc_nghiem_thong_ke.py
python web_app.py
```

Trang localhost: http://127.0.0.1:5000/ . Ban nay van ho tro cac vi du 01-08 va xoa nhieu khoa.

## Minh chung anh / bao cao

- Hinh minh hoa cay BST / website da chup neu cung du lieu va ket qua thi khong can chup lai het.
- Chup LAI cac anh co chua output cua `demo.py` (do ten nhan thong ke doi) va anh ket qua test/clone/repo cung SHA phien ban cu de chung minh ban cuoi.
- Chay `python -m test.runtests` va bo unittest, chup log that; nen chup them ket qua ke vi sau va xoa lien tiep phuc vu bao cao.
- Chot commit SHA moi sau khi GitHub va Render cap nhat. Khong su dung anh cu de chung minh test/commit cua ban moi.

## Muc tieu hieu nang

- `duyet_giua`: O(n) thoi gian, O(n) de luu output va O(h) ngan xep de quy.
- `nho_nhat`: O(h_phai) thoi gian, O(1) bo nho phu khong tinh callback/snapshot.
- `xoa`: O(h) thoi gian, O(h) ngan xep de quy, chua tinh tu dong ghi snapshot/ve do thi neu web mo trace.
