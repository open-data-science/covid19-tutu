# -*- coding: utf-8 -*-
'''
Visualization of public transport flows and population density
for a dataset provided by Tutu.ru for ODS.AI
License - Creative Commons CC BY-NC-SA 4.0.

Created on Sun Mar 22 18:03:19 2020

@author: Vadym Safronov
'''

from flask import Flask, render_template
import os
import numpy as np
import pandas as pd

app = Flask(__name__)
app._static_folder = os.path.abspath('static/')

@app.route('/')
def home():
    return render_template('OUTPUT.html')

@app.route('/fit')
def fit():
    df = pd.read_csv('../data/full_graph.csv')

    citiesAll = set(df['source'].unique())
    citiesA = set(df[df['transport']=='avia']['source'].unique())
    citiesB = set(df[df['transport']=='train']['source'].unique()) - citiesA
    citiesC = set(df[df['transport']=='bus']['source'].unique()) - citiesA - citiesB

    reference = {}

    for item in citiesA:
        reference[item] = 2

    for item in citiesB:
        reference[item] = 1

    for item in citiesC:
        reference[item] = 0

    df['transport_class'] = df['source'].map(reference, na_action='ignore')


    xf = pd.DataFrame(df[['source', 'source_lat', 'source_lng', 'transport_class',
                      'source_population']].groupby(['source','transport_class']).first())
    xf['city'] = xf.index
    def cutter(trx):
        return trx[0]
    def butter(trx):
        return trx[1]
    xf['ccc'] = xf['city'].apply(cutter)
    xf['bbb'] = xf['city'].apply(butter)
    xf = xf.drop(columns=['city'])

    zf = pd.DataFrame(xf.values, columns=['source_lat', 'source_lng', 'source_population', 'source', 'transport_class'])

    def make_points(data):
        destinations = []
        palette = {0: 'blue', 1: 'red', 2: 'white'}
        for row in data.itertuples():
            size = str(.3 * row[3] / 11514330.0)
            destination = '''
                {
                    lng: ''' + str(row[2]) + ''',
                    lat: ''' + str(row[1]) + ''',
                    size: ''' + size + ''',
                    color: ' ''' + palette[row[5]] + ''' ',
                    radius: ''' + str(.1 + .1*row[5]) + ''',
                    label: ' ''' + str(row[4]) + ''' '
                }
                '''
            destinations.append(destination)
        destinationsAll = ','.join(destinations)
        return destinationsAll

    # get avia destinations 
    af = zf[zf['transport_class']==2]
    airportLocations = make_points(af)

    # trains
    bf = zf[zf['transport_class']!=0]
    airportAndTrainLocations = make_points(bf)

    # buses
    transportLocations = make_points(zf)

    # cleanup for compatibility with the following part
    df = df.drop(columns=['transport_class'])

    df = df[df['transport']=='avia']
    df = df.sort_values(by=['pass_day'])
    df['pass_day_cumsum'] = df['pass_day'].cumsum()
    X = df['pass_day'].sum()
    A = X*.5
    B = X*.8
    def ranker(amount):
        if amount < A:
            return 0
        elif amount < B:
            return 1
        else:
            return 2

    df['class'] = df['pass_day_cumsum'].apply(ranker)

    def fligtArcs(data):
        flights = []
        destinations = []
        op = {0: '.1', 1: '1', 2: '1'}
        palette = {0: 'rgba(255, 255, 255, ', 1: 'rgba(0, 0, 255, ', 2: 'rgba(255, 0, 0, '}
        speed = {0: '0', 1: '5500', 2: '15500'}

        for row in data[data['transport']=='avia'].itertuples():

            item = '''
            {
            startLat: ''' + str(row[5]) + ''',
            startLng: ''' + str(row[6]) + ''',
            endLat: ''' + str(row[7]) + ''',
            endLng: ''' + str(row[8]) + ''',
            color: ' ''' + palette[row[12]] + op[row[12]] + ''')',
            speed: ''' + op[row[12]] + '''
            }
            '''
            flights.append(item)

        return ','.join(flights)

    allFlights = fligtArcs(df)

    pf = df[df['class'] > 0]
    halFlights = fligtArcs(pf)

    rf = df[df['class'] == 2]
    topFlights = fligtArcs(rf)

    file = open('./templates/DUMMY.html')
    contents = file.read()
    file.close()

    XXX = contents.replace('AAAAA', allFlights)
    XXX = XXX.replace('BBBBB', halFlights)
    XXX = XXX.replace('CCCCC', topFlights)
    XXX = XXX.replace('FFFFF', airportLocations)
    XXX = XXX.replace('GGGGG', airportAndTrainLocations)
    XXX = XXX.replace('HHHHH', transportLocations)

    file = open('./templates/OUTPUT.html','w')
    file.write(XXX)
    file.close()

    return render_template('OUTPUT.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)