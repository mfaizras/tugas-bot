from service.DatabaseService import SqLite as Database
from sqlite3 import Error
import dateutil.parser as parser
import dateutil.tz as tz
import datetime
import os
from dotenv import load_dotenv
import pytz

class TugasDataHandler:
    def __init__(self,tugas:tuple):
        load_dotenv()
        date = tugas[6]
        splittedDate = date.split(",")

        date = parser.parse(date)

        self.id = tugas[0]
        self.assignment_id = tugas[1]
        self.assignment_source = tugas[2]
        self.title:str = tugas[3]
        self.course_name:str = tugas[4]
        self.description:str = tugas[5]
        self.deadline:str = date.isoformat()
        self.assignment_url:str = tugas[7]

class NotifyModel:
    def __init__(self) -> None:
        load_dotenv()
        self.db = Database().db
        cursor = self.db.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS notify (id INTEGER PRIMARY KEY AUTOINCREMENT,assignment_id INTEGER,date TEXT, send_at TEXT")
        except Error as e:
            print(e)
        self.db.commit()

    def get_all_data(self, limit:int = None)->list:
        cursor = self.db.cursor()

        if limit == None:
            sql = "SELECT * FROM tugas ORDER BY id DESC"
        else:
            sql = f"SELECT * FROM tugas ORDER BY id DESC LIMIT {limit}"

        data = cursor.execute(sql)
        datas = data.fetchall()
        return [TugasDataHandler(dat) for i,dat in enumerate(datas)]
    
    def get_upcoming_tugas(self):
        cursor = self.db.cursor()
        timeNow = datetime.datetime.now(pytz.timezone(os.getenv('TIMEZONE'))).replace(tzinfo=None)
        # timeNow = pytz.timezone(os.getenv('TIMEZONE')).localize(timeNow)
        timeNow = timeNow.isoformat()

        sql = f"SELECT * FROM tugas WHERE deadline > '{timeNow}'"

        try:
            data = cursor.execute(sql)
            datas = data.fetchall()
            return [TugasDataHandler(dat) for i,dat in enumerate(datas)]
        except Error as e:
            print(e)
            return []
        
    def get_tugas_not_send(self):
        cursor = self.db.cursor()

        sql = f"SELECT * FROM tugas WHERE is_send = 0"

        try:
            data = cursor.execute(sql)
            datas = data.fetchall()
            return [TugasDataHandler(dat) for i,dat in enumerate(datas)]
        except Error as e:
            print(e)
            return []
    
    def get_assignment_id(self,limit:int = None):
        cursor = self.db.cursor()
        if limit == None:
            sql = "SELECT assignment_id FROM tugas DESC"
        else:
            sql = f"SELECT assignment_id FROM tugas DESC LIMIT {limit}"

        data = cursor.execute(sql)
        data = data.fetchall()
        return [dat[0] for i,dat in enumerate(data)]
    
    def add_data(self, datas:list[TugasDataHandler]):
        cursor = self.db.cursor()
        dataId = self.get_assignment_id(100)
        newData = []
        try:
            for i, data in enumerate(datas):
                if data.assignment_id != None and ((int(data.assignment_id) in dataId and data.assignment_source == "VCLASS") or (int(data.assignment_id) in dataId and data.assignment_source == "IFLAB")):
                    continue
                if data.assignment_id == None:
                    cursor.execute("INSERT INTO tugas (assignment_source,title,course_name,description,deadline,assignment_url) VALUES (?,?,?,?,?,?)",[data.assignment_source,data.title,data.course_name,data.description,data.deadline,data.assignment_url])
                else :            
                    cursor.execute("INSERT INTO tugas (assignment_id,assignment_source,title,course_name,description,deadline,assignment_url) VALUES (?,?,?,?,?,?,?)",[data.assignment_id,data.assignment_source,data.title,data.course_name,data.description,data.deadline,data.assignment_url])

                newData.append(data)
        except Error as e:
            print(e)
        
        self.db.commit()

    def update_notified(self, datas:list[TugasDataHandler]):
        cursor = self.db.cursor()
        for i, data in enumerate(datas):
            print(data.id)
            cursor.execute(f"UPDATE tugas SET is_send = 1 WHERE id = {int(data.id)}")
        self.db.commit()

        




