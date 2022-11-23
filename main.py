import time, requests, json
from collections import defaultdict
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


#btcturk uzerinde bulunan butun coinlerin listesini veren fonksiyon
def getcoins():
    base = "https://api.btcturk.com"
    method = "/api/v2/server/exchangeinfo"
    uri = base + method
    result = requests.get(url=uri)
    result = json.loads(result.text)
    coins = result['data']
    return coins

#pd dataframe'i formatinda coinlerin istenen bir zaman araliginda ve olcum sikligina gore degerlerini veren fonksiyon
def getdf(name, interval, intervalN):
    base = "https://graph-api.btcturk.com"
    to = int(time.time())
    # interval = 5
    # intervalN = 19
    From = to - 60 * interval * intervalN
    method = "/v1/klines/history?from=" + str(From) + "&resolution=" + str(interval) + "&symbol=" + name + "&to=" + str(
        to)
    uri = base + method
    result = requests.get(uri)
    df = pd.read_json(result.text)

    return df


app = Dash(__name__)
sleeptime = 10  # dk olarak grafik yenileme suresi belirleme

app.layout = html.Div(
    [
        dcc.Graph(id='live-graph',
                  figure={"layout": {
                      "title": "BTCTURK PriceXAmount Graph T-20 Coins",
                      "height": 700,  #700px rastgele bir sekilde belirledim
                  },
                  },
                  ),
        dcc.Interval(
            id='interval-component',
            interval=sleeptime * 60 * 1000, #olcumler arasinda gecen sure [ms]
            n_intervals=1, #baslangicta alinmasi gereken olcum sayisi

        ),
    ]
)


@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_scatter(n):
    names = defaultdict(list) #statusu trading olan coinlerin ve total degerlerinin bulundugu map ( coin_ismi , coin_total )
    names.clear()
    coins = getcoins()

    for i in coins['symbols']:
        try:
            name = i['name']
            if i['status'] == 'TRADING' and name[len(name) - 1] == 'Y':
                tot = getdf(name, 60, 1)    #bir saat onceki olcumu aliyoruz
                tot = (int(((tot['o'][0] + tot['c'][0]) / 2) * tot['v'][0]))  #total hesabini acilik+kapanis fiyati/ 2 * volum olarak hesapladim

                names[name].append(tot)

        except:
            print('VAL NA')

    names = sorted(names.items(), key=lambda x: x[1], reverse=True)  #names dictionarysini coinlerin total degerlerine gore siralayan bir lambda function
    print(names)
    df = getdf(names[0][0], 5, 19)
    df = vol = ((df['o'] + df['c']) / 2) * df['v']

    df = df.rename(names[0][0])
    print(df)
    #coinlerin degerlerinin bulundugu df'in ilk columnunu getdf ile aliyorum sonrasinda asagidaki loop ile diger columnlari y axisi uzerinde sirayla ekliyorum
    for i in range(1, len(names)):
        print('1')
        df2 = getdf(names[i][0], 5, 19)
        df2 = ((df2['o'] + df2['c']) / 2) * df2['v']
        vol = vol.add(df2, fill_value=0) #vol dfsine diger coinlerin total degerlerini topluyorum boylece toplam anlik volumu hesapliyorum
        if i < 20: #sadece total degeri en yuksek olan 20 coini df'ye kaydediyorum
            df = pd.concat([df, df2.rename(names[i][0])], axis=1)

    col = pd.DataFrame()  #df ile ayni boyutta sadece anlik toplam volumden olusan bir 20 x 20 df olusturuyorum her column birbiriyle ayni
    for i in range(20):
        col = pd.concat((col, vol), axis=1)

    df = df.fillna(0) #bazen btcturk degerleri NAN olarak veriyor bu da bazen asagidaki divide fonksiyonunun hata vermesine sebep oluyor bunu engellemek icin df nin nan olan degerlerini 0 ile degistiriyorum
    res = np.divide(*df.align(col, axis=0))  #iki dfyi indexleri uzerinde zorla align ettiriyorum bu adimi atlayinca divide fonksiyonu bazen sacmalayabiliyor
    res = res * 100 #res df'sinde her coinin anlik volumleri var
    res.columns = df.columns #plotlynin customdata ozelliginin dfin her bir elementi icin resden karsiligini vermesi icin indexlerini ve column isimlerini esitliyorum
    res.index = (res.index + 1) * 5
    df.index = (df.index + 1) * 5

    fig = go.Figure()
    for col in df.columns:  #plotly'nin graph object librarysi toplu olarak dfnin her bir columnu icin grafik cizmeme izin vermiyor o yuzden her column icin yeni bir scatter plot ekletiyorum
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col, customdata=res[col],
                                 hovertemplate='Coin: %{name} <br> Val: %{y} <br> Perc: %{customdata}%'))

    fig.update_layout(   #grafigin estetik ayarlari
        title="BTCTURK PriceXAmount Graph T-20 Coins",
        xaxis_title="Time [min]",
        yaxis_title="Price x Amount",
        legend_title="Coins",
    )

    return fig


app.run_server(debug=True, use_reloader=False)


