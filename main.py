import time, base64, hmac, hashlib, requests, json
from collections import defaultdict
import time, base64, hmac, hashlib, requests, json
import matplotlib.pyplot as plt
import pandas as pd

def total(name):
    base = "https://graph-api.btcturk.com"
    To = int(time.time())
    From = (To - 3600 * 24)
    method = "/v1/ohlcs?pair=" + name + "&from=" + str(From) + "&to=" + str(To)
    uri = base + method
    result = requests.get(uri)
    result = json.loads(result.text)
    result = result[0]
    total = result['total']
    return total

def getdf(name): 
    base = "https://graph-api.btcturk.com"
    to = int(time.time())
    interval = 5
    From = to-5*60*20
    to = str(to)
    From = str(From)
    method = "/v1/klines/history?from="+From + "&resolution="+str(interval)+"&symbol="+name+"&to="+ to
    uri = base+method
    result = requests.get(uri)
    df = pd.read_json(result.text)
    
    return df
    
   

base = "https://api.btcturk.com"
method = "/api/v2/server/exchangeinfo"
uri = base+method

count = 0
while(True):
    names = defaultdict(list)
    plt.style.use('ggplot')
    names.clear()
    result = requests.get(uri)
    result = json.loads(result.text)
    coins = result['data']
    for i in coins['symbols']:
        try:
            name = i['name']
            if i['status']=='TRADING' and name[len(name)-1] == 'Y':
                
                names[name].append(int(total(name)))
               
        except: 
            print('VAL NA')
    names = sorted(names.items(), key=lambda x: x[1], reverse=True)   
    print(names)
    #df1 = getdf(names[0][0]) 
    #df1 = df1['v']*df1['o']    
    #ax = df1.plot(label=names[1][0])

    for i in range(20): 
        df2 =getdf(names[i][0])
        df2 = ((df2['o']+df2['c'])/2)*df2['v'] #OCLHS'de total degerinin ortalama satis ucreti * volum olarak alindigini gordum o yuzden kapanma ve acilma fiyatlarinin basit bir ortalamasini alarak ilerledim 
        df2.plot(label=names[i][0])
       
    plt.legend()
    fname = 't20'+str(count)+'.png'
    plt.savefig(fname)
    count += 1
    time.sleep(60*60)
