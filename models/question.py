from dbconfig import connstr
import pyodbc as db
class QuestionModel:

    @staticmethod
    def updateQuestion(args, content):
        try:
            connection = db.connect(connstr)
            cursor = connection.cursor()
            sql = """UPDATE dbo.Questions set Question_Description = ? where QID = ? """
            cursor.execute(sql, [args.get('qa'), args.get('qId')])
            connection.commit()
            options = content['rating'];
            for rating in options:
                sql = """UPDATE dbo.Options set Option_Description = ? where OptionID = ?"""
                cursor.execute(sql, [rating['legend'], rating['optionId']])
                connection.commit()
            cursor.close()
            connection.close()
            return "Question updated successfully"
        except Exception as e:
            return str(e)

           