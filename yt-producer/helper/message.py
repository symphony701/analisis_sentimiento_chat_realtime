#Formato el cual se enviara desde el producer en el servidor de flask hacia Kafka
class Message:
    def __init__(self, message, nombre_canal = ""):
        self.message = message
        self.texto = message["message"]
        self.autor = message["author"]['name']
        self.autor_id = message["author"]["id"]
        self.message_id = message["message_id"]
        self.timestamp = message["timestamp"]
        self.nombre_canal = nombre_canal

    def to_dict(self):
        return {
            "texto": self.texto,
            "autor": self.autor,
            "autor_id": self.autor_id,
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "nombre_canal": self.nombre_canal
        }