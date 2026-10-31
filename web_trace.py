"""Snapshot ghi truc tiep tu callback cua thuat toan BST goc."""
from src.bst import tao_cay, xoa, ThongKe, duyet_giua, chieu_cao, dem_nut, kiem_bst


def serialize(root):
    if root is None:
        return None
    return {'key': root.khoa, 'left': serialize(root.trai), 'right': serialize(root.phai)}


def analyze(values, target):
    root = tao_cay(values)
    before = {'tree': serialize(root), 'inorder': duyet_giua(root),
              'count': dem_nut(root), 'height': chieu_cao(root)}
    frames = []
    messages = {
        'bat_dau': 'Bắt đầu xóa khóa {khoa}.',
        'tham_nut': 'Đang so sánh khóa {muc_tieu} với nút {khoa}.',
        're_trai': '{muc_tieu} < {khoa}: duyệt cây con trái.',
        're_phai': '{muc_tieu} > {khoa}: duyệt cây con phải.',
        'khong_tim_thay': 'Không tìm thấy khóa {khoa} trên nhánh đang xét.',
        'xoa_la': 'Xóa nút lá {khoa}, trả về None.',
        'xoa_mot_con': 'Xóa nút {khoa}, trả về nút con {con}.',
        'xoa_hai_con': 'Nút {khoa} có hai con: tìm nút kế vị trong cây con phải.',
        'xet_ke_vi': 'Đang xét nút {khoa} để tìm khóa kế vị nhỏ nhất.',
        'thay_khoa': 'Thay khóa {khoa_cu} bằng kế vị {khoa_moi}; chuẩn bị xóa bản sao.',
        'noi_nhanh_trai': 'Đã cập nhật liên kết nhánh trái của nút {khoa}.',
        'noi_nhanh_phai': 'Đã cập nhật liên kết nhánh phải của nút {khoa}.',
        'hoan_tat': 'Hoàn tất thao tác xóa khóa {khoa}.',
    }
    def ghi_buoc(event, **meta):
        # Goc moi chi duoc cap nhat khi ham xoa tra ve.
        current = result_holder[0] if event == 'hoan_tat' else root
        if event == 'hoan_tat':
            current = result_holder[0]
        active = meta.get('khoa') if event not in ('bat_dau','hoan_tat','thay_khoa') else None
        frames.append({'tree': serialize(current), 'active': active,
                       'successor': meta.get('khoa') if event == 'xet_ke_vi' else meta.get('khoa_moi') if event == 'thay_khoa' else None,
                       'message': messages[event].format(**meta), 'kind': event,
                       'event': event, 'metadata': meta})
    # Ham xoa phat 'hoan_tat' truoc khi tra ve. Goc thay doi duoc chot
    # bang snapshot cuoi ben duoi, thay vi suy doan con tro goc moi.
    result_holder = [root]
    tk = ThongKe()
    result = xoa(root, target, tk, ghi_buoc=ghi_buoc)
    result_holder[0] = result
    assert kiem_bst(result), 'Cây sau xóa không còn là BST.'
    after = {'tree': serialize(result), 'inorder': duyet_giua(result),
             'count': dem_nut(result), 'height': chieu_cao(result),
             'root': result.khoa if result else None, 'valid': True}
    frames.append({'tree': serialize(result), 'active': None, 'successor': None,
                   'message': 'Đã hoàn tất cập nhật gốc và tất cả liên kết; cây BST hợp lệ.',
                   'kind': 'done', 'event': 'ket_qua', 'metadata': {}})
    return {'before': before, 'after': after, 'frames': frames,
            'stats': {'case': tk.truong_hop, 'successor': tk.ke_vi,
                      'comparisons': tk.so_sanh_tim, 'successor_steps': tk.so_buoc_ke_vi}}
