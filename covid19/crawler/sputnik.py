import os

import requests
import tqdm
import pandas as pd


def __extract_province(d):
    try:
        return d['result']['address'][0]['features'][0]['properties']['address_components'][1]['value']
    except:
        return ''


def __download(cities, limit=None, progress_bar=True):
    provinces = []
    url = 'http://search.maps.sputnik.ru/search/addr'
    for city in tqdm.tqdm(cities, desc='downloading provinces', disable=not progress_bar):
        try:
            resp = requests.get(f'{url}?q=%s' % city).json()
        except:
            provinces.append('')
            continue
        provinces.append(__extract_province(resp))
        if limit is not None and len(provinces) == limit:
            break
    return provinces


def download_provinces(path, cities, progress_bar=True, cache=True):
    if os.path.exists(path) and cache:
        df = pd.read_csv(path)
        return df

    provinces = __download(cities, progress_bar=progress_bar)

    columns = ['City', 'Provinces/State']
    mapping = list(zip(cities, provinces))
    df = pd.DataFrame(mapping, columns=columns)
    df.to_csv(path, index=False)
    return df
