from flask import Flask, request, render_template, jsonify
import openai
import json

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Initialize OpenAI API with the API key from the config file
openai.api_key = config["OPENAI_API_KEY"]

# Load instructions from instrucciones.json
with open('instrucciones.json', encoding="utf-8") as instructions_file:
    instrucciones = json.load(instructions_file)

# Convert instrucciones.json to a concise string to provide as context
instrucciones_contexto = json.dumps(instrucciones)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Mensaje del sistema para guiar el comportamiento del asistente con contexto de instrucciones.json
    system_message = {
        "role": "system",
        "content": f"Eres un asistente especializado en el ómnibus BYD K9W, un vehículo 100% eléctrico. Solo debes responder consultas relacionadas con este modelo específico, incluyendo temas de mantenimiento, funcionamiento, características técnicas, y solución de problemas. Usa el siguiente contexto para responder las preguntas de forma precisa: {instrucciones_contexto}"
    }

    # Llamada a la API de OpenAI para obtener la respuesta del asistente usando ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Usando el modelo gpt-4-turbo
        messages=[
            system_message,
            {"role": "user", "content": user_message}
        ]
    )

    assistant_message = response['choices'][0]['message']['content'].strip()

    return jsonify({"message": assistant_message})


if __name__ == '__main__':
    app.run(debug=True)

