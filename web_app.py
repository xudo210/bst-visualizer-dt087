"""Chay: python web_app.py | mo http://127.0.0.1:5000"""
from flask import Flask, jsonify, render_template, request
from web_trace import analyze, analyze_batch

app = Flask(__name__)
app.json.ensure_ascii = False


def valid_values(values):
    return (isinstance(values, list) and len(values) <= 100
            and all(type(v) is int for v in values)
            and len(values) == len(set(values)))


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/analyze')
def api_analyze():
    """Endpoint cu, van nhan dung 1 target."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Dữ liệu JSON không hợp lệ.'), 400
    values, target = data.get('values'), data.get('target')
    if not isinstance(values, list) or len(values) > 100 or any(type(v) is not int for v in values):
        return jsonify(error='Dãy chèn phải là danh sách tối đa 100 số nguyên.'), 400
    if len(values) != len(set(values)):
        return jsonify(error='Dãy chèn chứa khóa trùng nhau.'), 400
    if type(target) is not int:
        return jsonify(error='Khóa cần xóa phải là số nguyên.'), 400
    try:
        return jsonify(analyze(values, target))
    except (ValueError, RecursionError) as error:
        return jsonify(error=str(error)), 400


@app.post('/api/analyze-batch')
def api_analyze_batch():
    """Endpoint moi: danh sach targets duoc xoa lien tiep tren 1 cay."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Dữ liệu JSON không hợp lệ.'), 400
    values, targets = data.get('values'), data.get('targets')
    if not isinstance(values, list) or len(values) > 100 or any(type(v) is not int for v in values):
        return jsonify(error='Dãy chèn phải là danh sách tối đa 100 số nguyên.'), 400
    if len(values) != len(set(values)):
        return jsonify(error='Dãy chèn chứa khóa trùng nhau.'), 400
    if not isinstance(targets, list) or not 1 <= len(targets) <= 20 or any(type(t) is not int for t in targets):
        return jsonify(error='Nhập từ 1 đến 20 khóa xóa nguyên, cách nhau bởi dấu phẩy.'), 400
    try:
        return jsonify(analyze_batch(values, targets))
    except (ValueError, RecursionError) as error:
        return jsonify(error=str(error)), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
