## Uso del proyecto:
Para poder usar el proyecto en Debian, hay que activar un entorno virtual. Para ello, sigue estos pasos:

1. Crea un entorno virtual:
    ```bash
    python3 -m venv "proyecto flask"
    ```

2. Activa el entorno virtual:
    ```bash
    source "proyecto flask/bin/activate"
    ```

3. Instala Flask:
    ```bash
    pip install flask
    ```

4. Guarda las dependencias en el archivo `requirements.txt`:
    ```bash
    pip freeze > "proyecto flask/requirements.txt"
    ```
