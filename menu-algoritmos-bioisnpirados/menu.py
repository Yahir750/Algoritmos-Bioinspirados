import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from typing import List, Tuple
import io
from PIL import Image
import base64

st.title("Menú de algoritmos bioinspirados en Streamlit")

# Diccionario de algoritmos disponibles en nuestro menu
algoritmos = {
    "Algoritmo genético": {
        "archivo": "algoritmo_genetico.py",
        "descripcion": "Este algoritmo imita el proceso de evolución natural para encontrar una solución óptima (en este caso, la cadena '1101110101'). Comienza con un grupo aleatorio de posibles soluciones ('individuos') y mediante un proceso iterativo de selección, combinación y mutación, va mejorando progresivamente la población hasta alcanzar la solución deseada.",
        "parametros": {
            "Poblacion": {"key": "poblacion", "tipo": "int"},
            "Mutacion": {"key": "mutacion", "tipo": "float"}
        }
    },
    "Algoritmo inmune": {
        "archivo": "algoritmo_inmune.py",
        "descripcion": "Este algoritmo imita el funcionamiento del sistema inmunológico humano para detectar patrones anómalos en datos. Utiliza 'anticuerpos' virtuales que buscan similitudes con los datos de entrada ('antígenos'). Si un anticuerpo no reconoce bien un dato (baja afinidad), se marca como posible anomalía. Los anticuerpos más efectivos se clonan y mutan para mejorar su capacidad de detección, mientras que los menos eficientes se descartan. Con el tiempo, el sistema 'aprende' a identificar qué datos son normales y cuáles son sospechosos.",
        "parametros": {
            "Anticuerpos": {"key": "anticuerpos", "tipo": "int"},
            "Umbral": {"key": "umbral", "tipo": "float"}
        }
    },

    "Algoritmo de hormiguero": {
        "archivo": "algoritmo_hormiguero.py",  # Asegúrate de que este archivo existe
        "descripcion": "Este algoritmo simula el comportamiento de hormigas para resolver problemas de optimización, como encontrar la ruta más corta entre varias ciudades. Las 'hormigas' virtuales exploran diferentes caminos, dejando rastros de feromonas que atraen a otras. Con el tiempo, los caminos más cortos acumulan más feromonas, mientras que los menos eficientes se evaporan. El algoritmo combina explotación (elegir el mejor camino conocido) y exploración (buscar nuevas rutas) para encontrar una solución óptima o cercana a óptima. Al final, devuelve la mejor ruta encontrada y su distancia total.",
        "parametros": {
            "Hormigas": {"key": "hormigas", "tipo": "int"},
            "Iteraciones": {"key": "iteraciones", "tipo": "int"}
        }},

    "Algoritmo de recocido simulado": {
        "archivo": "algoritmo_recocido.py",
        "descripcion": "Este algoritmo imita el proceso de recocido en metalurgia, donde un material se calienta y luego se enfría gradualmente para mejorar sus propiedades. En este caso, se usa para encontrar la mejor solución (el 'punto más bajo') en un terreno complejo con muchos altibajos",
        "parametros": {
            "Tamaño de paso": {"key": "tamaño", "tipo": "float"},
            "Iteraciones": {"key": "iteraciones", "tipo": "int"}
        }
    }
}

# Pestañas

tabs = st.tabs(list(algoritmos.keys()))

# Cada algoritmo con descripcion y parametros en su pestaña
for i, (nombre, datos) in enumerate(algoritmos.items()):
    with tabs[i]:
        st.subheader(nombre)
        st.write(datos["descripcion"])
        
        valores = {}
        for param_name, param_data in datos["parametros"].items():
            if param_data["tipo"] == "int":
                valores[param_name] = st.number_input(param_name, min_value=1, step=1, key=f"{param_data['key']}_{nombre}")
            elif param_data["tipo"] == "float":
                valores[param_name] = st.number_input(param_name, min_value=0.0, step=0.1, key=f"{param_data['key']}_{nombre}")
        
        if st.button(f"Ejecutar {nombre}"):
            try:
                resultado = subprocess.run(
                ["python", datos["archivo"]] + [str(v) for v in valores.values()],
                capture_output=True,
                text=True
                )   
                st.text_area("Salida:", resultado.stdout)
                comando = ["python", datos["archivo"]] + [str(v) for v in valores.values()]
                resultado = subprocess.run(comando, capture_output=True, text=True)
                
                if resultado.returncode == 0:
                    st.success("Algoritmo ejecutado correctamente")
                    
                    # Procesar la salida
                    for linea in resultado.stdout.splitlines():
                        if linea.startswith("success|"):
                            _, clave, valor = linea.split("|")
                            st.info(f"{clave}: {valor}")
                        elif linea.startswith("image|"):
                            _, titulo, img_data = linea.split("|")
                            img_bytes = base64.b64decode(img_data)
                            img = Image.open(io.BytesIO(img_bytes))
                            st.image(img, caption=titulo, use_container_width=True)
                else:
                    st.error(f"Error en la ejecución: {resultado.stderr}")
                    
            except Exception as e:
                st.error(f"Error al ejecutar el algoritmo: {str(e)}")