import requests
import pandas as pd

def get_aemet_weather(api_key: str, station_id: str, date: str) -> pd.DataFrame:
    """
    Descarga datos diarios de meteorología desde la AEMET para una estación.
    Estación: código AEMET (ej. '3195' para Madrid-Retiro).
    Fecha en formato 'YYYY-MM-DD'.
    """
    # Paso 1: Construir la URL del primer paso (metadatos)
    url = (
        f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/"
        f"datos/fechaini/{date}T00:00:00UTC/fechafin/{date}T23:59:59UTC/"
        f"estacion/{station_id}/?api_key={api_key}"
    )

    # Paso 2: Obtener la URL real de descarga
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"❌ Error al consultar la API de AEMET: {response.status_code}")

    data_url = response.json().get("datos")
    if not data_url:
        raise Exception("❌ No se encontró la URL de datos en la respuesta.")

    # Paso 3: Descargar los datos reales
    data_response = requests.get(data_url, headers=headers)
    if data_response.status_code != 200:
        raise Exception(f"❌ Error al descargar los datos meteorológicos: {data_response.status_code}")

    #df = pd.read_json(data_response.content)
    df = pd.read_json(data_response.text)


    return df
