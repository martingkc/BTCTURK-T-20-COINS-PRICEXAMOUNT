import time, base64, hmac, hashlib, requests, json
from collections import defaultdict
import time, base64, hmac, hashlib, requests, json
import matplotlib.pyplot as plt
import pandas as pd
def getklinedata(name, interval, Ninterval):
    base = "https://graph-api.btcturk.com"
    to = int(time.time())
    From = to-60*interval*Ninterval
    method = "/v1/klines/history?from="+str(From) + "&resolution="+str(interval)+"&symbol="+name+"&to="+ str(to)
    uri = base + method
    result = requests.get(uri)
    
    return result

def total(name):
    result = getklinedata(name, 60, 1)
    result = json.loads(result.text)
    return (int(((result['o'][0]+result['c'][0])/2)*result['v'][0]))

def getdf(name): 
    result = getklinedata(name, 5, 20)
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
            if i['status']=='TRADING':
                
                names[name].append(int(total(name)))
               
        except: 
            print('VAL NA')
    names = sorted(names.items(), key=lambda x: x[1], reverse=True)   
    print(names)
    
    for i in range(20): 
        df2 =getdf(names[i][0])
        df2 = ((df2['o']+df2['c'])/2)*df2['v'] #OCLHS'de total degerinin ortalama satis ucreti * volum olarak alindigini gordum o yuzden kapanma ve acilma fiyatlarinin basit bir ortalamasini alarak ilerledim 
        df2.plot(label=names[i][0])
    plt.legend()
    plt.grid()
    plt.title("BTCTURK T-20 priceXamount")
    fname = 't20'+str(count)+'.png'
    plt.savefig(fname)
    count += 1
    time.sleep(60*60)

