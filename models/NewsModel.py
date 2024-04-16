from service.DatabaseService import SqLite as Database
from sqlite3 import Error
class NewsModel:

    def __init__(self, news:dict = {}) -> None:
        self.id = news.get("id")
        self.title = news.get("title")
        self.url = news.get("url")
        self.body = news.get("body")
        self.date = news.get("date")
        self.source = news.get("source")
        
    def body_message(self)-> str:
        return f"\n```------- BERITA {self.source} ------\nJudul: {self.title}\nTanggal: {self.date}``````{self.body}```\nLihat selengkapnya: {self.url}"
    
class NewsHandler:
    def __init__(self):
        self.db = Database().db
        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT,news_id INTEGER,news_source TEXT, title TEXT,url TEXT, body TEXT, date TEXT,summarize TEXT,is_send INTEGER default(0))")
        self.db.commit()

    def get_data(self,limit:int = None):
        cursor = self.db.cursor()
        if limit == None:
            sql = "SELECT * FROM news"
        else:
            sql = f"SELECT * FROM news LIMIT {limit}"

        data = cursor.execute(sql)
        data = data.fetchall()
        return [NewsModel(dat) for i,dat in enumerate(data)]
    
    def get_news_baak_id(self,limit:int = None):
        cursor = self.db.cursor()
        if limit == None:
            sql = "SELECT news_id FROM news WHERE news_source='BAAK' ORDER BY id DESC"
        else:
            sql = f"SELECT news_id FROM news WHERE news_source='BAAK' ORDER BY id DESC LIMIT {limit}"
        try:
            data = cursor.execute(sql)
            data = data.fetchall()
            return [dat[0] for i,dat in enumerate(data)]
        except Error as e:
            print(e)
            self.db.rollback()
            return []
        
    
    def get_news_ssite_id(self,limit:int = None):
        cursor = self.db.cursor()
        if limit == None:
            sql = "SELECT news_id FROM news WHERE news_source='STUDENT SITE' ORDER BY id DESC"
        else:
            sql = f"SELECT news_id FROM news WHERE news_source='STUDENT SITE' ORDER BY id DESC LIMIT {limit}"

        try:
            data = cursor.execute(sql)
            data = data.fetchall()
            return [dat[0] for i,dat in enumerate(data)]
        except Error as e:
            print(e)
            self.db.rollback()
            return []

    def add_data(self, datas:list[NewsModel]):
        cursor = self.db.cursor()
        dataIdBaak = self.get_news_baak_id(100)
        dataIdSsite = self.get_news_ssite_id()
        try:
            for i, data in enumerate(datas):
                if data.id != None and ((int(data.id) in dataIdBaak and data.source == "BAAK") or (int(data.id) in dataIdSsite and data.source == "STUDENT SITE")):
                    continue
                else:
                    print(data.id)
                    if data.id == None:
                        cursor.execute("INSERT INTO news (news_source,title,url,body,date) VALUES (?,?,?,?,?)",[data.source,data.title,data.url,data.body,data.date])
                    else :            
                        cursor.execute("INSERT INTO news (news_id,news_source,title,url,body,date) VALUES (?,?,?,?,?,?)",[data.id,data.source,data.title,data.url,data.body,data.date])
        except Error as e:
            print(e)
            self.db.rollback()
            return
        
        self.db.commit()