import os
import time
import gspread
import mysql.connector
from oauth2client.service_account import ServiceAccountCredentials
import sys

class SYM:

    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
    MYSQL_PORT = os.environ.get('MYSQL_PORT')
    SPREADSHEETS = os.environ.get('SPREADSHEETS')

    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            f'{os.path.abspath(os.path.dirname(__file__))}/credentials.json', scope)
        self.client = gspread.authorize(credentials)
        self.spreadsheets = os.environ.get('SPREADSHEETS').split(',')
        self.db_conn = mysql.connector.connect(
            host=self.MYSQL_HOST,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            database=self.MYSQL_DATABASE,
            port=self.MYSQL_PORT)
        
    def getSpreadsheetsData(self):
        try:
            data = []
            for spreadsheet in self.spreadsheets:
                spreadsheet_obj = self.client.open(spreadsheet)
                for worksheet in spreadsheet_obj.worksheets():
                    worksheet_obj = spreadsheet_obj.worksheet(worksheet.title)
                    keys = []
                    for idx,row in enumerate(worksheet_obj.get_all_values()):
                        if idx == 0:
                            keys = [ x for x in row if idx == 0 ]
                        else:
                            values = [ x for x in row if idx > 0 ]
                            value = float(dict(zip(keys,values))['value'])
                            date = dict(zip(keys,values))['date']
                            _dict = dict(zip(keys,values))
                            del _dict['value']
                            del _dict['date']
                            _dict['date'] = date
                            _dict['value'] = value
                            _dict['necessary'] = bool(_dict['date'])
                            data.append(_dict)
            return data
        except Exception as err:
            print(f'Error: {err}')
            print('It is possible that your sheet has a inconsistent date.')
            sys.exit(1)

    def deleteData(self):
        cursor = self.db_conn.cursor()
        cursor.execute('delete from amounts')
        cursor.execute('ALTER TABLE amounts AUTO_INCREMENT = 1')

    def insertData(self):
        self.deleteData()
        cursor = self.db_conn.cursor()
        data = self.getSpreadsheetsData()
        for row in data:
            sql = "INSERT INTO amounts \
                (name,category,method,necessary,date,value,amount_type) \
                values ('{}','{}','{}',{},'{}',{}, '{}')".format(
                row['name'],row['category'],row['method'],row['necessary'],row['date'],row['value'],row['type'])
            cursor.execute(sql)
        self.db_conn.commit()
        cursor.close()

while True:
    sym = SYM()
    sym.insertData()
    sym.db_conn.close()
    time.sleep(30)