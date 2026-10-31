"""Kiem tra cac cai tien thuat toan BST khong lam thay doi ket qua / trace.

Chay: python -m unittest test.test_cai_tien_bst -v
"""
import unittest

from src.bst import Nut, ThongKe, chen, tao_cay, nho_nhat, xoa, duyet_giua, kiem_bst
from web_trace import analyze, analyze_batch


class TestCaiTienBST(unittest.TestCase):
    def test_duyet_giua_cay_rong(self):
        self.assertEqual(duyet_giua(None), [])

    def test_duyet_giua_cay_can_bang(self):
        g = tao_cay([5, 3, 7, 2, 4, 6, 8])
        self.assertEqual(duyet_giua(g), [2, 3, 4, 5, 6, 7, 8])
        self.assertTrue(kiem_bst(g))

    def test_duyet_giua_cay_suy_bien_100_khoa(self):
        g = tao_cay(list(range(1, 101)))
        self.assertEqual(duyet_giua(g), list(range(1, 101)))
        self.assertEqual(duyet_giua(g), list(range(1, 101)))

    def test_duyet_giua_khong_chinh_sua_cay(self):
        g = tao_cay([50, 30, 80, 60, 90, 70, 65])
        before = (g.khoa, g.phai.trai.khoa, g.phai.trai.phai.khoa)
        self.assertEqual(duyet_giua(g), [30, 50, 60, 65, 70, 80, 90])
        self.assertEqual((g.khoa, g.phai.trai.khoa, g.phai.trai.phai.khoa), before)

    def test_nho_nhat_thong_ke_khong_sua_cay(self):
        g = tao_cay([50, 30, 80, 70, 90, 60, 75, 55, 65])
        tk = ThongKe()
        nodes = []
        successor = nho_nhat(g.phai, tk, ghi_xet=lambda node: nodes.append(node.khoa))
        self.assertEqual(successor.khoa, 55)
        self.assertEqual(nodes, [80, 70, 60, 55])
        self.assertEqual((tk.so_nut_xet_ke_vi, tk.so_buoc_ke_vi), (4, 3))
        self.assertEqual(duyet_giua(g), [30, 50, 55, 60, 65, 70, 75, 80, 90])

    def test_nho_nhat_mot_nut(self):
        tk = ThongKe()
        g = Nut(9, phai=Nut(11))
        self.assertIs(nho_nhat(g, tk), g)
        self.assertEqual((tk.so_nut_xet_ke_vi, tk.so_buoc_ke_vi), (1, 0))

    def test_nho_nhat_cay_rong(self):
        with self.assertRaises(ValueError):
            nho_nhat(None)

    def test_trace_ke_vi_sau_giu_nguyen_bo_dem(self):
        d = analyze([50, 30, 80, 70, 90, 60, 75, 55, 65], 50)
        s = d['stats']
        self.assertEqual((s['successor'], s['search_nodes'], s['successor_visits'],
                          s['successor_steps'], s['cleanup_visits'], s['total_visits']),
                          (55, 1, 4, 3, 4, 9))
        self.assertEqual(d['after']['root'], 55)
        self.assertEqual([f['metadata']['khoa'] for f in d['frames'] if f['event'] == 'xet_ke_vi'],
                         [80, 70, 60, 55])

    def test_ke_vi_co_con_phai_khong_mat_nut(self):
        d = analyze([50, 30, 80, 60, 90, 70, 65], 50)
        self.assertEqual(d['after']['inorder'], [30, 60, 65, 70, 80, 90])
        self.assertTrue(d['after']['valid'])

    def test_xoa_nhieu_khoa_giu_nguyen_ket_qua(self):
        d = analyze_batch([5, 3, 7, 2, 4, 6, 8], [5, 3, 99, 6])
        self.assertEqual([r['after']['root'] for r in d['runs']], [6, 6, 6, 7])
        self.assertEqual([r['after']['inorder'] for r in d['runs']], [
            [2, 3, 4, 6, 7, 8], [2, 4, 6, 7, 8], [2, 4, 6, 7, 8], [2, 4, 7, 8]
        ])


if __name__ == '__main__':
    unittest.main()
