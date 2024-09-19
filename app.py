from flask import Flask, render_template, request, jsonify, send_from_directory
import base64
import os

app = Flask(__name__)

# Папка для сохранения изображений
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data['image']

    # Убираем "data:image/png;base64," из начала строки
    image_data = image_data.replace('data:image/png;base64,', '')
    image_data = base64.b64decode(image_data)

    # Сохраняем файл
    filepath = os.path.join(UPLOAD_FOLDER, 'photo.png')
    with open(filepath, 'wb') as f:
        f.write(image_data)

    return jsonify({'filepath': filepath})

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)