from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.functions import MapFunction, RuntimeContext
from pyflink.common.serialization import SerializationSchema
from pyflink.common.typeinfo import Types

import json
import requests
import logging

#Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sentimiento_parser(sentimiento:str) -> str:

    #Función para parsear el sentimiento ya que el modelo lo devuelve en diferentes formatos

    sentimiento = sentimiento.lower()
    if 'POS' in sentimiento:
        return 'positivo'
    elif 'NEG' in sentimiento:
        return 'negativo'
    elif 'NEU' in sentimiento:
        return 'neutral'
    elif 'anger' in sentimiento:
        return 'enojo'
    elif 'joy' in sentimiento:
        return 'alegría'
    elif 'sadness' in sentimiento:
        return 'tristeza'
    elif 'fear' in sentimiento:
        return 'miedo'
    elif 'disgust' in sentimiento:
        return 'desagrado'
    elif 'surprise' in sentimiento:
        return 'sorpresa'
    elif 'neutral' in sentimiento:
        return 'neutral'
    elif 'ironic' in sentimiento:
        return 'irónico'
    else:
        return 'desconocido'

class SentimentAnalysisFunction(MapFunction):
    def __init__(self):
        self.session = None
    
    def open(self, runtime_context: RuntimeContext):
        # Inicializaremos la sesión HTTP
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        logger.info("Inicializada SentimentAnalysisFunction")
    
    def close(self):
        # Limpiar recursos al terminar el job
        if self.session:
            self.session.close()
            logger.info("Sesión HTTP cerrada")
    
    def map(self, message):
        try:
            # Intentar parsear el mensaje como JSON
            data = json.loads(message)
            
            if 'texto' not in data:
                logger.warning(f"Mensaje sin campo 'texto': {message}")
                return json.dumps({"error": "Mensaje sin campo 'texto'", "mensaje_original": message})
            
            # Realizar la llamada HTTP al servidor Flask el cual tiene el modelo de análisis de sentimiento
            try:
                data["timestamp"] = int(data["timestamp"]) // 1000
                url = "http://model-flask-server:5000/analyze"
                response = self.session.post(
                    url, 
                    json={"texto": data['texto']},
                    timeout=5  # 5 segundos de timeout para la solicitud HTTP
                )
                
                if response.status_code == 200:
                    result = response.json()
                    sentimiento_encontrado = result.get('sentimiento', 'unknown')
                    sentimiento_procesado = sentimiento_parser(sentimiento_encontrado)
                    # Guardar el sentimiento procesado en el diccionario para devolverlo por el sink
                    data['sentimiento'] = sentimiento_procesado
                    logger.info(f"Análisis exitoso: {data['sentimiento']}")
                else:
                    data['sentimiento'] = 'unknown'
                    data['error'] = f"HTTP error: {response.status_code}"
                    logger.error(f"Error en respuesta HTTP: {response.status_code}")
            except requests.exceptions.RequestException as e:
                data['sentimiento'] = 'unknown'
                data['error'] = f"Error de conexión: {str(e)}"
                logger.error(f"Error de conexión: {str(e)}")
            
            return json.dumps(data)
        except json.JSONDecodeError:
            logger.error(f"Error al parsear JSON: {message}")
            return json.dumps({"error": "Formato JSON inválido", "mensaje_original": message})
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return json.dumps({"error": f"Error: {str(e)}", "mensaje_original": message})
        
class CustomStringSerializationSchema(SerializationSchema):
    # Esta clase se utiliza para serializar los mensajes que se envían a Kafka bytes
    def serialize(self, element):
        if isinstance(element, str):
            return element.encode('utf-8')
        elif isinstance(element, bytes):
            return element
        else:
            return str(element).encode('utf-8')

def main():
    # Configuración del entorno de ejecución de Flink
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10000)  # Esto es para habilitar los checkpoints cada 10 segundos
    env.set_parallelism(1)  # Establecemos la paralelización a 1 para evitar problemas de concurrencia
    
    # Añadir los JARs necesarios para comunicarnos con Kafka, estos los debemos de tener en el contenedor
    # de Flink, en la carpeta /opt/flink/lib
    env.add_jars("file:///opt/flink/lib/flink-connector-kafka-1.17.1.jar",
                "file:///opt/flink/lib/kafka-clients-3.2.0.jar")
    
    # Configuramos propiedades de Kafka
    kafka_props = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'flink-consumer-group',
        'auto.offset.reset': 'latest',  
        'enable.auto.commit': 'false', 
    }
    
    # Creamos el consumidor de Kafka
    consumer = FlinkKafkaConsumer(
        topics='chat-live-topic', # Este es el topic de Kafka del cual vamos a leer
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )
    
    # Configuramos el consumidor para que empiece a leer desde el último offset
    # Esto es útil para evitar leer mensajes antiguos al reiniciar el job
    consumer.set_start_from_latest()
    
    # Añadimos el consumidor al entorno de ejecución
    ds = env.add_source(consumer)
    
    # Con esto se procesa los mensajes de Kafka
    # el output_type es el tipo de dato que se va a devolver
    processed_stream = ds.map(SentimentAnalysisFunction(), output_type=Types.STRING())
    
    
    #Creamos la configuración del sink de Kafka ya que esta parte se comportará como un producer para enviar los mensajes procesados a otro topic
    producer_props = {
            'bootstrap.servers': 'kafka:9092'
    }
        
    # Creamos el producer 
    producer = FlinkKafkaProducer(
            topic='chat-live-topic-processed', # Este es el topic de Kafka al cual vamos a enviar los mensajes procesados
            serialization_schema=SimpleStringSchema(),
            producer_config=producer_props
    )
    # Añadimos el sink al stream procesado
    processed_stream.add_sink(producer)
    # Mantenemos el sink de impresión para depuración
    processed_stream.print()
    
    # Ejecutamos el job completo, tanto el consumer como el producer
    # Esto es lo que inicia el job y lo mantiene en ejecución
    env.execute("Consumo y análisis de sentimiento desde Kafka con PyFlink")



if __name__ == "__main__":
    main()