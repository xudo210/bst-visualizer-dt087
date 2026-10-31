"""Bo 12 ca doc lap va 3 quy mo. Chay tu thu muc du an: python -m test.runtests"""
from src.bst import ThongKe, tao_cay, xoa, duyet_giua, dem_nut, chieu_cao, kiem_bst, nho_nhat

# Test data and expected are fixed independently from the algorithm under test.
CA_KIEM = [
    ('VD01', [5,3,7,2,4,6,8], 5, [2,3,4,6,7,8], 6, 'hai_con'),
    ('VD02', [4,2,6,1], 2, [1,4,6], 4, 'mot_con'),
    ('BIEN01', [], 1, [], None, 'khong_tim_thay'),
    ('TK01', [2,1,3], 1, [2,3], 2, 'la'),
    ('TK02', [2,1], 2, [1], 1, 'mot_con'),
    ('KT09', [2,1,3], 2, [1,3], 3, 'hai_con'),
    ('KT10', [2,1,3], 9, [1,2,3], 2, 'khong_tim_thay'),
    ('BIEN02', [7], 7, [], None, 'la'),
    ('BIEN03', [5,3,8,7,9], 5, [3,7,8,9], 7, 'hai_con'),
    ('KT11', [10,5,20,15,30,12,17], 10, [5,12,15,17,20,30], 12, 'hai_con'),
    ('KT12', [1,2,3,4,5], 1, [2,3,4,5], 2, 'mot_con'),
]

def main():
    dat = 0
    for ma, day, khoa, expected, goc_expected, loai in CA_KIEM:
        g = tao_cay(day)
        tk = ThongKe()
        g = xoa(g, khoa, tk)
        actual = duyet_giua(g)
        goc = g.khoa if g else None
        ok = (actual == expected and goc == goc_expected
              and tk.truong_hop == loai and kiem_bst(g)
              and dem_nut(g) == len(expected))
        print(f'{ma:7} input={day} xoa={khoa} expected={expected} actual={actual} '
              f'goc={goc} case={tk.truong_hop} => {"PASS" if ok else "FAIL"}')
        if not ok:
            raise AssertionError(ma)
        dat += 1

    # LOI01: validator rejects duplicate keys
    try:
        tao_cay([3,3])
    except ValueError:
        print('LOI01   input=[3,3] expected=ValueError actual=ValueError => PASS')
        dat += 1
    else:
        raise AssertionError('LOI01')

    # Additional check: min of the right subtree of example 1
    g = tao_cay([5,3,7,2,4,6,8])
    assert nho_nhat(g.phai).khoa == 6
    print('DOC_LAP successor cua cay phai VD01 = 6 => PASS')
    print(f'TONG KET: {dat}/12 ca doc lap PASS')
    print('\nKHAO SAT QUY MO (day tang dan vs day can bang khi chen):')
    for n in [5,20,50]:
        tang = list(range(1,n+1))
        can_bang = []
        def them_giua(a):
            if not a: return
            i=(len(a)-1)//2
            can_bang.append(a[i])
            them_giua(a[:i]); them_giua(a[i+1:])
        them_giua(tang)
        for nhan, day in [('tang_dan',tang),('chia_giua',can_bang)]:
            g = tao_cay(day)
            h = chieu_cao(g)
            tk=ThongKe()
            g=xoa(g,n,tk)
            assert kiem_bst(g) and dem_nut(g)==n-1
            print(f'n={n:2} order={nhan:9} h_truoc={h:2} so_sanh_tim={tk.so_sanh_tim:2} '
                  f'buoc_ke_vi={tk.so_buoc_ke_vi:2} h_sau={chieu_cao(g):2}')
if __name__ == '__main__':
    main()
