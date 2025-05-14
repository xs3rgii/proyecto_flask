from flask import Flask, render_template, request, abort
import json
import os

# Inicializa la aplicación Flask
app = Flask(__name__)

# Función para cargar los datos del archivo JSON
def load_data():
    templates_dir = os.path.join(app.root_path, 'templates')  # Ubicación de la carpeta de plantillas
    json_path = os.path.join(templates_dir, 'hardware.json')  # Ruta del archivo JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            componentes = data.get('componentes', [])  # Obtiene la lista de componentes
            # Extrae y ordena los modelos únicos de los componentes
            modelos = sorted({comp['detalles']['modelo'] for comp in componentes})
            return componentes, modelos
    except Exception as e:
        print(f"Error cargando JSON en {json_path}: {e}")
        return [], []

# Carga inicial de los datos JSON al iniciar el servidor
componentes_data, all_models = load_data()

# Función para filtrar componentes según el modelo y consulta del usuario
def filtrar_componentes(componentes, query='', modelo_seleccionado=''):
    query = query.lower().strip()  # Normaliza la consulta a minúsculas y sin espacios
    modelo_seleccionado = modelo_seleccionado.lower().strip()

    resultados = []
    for comp in componentes:
        modelo = comp['detalles']['modelo'].lower()
        if modelo_seleccionado and modelo != modelo_seleccionado:  # Filtra por modelo si se selecciona uno
            continue

        detalles = comp['detalles']
        marca = detalles.get('marca', '').lower()
        modelo_nombre = detalles.get('modelo', '').lower()
        nombre_completo = f"{marca} {modelo_nombre}".strip()  # Combina marca y modelo

        texto_busqueda = nombre_completo  # La búsqueda se enfoca en el nombre completo

        if query and not texto_busqueda.startswith(query):  # Filtra solo si el texto comienza como la consulta
            continue

        disponibilidad = comp.get('disponibilidad', {})
        # Construye el resultado del componente
        resultado = {
            'id': comp.get('id'),
            'marca': detalles.get('marca', ''),
            'modelo': detalles.get('modelo', ''),
            'precio': detalles.get('precio', ''),
            'categoria': comp.get('categoria', ''),
            'proveedor': disponibilidad.get('proveedor', 'No especificado')
        }
        resultados.append(resultado)
    return resultados

# Ruta principal que carga la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el formulario de búsqueda de componentes
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    selected_model = request.form.get('model_select', '')  # Obtiene el modelo seleccionado
    resultados = []
    query = ''  # Inicializa la consulta

    if request.method == 'POST':
        query = request.form.get('query', '')  # Obtiene la consulta del usuario
        # Filtra componentes según la consulta y modelo seleccionado
        resultados = filtrar_componentes(componentes_data, query, selected_model)

    # Renderiza el formulario y muestra los resultados
    return render_template(
        'formulario.html',
        resultados=resultados,
        all_models=all_models,
        selected_model=selected_model,
        query=query
    )

# Ruta para listar componentes según la consulta
@app.route('/listar_xxxs', methods=['POST', 'GET'])
def listar_xxxs():
    # Obtiene la consulta y el modelo si están en la solicitud
    query = request.form.get('nombre_xxx', '') if request.method == 'POST' else ''
    modelo = request.form.get('model_select', '') if request.method == 'POST' else ''

    # Filtra los componentes según la consulta y modelo
    resultados = filtrar_componentes(componentes_data, query, modelo)

    # Renderiza los resultados en la plantilla
    return render_template('resultado_busqueda.html', nombre_buscado=query, lista_xxxs=resultados)

# Ruta para mostrar detalles de un componente específico
@app.route('/xxx/<int:identificador>')
def detalle_xxx(identificador):
    # Busca el componente por ID
    componente = next((item for item in componentes_data if item['id'] == identificador), None)
    if componente:
        # Muestra la plantilla de detalles del componente si existe
        return render_template('detalle.html', xxx=componente)
    else:
        # Muestra un error 404 si el componente no existe
        abort(404)

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Inicia la aplicación en modo de depuración
    app.run(host='0.0.0.0', port=5000, debug=True)
