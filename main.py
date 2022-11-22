import time, requests, json
from collections import defaultdict
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def total(name):
    base = "https://graph-api.btcturk.com"
    to = int(time.time())
    interval = 60
    intervalN = 1
    From = to - 60 * interval * intervalN

    method = "/v1/klines/history?from=" + str(From) + "&resolution=" + str(interval) + "&symbol=" + name + "&to=" + str(
        to)
    uri = base + method
    result = requests.get(uri)
    result = json.loads(result.text)
    return (int(((result['o'][0] + result['c'][0]) / 2) * result['v'][0]))


def getdf(name):
    base = "https://graph-api.btcturk.com"
    to = int(time.time())
    interval = 5
    intervalN = 19
    From = to - 60 * interval * intervalN
    method = "/v1/klines/history?from=" + str(From) + "&resolution=" + str(interval) + "&symbol=" + name + "&to=" + str(
        to)
    uri = base + method
    result = requests.get(uri)
    df = pd.read_json(result.text)

    return df





sleeptime = 60 * 60  # sn olarak aralik belirleme

while (True):
    print('1')
    time.sleep(sleeptime / 60)
    namelab = []
    base = "https://api.btcturk.com"
    method = "/api/v2/server/exchangeinfo"
    uri = base + method
    names = defaultdict(list)

    names.clear()
    result = requests.get(url=uri)
    result = json.loads(result.text)
    coins = result['data']

    for i in coins['symbols']:
        try:
            name = i['name']
            if i['status'] == 'TRADING' and name[len(name) - 1] == 'Y':
                names[name].append(total(name))


        except:
            print('VAL NA')

    names = sorted(names.items(), key=lambda x: x[1], reverse=True)
    print(names)
    df = getdf(names[0][0])
    df = vol = ((df['o'] + df['c']) / 2) * df['v']

    df = df.rename(names[0][0])

    for i in range(1, len(names)):
        df2 = getdf(names[i][0])
        namelab.append(names[i][0])
        df2 = ((df2['o'] + df2['c']) / 2) * df2['v']
        vol = vol.add(df2, fill_value=0)
        if i < 20:
            df = pd.concat([df, df2.rename(names[i][0])], axis=1)

        # OCLHS'de total degerinin ortalama satis ucreti * volum olarak alindigini gordum o yuzden kapanma ve acilma fiyatlarinin basit bir ortalamasini alarak ilerledim
    col = pd.DataFrame()
    for i in range(20):
        col = pd.concat((col, vol), axis=1)



    df = df.fillna(0)
    res = np.divide(*df.align(col, axis=0))
    res = res * 100
    res.columns = df.columns
    res.index = (res.index + 1) * 5
    df.index = (df.index + 1) * 5

    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col, customdata=res[col],
                                 hovertemplate='Val: %{y} <br> Perc: %{customdata}%'))
    fig.show()
    time.sleep(sleeptime)



