"""Kiem thu mo rong: xoa nhieu khoa lien tiep tren CHINH cay BST."""
import unittest
from web_trace import analyze_batch


class TestBatchTree(unittest.TestCase):
    def test_four_deletes_in_order(self):
        result = analyze_batch([5, 3, 7, 2, 4, 6, 8], [5, 3, 99, 6])
        runs = result['runs']
        self.assertEqual(len(runs), 4)
        self.assertEqual([r['after']['inorder'] for r in runs], [
            [2, 3, 4, 6, 7, 8],
            [2, 4, 6, 7, 8],
            [2, 4, 6, 7, 8],
            [2, 4, 7, 8],
        ])
        self.assertEqual([r['after']['root'] for r in runs], [6, 6, 6, 7])
        self.assertEqual(runs[1]['before']['tree'], runs[0]['after']['tree'])
        self.assertEqual(runs[2]['before']['tree'], runs[1]['after']['tree'])
        self.assertEqual(runs[3]['before']['tree'], runs[2]['after']['tree'])
        self.assertTrue(all(r['after']['valid'] for r in runs))
        self.assertEqual(runs[2]['stats']['case'], 'khong_tim_thay')

    def test_repeat_same_delete(self):
        runs = analyze_batch([2, 1, 3], [2, 2])['runs']
        self.assertEqual(runs[0]['after']['inorder'], [1, 3])
        self.assertEqual(runs[1]['after']['inorder'], [1, 3])
        self.assertEqual(runs[1]['stats']['case'], 'khong_tim_thay')

    def test_empty_tree(self):
        runs = analyze_batch([], [1, 1])['runs']
        self.assertEqual([r['after']['count'] for r in runs], [0, 0])

    def test_successor_right_child_retained(self):
        runs = analyze_batch([50, 30, 80, 60, 90, 70, 65], [50])['runs']
        self.assertEqual(runs[0]['after']['inorder'], [30, 60, 65, 70, 80, 90])
        self.assertEqual(runs[0]['after']['root'], 60)


try:
    from web_app import app
except ImportError:
    app = None


@unittest.skipIf(app is None, 'Chua cai Flask; bo qua kiem thu API, logic BST van duoc kiem tra')
class TestBatchAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_batch_endpoint(self):
        response = self.client.post('/api/analyze-batch', json={
            'values': [5, 3, 7, 2, 4, 6, 8], 'targets': [5, 3, 99, 6]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['runs'][-1]['after']['inorder'], [2, 4, 7, 8])

    def test_reject_empty_targets(self):
        self.assertEqual(self.client.post('/api/analyze-batch', json={
            'values': [1], 'targets': []}).status_code, 400)

    def test_reject_non_integer(self):
        self.assertEqual(self.client.post('/api/analyze-batch', json={
            'values': [1], 'targets': [True]}).status_code, 400)

    def test_reject_too_many(self):
        self.assertEqual(self.client.post('/api/analyze-batch', json={
            'values': [1], 'targets': [1] * 21}).status_code, 400)

    def test_old_endpoint_unchanged(self):
        response = self.client.post('/api/analyze', json={
            'values': [4, 2, 6, 1], 'target': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['after']['inorder'], [1, 4, 6])


if __name__ == '__main__':
    unittest.main()
