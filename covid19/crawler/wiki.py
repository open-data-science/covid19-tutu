import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


def __extract_date(l):
    d = l[0].split(' ')[-1]
    f = '/'.join(d.split('.')[:-1])
    return f


def __extract_raw_table(content):
    l = content.split('\n')
    return list(filter(lambda el: len(el) > 0, l))


def __filter_cond(i, n):
    return i < 3 or i >= n - 3


def __build_dataframe(table, columns):
    df = pd.DataFrame.from_dict(table)
    df.columns = columns

    df['Province'] = df['Province'].astype(str)
    df['Deaths'] = df['Deaths'].astype(int)
    df['Confirmed'] = df['Confirmed'].astype(int)
    df['Recovered'] = df['Recovered'].astype(int)
    df['Sick'] = df['Sick'].astype(int)

    sick = df['Confirmed'] - df['Deaths'] - df['Recovered']
    assert df[sick != df['Sick']].shape[0] == 0, 'Invalid wikipedia data'
    df = df.drop('Sick', axis=1)

    df['Country\Region'] = 'Russia'
    return df


def __extractor(soup):
    tags = soup.find_all('table')
    n = len(tags)

    columns = ['Province', 'Confirmed', 'Deaths', 'Recovered', 'Sick', 'Date']
    table = [[]]
    for i, content in enumerate(tags):
        if __filter_cond(i, n):
            continue
        raw_data = content.get_text()
        raw_table = __extract_raw_table(raw_data)
        date = __extract_date(raw_table)
        raw_table = raw_table[6:]
        for j, el in enumerate(raw_table):
            table[-1].append(el)
            if (j + 1) % 5 != 0:
                continue
            table[-1].append(date)
            table.append([])
    table = table[:-1]
    df = __build_dataframe(table, columns)
    return df


def download_russia_desease(path, cache=True):
    if os.path.exists(path) and cache:
        df = pd.read_csv(path)
        return df
    url = 'https://ru.wikipedia.org/wiki/Распространение_COVID-19_в_России#cite_note-sptbl5b-60'
    resp = requests.get(url)
    soup = BeautifulSoup(resp._content.decode('utf-8'), 'html.parser')
    df = __extractor(soup)
    df.to_csv(path, index=False)
    return df
