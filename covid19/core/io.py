import pandas as pd

from covid19.crawler import sputnik


def add_meta_fields(df, t):
    df_ = df.copy(deep=True)
    df_['Name'] = df_['Country/Region'] + '--' + df_['Province/State'].fillna('')
    df_['Type'] = t
    df_ = df_.set_index('Name')
    return df_


def get_fnames(names):
    if names is None:
        names = {}
    confirmed = 'time_series_19-covid-Confirmed.csv'
    if 'confirmed' in names:
        confirmed = names['confirmed']

    recovered = 'time_series_19-covid-Recovered.csv'
    if 'recovered' in names:
        recovered = names['recovered']
    deapths = 'time_series_19-covid-Deaths.csv'
    if 'deapths' in names:
        deapths = names['deapths']
    return confirmed, recovered, deapths


def read_frames(path, confirmed, recovered, deapths):
    df_c = pd.read_csv(path + confirmed, encoding='utf8')
    df_r = pd.read_csv(path + recovered, encoding='utf8')
    df_d = pd.read_csv(path + deapths, encoding='utf8')

    df_c = add_meta_fields(df_c, 'Confirmed')
    df_r = add_meta_fields(df_r, 'Recovered')
    df_d = add_meta_fields(df_d, 'Deaths')
    df = pd.concat([df_c, df_r, df_d])
    df = df.reset_index()
    df = df[df.columns[1:]]
    return df


def rename_columns(df):
    dates = list(map(lambda el: '/'.join(el.split('/')[:-1]), df.columns[4:-1]))
    prefix = df.columns[:4].tolist()
    suffix = df.columns[-1:].tolist()
    df_ = df.copy(deep=True)
    df_.columns = prefix + dates + suffix
    return df_


def read_covid(path, names=None):
    confirmed, recovered, deapths = get_fnames(names)
    df = read_frames(path, confirmed, recovered, deapths)
    df = rename_columns(df)
    return df


def read_population(path):
    mapping = {
        'Macedonia, FYR': 'North Macedonia',
        'Slovak Republic': 'Slovakia',
        'Brunei Darussalam': 'Brunei',
        'Egypt, Arab Rep.': 'Egypt',
        'United States': 'US',
        'Iran, Islamic Rep.': 'Iran',
        'Korea, Dem. People’s Rep.': 'Korea, South',
        'Czech Republic': 'Czechia',
        'Russian Federation': 'Russia',
        'Congo, Dem. Rep.': 'Congo (Kinshasa)',
        'Venezuela, RB': 'Venezuela',
        'St. Lucia': 'Saint Lucia',
        'St. Vincent and the Grenadines': 'Saint Vincent and the Grenadines',
        'Congo, Rep.': 'Congo (Brazzaville)',
        'Kyrgyz Republic': 'Kyrgyzstan',
    }
    population = pd.read_csv(path, sep=',')
    population = population[['Country', 'Year_2016']]
    population.columns = ['Country/Region', 'Country population']
    population['Country/Region'] = population['Country/Region'].replace(mapping)
    return population


def read_cities(path, cache_provinces_path, cache_provinces=True, progress_bar=True):
    df_cities = pd.read_csv(path)
    df_cities.columns = ['Lat', 'Long', 'City', 'osm_accuracy', 'City population']
    df_cities = df_cities.drop(['osm_accuracy'], axis=1)
    cities = df_cities['City'].values.tolist()
    cache = cache_provinces
    cache_path = cache_provinces_path
    pb = progress_bar
    provinces = sputnik.download_provinces(path=cache_path, cities=cities, progress_bar=pb, cache=cache)
    df_cities['Provinces/State'] = provinces['Provinces/State']
    return df_cities
