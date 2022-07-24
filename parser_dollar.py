import urllib.request
from xml.dom import minidom

# Напишем процедуру для сбора данных и записи их в «.xml» файл.
def ParseValute():
    url = "http://www.cbr.ru/scripts/XML_daily.asp" # Переменная «url» хранит ссылку на документ с деревом данных
    webFile = urllib.request.urlopen(url)
    data = webFile.read() # Открываем и считываем его
    UrlSplit = url.split("/")[-1] # Далее нам надо сохранить данные в файл на жестком диске. По задумке файл должен иметь такое же название, как и конец URL-адреса, но с расширением «.xml» Для этого сначала по слэшам разбиваем весь URL-адрес и извлекаем его концовку.
    ExtSplit = UrlSplit.split(".")[1]
    FileName = UrlSplit.replace(ExtSplit, "xml") # Затем концовку отсеченной части URL-адреса (XML_daily.asp) заменяем на «.xml»
    with open(FileName, "wb") as localFile: # Теперь открываем/создаём на жестком диске файл, в который записывается информация, полученная с интернет страницы:
        localFile.write(data)
    webFile.close()

def Dollar_Rub():
    dollar_id = "R01235" # Создаём переменную «dollar_id» в которой хранится id Dollara
    doc = minidom.parse("XML_daily.xml") #  Открываем скачанный документ для парсинга
    Valute_Array=doc.getElementsByTagName("Valute") # Создаём список в котором будут хранится все валюты

    for each_Val in Valute_Array:
        Valute_ID= each_Val.getAttribute("ID") # Перебираем этот список и ищем Dollar, путём сравнивания id. 
        if Valute_ID == dollar_id:
            value= each_Val.getElementsByTagName("Value")[0]
            d_value = value.firstChild.data # Если такой id существует, то в переменную value мы кладём значение, лежащее по этому id.
            print(d_value.replace(',', '.'))
            # return value.firstChild.data
            return d_value.replace(',', '.')
           

ParseValute()
dollar_in_float = float(Dollar_Rub())







