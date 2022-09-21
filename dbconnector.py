import pyodbc
from dotenv import load_dotenv
import os
load_dotenv()


class BaseObject:
    def __init__(self, ServerName, Responsible):
        self.serverName = ServerName
        self.responsible = Responsible


def GetWrongDefinitions(Standart, LikeQuery):
    result = []
    conn = pyodbc.connect(os.getenv("CONNECTION_STRING"))
    cursor = conn.cursor()
    cursor.execute(os.getenv("SQL_QUERY").format(standart = Standart, likeQuery = LikeQuery))
    for i in cursor:
        obj = BaseObject(i[0], i[2])
        result.append(obj)

    return result


def loadStandarts():
    result = []

    result.append(os.getenv("UYGULAMA_STANDART"))
    result.append(os.getenv("VERITABANI_STANDART"))
    result.append(os.getenv("DREAM_STANDART"))
    result.append(os.getenv("TURIZM_STANDART"))
    result.append(os.getenv("DIJITALCOZUM_STANDART"))
    result.append(os.getenv("MOBILITE_STANDART"))
    result.append(os.getenv("DEPOLAMA_STANDART"))
    result.append(os.getenv("BILGI_STANDART"))

    return result



#print(GetWrongDefinitions("DT-Uygulama Yonetimi", "uyg")[0].serverName)

# print(type(getResult()))
# print(type(getResult()[0].serverName))
# print(type(getResult()[0].responsible))


