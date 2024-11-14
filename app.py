from flask import Flask, request, render_template, jsonify
import openai
import json
import os

# Cargar la clave de API de OpenAI desde la variable de entorno en Render
openai_api_key = os.getenv("OPENAI_API_KEY")

# Si no está en las variables de entorno, cargar desde config.json (para uso local)
if not openai_api_key:
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            openai_api_key = config.get("OPENAI_API_KEY")
    except FileNotFoundError:
        print("Error: No se encontró la clave de API. Asegúrate de tener config.json en local o configurar la variable de entorno.")

# Asignar la clave a la configuración de OpenAI si se ha encontrado
if openai_api_key:
    openai.api_key = openai_api_key
else:
    raise ValueError("No se pudo encontrar la clave de API de OpenAI. Verifica config.json o la variable de entorno OPENAI_API_KEY.")

# Cargar instrucciones desde instrucciones.json
with open('instrucciones.json', encoding="utf-8") as instructions_file:
    instrucciones = json.load(instructions_file)

# Convertir instrucciones.json a una cadena para usar como contexto
instrucciones_contexto = json.dumps(instrucciones)

# Inicializar la aplicación Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Mensaje del sistema con el contexto de instrucciones.json
    system_message = {
        "role": "system",
        "content": f"Eres un asistente especializado en el ómnibus BYD K9W, un vehículo 100% eléctrico. Solo debes responder consultas relacionadas con este modelo específico, incluyendo temas de mantenimiento, funcionamiento, características técnicas, y solución de problemas. Usa el siguiente contexto para responder las preguntas de forma precisa: {instrucciones_contexto}"
    }

    # Llamada a la API de OpenAI para obtener la respuesta del asistente usando ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            system_message,
            {"role": "user", "content": user_message}
        ]
    )

    assistant_message = response['choices'][0]['message']['content'].strip()
    return jsonify({"message": assistant_message})

if __name__ == '__main__':
    app.run(debug=True)

