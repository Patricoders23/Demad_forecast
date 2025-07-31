import requests
import pandas as pd

def get_renewable_penetration(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Descarga datos de penetración de energías renovables (demanda relativa).
    """

    base_url = "https://apidatos.ree.es/es/datos/demanda/penetracion-renovable"
    params = {
        "start_date": f"{start_date}T00:00",
        "end_date": f"{end_date}T23:59",
        "time_trunc": "hour",
        "geo_limit": "peninsular"
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    data = response.json()
    values = data['included'][0]['attributes']['values']

    df = pd.DataFrame(values)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.rename(columns={'value': 'penetracion_renovable'}, inplace=True)

    return df
