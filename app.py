import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

dic = {0: 'Bercak Cokelat',  
       1: 'Busuk Daun',
       2: 'Hawar Daun Bakteri'}

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("classification.html")

@app.route("/submit", methods=['POST'])
def get_output():
    if 'my_image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    img = request.files['my_image']
    if img.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Acak hasil klasifikasi
    prediction = dic[random.randint(0, 2)]
    
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)