import os
import shutil
import gdown  # Tambahkan gdown untuk mengunduh dari Google Drive
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Kamus untuk klasifikasi
dic = {0: 'Bercak Cokelat',  
       1: 'Busuk Daun',
       2: 'Hawar Daun Bakteri'}

# Download model dari Google Drive jika belum ada di folder
def download_model():
    model_file = 'Convolution UAS-Batik Exception-66.66.h5'
    if not os.path.exists(model_file):
        url = 'https://drive.google.com/uc?id=1FEx-zhHb5D00W5vDmfZfGkm9I2pebHUb'  # URL Google Drive model Anda
        gdown.download(url, model_file, quiet=False)

# Pastikan model diunduh sebelum digunakan
download_model()

# Memuat model
model = load_model('Convolution UAS-Batik Exception-66.66.h5')

def predict_label(img_path):
    i = image.load_img(img_path, target_size=(224, 224))
    i = image.img_to_array(i) / 255.0
    i = i.reshape(1, 224, 224, 3)
    p = model.predict(i)
    p = p.argmax(axis=-1)
    return dic[p[0]]

# Fungsi untuk menghapus semua file gambar di folder static
def delete_all_images():
    static_folder = 'static/'
    for filename in os.listdir(static_folder):
        file_path = os.path.join(static_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("classification.html")

@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']

        # Hapus semua gambar di folder static sebelum menyimpan gambar baru
        delete_all_images()

        # Pastikan nama file ada
        if img.filename != '':
            img_path = "static/" + img.filename
            img.save(img_path)

            p = predict_label(img_path)
            return render_template("classification.html", prediction=p, img_path=img_path, img_filename=img.filename)

    return render_template("classification.html")

# route untuk menghapus gambar
@app.route('/delete_image', methods=['POST'])
def delete_image():
    data = request.get_json()
    filename = data.get('filename')
    
    if filename:
        file_path = os.path.join('static', filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': f'Image {filename} deleted successfully'}), 200
        else:
            return jsonify({'error': 'File not found'}), 404
    return jsonify({'error': 'No filename provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)