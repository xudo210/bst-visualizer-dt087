"""Chay: python demo.py --example 1 | --example 2 | --interactive"""
import argparse
from src.bst import ThongKe, tao_cay, xoa, duyet_giua, dem_nut, chieu_cao, ve_cay_chu


def chay(day, day_xoa):
    g = tao_cay(day)
    print('Day chen:', day)
    print('Inorder ban dau:', duyet_giua(g))
    print(ve_cay_chu(g), end='')
    for khoa in day_xoa:
        print(f'\n--- XOA {khoa} ---')
        truoc = duyet_giua(g)
        tk = ThongKe()
        g = xoa(g, khoa, tk)  # BAT BUOC gan lai goc
        print('Truoc:', truoc)
        print('Sau:  ', duyet_giua(g))
        print('Goc:', g.khoa if g else 'nothing')
        print('So nut:', dem_nut(g), '| Chieu cao:', chieu_cao(g))
        print('Truong hop:', tk.truong_hop,
              '| Ke vi:', tk.ke_vi if tk.ke_vi is not None else 'khong co')
        # Cac gia tri sau la luot xet NUT, khong phai so toan tu <, >, ==.
        print('Nut xet khi tim khoa:', tk.so_sanh_tim,
              '| Nut xet de tim ke vi:', tk.so_nut_xet_ke_vi)
        print('Buoc sang trai tim ke vi:', tk.so_buoc_ke_vi,
              '| Nut xet de xoa ban sao:', tk.so_nut_xet_xoa_ban_sao)
        print(ve_cay_chu(g), end='')


def parse_nums(s: str) -> list[int]:
    if not s.strip():
        return []
    return [int(part.strip()) for part in s.replace(';', ',').split(',') if part.strip()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DT087 - Xoa BST bang ke vi min cay phai')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--example', type=int, choices=[1, 2])
    group.add_argument('--interactive', action='store_true')
    args = parser.parse_args()
    if args.example == 1:
        chay([5, 3, 7, 2, 4, 6, 8], [5])
    elif args.example == 2:
        chay([4, 2, 6, 1], [2])
    else:
        try:
            ds = parse_nums(input('Nhap cac khoa nguyen phan biet (vd 5,3,7): '))
            can_xoa = parse_nums(input('Nhap cac khoa can xoa (vd 5,7): '))
            chay(ds, can_xoa)
        except ValueError as exc:
            print('DU LIEU KHONG HOP LE:', exc)
            raise SystemExit(2)
