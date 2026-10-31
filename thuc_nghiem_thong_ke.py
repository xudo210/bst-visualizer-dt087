"""Bang thuc nghiem DT087: dem luot xet nut tai 3 pha cua phep xoa."""
from web_trace import analyze

CA = [
    ('VD01-hai-con', [5, 3, 7, 2, 4, 6, 8], 5),
    ('VD02-mot-con', [4, 2, 6, 1], 2),
    ('Khong-ton-tai', [5, 3, 7], 99),
    ('Ke-vi-sau', [50, 30, 80, 70, 90, 60, 75, 55, 65], 50),
    ('Ke-vi-co-con-phai', [50, 30, 80, 60, 90, 70, 65], 50),
]


def main():
    columns = ('Ca', 'n', 'xoa', 'h', 'tim', 'kv_nut', 'kv_trai', 'xoa_ban_sao', 'tong')
    print(' | '.join(f'{v:>14}' for v in columns))
    print('-' * 145)
    for name, values, target in CA:
        data = analyze(values, target)
        s = data['stats']
        row = (name, len(values), target, data['before']['height'], s['search_nodes'],
               s['successor_visits'], s['successor_steps'], s['cleanup_visits'], s['total_visits'])
        print(' | '.join(f'{str(v):>14}' for v in row))
    print('\nQUY UOC: tim = so nut xet khi tim khoa; kv_nut = so nut xet de tim ke vi;')
    print('kv_trai = so canh trai da di; xoa_ban_sao = so nut xet khi xoa nut ke vi cu.')
    print('tong = tim + kv_nut + xoa_ban_sao; chua tinh dung cay, SVG, callbacks, inorder.')
    print('Chi phi thuat toan xoa la O(h); khong lay tong luot xet lam thoi gian chay.')


if __name__ == '__main__':
    main()
