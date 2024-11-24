import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from PIL import Image
import tempfile

# Inicializa Flask
app = Flask(__name__)
CORS(app)

# Ruta del modelo guardado
MODEL_PATH = os.getenv("MODEL_PATH", "C:\\Users\\Jose Cardenas\\Downloads\\CICLO 8\\IA AVANZADA\\Quasar\\VGG16_model.h5")
model = load_model(MODEL_PATH)
print("Modelo cargado correctamente desde:", MODEL_PATH)

# Etiquetas de clases
CLASS_LABELS = {0: "Defect", 1: "Fresh"}

# Endpoint para clasificar la imagen
@app.route('/clasificador', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'El archivo está vacío'}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            image.save(temp_file.name)
            image_path = temp_file.name

        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_label = CLASS_LABELS[np.argmax(predictions)]

        return jsonify({'label': predicted_label})
    except Exception as e:
        print("Error al procesar la imagen:", e)
        return jsonify({'error': f'Error procesando la imagen: {str(e)}'}), 500
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

# Iniciar el servidor Flask
if __name__ == "__main__":
    print("Iniciando el servidor Flask en http://127.0.0.1:5000")
    app.run(debug=True)
