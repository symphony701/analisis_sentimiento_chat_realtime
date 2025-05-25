from chat_downloader import ChatDownloader
from kafka import KafkaProducer
import json
import time

from helper.message import Message

# Configuración del producer de Kafka
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Ajustamos el servidor de Kafka
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8') # Serializamos el mensaje a JSON
)

URL = "https://www.youtube.com/watch?v=EtQwhSbYqrU"
CANAL_NOMBRE = "Icarus"

chat = ChatDownloader().get_chat(URL)
for message in chat:
    final_message = Message(message, CANAL_NOMBRE)
    producer.send('chat-live-topic', value=final_message.to_dict())
    print(f"Mensaje enviado: {final_message.to_dict()}")
    producer.flush()  # Aseguramos que el mensaje se envíe inmediatamente
    time.sleep(0.1)  # Pequeña pausa para evitar sobrecargar el broker