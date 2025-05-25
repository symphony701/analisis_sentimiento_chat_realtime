from flask import Flask, request, jsonify
from pysentimiento import create_analyzer

app = Flask(__name__)

# Aqui inicializamos los analizadores de sentimientos con el idioma español
emotion_analyzer = create_analyzer(task="emotion", lang="es")
#hate_speech_analyzer = create_analyzer(task="hate_speech", lang="es")
irony_analyzer = create_analyzer(task="irony", lang="es")
sentiment_analyzer = create_analyzer(task="sentiment", lang="es")

# Definimos la ruta http para recibir el texto a analizar
@app.route('/analyze', methods=['POST'])
def analyze_text():
    datos = request.get_json()
    texto = datos.get('texto', '')
    #Esto es simple, primero verificamos si el texto es vacio, y si lo es, devolvemos un error 400
    #Luego predecimos las emociones, y si no es "others", devolvemos la prediccion
    #Si no es "others", predecimos la ironia, y si es "ironic", devolvemos la prediccion
    #Si no es "ironic", predecimos el sentimiento, y si no es "", devolvemos la prediccion
    #Si no es "", devolvemos un error 500
    if not texto:
        return jsonify({'error': 'No se proporcionó texto'}), 400
    response_normal = emotion_analyzer.predict(texto)
    if response_normal.output != 'others':
        return jsonify({'sentimiento': response_normal.output}), 200
    #response_hate = hate_speech_analyzer.predict(texto)
    response_irony = irony_analyzer.predict(texto)
    if response_irony.output == 'ironic':
        return jsonify({'sentimiento': response_irony.output}), 200
    response_sentiment = sentiment_analyzer.predict(texto)
    if response_sentiment.output != "" and response_sentiment != None:
        return jsonify({'sentimiento': response_sentiment.output}), 200
    else:
        return jsonify({'error': 'No se pudo analizar el texto'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)