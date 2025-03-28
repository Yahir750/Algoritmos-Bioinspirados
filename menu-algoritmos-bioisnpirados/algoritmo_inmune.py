"""
Algoritmo Inmune Adaptado para Streamlit
"""
import random
import sys

def calcular_afinidad(anticuerpo, antigeno):
    return sum(1 for a, b in zip(anticuerpo, antigeno) if a == b) / len(anticuerpo)

def crear_anticuerpo(longitud):
    return ''.join(random.choice('01') for _ in range(longitud))

def sistema_inmune_artificial(num_anticuerpos, umbral):
    # Configuración
    LONGITUD = 10
    GENERACIONES = 10
    TASA_MUTACION = 0.1
    
    # 1. Generar datos (80% normales, 20% anomalías)
    normales = [crear_anticuerpo(LONGITUD) for _ in range(num_anticuerpos)]
    anomalias = [''.join('1' if c == '0' else '0' for c in ab) for ab in normales[:int(num_anticuerpos*0.2)]]
    antigenos = normales + anomalias
    random.shuffle(antigenos)
    
    # 2. Población inicial
    poblacion = [crear_anticuerpo(LONGITUD) for _ in range(num_anticuerpos)]
    resultados = {
        'detectadas': 0,
        'mejor_afinidad': 0,
        'evolucion': []
    }

    # 3. Proceso evolutivo
    for generacion in range(GENERACIONES):
        for antigeno in antigenos:
            mejor_afinidad = 0
            mejor_anticuerpo = None
            
            for anticuerpo in poblacion:
                afinidad = calcular_afinidad(anticuerpo, antigeno)
                
                if afinidad < umbral:
                    resultados['detectadas'] += 1
                
                if afinidad > mejor_afinidad:
                    mejor_afinidad = afinidad
                    mejor_anticuerpo = anticuerpo
            
            if mejor_anticuerpo:
                nuevo = ''.join(
                    c if random.random() > TASA_MUTACION else '1' if c == '0' else '0'
                    for c in mejor_anticuerpo
                )
                poblacion.append(nuevo)
                resultados['mejor_afinidad'] = max(resultados['mejor_afinidad'], mejor_afinidad)
        
        resultados['evolucion'].append({
            'generacion': generacion,
            'poblacion': len(poblacion),
            'detecciones': resultados['detectadas']
        })

    resultados['poblacion_final'] = len(poblacion)
    return resultados

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("error|Uso: python algoritmo_inmune.py <anticuerpos> <umbral>")
        sys.exit(1)

    try:
        anticuerpos = int(sys.argv[1])
        umbral = float(sys.argv[2])
        
        if not 5 <= anticuerpos <= 50:
            print("error|Anticuerpos debe estar entre 5 y 50")
            sys.exit(1)
            
        if not 0.1 <= umbral <= 0.9:
            print("error|Umbral debe estar entre 0.1 y 0.9")
            sys.exit(1)

        resultados = sistema_inmune_artificial(anticuerpos, umbral)
        
        # Formato para Streamlit (pipe-separated)
        print(f"Anomalías detectadas {resultados['detectadas']}")
        print(f"Población Final {resultados['poblacion_final']}")
        
    except Exception as e:
        print(f"error|{str(e)}")
        sys.exit(1)