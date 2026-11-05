"""Thuc nghiem BST DT087: cung input, bo dem, ket qua, CSV de tai lap.

Chay o thu muc goc: python -m experiments.benchmark
Du lieu khong dung thoi gian he thong nen co the tai lap tren cac may khac nhau.
Chi thong ke so luot XET NUT: khong phai milliseconds hay so toan tu so sanh.
"""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

from src.bst import ThongKe, tao_cay, xoa, duyet_giua, dem_nut, chieu_cao, kiem_bst

FIELDNAMES = [
    'ma_ca', 'n', 'kieu_cay', 'tinh_huong', 'day_chen', 'khoa_xoa',
    'goc_truoc', 'goc_sau', 'cao_truoc', 'cao_sau', 'nut_truoc', 'nut_sau',
    'truong_hop', 'ke_vi', 'nut_xet_tim_khoa', 'nut_xet_tim_ke_vi',
    'buoc_trai_ke_vi', 'nut_xet_xoa_ban_sao', 'tong_luot_xet',
    'inorder_truoc', 'inorder_sau', 'hop_le',
]


def thu_tu_chia_giua(nums: list[int]) -> list[int]:
    """Chen trung vi truoc de co BST gan can doi; KHONG can bang sau chen."""
    if not nums:
        return []
    i = (len(nums) - 1) // 2
    return [nums[i], *thu_tu_chia_giua(nums[:i]), *thu_tu_chia_giua(nums[i + 1:])]


def lap_danh_sach_ca() -> list[tuple[str, list[int], int, str, str]]:
    cases = []
    for n in (5, 20, 50):
        values = list(range(1, n + 1))
        rng = random.Random(87000 + n)  # seed co dinh, tai lap duoc
        shuffle = values.copy()
        rng.shuffle(shuffle)
        for shape, order in [
            ('tang_dan', values),
            ('chia_giua', thu_tu_chia_giua(values)),
            ('tron_co_dinh', shuffle),
        ]:
            # Xoa goc / xoa max / khong ton tai: 3 phep xoa DOC LAP.
            # Moi ca tao lai cay ban dau de khong nham voi xoa lien tiep.
            for action, key in [('xoa_goc', order[0]), ('xoa_lon_nhat', n),
                                ('khong_ton_tai', n + 1)]:
                cases.append((f'N{n:02}_{shape}_{action}', order.copy(), key,
                              shape, action))
    cases.extend([
        ('KE_VI_SAU', [50, 30, 80, 70, 90, 60, 75, 55, 65], 50,
         'ca_dac_biet', 'ke_vi_sau'),
        ('KE_VI_CO_CON_PHAI', [50, 30, 80, 60, 90, 70, 65], 50,
         'ca_dac_biet', 'ke_vi_co_con_phai'),
    ])
    return cases


def chay_mot_ca(ma: str, values: list[int], target: int,
                 shape: str, action: str) -> dict:
    root = tao_cay(values)
    before = duyet_giua(root)
    height_before = chieu_cao(root)
    root_before = root.khoa if root else None
    stats = ThongKe()
    root = xoa(root, target, stats)
    after = duyet_giua(root)
    expected = sorted(set(values) - {target})
    exists = target in values
    passed = (after == expected and kiem_bst(root) and
              dem_nut(root) == len(values) - int(exists) and
              target not in after and
              (stats.truong_hop != 'khong_tim_thay') == exists)
    if not passed:
        raise AssertionError(f'{ma}: sai ket qua xoa, inorder, BST hoac thong ke truong hop')
    visits = (stats.so_sanh_tim + stats.so_nut_xet_ke_vi
              + stats.so_nut_xet_xoa_ban_sao)
    if visits > 3 * height_before:
        raise AssertionError(f'{ma}: tong luot xet nut vuot 3*h ({visits} > {3*height_before})')
    return dict(
        ma_ca=ma, n=len(values), kieu_cay=shape, tinh_huong=action,
        day_chen=' '.join(map(str, values)), khoa_xoa=target,
        goc_truoc=root_before, goc_sau=root.khoa if root else None,
        cao_truoc=height_before, cao_sau=chieu_cao(root),
        nut_truoc=len(values), nut_sau=dem_nut(root),
        truong_hop=stats.truong_hop, ke_vi=stats.ke_vi,
        nut_xet_tim_khoa=stats.so_sanh_tim,
        nut_xet_tim_ke_vi=stats.so_nut_xet_ke_vi,
        buoc_trai_ke_vi=stats.so_buoc_ke_vi,
        nut_xet_xoa_ban_sao=stats.so_nut_xet_xoa_ban_sao,
        tong_luot_xet=visits,
        inorder_truoc=' '.join(map(str, before)),
        inorder_sau=' '.join(map(str, after)), hop_le='PASS',
    )


def chay_tat_ca() -> list[dict]:
    return [chay_mot_ca(*case) for case in lap_danh_sach_ca()]


def xuat_csv(rows: list[dict], file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def bang_markdown(rows: list[dict]) -> str:
    short = [r for r in rows if r['kieu_cay'] in ('tang_dan', 'chia_giua')
             and r['tinh_huong'] in ('xoa_goc', 'xoa_lon_nhat')]
    lines = [
        '# DT087 — Ket qua thuc nghiem co the tai lap', '',
        'Du lieu tao boi `python -m experiments.benchmark` tu ma nguon BST hien tai.',
        'Moi ca dung **cay moi**; cac phep xoa trong bang **khong lien tiep**.',
        'Chieu cao: cay rong 0, la 1. Danh sach khoa 1..n; `chia_giua` chen trung vi truoc.',
        'Khong suy ra thoi gian mili giay tu so luot xet nut.', '',
        '| n | Kieu cay | Khoa xoa | h truoc | Loai xoa | Tim khoa | Xet ke vi | Di trai | Don ban sao | Tong luot xet |',
        '|---:|---|---:|---:|---|---:|---:|---:|---:|---:|',
    ]
    for r in short:
        lines.append('| ' + ' | '.join(str(r[k]) for k in [
            'n', 'kieu_cay', 'khoa_xoa', 'cao_truoc', 'truong_hop',
            'nut_xet_tim_khoa', 'nut_xet_tim_ke_vi', 'buoc_trai_ke_vi',
            'nut_xet_xoa_ban_sao', 'tong_luot_xet']) + ' |')
    lines.extend(['', '## Hai ca ke vi dac biet', '',
                  '| Ca | Khoa xoa | Ke vi | Tim khoa | Xet ke vi | Di trai | Don ban sao | Tong |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|'])
    for r in rows[-2:]:
        lines.append('| ' + ' | '.join(str(r[k]) for k in [
            'ma_ca','khoa_xoa','ke_vi','nut_xet_tim_khoa',
            'nut_xet_tim_ke_vi','buoc_trai_ke_vi',
            'nut_xet_xoa_ban_sao','tong_luot_xet']) + ' |')
    lines.extend(['', '## Quy uoc va nhan xet', '',
        '- `Tim khoa`: moi nut duoc xet tren duong di den khoa xoa, khong phai tong toan tu `<`, `>`, `==`.',
        '- `Xet ke vi`: moi nut duoc xet tren duong tim min cay con phai (bao gom min).',
        '- `Di trai`: so canh trai di qua, bang `xet ke vi - 1` khi co ke vi.',
        '- `Don ban sao`: so nut duoc xet trong lan xoa nut ke vi cu.',
        '- `Tong luot xet = tim khoa + xet ke vi + don ban sao` (khong cong di trai lan hai).',
        '- Khong tinh dung cay, duyet inorder, in chuoi, ve hinh, callback va Flask vao so lieu xoa.',
        '- BST lech co h=n; BST chen theo chia giua co h~log2(n). Thao tac xoa O(h), xau nhat O(n).',
        '- Day tang dan xoa goc chi xet 1 nut vi goc co mot con; de thay chi phi O(n) phai xoa khoa o cuoi.',
        '- CSV chua du day chen, goc, so nut, inorder truoc/sau, va trang thai PASS tung ca.',
        '', '## Cach tai lap', '', '```powershell', 'python -m experiments.benchmark',
        'python -m unittest test.test_thuc_nghiem -v', '```', ''])
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description='DT087: xuat thuc nghiem BST co the tai lap')
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).resolve().parent / 'ket_qua.csv')
    args = parser.parse_args()
    rows = chay_tat_ca()
    xuat_csv(rows, args.output)
    report = args.output.with_name('BANG_KET_QUA.md')
    report.write_text(bang_markdown(rows), encoding='utf-8')
    for r in rows:
        print(f"{r['ma_ca']:39} n={r['n']:2} h={r['cao_truoc']:2} "
              f"tim={r['nut_xet_tim_khoa']:2} ke_vi={r['nut_xet_tim_ke_vi']:2} "
              f"don={r['nut_xet_xoa_ban_sao']:2} "
              f"tong={r['tong_luot_xet']:2} {r['hop_le']}")
    print(f'KET QUA: {len(rows)}/{len(rows)} ca PASS')
    print(f'CSV: {args.output.resolve()}')
    print(f'BANG MARKDOWN: {report.resolve()}')


if __name__ == '__main__':
    main()
