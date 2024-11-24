from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta donde guardaste tu modelo .h5
model_path = "C:\Users\Jose Cardenas\Downloads\CICLO 8\IA AVANZADA\Quasar" # Cambia esta ruta con la ubicación real de tu modelo
vgg16_model = load_model(model_path)

# Definir las clases
class_names = ['Defect', 'Fresh']  # Asegúrate de que las clases estén bien definidas

# Función para preprocesar la imagen
def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

@app.route('/clasificador', methods=['POST'])
def classify():
    file = request.files['image']  # Obtén la imagen del formulario
    img_path = os.path.join('/tmp', file.filename)  # Guarda temporalmente la imagen
    file.save(img_path)
    
    # Preprocesa la imagen
    img_array = preprocess_image(img_path)
    
    # Realiza la predicción
    predictions = vgg16_model.predict(img_array)
    
    # Obtener la clase con la mayor probabilidad
    predicted_class = class_names[np.argmax(predictions)]
    
    # Retorna la clasificación
    return jsonify({'label': predicted_class})

if __name__ == '__main__':
    print("Iniciando el servidor Flask en http://127.0.0.1:5000")
    app.run(debug=True)