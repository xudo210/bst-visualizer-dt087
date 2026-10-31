"""DT087 - Xoa nut BST, chon successor la khoa nho nhat cay con phai.
Quy uoc: khoa nguyen phan biet, cay rong cao 0, nut la cao 1.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Nut:
    khoa: int
    trai: Optional['Nut'] = None
    phai: Optional['Nut'] = None


@dataclass
class ThongKe:
    so_sanh_tim: int = 0
    so_buoc_ke_vi: int = 0
    truong_hop: str = 'khong_tim_thay'
    ke_vi: Optional[int] = None


def chen(g: Optional[Nut], x: int) -> Nut:
    """Chen khoa x vao BST. Khoa trung se bi tu choi."""
    if type(x) is not int:
        raise ValueError('Khoa phai la so nguyen.')
    if g is None:
        return Nut(x)
    if x < g.khoa:
        g.trai = chen(g.trai, x)
    elif x > g.khoa:
        g.phai = chen(g.phai, x)
    else:
        raise ValueError(f'Khoa trung: {x}')
    return g


def tao_cay(day: list[int]) -> Optional[Nut]:
    if len(day) > 100:
        raise ValueError('Chi nhan toi da 100 khoa.')
    if any(type(x) is not int for x in day) or len(day) != len(set(day)):
        raise ValueError('Day phai gom cac khoa nguyen phan biet.')
    g = None
    for x in day:
        g = chen(g, x)
    return g


def nho_nhat(g: Nut, tk: Optional[ThongKe] = None) -> Nut:
    """Tra ve nut trai nhat cua cay con khong rong, khong sua lien ket."""
    if g is None:
        raise ValueError('Khong tim min cua cay rong.')
    nut = g
    while nut.trai is not None:
        if tk is not None:
            tk.so_buoc_ke_vi += 1
        nut = nut.trai
    return nut


def xoa(g: Optional[Nut], x: int, tk: Optional[ThongKe] = None, ghi_buoc=None) -> Optional[Nut]:
    """Xoa khoa x, tra goc moi; callback ghi_buoc(event, **metadata) tuy chon.

    Ghi buoc duoc phat TRONG luc thuat toan chay, khong mo phong lai.
    Su kien 'thay_khoa' co the tao BST tam thoi chua hop le do khoa ke vi
    chua bi xoa; bat bien chi duoc kiem tra sau khi thuat toan hoan tat.
    """
    if type(x) is not int:
        raise ValueError('Khoa xoa phai la so nguyen.')
    if tk is None:
        tk = ThongKe()

    def phat(event, **metadata):
        if ghi_buoc is not None:
            ghi_buoc(event, **metadata)

    def _xoa(nut: Optional[Nut], khoa: int, dang_xoa_ke_vi: bool = False) -> Optional[Nut]:
        if nut is None:
            phat('khong_tim_thay', khoa=khoa, don_ke_vi=dang_xoa_ke_vi)
            return None
        if not dang_xoa_ke_vi:
            tk.so_sanh_tim += 1
        phat('tham_nut', khoa=nut.khoa, muc_tieu=khoa, don_ke_vi=dang_xoa_ke_vi)
        if khoa < nut.khoa:
            phat('re_trai', khoa=nut.khoa, muc_tieu=khoa, don_ke_vi=dang_xoa_ke_vi)
            nut.trai = _xoa(nut.trai, khoa, dang_xoa_ke_vi)
            phat('noi_nhanh_trai', khoa=nut.khoa, don_ke_vi=dang_xoa_ke_vi)
        elif khoa > nut.khoa:
            phat('re_phai', khoa=nut.khoa, muc_tieu=khoa, don_ke_vi=dang_xoa_ke_vi)
            nut.phai = _xoa(nut.phai, khoa, dang_xoa_ke_vi)
            phat('noi_nhanh_phai', khoa=nut.khoa, don_ke_vi=dang_xoa_ke_vi)
        else:
            if nut.trai is None and nut.phai is None:
                if not dang_xoa_ke_vi:
                    tk.truong_hop = 'la'
                phat('xoa_la', khoa=nut.khoa, don_ke_vi=dang_xoa_ke_vi)
                return None
            if nut.trai is None or nut.phai is None:
                if not dang_xoa_ke_vi:
                    tk.truong_hop = 'mot_con'
                con = nut.trai if nut.trai is not None else nut.phai
                phat('xoa_mot_con', khoa=nut.khoa, con=con.khoa, don_ke_vi=dang_xoa_ke_vi)
                return con
            if not dang_xoa_ke_vi:
                tk.truong_hop = 'hai_con'
            phat('xoa_hai_con', khoa=nut.khoa, don_ke_vi=dang_xoa_ke_vi)
            ke_vi = nut.phai
            phat('xet_ke_vi', khoa=ke_vi.khoa)
            while ke_vi.trai is not None:
                tk.so_buoc_ke_vi += 1
                ke_vi = ke_vi.trai
                phat('xet_ke_vi', khoa=ke_vi.khoa)
            if not dang_xoa_ke_vi:
                tk.ke_vi = ke_vi.khoa
            khoa_cu = nut.khoa
            nut.khoa = ke_vi.khoa
            phat('thay_khoa', khoa_cu=khoa_cu, khoa_moi=ke_vi.khoa)
            nut.phai = _xoa(nut.phai, ke_vi.khoa, True)
            phat('noi_nhanh_phai', khoa=nut.khoa, don_ke_vi=True)
        return nut

    phat('bat_dau', khoa=x)
    ket_qua = _xoa(g, x)
    phat('hoan_tat', khoa=x, goc_moi=ket_qua.khoa if ket_qua else None)
    return ket_qua


def duyet_giua(g: Optional[Nut]) -> list[int]:
    if g is None:
        return []
    return duyet_giua(g.trai) + [g.khoa] + duyet_giua(g.phai)


def dem_nut(g: Optional[Nut]) -> int:
    if g is None:
        return 0
    return 1 + dem_nut(g.trai) + dem_nut(g.phai)


def chieu_cao(g: Optional[Nut]) -> int:
    if g is None:
        return 0
    return 1 + max(chieu_cao(g.trai), chieu_cao(g.phai))


def kiem_bst(g: Optional[Nut], can_duoi=None, can_tren=None) -> bool:
    if g is None:
        return True
    if can_duoi is not None and g.khoa <= can_duoi:
        return False
    if can_tren is not None and g.khoa >= can_tren:
        return False
    return kiem_bst(g.trai, can_duoi, g.khoa) and kiem_bst(g.phai, g.khoa, can_tren)


def ve_cay_chu(g: Optional[Nut], muc: int = 0, nhan: str = 'ROOT') -> str:
    if g is None:
        return ('    ' * muc) + f'{nhan}: rong\n'
    kq = ('    ' * muc) + f'{nhan}: {g.khoa}\n'
    if g.trai is not None or g.phai is not None:
        kq += ve_cay_chu(g.trai, muc + 1, 'L')
        kq += ve_cay_chu(g.phai, muc + 1, 'R')
    return kq
