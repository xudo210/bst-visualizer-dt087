"""Kiem tra giao dien tinh va lien ket voi API khong can Flask."""
from pathlib import Path
import re
import unittest

BASE = Path(__file__).resolve().parents[1]

class TestGiaoDienCuoi(unittest.TestCase):
    def test_assets_and_all_examples(self):
        html = (BASE / 'templates/index.html').read_text(encoding='utf-8')
        self.assertIn('06 · Xóa nhiều khóa', html)
        self.assertIn('07 · Kế vị nhiều bước', html)
        self.assertIn('08 · Kế vị có con phải', html)
        self.assertIn('id="downloadTrace"', html)
        self.assertTrue((BASE/'static/favicon.svg').exists())

    def test_frontend_element_ids_exist(self):
        html = (BASE / 'templates/index.html').read_text(encoding='utf-8')
        js = (BASE / 'static/app.js').read_text(encoding='utf-8')
        missing = [name for name in set(re.findall(r"\$\('([A-Za-z][A-Za-z0-9]*)'\)",js))
                   if f'id="{name}"' not in html]
        self.assertEqual(missing, [], f'ID JavaScript khong co trong HTML: {missing}')

    def test_api_and_stats_are_wired(self):
        js = (BASE / 'static/app.js').read_text(encoding='utf-8')
        self.assertIn("'/api/analyze-batch'", js)
        self.assertIn('frame.progress', js)
        self.assertIn('DT087_nhat_ky_xoa_BST.txt', js)

if __name__ == '__main__': unittest.main()
