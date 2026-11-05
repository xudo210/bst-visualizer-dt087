"""Kiem tra pipeline thuc nghiem, doc lap voi ket qua ghi san."""
import csv
import random
import tempfile
import unittest
from pathlib import Path

from experiments.benchmark import (lap_danh_sach_ca, chay_tat_ca,
                                   thu_tu_chia_giua, xuat_csv)
from src.bst import ThongKe, chieu_cao, dem_nut, duyet_giua, kiem_bst, tao_cay, xoa


class TestThucNghiem(unittest.TestCase):
    def test_29_ca_lap_lai_duoc(self):
        rows = chay_tat_ca()
        self.assertEqual(len(rows), 29)
        self.assertEqual(len({r['ma_ca'] for r in rows}), len(rows))
        self.assertTrue(all(r['hop_le'] == 'PASS' for r in rows))
        self.assertEqual(chay_tat_ca(), rows)

    def test_cay_tang_dan_va_chia_giua(self):
        for n in (5, 20, 50):
            nums = list(range(1, n+1))
            self.assertEqual(chieu_cao(tao_cay(nums)), n)
            self.assertLessEqual(chieu_cao(tao_cay(thu_tu_chia_giua(nums))),
                                 (n-1).bit_length())

    def test_tham_nut_khong_qua_ba_lan_chieu_cao(self):
        for row in chay_tat_ca():
            self.assertLessEqual(row['tong_luot_xet'], 3 * row['cao_truoc'])
            self.assertEqual(row['tong_luot_xet'], row['nut_xet_tim_khoa']
                             + row['nut_xet_tim_ke_vi'] + row['nut_xet_xoa_ban_sao'])
            if row['ke_vi'] is not None:
                self.assertEqual(row['nut_xet_tim_ke_vi'], row['buoc_trai_ke_vi'] + 1)

    def test_thu_tu_co_dinh_va_csv_roundtrip(self):
        self.assertEqual(lap_danh_sach_ca(), lap_danh_sach_ca())
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'results.csv'
            xuat_csv(chay_tat_ca(), path)
            first = path.read_bytes()
            with path.open(encoding='utf-8-sig', newline='') as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 29)
            self.assertEqual(rows[0]['hop_le'], 'PASS')
            xuat_csv(chay_tat_ca(), path)
            self.assertEqual(path.read_bytes(), first)

    def test_kiem_bat_bien_moi_buoc_xoa_ngau_nhien(self):
        rng = random.Random(87185)
        for _ in range(35):
            values = rng.sample(range(-1000, 1001), rng.randrange(0, 101))
            tree = tao_cay(values)
            reference = set(values)
            keys = list(values) + [10001, 10002]
            rng.shuffle(keys)
            for key in keys:
                old_count = len(reference)
                stats = ThongKe()
                tree = xoa(tree, key, stats)
                reference.discard(key)
                self.assertEqual(duyet_giua(tree), sorted(reference))
                self.assertEqual(dem_nut(tree), len(reference))
                self.assertEqual(old_count - len(reference), int(key in values))
                self.assertTrue(kiem_bst(tree))


if __name__ == '__main__':
    unittest.main()
