# 📊 Real-Time Sentiment Analysis of YouTube Live Chat (Spanish)
Este proyecto implementa un **pipeline de análisis de sentimiento en tiempo real** para mensajes de chat en vivo de transmisiones de YouTube en español. Usa una arquitectura de microservicios completamente contenedorizada con Docker Compose.

🎯 Además, este sistema fue diseñado como una prueba de concepto para mostrar habilidades prácticas en ingeniería de datos en tiempo real y procesamiento de flujo.

## 🔗 Repositorio
👉 [Enlace al repositorio de GitHub](https://github.com/tuusuario/aqui-tu-repo) ← *(pendiente de agregar)*

---

## 📁 Estructura del Proyecto

├── flink/ # Trabajos de Apache Flink (PyFlink)
├── model-server/ # API Flask con el modelo de análisis de sentimiento
├── yt-producer/ # Productor de mensajes desde el chat en vivo de YouTube
├── docker-compose.yml # Orquestación de servicios
├── druid/ # Apache Druid (almacén OLAP)
├── superset/ # Apache Superset (dashboards)
└── LICENSE
---

## 🛠️ Tecnologías Utilizadas

### Principales
- **Apache Kafka**: Sistema de colas para transmisión de mensajes
- **Apache Zookeeper**: Coordinación de clúster Kafka
- **Apache Flink (PyFlink)**: Procesamiento de flujos en tiempo real
- **Flask**: Servidor REST para inferencia del modelo
- **Apache Druid**: Almacén OLAP para consultas analíticas en tiempo real
- **Apache Superset**: Dashboards interactivos sobre datos procesados
- **Docker Compose**: Orquestación de contenedores

### Librerías de Python
- `chat_downloader`: Extracción del chat de YouTube
- `kafka-python`: Cliente productor de Kafka
- `pysentimiento`: Modelos de análisis de sentimiento en español
- `requests`: Comunicación HTTP entre servicios

---

## ⚙️ Configuración

### Requisitos
- Docker
- Docker Compose

### Servicios y Puertos
| Servicio         | Puerto         |
|------------------|----------------|
| Kafka (broker)   | 9092 / 29092   |
| Flink Dashboard  | localhost:8081 |
| Flask API        | localhost:5000 |
| Superset UI      | localhost:8088 |
| Druid UI         | localhost:8888 |

### Despliegue
```bash
docker-compose up
El servicio init-kafka crea automáticamente los topics necesarios:

chat-live-topic

chat-live-topic-processed

Se respeta el orden de dependencias: Zookeeper → Kafka → Servicios
