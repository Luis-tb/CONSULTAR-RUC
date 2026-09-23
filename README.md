# API Consulta RUC — Microservicio de Validación Tributaria (SUNAT)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![JWT](https://img.shields.io/badge/Auth-JWT%20Bearer-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)

---

## 📌 Descripción

Microservicio RESTful ligero y contenerizado desarrollado en **Python (Flask)** para la extracción, consulta y validación automatizada de información de contribuyentes desde el portal público de **SUNAT** (Perú).

Diseñado para integrarse con sistemas ERP, software de facturación electrónica y plataformas contables que requieren autocompletar o verificar la razón social y dirección fiscal a partir del número de RUC.

---

## ✨ Características

- ⚡ **API RESTful Rápida:** Endpoints estandarizados con respuestas en formato JSON.
- 🔒 **Seguridad con JWT:** Acceso protegido mediante tokens Bearer (`PyJWT`).
- 🐳 **100% Contenerizado:** Listo para despliegue con Docker y Docker Compose en cualquier servidor o VPS.
- 🧹 **Parsing Resiliente:** Extracción y normalización de datos HTML estructurados mediante BeautifulSoup.

---

## 🚀 Despliegue con Docker Compose (Recomendado)

### 1. Clonar el repositorio
```bash
git clone https://github.com/Luis-tb/CONSULTAR-RUC.git
cd CONSULTAR-RUC
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
```
*(Edita el archivo `.env` y define tu propio `JWT_SECRET`).*

### 3. Construir y levantar el contenedor
```bash
docker-compose up -d --build
```
El servicio estará disponible de inmediato en `http://localhost:5000`.

---

## 💻 Ejecución Local (Sin Docker)

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o .\venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor
python index.py
```

---

## 📖 Especificación del Endpoint

### `GET /consulta-ruc/<numero_ruc>`
Consulta los datos públicos asociados a un número de RUC válido de 11 dígitos.

#### Cabeceras Requeridas:
```http
Authorization: Bearer <TU_TOKEN_JWT>
```

#### Ejemplo de Petición (`cURL`):
```bash
curl -X GET "http://localhost:5000/consulta-ruc/20100070970" \
     -H "Authorization: Bearer <TU_TOKEN_JWT>"
```

#### Respuesta Exitosa (`200 OK`):
```json
{
  "ruc": "20100070970",
  "razon_social": "SUPERMERCADOS PERUANOS SOCIEDAD ANONIMA",
  "direccion": "CAL. MORELLI NRO. 181 URB. SAN BORJA (PISO 2) LIMA - LIMA - SAN BORJA"
}
```

#### Respuestas de Error:
* **`401 Unauthorized`:** Token JWT ausente, expirado o con firma inválida.
* **`404 Not Found`:** RUC no encontrado o inexistente en los registros de SUNAT.

---

## ⚖️ Descargo de Responsabilidad (Disclaimer)

Este proyecto ha sido desarrollado exclusivamente con fines educativos, de investigación y para la integración técnica de consultas contables automatizadas. Todas las consultas se realizan sobre información de libre acceso público provista por el portal oficial de la Superintendencia Nacional de Aduanas y de Administración Tributaria (SUNAT). Este software no guarda relación oficial con la entidad tributaria.

---

## 👤 Autor

**Luis David Torres Barreto**  
- **GitHub:** [@Luis-tb](https://github.com/Luis-tb)  
- **Email:** torresbarretoluisdavid@gmail.com
