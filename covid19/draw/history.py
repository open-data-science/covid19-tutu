from covid19 import draw
from covid19.core import transform


def plot_history(df, country=None, province=None):
    no_country_with_province = country is None and province is not None
    assert not no_country_with_province, 'provice must be set with country'
    df_instance = transform.get_history(df, country=country, province=province)

    days = df_instance.index.tolist()
    amounts = df_instance.Confirmed.values.tolist()

    title = 'Amount confirmed desease'

    title += f' for {country}' if country is not None else ''
    title += f' of {province}' if province is not None else ''

    draw.plot(days, amounts, ticks=(None, 4), title=title, x_label='day', y_label='amounts')
