# API Consulta RUC

Este proyecto es una API en Flask para consultar información de RUCs utilizando la web de SUNAT.

## Requisitos

*   Docker
*   Git

## Instalación y Ejecución con Docker

1.  Clona el repositorio:
    ```bash
    git clone <url-del-repositorio>
    cd API
    ```

2.  Crea un archivo `.env` basado en tus necesidades (asegúrate de configurar `JWT_SECRET`).

3.  Construye la imagen de Docker:
    ```bash
    docker build -t consulta-ruc-api .
    ```

4.  Ejecuta el contenedor:
    ```bash
    docker run -d -p 5000:5000 --env-file .env --name consulta-ruc-container consulta-ruc-api
    ```

La API estará disponible en `http://localhost:5000`.

## Endpoints

*   `GET /consulta-ruc/<numero_ruc>`: Consulta información de un RUC. Requiere token Bearer.

## Desarrollo Local

1.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

2.  Ejecuta la aplicación:
    ```bash
    python index.py
    ```
