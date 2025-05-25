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
