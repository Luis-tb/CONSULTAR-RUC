# API Consulta RUC

Este proyecto es una API en Flask para consultar información de RUCs utilizando la web de SUNAT.

## Requisitos

*   Docker
*   Docker Compose
*   Git

## Instalación y Ejecución con Docker Compose

1.  Clona el repositorio:
    ```bash
    git clone <url-del-repositorio>
    cd API
    ```

2.  Crea un archivo `.env` basado en el ejemplo `.env.example` y configura tu `JWT_SECRET`:
    ```bash
    cp .env.example .env
    ```

3.  Construye y levanta el servicio:
    ```bash
    docker-compose up -d --build
    ```

La API estará disponible en `http://localhost:5000`.

## Endpoints

*   `GET /consulta-ruc/<numero_ruc>`: Consulta información de un RUC. Requiere token Bearer.

## Desarrollo Local (sin Docker)

1.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

2.  Ejecuta la aplicación:
    ```bash
    python index.py
    ```
