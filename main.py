import time, requests, json
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
# olcumleri to = su anki zaman ve from = to - olcumsuresi(dk)*60(s)*olcumsayisi olarak aliyorum 
#bu parametreler sonra url'yi olusturmak icin kullaniliyor 
#orn: total hesabinda from = to - 60*60*1 60dklikolcumler*60s*1olcum
#olcumlerden alinan dataframeler x axisi uzerinde concatenate ediliyor (axis =1)  pd.concat([df, df2], axis=1) 
#pricexamount degeri fiyatin acilis ve kapanis degerlerinin aritmetik ortalamasina gore hesaplaniyor ort. fiyat = (open + close)/2 // ortfiyat*volum
#degerleri try karsiliginda olan ve statusu trading olan coinler key'i ismi olan ve degeri total olan bir dictionary'ye 
#kaydediliyor sonrasinda bir lambda function ile degerlerine gore siralandiriliyorlar
#her iterasyonda en pricexammount degeri en yuksek olan 20 coinin isimleri numlab arrayine kaydediliyor sonrasinda bu array graph'in legendini olusturmak icin kullaniliyor
#graphler otomatik olarak filein bulundugu klasore t20-(sayi).png olarak kaydediliyorlar
#programin tekrarlama suresi sleeptime variableinin degerini degistirerek ayarlanabilir
#(eger deger dusuk olursa btcturkun ddos korumasi siteye erisimi kisitliyor boyle bir durumda iki dk sonra tekrardan denemek gerekiyor) 
#eger degerler alinirken terminalde VAL NA degeri cikiyorsa veya index must be an int uyarisi geliyorsa bu ustteki degerden dolayi kaynaklaniyor, bu durumda iki dk bekleyip tekrardan denemeniz gerekiyor
# calistirmadan once >pip install matplotlib ve >pip install pandas komutlarini kullanarak bu iki packagei indirmek gerekiyor 



def total(name):
    base = "https://graph-api.btcturk.com"
    to = int(time.time())
    interval = 60
    intervalN = 1
    From = to-60*interval*intervalN
    
    method = "/v1/klines/history?from="+str(From) + "&resolution="+str(interval)+"&symbol="+name+"&to="+ str(to)
    uri = base + method
    result = requests.get(uri)
    result = json.loads(result.text)
    return (int(((result['o'][0]+result['c'][0])/2)*result['v'][0]))

def getdf(name): 
    base = "https://graph-api.btcturk.com"
    to = int(time.time())
    interval = 5
    intervalN = 19
    From = to-60*interval*intervalN
    method = "/v1/klines/history?from="+str(From) + "&resolution="+str(interval)+"&symbol="+name+"&to="+ str(to)
    uri = base + method
    result = requests.get(uri)
    df = pd.read_json(result.text)
    
    return df
    
   


sleeptime = 60*60 #sn olarak aralik belirleme

plt.figure(figsize=(11,11))
plt.title("BTCTURK T-20 priceXamount TRY")
def update(i):
    namelab = []
    base = "https://api.btcturk.com"
    method = "/api/v2/server/exchangeinfo"
    uri = base+method
    names = defaultdict(list)
    plt.style.use('ggplot')
    names.clear()
    result = requests.get(url =uri)
    result = json.loads(result.text)
    coins = result['data']
    for i in coins['symbols']:
        try:
            name = i['name']
            if i['status']=='TRADING' and name[len(name)-1] == 'Y':
                names[name].append(total(name))
               
        except:
            print('VAL NA')
    names = sorted(names.items(), key=lambda x: x[1], reverse=True)   
    print(names)
    namelab.append(names[0][0])
    df = getdf(names[0][0])
    
    df = ((df['o']+df['c'])/2)*df['v']
    
    for i in range(1,20): 
        df2 =getdf(names[i][0])
        namelab.append(names[i][0])
        df2 = ((df2['o']+df2['c'])/2)*df2['v']
        df = pd.concat([df, df2], axis=1)
        #OCLHS'de total degerinin ortalama satis ucreti * volum olarak alindigini gordum o yuzden kapanma ve acilma fiyatlarinin basit bir ortalamasini alarak ilerledim 
    print(df) 
    plt.cla()
   
    lines = plt.plot( df)
    plt.legend(iter(lines), namelab,loc='upper right')
    
    
    plt.grid()
    plt.tight_layout()

    
    
    
ani = FuncAnimation(plt.gcf(), update, interval=sleeptime*1000) 

plt.tight_layout()
plt.show()

