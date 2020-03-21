import pandas as pd


def __extract_population(df, country):
    if country is None:
        populations = df.groupby('Country/Region')['Country population'].mean()
        return populations.sum()
    mask = df['Country/Region'] == country
    return df[mask]['Country population'].iloc[0]


def __calc_hist(df_):
    population = __extract_population(df_, None)
    df_ = df_.groupby(['Type']).sum().reset_index().sort_values('Type').T
    df_.columns = df_.iloc[0]
    df_ = df_.iloc[1:]
    df_['Population'] = population
    return df_.iloc[:-1]


def __calc_country_hist(df_, country):
    population = __extract_population(df_, country)
    df_country = df_.groupby(['Country/Region', 'Type']).sum().reset_index()
    df_country = df_country[df_country['Country/Region'] == country].sort_values('Type').T
    df_country.columns = df_country.iloc[1]
    df_country = df_country.iloc[2:]
    df_country['Population'] = population
    return df_country.iloc[:-1]


def __calc_province_hist(df_, country, province):
    df_province = df_.dropna()
    mask_country = df_province['Country/Region'] == country
    mask_province = df_province['Province/State'] == province
    mask = mask_country & mask_province
    inds = ['Province/State', 'Country/Region', 'Type']
    df_province = df_province[mask].set_index(inds).reset_index()
    df_province = df_province.sort_values('Type').T
    df_province.columns = df_province.iloc[2]
    df_province = df_province.iloc[3:]
    df_province['Population'] = float('NaN')
    return df_province.iloc[:-1]


def get_history(df, country=None, province=None):
    no_country_with_province = country is None and province is not None
    assert not no_country_with_province, 'provice must be set with country'
    df_ = df[df.columns[4:].tolist() + df.columns[:2].tolist()]
    if country is None:
        return __calc_hist(df_)
    if province is None:
        return __calc_country_hist(df_, country)
    return __calc_province_hist(df_, country, province)


def get_countries(df):
    return pd.DataFrame(df['Country/Region'].unique(), columns=['Country/Region'])


def get_provinces(df):
    return df.dropna()[['Province/State', 'Country/Region']]
