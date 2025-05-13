from flask import Flask, render_template, request, abort
import json
import os

app = Flask(__name__)

# Cargar datos JSON una vez al iniciar la aplicación
def load_data():
    templates_dir = os.path.join(app.root_path, 'templates')
    json_path = os.path.join(templates_dir, 'hardware.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            componentes = data.get('componentes', [])
            # Extraer modelos únicos para filtros
            modelos = sorted({comp['detalles']['modelo'] for comp in componentes})
            return componentes, modelos
    except Exception as e:
        print(f"Error cargando JSON en {json_path}: {e}")
        return [], []

componentes_data, all_models = load_data()

def filtrar_componentes(componentes, query='', modelo_seleccionado=''):
    query = query.lower().strip()
    modelo_seleccionado = modelo_seleccionado.lower().strip()

    resultados = []
    for comp in componentes:
        modelo = comp['detalles']['modelo'].lower()
        if modelo_seleccionado and modelo != modelo_seleccionado:
            continue

        detalles = comp['detalles']
        marca = detalles.get('marca', '').lower()
        modelo_nombre = detalles.get('modelo', '').lower()
        nombre_completo = f"{marca} {modelo_nombre}".strip()

        texto_busqueda = nombre_completo # Ahora la búsqueda se enfoca en el nombre completo

        if query and not texto_busqueda.startswith(query): # Filtramos por inicio de cadena
            continue

        disponibilidad = comp.get('disponibilidad', {})
        resultado = {
            'id': comp.get('id'), # Aseguramos incluir el ID
            'marca': detalles.get('marca', ''),
            'modelo': detalles.get('modelo', ''),
            'precio': detalles.get('precio', ''),
            'categoria': comp.get('categoria', ''),
            'proveedor': disponibilidad.get('proveedor', 'No especificado')
        }
        resultados.append(resultado)
    return resultados

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        query = request.form.get('query', '')
        modelo = request.form.get('model_select', '')
        resultados = filtrar_componentes(componentes_data, query, modelo)
    else:
        resultados = []

    return render_template('formulario.html', resultados=resultados, all_models=all_models)

@app.route('/listar_xxxs', methods=['POST', 'GET'])
def listar_xxxs():
    query = request.form.get('nombre_xxx', '') if request.method == 'POST' else ''
    modelo = request.form.get('model_select', '') if request.method == 'POST' else ''

    # Filtrar los componentes
    resultados = filtrar_componentes(componentes_data, query, modelo)

    # Renderizar los resultados
    return render_template('resultado_busqueda.html', nombre_buscado=query, lista_xxxs=resultados)

@app.route('/xxx/<int:identificador>')
def detalle_xxx(identificador):
    componente = next((item for item in componentes_data if item['id'] == identificador), None)
    if componente:
        return render_template('detalle.html', xxx=componente)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)