import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import time

from parser_dollar import dollar_in_float

while True:
    def gsheet2df(spreadsheet_name, sheet_num):
 
        try:
            #Определяем объем вызова, который будет взаимодействовать с google диском и указываем путь к json-у с уч.данными
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            credentials_path = 'credentials.json'

            # Извлекаем уч.данные и используем их для авторизации к googlesheets
            credentials = sac.from_json_keyfile_name(credentials_path, scope)
            client = gspread.authorize(credentials)
            
            #Открываем таблицу, выбираем лист и достаем все данные в виде словаря, словарь же преобразуем в dataframe
            sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records()
            df =  pd.DataFrame.from_dict(sheet)
            
            col_price_in_dollar = df.loc[:, 'стоимость, $'] #Из dataframe берем нужную нам колонку при помощи метода loc
            col_price_in_rubles = col_price_in_dollar * float(dollar_in_float) # Вычисляем стоимость в рублях 
            list = col_price_in_rubles.values.tolist() # Записываем значения в словарь, чтобы далее добавить в dataframe 
            df.insert(3, 'стоимость, руб.', list) # Добавляем столбец стоимость в рублях в dataframe
            print(df)

            
        except:
            print('Возникла ошибка')

    #Подсоединяемся к базе данных postgres через sqlalchemy: ('СУБД//username://password@address/dbname')

    # Записываем dataframe в Postgres: сначала удаляем старую таблицу, затем создаем новую. 
        try:
            engine = create_engine('postgresql://postgres:balkonchik@127.0.0.1:5432/googlesheets')
            
            df.to_sql(
                'googlesheets', 
                engine,
                schema=None,
                if_exists='replace', #'fail'
                index=False,
                index_label=None,
                chunksize=None,
                dtype=None,
                method=None)

            return df.head() 

        except: 
            print('Возникла ошибка')
    
    time.sleep(5)
    gsheet2df('test1', 0)

























# def create_database(connection, query):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Query executed successfully")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")

# create_database_query = "CREATE DATABASE sheet1"
# create_database(connection, create_database_query)

# connection = create_connection(
#     "sheet1", "postgres", "balkonchik", "127.0.0.1", "5432"
# )

