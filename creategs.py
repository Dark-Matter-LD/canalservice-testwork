# Подключаем библиотеки
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	

CREDENTIALS_FILE = 'credentials.json'  # Имя файла с закрытым ключом
spreadsheet_id = '1bvZhdFkpw0HIou-I6KkdXUrjr-VSgOyIaTyil7Xez-M' # id 

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

def createsheet():
    spreadsheet = service.spreadsheets().create(body = {
        'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                'sheetId': 0,
                                'title': 'Лист номер один',
                                'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
    }).execute()
    spreadsheet_id = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
    print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)

    # Даем доступ юзеру с правами редактирования
    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId = spreadsheet_id,
        body = {'type': 'user', 'role': 'writer', 'emailAddress': 'irbispro10@gmail.com'},  # Открываем доступ на редактирование
        fields = 'id'
    ).execute()

# Чтобы отслеживать изменения в гугл-таблице нам необходимо воспользоваться Apps Script (зайти туда можно с гугл-таблицы: 
# Расширения - Apps Script) и написать там функцию в редакторе, но чтобы запустить этот скрипт нужно передать 
# права владения с сервисного аккаунта на пользовательский. Для этого отправим запрос на смену владельца 
# (после выполнения переменной update придет письмо на почту, указанную в переменной access , далее нужно открыть таблицу, 
# перейти в настройки доступа и там принять запрос на смену владельца)
    update = driveService.permissions().update(
            fileId = spreadsheet_id,
            permissionId = access.get('id'),
            body = {'role': 'writer', 'pendingOwner': True},  

        ).execute()
    
createsheet()

#После выполнения функции createsheet в терминале будет ссылка, из этой ссылки копируем значение после "https://docs.google.com/spreadsheets/d/"
# и вставляем это в переменную spreadsheet_id (она находится вначале этого файла). 
# Комментируем выполнение функции createsheet() и запускаем скрипт еще раз. Переходим по ссылке из терминала.


# Добавляем входные данные в гугл-таблицу из тестового задания

def add_data():
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheet_id, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "Лист номер один!A1:D14",
            "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
            "values": [
                        ["№", "заказ №", "стоимость, $", "срок поставки"], # Заполняем первую строку
                        ['1', "1182407", "214", "13.05.2022"], 
                        ['2', "1120833", "610", "05.05.2022"],
                        ['3', "1135907", "682", "02.05.2022"], 
                        ['4', "1235370", "1330", "05.05.2022"],
                        ['5', "1329994", "646", "12.05.2022"],
                        ['6', "1876515", "1335", "15.05.2022"],
                        ['7', "1835607", "1227", "05.05.2022"],
                        ['8', "1465034", "719", "12.05.2022"],
                        ['9', "1077923", "508", "01.06.2022"],
                        ['10', "1682035", "1867", "09.05.2022"],
                        ['11', "1686040", "129", "01.06.2022"],
                        ['12', "1888432", "388", "11.05.2022"],
                        ['13', "1938886", "1021", "03.05.2022"],
                    ]}
        ]
    }).execute()

add_data()

