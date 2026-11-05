import unittest
try:
    from web_app import app
except ModuleNotFoundError as exc:
    if exc.name != 'flask':
        raise
    app = None

@unittest.skipIf(app is None, "Chưa cài Flask: bỏ qua kiểm thử HTTP; khi cài sẽ chạy đầy đủ")
class TestWeb(unittest.TestCase):
    def setUp(self): self.client=app.test_client()
    def analyze(self, values, target): return self.client.post('/api/analyze',json={'values':values,'target':target})
    def test_home(self): self.assertEqual(self.client.get('/').status_code,200)
    def test_two_children(self):
        d=self.analyze([5,3,7,2,4,6,8],5).get_json()
        self.assertEqual(d['after']['inorder'],[2,3,4,6,7,8]);self.assertEqual(d['after']['root'],6)
        self.assertEqual(d['stats']['case'],'hai_con');self.assertTrue(d['after']['valid'])
    def test_one_child(self):
        d=self.analyze([4,2,6,1],2).get_json()
        self.assertEqual(d['after']['inorder'],[1,4,6]);self.assertEqual(d['stats']['case'],'mot_con')
    def test_leaf(self): self.assertEqual(self.analyze([2,1,3],1).get_json()['stats']['case'],'la')
    def test_empty(self): self.assertEqual(self.analyze([],1).get_json()['after']['count'],0)
    def test_missing(self): self.assertEqual(self.analyze([2,1,3],9).get_json()['stats']['case'],'khong_tim_thay')
    def test_duplicate(self): self.assertEqual(self.analyze([3,3],3).status_code,400)
    def test_invalid(self): self.assertEqual(self.analyze([2,'3'],2).status_code,400)
    def test_limit(self): self.assertEqual(self.analyze(list(range(101)),0).status_code,400)
    def test_successor(self): self.assertEqual(self.analyze([5,3,8,7,9],5).get_json()['stats']['successor'],7)

if __name__=='__main__': unittest.main()
