"""Chay: python web_app.py | mo http://127.0.0.1:5000"""
from flask import Flask, jsonify, render_template, request
from web_trace import analyze

app = Flask(__name__)
app.json.ensure_ascii = False

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/api/analyze')
def api_analyze():
    data = request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify(error='Dữ liệu JSON không hợp lệ.'),400
    values, target = data.get('values'), data.get('target')
    if not isinstance(values,list) or len(values)>100 or any(type(v) is not int for v in values):
        return jsonify(error='Dãy chèn phải là danh sách tối đa 100 số nguyên.'),400
    if len(values)!=len(set(values)):
        return jsonify(error='Dãy chèn chứa khóa trùng nhau.'),400
    if type(target) is not int:
        return jsonify(error='Khóa cần xóa phải là số nguyên.'),400
    try:
        return jsonify(analyze(values,target))
    except (ValueError, RecursionError) as e:
        return jsonify(error=str(e)),400

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000,debug=False)
