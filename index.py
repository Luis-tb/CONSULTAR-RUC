from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import os
import re
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv
from consulta_ruc import consultar_ruc

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = 'HS256'


def verificar_token(token):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return None
    except ExpiredSignatureError:
        return jsonify({"valido": False, "error": "Token expirado"}), 401
    except InvalidTokenError:
        return jsonify({"valido": False, "error": "Token inválido"}), 401


@app.route('/consulta-ruc/<numero_ruc>', methods=['GET'])
def consulta_ruc_route(numero_ruc):
    print(numero_ruc)
    # Obtener token desde el header
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if not auth_header or not auth_header.startswith('Bearer '):
        print('error de bearer')
        return jsonify({"error": "Falta el token Bearer en la cabecera"}), 401

    token = auth_header.split(" ")[1]

    # Verificar token
    verificacion = verificar_token(token)
    if verificacion:
        return verificacion

    # Llamar a la función que consulta el RUC
    tipo_respuesta, mensaje_respuesta = consultar_ruc(numero_ruc)

    if tipo_respuesta == "C":
        try:
            nombre_contribuyente = mensaje_respuesta["RUC:"].split(" - ", 1)[1]
            domicilio_fiscal = re.sub(r'\s+', ' ', mensaje_respuesta["Domicilio Fiscal:"]).strip()
            print(nombre_contribuyente, domicilio_fiscal)
            return jsonify({
                "ruc": numero_ruc,
                "razon_social": nombre_contribuyente,
                "direccion": domicilio_fiscal
            }), 200

        except Exception as e:
            return jsonify({"error": "Error al procesar los datos", "detalle": str(e)}), 500
    else:
        return jsonify({"error": mensaje_respuesta}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
