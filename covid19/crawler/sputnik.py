import os

import requests
import tqdm
import pandas as pd
import numpy as np


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


def __not_found_mapping():
    return [
        ['Оренбургская область', 'Абдулино'],
        ['Республика Татарстан', 'Арск'],
        ['Кабардино-Балкарская Республика', 'Баксан'],
        ['Калужская область', 'Балабаново'],
        ['Ставропольский край', 'Будённовск'],
        ['Вологодская область', 'Великий Устюг'],
        ['Свердловская область', 'Верхняя Салда'],
        ['Ленинградская область', 'Волхов'],
        ['Кемеровская область', 'Гурьевск'],
        ['Краснодарский край', 'Дагомыс'],
        ['Ивановская область', 'Заволжск'],
        ['Астраханская область', 'Знаменск'],
        ['Тверская область', 'Зубцов'],
        ['Алтайский край', 'Камень-на-Оби'],
        ['Рязанская область', 'Касимов'],
        ['Республика Коми', 'Кослан'],
        ['Краснодарский край', 'Лоо'],
        ['Московская область', 'Луховицы'],
        ['Республика Коми', 'Микунь'],
        ['Нижегородская область', 'Навашино'],
        ['Московская область', 'Ожерелье'],
        ['Республика Коми', 'Печора'],
        ['Ленинградская область', 'Пикалёво'],
        ['Смоленская область', 'Починок'],
        ['Республика Саха (Якутия)', 'Саккырыр'],
        ['Челябинская область', 'Сатка'],
        ['Новгородская область', 'Сольцы'],
        ['Новгородская область', 'Сосновка'],
        ['Республика Коми', 'Сосногорск'],
        ['Тверская область', 'Старица'],
        ['Кабардино-Балкарская Республика', 'Терек'],
        ['Республика Саха (Якутия)', 'Томмот'],
        ['Тверская область', 'Удомля'],
        ['Липецкая область', 'Усмань'],
        ['Краснодарский край', 'Хоста'],
        ['Орловская область', 'Хотынец'],
        ['Чувашская Республика', 'Цивильск'],
        ['Ивановская область', 'Южа'],
    ]


def __replace_nan(df_):
    df = df_.copy(deep=True)
    not_founded_mapping = __not_found_mapping()
    not_founded_mapping = np.array(sorted(not_founded_mapping, key=lambda el: el[1]))
    df = df.sort_values(['City', 'Provinces/State'])
    df.loc[df.isnull()['Provinces/State'], 'Provinces/State'] = not_founded_mapping[:, 0]
    return df


def __build_dataframe(cities, provinces):
    columns = ['City', 'Provinces/State']
    mapping = list(zip(cities, provinces))
    df = pd.DataFrame(mapping, columns=columns)
    return df


def download_provinces(path, cities, progress_bar=True, cache=True):
    if os.path.exists(path) and cache:
        df = pd.read_csv(path)
        return df
    provinces = __download(cities, progress_bar=progress_bar)
    df = __build_dataframe(cities, provinces)
    df = __replace_nan(df)
    df.to_csv(path, index=False)
    return df
