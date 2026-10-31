"""Kiem thu mo rong co the lap lai: python -m unittest discover -s test -p 'test_*.py'."""
import random
import unittest
from src.bst import tao_cay, xoa, duyet_giua, kiem_bst, ThongKe
from web_trace import analyze

class TestNangCao(unittest.TestCase):
    def test_successor_has_right_child(self):
        d = analyze([50, 30, 80, 60, 90, 70, 65], 50)
        self.assertEqual(d['stats']['successor'], 60)
        self.assertEqual(d['after']['inorder'], [30, 60, 65, 70, 80, 90])
        self.assertTrue(d['after']['valid'])

    def test_trace_real_events(self):
        d = analyze([5, 3, 7, 2, 4, 6, 8], 5)
        events = [f['event'] for f in d['frames']]
        self.assertIn('thay_khoa', events)
        self.assertIn('xoa_la', events)
        self.assertIn('noi_nhanh_phai', events)
        self.assertEqual(d['frames'][-1]['tree'], d['after']['tree'])
        self.assertEqual(d['frames'][0]['tree'], d['before']['tree'])

    def test_delete_root_to_empty(self):
        self.assertEqual(analyze([9], 9)['after']['inorder'], [])

    def test_random_sequential_deletions(self):
        rng = random.Random(20261031)
        for _ in range(150):
            values = rng.sample(range(-1000, 1001), rng.randint(0, 65))
            root = tao_cay(values)
            expected = set(values)
            for key in rng.sample(values, len(values)) + [2002]:
                stats = ThongKe()
                root = xoa(root, key, stats)
                expected.discard(key)
                self.assertEqual(duyet_giua(root), sorted(expected))
                self.assertTrue(kiem_bst(root))

    def test_random_trace_matches_result(self):
        rng = random.Random(87)
        for _ in range(100):
            values = rng.sample(range(-300, 301), rng.randint(0, 35))
            target = rng.choice(values) if values and rng.random() < .8 else 999
            d = analyze(values, target)
            self.assertEqual(d['after']['inorder'], sorted(set(values) - {target}))
            self.assertEqual(d['frames'][-1]['tree'], d['after']['tree'])

if __name__ == '__main__':
    unittest.main()
