# DT087 — Ket qua thuc nghiem co the tai lap

Du lieu tao boi `python -m experiments.benchmark` tu ma nguon BST hien tai.
Moi ca dung **cay moi**; cac phep xoa trong bang **khong lien tiep**.
Chieu cao: cay rong 0, la 1. Danh sach khoa 1..n; `chia_giua` chen trung vi truoc.
Khong suy ra thoi gian mili giay tu so luot xet nut.

| n | Kieu cay | Khoa xoa | h truoc | Loai xoa | Tim khoa | Xet ke vi | Di trai | Don ban sao | Tong luot xet |
|---:|---|---:|---:|---|---:|---:|---:|---:|---:|
| 5 | tang_dan | 1 | 5 | mot_con | 1 | 0 | 0 | 0 | 1 |
| 5 | tang_dan | 5 | 5 | la | 5 | 0 | 0 | 0 | 5 |
| 5 | chia_giua | 3 | 3 | hai_con | 1 | 1 | 0 | 1 | 3 |
| 5 | chia_giua | 5 | 3 | la | 3 | 0 | 0 | 0 | 3 |
| 20 | tang_dan | 1 | 20 | mot_con | 1 | 0 | 0 | 0 | 1 |
| 20 | tang_dan | 20 | 20 | la | 20 | 0 | 0 | 0 | 20 |
| 20 | chia_giua | 10 | 5 | hai_con | 1 | 3 | 2 | 3 | 7 |
| 20 | chia_giua | 20 | 5 | la | 5 | 0 | 0 | 0 | 5 |
| 50 | tang_dan | 1 | 50 | mot_con | 1 | 0 | 0 | 0 | 1 |
| 50 | tang_dan | 50 | 50 | la | 50 | 0 | 0 | 0 | 50 |
| 50 | chia_giua | 25 | 6 | hai_con | 1 | 4 | 3 | 4 | 9 |
| 50 | chia_giua | 50 | 6 | la | 6 | 0 | 0 | 0 | 6 |

## Hai ca ke vi dac biet

| Ca | Khoa xoa | Ke vi | Tim khoa | Xet ke vi | Di trai | Don ban sao | Tong |
|---|---:|---:|---:|---:|---:|---:|---:|
| KE_VI_SAU | 50 | 55 | 1 | 4 | 3 | 4 | 9 |
| KE_VI_CO_CON_PHAI | 50 | 60 | 1 | 2 | 1 | 2 | 5 |

## Quy uoc va nhan xet

- `Tim khoa`: moi nut duoc xet tren duong di den khoa xoa, khong phai tong toan tu `<`, `>`, `==`.
- `Xet ke vi`: moi nut duoc xet tren duong tim min cay con phai (bao gom min).
- `Di trai`: so canh trai di qua, bang `xet ke vi - 1` khi co ke vi.
- `Don ban sao`: so nut duoc xet trong lan xoa nut ke vi cu.
- `Tong luot xet = tim khoa + xet ke vi + don ban sao` (khong cong di trai lan hai).
- Khong tinh dung cay, duyet inorder, in chuoi, ve hinh, callback va Flask vao so lieu xoa.
- BST lech co h=n; BST chen theo chia giua co h~log2(n). Thao tac xoa O(h), xau nhat O(n).
- Day tang dan xoa goc chi xet 1 nut vi goc co mot con; de thay chi phi O(n) phai xoa khoa o cuoi.
- CSV chua du day chen, goc, so nut, inorder truoc/sau, va trang thai PASS tung ca.

## Cach tai lap

```powershell
python -m experiments.benchmark
python -m unittest test.test_thuc_nghiem -v
```
