"""DT087: test dem chi phi tim khoa, ke vi va don ban sao theo su kien thuc."""
import unittest
from web_trace import analyze, analyze_batch
from src.bst import ThongKe, tao_cay, xoa


class TestThongKe(unittest.TestCase):
    def check_progress(self, data):
        frames = data['frames']
        keys = ['search_nodes', 'successor_visits', 'successor_steps', 'cleanup_visits', 'total_visits']
        self.assertEqual(frames[0]['progress'], dict.fromkeys(keys, 0))
        for before, after in zip(frames, frames[1:]):
            for key in keys:
                self.assertLessEqual(before['progress'][key], after['progress'][key])
        self.assertEqual(frames[-1]['progress'], {key: data['stats'][key] for key in keys})
        self.assertEqual(data['stats']['total_visits'], (
            data['stats']['search_nodes'] + data['stats']['successor_visits']
            + data['stats']['cleanup_visits']))
        if data['stats']['case'] == 'hai_con':
            self.assertEqual(data['stats']['successor_visits'], data['stats']['successor_steps'] + 1)
        else:
            self.assertEqual(data['stats']['successor_visits'], 0)
            self.assertEqual(data['stats']['successor_steps'], 0)
            self.assertEqual(data['stats']['cleanup_visits'], 0)
        self.assertEqual(data['stats']['comparisons'], data['stats']['search_nodes'])

    def test_two_children(self):
        data = analyze([5,3,7,2,4,6,8],5)
        self.assertEqual([data['stats'][k] for k in
                          ('search_nodes','successor_visits','successor_steps','cleanup_visits','total_visits')],
                          [1,2,1,2,5])
        self.check_progress(data)

    def test_deep_successor(self):
        data = analyze([50,30,80,70,90,60,75,55,65],50)
        self.assertEqual(data['stats']['successor'],55)
        self.assertEqual([data['stats'][k] for k in
                          ('search_nodes','successor_visits','successor_steps','cleanup_visits','total_visits')],
                          [1,4,3,4,9])
        self.assertEqual(data['after']['root'],55)
        self.check_progress(data)

    def test_successor_with_right_child(self):
        data = analyze([50,30,80,60,90,70,65],50)
        self.assertEqual(data['stats']['successor'],60)
        self.assertEqual(data['after']['inorder'],[30,60,65,70,80,90])
        self.assertEqual([data['stats'][k] for k in
                          ('search_nodes','successor_visits','successor_steps','cleanup_visits','total_visits')],
                          [1,2,1,2,5])
        self.check_progress(data)

    def test_missing(self):
        data = analyze([5,3,7],99)
        self.assertEqual(data['stats']['search_nodes'],2)
        self.assertEqual(data['stats']['total_visits'],2)
        self.check_progress(data)

    def test_leaf_and_one_child(self):
        for values, target in [([2,1,3],1),([4,2,6,1],2)]:
            data = analyze(values,target)
            self.assertEqual(data['stats']['search_nodes'],2)
            self.check_progress(data)

    def test_empty(self):
        data = analyze([],1)
        self.assertEqual(data['stats']['total_visits'],0)
        self.check_progress(data)

    def test_batch_counters_reset(self):
        result = analyze_batch([5,3,7,2,4,6,8],[5,3,99,6])
        for item in result['runs']:
            self.check_progress(item)
        self.assertEqual([run['stats']['search_nodes'] for run in result['runs']], [1,2,3,1])

    def test_event_counts_match_trace(self):
        for values, target in [
            ([5,3,7,2,4,6,8],5),
            ([50,30,80,70,90,60,75,55,65],50),
            ([50,30,80,60,90,70,65],50),
            ([3,2,4],99),
        ]:
            data = analyze(values, target)
            events = data['frames']
            count_search = sum(f['event'] == 'tham_nut' and not f['metadata'].get('don_ke_vi')
                               for f in events)
            count_cleanup = sum(f['event'] == 'tham_nut' and f['metadata'].get('don_ke_vi')
                                for f in events)
            count_successor = sum(f['event'] == 'xet_ke_vi' for f in events)
            s = data['stats']
            self.assertEqual(s['search_nodes'],count_search)
            self.assertEqual(s['cleanup_visits'],count_cleanup)
            self.assertEqual(s['successor_visits'],count_successor)

    def test_core_api_stats(self):
        stats = ThongKe()
        root = tao_cay([5,3,7,2,4,6,8])
        root = xoa(root,5,stats)
        self.assertEqual((stats.so_sanh_tim,stats.so_nut_xet_ke_vi,stats.so_buoc_ke_vi,
                          stats.so_nut_xet_xoa_ban_sao),(1,2,1,2))


try:
    from web_app import app
except ImportError:
    app = None


@unittest.skipIf(app is None,'Chua cai Flask: bo qua test HTTP, test logic van chay')
class TestThongKeAPI(unittest.TestCase):
    def test_api_current_and_legacy(self):
        client = app.test_client()
        for endpoint, payload in [
            ('/api/analyze',{'values':[5,3,7,2,4,6,8],'target':5}),
            ('/api/analyze-batch',{'values':[5,3,7,2,4,6,8],'targets':[5]})
        ]:
            response = client.post(endpoint,json=payload)
            self.assertEqual(response.status_code,200)
            body = response.get_json()
            result = body['runs'][0] if endpoint.endswith('batch') else body
            self.assertEqual(result['stats']['comparisons'],1)
            self.assertEqual(result['stats']['successor_visits'],2)
            self.assertEqual(result['frames'][-1]['progress']['total_visits'],5)

if __name__=='__main__': unittest.main()
