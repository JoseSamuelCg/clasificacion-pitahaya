<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md">
      <h2>Clasificador de Pitahaya</h2>
      <p class="intro-text">
        Sube una imagen de pitahaya para clasificar su tipo. Nuestro modelo de clasificación utiliza inteligencia
        artificial para reconocer una fruta en buen estado o en mal estado, de tal forma que se pueda mantener el control de calidad de la Pitahaya.
      </p>
      <q-form @submit.prevent="classifyImage">
        <q-uploader
          @added="onFileAdded"
          accept="image/*"
          label="Sube una imagen de pitahaya"
          ref="uploader"
          :auto-upload="false"
          :max-files="1"
          class="uploader"
        />
        <q-btn label="Clasificar" type="submit" color="secondary" class="q-mt-md button" />
      </q-form>
      <div v-if="result" class="q-mt-md text-h6">
        Clasificación: {{ result }}
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      files: [], // Almacenará los archivos seleccionados
      result: null, // Resultado de la clasificación
    };
  },
  methods: {
    // Manejar la adición de archivos
    onFileAdded(files) {
      this.files = files; // Guardar los archivos seleccionados
      console.log('Archivo seleccionado:', this.files); // Diagnóstico opcional
    },
    // Clasificar la imagen cargada
    async classifyImage() {
      if (this.files.length === 0) {
        this.$q.notify({ color: 'red', message: 'Por favor, sube una imagen' });
        return;
      }

      const formData = new FormData();
      formData.append('image', this.files[0]); // Agregar el primer archivo al formulario

      try {
        const response = await fetch('http://127.0.0.1:5000/clasificador', {
          method: 'POST',
          body: formData,
        });

        const data = await response.json();
        if (data.label) {
          this.result = data.label; // Mostrar el resultado de la clasificación
        } else {
          this.result = 'No se pudo clasificar la imagen.';
        }
      } catch (error) {
        console.error('Error en la clasificación:', error);
        this.$q.notify({ color: 'red', message: 'Error en la clasificación' });
      }
    },
  },
};
</script>

<style scoped>
.q-pa-md {
  max-width: 400px;
  text-align: center;
  font-family: 'Arial', sans-serif;
  padding: 20px;
  border-radius: 10px;
  background: linear-gradient(135deg, #f0f8ff, #c1e3ff); /* Degradado suave */
}

h2 {
  font-size: 45px;
  color: #0954a3; /* Cambia el color del título */
  font-weight: bold; /* Cambia el grosor del texto del título */
}

.intro-text {
  font-size: 16px;
  color: #666;
  margin-top: 10px;
  margin-bottom: 20px;
  line-height: 1.5;
}

.uploader {
  width: 100%;
  max-width: 500px; /* Ancho máximo para la caja de carga */
  margin-top: 10px;
}

.button {
  width: 100%;
  max-width: 200px; /* Ancho máximo para el botón */
  margin-top: 15px;
}
</style>
  