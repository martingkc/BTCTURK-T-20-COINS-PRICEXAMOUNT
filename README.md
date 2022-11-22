# BTCTURK-T-20-COINS-PRICEXAMOUNT



olcumleri to = su anki zaman ve from = to - olcumsuresi(dk)*60(s)*olcumsayisi olarak aliyorum 
bu parametreler sonra url'yi olusturmak icin kullaniliyor 
orn: total hesabinda from = to - 60*60*1 60dklikolcumler*60s*1olcum
olcumlerden alinan dataframeler x axisi uzerinde concatenate ediliyor (axis =1)  pd.concat([df, df2], axis=1) 
pricexamount degeri fiyatin acilis ve kapanis degerlerinin aritmetik ortalamasina gore hesaplaniyor ort. fiyat = (open + close)/2 // ortfiyat*volum
degerleri try karsiliginda olan ve statusu trading olan coinler key'i ismi olan ve degeri total olan bir dictionary'ye 
kaydediliyor sonrasinda bir lambda function ile degerlerine gore siralandiriliyorlar
her iterasyonda en pricexammount degeri en yuksek olan 20 coinin isimleri numlab arrayine kaydediliyor sonrasinda bu array graph'in legendini olusturmak icin kullaniliyor
graphler otomatik olarak filein bulundugu klasore t20-(sayi).png olarak kaydediliyorlar
programin tekrarlama suresi sleeptime variableinin degerini degistirerek ayarlanabilir
(eger deger dusuk olursa btcturkun ddos korumasi siteye erisimi kisitliyor boyle bir durumda iki dk sonra tekrardan denemek gerekiyor) 
eger degerler alinirken terminalde VAL NA degeri cikiyorsa veya index must be an int uyarisi geliyorsa bu ustteki degerden dolayi kaynaklaniyor, bu durumda iki dk bekleyip tekrardan denemeniz gerekiyor
 calistirmadan once >pip install matplotlib ve >pip install pandas komutlarini kullanarak bu iki packagei indirmek gerekiyor 
