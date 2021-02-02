from dbconfig import connstr
import pyodbc as db
class MessageModel:

    @staticmethod
    def updateMessage(args):
        try:
            connection = db.connect(connstr)
            cursor = connection.cursor()
            sql = """UPDATE dbo.Questions set Qmessage = ?, QSubMessage = ? where QID = ?"""
            cursor.execute(sql, [args.get('message'), args.get('subMessage'), args.get('qId')])
            connection.commit()
            cursor.close()
            connection.close()
            return "Message updated successfully"
        except Exception as e:
            return str(e)