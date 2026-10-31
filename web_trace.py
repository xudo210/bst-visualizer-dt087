"""Ghi snapshot truc tiep tu callback xoa BST goc, ho tro xoa 1/nhieu khoa."""
from src.bst import tao_cay, xoa, ThongKe, duyet_giua, chieu_cao, dem_nut, kiem_bst


def serialize(root):
    if root is None:
        return None
    return {'key': root.khoa, 'left': serialize(root.trai), 'right': serialize(root.phai)}


def _summary(root, final=False):
    result = {'tree': serialize(root), 'inorder': duyet_giua(root),
              'count': dem_nut(root), 'height': chieu_cao(root)}
    if final:
        result.update(root=root.khoa if root else None, valid=kiem_bst(root))
    return result


def analyze_one(root, target):
    """Xoa mot khoa tren cay hien tai; tra ve (goc_moi, ket_qua).

    Cac snapshot giua buoc co the chua la BST hop le; ket qua cuoi luon kiem tra.
    """
    before = _summary(root)
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
        # Khi callback dang chay, root co the chua la goc moi sau xoa.
        # Ket qua chinh xac duoc ghi lai trong frame 'ket_qua' sau khi xoa tra ve.
        active = meta.get('khoa') if event not in ('bat_dau', 'hoan_tat', 'thay_khoa') else None
        frames.append({
            'tree': serialize(root), 'active': active,
            'successor': meta.get('khoa') if event == 'xet_ke_vi'
                         else meta.get('khoa_moi') if event == 'thay_khoa' else None,
            'message': messages[event].format(**meta),
            'kind': event, 'event': event, 'metadata': meta,
        })

    stats = ThongKe()
    new_root = xoa(root, target, stats, ghi_buoc=ghi_buoc)
    if not kiem_bst(new_root):
        raise ValueError('Cây sau xóa không còn là BST.')
    after = _summary(new_root, final=True)
    if stats.truong_hop == 'khong_tim_thay':
        final_message = f'Không tìm thấy khóa {target}; cây giữ nguyên và vẫn là BST hợp lệ.'
    else:
        final_message = f'Đã xóa khóa {target}, cập nhật gốc và liên kết; cây BST hợp lệ.'
    frames.append({'tree': serialize(new_root), 'active': None, 'successor': None,
                   'message': final_message, 'kind': 'done', 'event': 'ket_qua',
                   'metadata': {}})
    return new_root, {
        'target': target, 'before': before, 'after': after, 'frames': frames,
        'stats': {'case': stats.truong_hop, 'successor': stats.ke_vi,
                  'comparisons': stats.so_sanh_tim,
                  'successor_steps': stats.so_buoc_ke_vi}
    }


def analyze(values, target):
    """API cu: giu nguyen dinh dang tra ve de khong anh huong cac test cu."""
    _, result = analyze_one(tao_cay(values), target)
    return result


def analyze_batch(values, targets):
    """Chen mot lan, xoa lan luot tren CHINH cay da cap nhat."""
    root = tao_cay(values)
    runs = []
    for i, target in enumerate(targets, start=1):
        root, result = analyze_one(root, target)
        result['index'] = i
        runs.append(result)
    return {'runs': runs, 'total': len(runs)}
