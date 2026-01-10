import requests
import traceback
import re
from bs4 import BeautifulSoup
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def extraer_contenido_entre_tags(cadena, posicion, nombre_inicio, nombre_fin, sensitivo=False):
    cadena_modificada = cadena.lower() if sensitivo else cadena
    nombre_inicio = nombre_inicio.lower() if sensitivo else nombre_inicio
    nombre_fin = nombre_fin.lower() if sensitivo else nombre_fin
    posicion_inicio = cadena_modificada.find(nombre_inicio, posicion)
    if posicion_inicio > -1:
        posicion_inicio += len(nombre_inicio)
        posicion_fin = cadena_modificada.find(nombre_fin, posicion_inicio)
        if posicion_fin > -1:
            return cadena[posicion_inicio:posicion_fin]
    return ""


def obtener_datos_ruc(contenido_html):
    try:
        soup = BeautifulSoup(contenido_html, 'html.parser')
        tabla = soup.find('table', {'class': 'form-table'})
        if tabla:
            datos_ruc = {}
            filas = tabla.find_all('tr')
            for fila in filas:
                columnas = fila.find_all('td')
                if len(columnas) == 2:
                    clave = columnas[0].text.strip()
                    valor = columnas[1].text.strip()
                    datos_ruc[clave] = valor
            return datos_ruc
        return None
    except Exception as e:
        print(f"Error al obtener datos del RUC: {e}")
        return None


def consultar_contenido_ruc(sesion, url_referencia, numero_ruc, numero_random):
    headers = {
        'Host': 'e-consultaruc.sunat.gob.pe',
        'Origin': 'https://e-consultaruc.sunat.gob.pe',
        'Referer': url_referencia,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    payload = {
        'accion': 'consPorRuc',
        'nroRuc': numero_ruc,
        'numRnd': numero_random
    }
    response = sesion.post(url_referencia, headers=headers, data=payload, verify=True)
    contenido_html = response.text
    if response.status_code == 200:
        if "El RUC ingresado no existe" in contenido_html:
            return "E", f"El RUC {numero_ruc} no existe en la base de datos de la SUNAT.", None
        else:
            datos_ruc = obtener_datos_ruc(contenido_html)
            if datos_ruc:
                return "C", datos_ruc, None
            else:
                return "E", "No se pudieron obtener los datos del RUC.", None
    else:
        return "E", f"Ocurrió un error al consultar el RUC {numero_ruc}. Código de estado: {response.status_code}", response.status_code


def consultar_ruc(numero_ruc):
    try:
        url_inicial = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
        headers = {
            'Host': 'e-consultaruc.sunat.gob.pe',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
        sesion = requests.Session()
        response = sesion.get(url_inicial, headers=headers, verify=True)
        if response.status_code == 200:
            numero_dni = "12345678"
            url = (
                f"https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorTipdoc&razSoc=&nroRuc=&nrodoc={numero_dni}"
                f"&contexto=ti-it&modo=1&search1=&rbtnTipo=2&tipdoc=1&search2={numero_dni}&search3=&codigo="
            )
            contenido_html = ""
            n_intentos = 0
            codigo_estado = 401
            while n_intentos < 3 and codigo_estado == 401:
                response = sesion.post(url, headers=headers, verify=True)
                codigo_estado = response.status_code
                contenido_html = response.text
                n_intentos += 1
            if codigo_estado == 200:
                numero_random = extraer_contenido_entre_tags(contenido_html, 0, "name=\"numRnd\" value=\"", "\">")
                n_intentos = 0
                codigo_estado = 401
                while n_intentos < 3 and codigo_estado == 401:
                    tipo_respuesta, mensaje_respuesta, codigo_estado = consultar_contenido_ruc(sesion, url_inicial,
                                                                                               numero_ruc,
                                                                                               numero_random)
                    n_intentos += 1
            else:
                mensaje_respuesta = f"Ocurrió un inconveniente ({response.status_code}) al consultar el número ramdom del RUC {numero_ruc}.\r\nDetalle: {contenido_html}"
        else:
            mensaje_respuesta = f"Ocurrió un inconveniente ({response.status_code}) al consultar la página principal con el RUC {numero_ruc}.\r\nDetalle: {response.text}"
    except Exception as e:
        tbinfo = traceback.format_exc()
        mensaje_respuesta = f"Error al intentar consultar el RUC {numero_ruc}:\r\n{tbinfo}"
        tipo_respuesta = "E"
    return tipo_respuesta, mensaje_respuesta
