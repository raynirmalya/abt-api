from dbconfig import connstr
import pyodbc as db
class QuestionnaireModel(object):
    def __init__(self):
        print("")
    def getAllQuestions(self):
        try:
            connection = db.connect(connstr)
            cursor = connection.cursor()
            sql = """Select O.Level, Q.QID, Q.Question_Description,
            Q.SubQuestion, Q.Qmessage, Q.QSubMessage, Q.Section,
            O.OptionID, O.SortingID, O.Option_Description,R.RID,
            R.Rating_Value, R.Rating_Description, S.SubscaleID,
            S.SubscaleDescription, Se.SectionName from dbo.Questions as Q 
            INNER JOIN dbo.Options as O on Q.QID = O.QID
            INNER JOIN dbo.Sections as Se on Se.SectionID = Q.Section
            LEFT OUTER JOIN dbo.Ratings as R on R.OptionID = O.OptionID
            LEFT OUTER JOIN dbo.Subscale as S on S.QID = O.QID
            order by Q.Section, O.SortingID, Q.QID """;
            cursor.execute(sql);
            rows = cursor.fetchall()
            data = []
            subscaleNames = [];
            sectionNames = [];
            sectionBasedSubscaleName = {};
            for row in rows:
                subScaleDesc = self.convert(row.SubscaleDescription)
                sectionName = self.convert(row.SectionName)
                rowData = {
                    'level': row.Level,
                    'qId': row.QID,
                    'questionDescription': row.Question_Description,
                    'subQuestion': row.SubQuestion,
                    'message': row.Qmessage,
                    'subMessage': row.QSubMessage,
                    'section': row.Section,
                    'optionId': row.OptionID,
                    'rank': row.SortingID,
                    'legend': row.Option_Description,
                    'rId': row.RID,
                    'subscaleId': row.SubscaleID,
                    'subscaleDescription': self.convert(subScaleDesc),
                    'value': row.Rating_Value,
                    'sectionName': sectionName
                }
                if sectionName not in sectionNames:
                    sectionBasedSubscaleName[sectionName] = {}
                    sectionNames.append(sectionName)
                if subScaleDesc not in subscaleNames and subScaleDesc is not None:
                    subscaleNames.append(subScaleDesc)
                if subScaleDesc is not None and subScaleDesc not in sectionBasedSubscaleName[sectionName]:
                    sectionBasedSubscaleName[sectionName][subScaleDesc] = {}
                data.append(rowData)
            #connection.close()
            responseObj = {}
            for sectionName in sectionNames:
                responseObj[sectionName] = {}
                if not bool(sectionBasedSubscaleName[sectionName]):
                    nosubscaleBasedQa = list(filter(lambda row: row['subscaleDescription'] is None and row['sectionName'] == sectionName, data))
                    responseObj[sectionName]['question'] = nosubscaleBasedQa[0]['questionDescription']
                    responseObj[sectionName]['subQuestion'] = nosubscaleBasedQa[0]['subQuestion']
                    responseObj[sectionName]['qId'] = nosubscaleBasedQa[0]['qId']
                    nosubscaleBasedQaLevel1Ans = list(filter(lambda row: row['level'] == '1', nosubscaleBasedQa))
                    answers = []
                    for ans in nosubscaleBasedQaLevel1Ans: 
                        isAnsAdded = list(filter(lambda row: row['legend'] == ans['legend'], answers))
                        if ( len(isAnsAdded) == 0): 
                            answers.append({
                                'value': ans['value'],
                                'legend': ans['legend'],
                                'optionId': ans['optionId'],
                                'rank': ans['rank']
                            })
                    responseObj[sectionName]['answers'] = answers
                    nosubscaleBasedQaLevel2Mess = list(filter(lambda row: row['level'] == '2' and row['qId'] == nosubscaleBasedQa[0]['qId'] and row['message'] != '', nosubscaleBasedQa))
                    nosubscaleBasedQaLevel2Ques = list(filter(lambda row: row['level'] == '2' and row['qId'] == nosubscaleBasedQa[0]['qId'], nosubscaleBasedQa))
                    responseObj[sectionName]['noAnswer'] = {
                        'message': nosubscaleBasedQaLevel2Mess[0]['subQuestion'],
                        'subMessage': nosubscaleBasedQaLevel2Mess[0]['message'],
                        'qId':  nosubscaleBasedQaLevel2Mess[0]['qId']
                    } 
                    answers = []
                    for ans in nosubscaleBasedQaLevel2Ques: 
                        isAnsAdded = list(filter(lambda row: row['legend'] == ans['legend'], answers))
                        if ( len(isAnsAdded) == 0): 
                            answers.append({
                                'value': ans['value'],
                                'legend': ans['legend'],
                                'optionId': ans['optionId'],
                                'rank': ans['rank']
                            })
                    responseObj[sectionName]['noAnswer']['answers'] = answers
                for subscaleName in sectionBasedSubscaleName[sectionName]:
                    if subscaleName is not None:
                        responseObj[sectionName][subscaleName] = {}
                        subscaleBasedQa = list(filter(lambda row: row['subscaleDescription'] == subscaleName, data))
                        responseObj[sectionName][subscaleName]['message'] = subscaleBasedQa[0]['message']
                        responseObj[sectionName][subscaleName]['subMessage'] = subscaleBasedQa[0]['subMessage']
                        responseObj[sectionName][subscaleName]['qId'] = subscaleBasedQa[0]['qId']
                        responseObj[sectionName][subscaleName]['questionsArray'] = []
                        for ques in subscaleBasedQa: 
                            isQAdded = list(filter(lambda row: row['qId'] == ques['qId'], responseObj[sectionName][subscaleName]['questionsArray']))
                            if ( len(isQAdded) == 0): 
                                optionsWithValue = list(filter(lambda row: row['qId'] == ques['qId'], subscaleBasedQa))
                                rating = []
                                for value in optionsWithValue:
                                    rating.append({
                                        'value': value['value'],
                                        'legend': value['legend'],
                                        'optionId': value['optionId']
                                    })
                                responseObj[sectionName][subscaleName]['questionsArray'].append({
                                'qa':  ques['questionDescription'],
                                'rank': ques['rank'],
                                'qId': ques['qId'],
                                'rating': rating
                                })
            cursor.close()
            connection.close()
            return responseObj
        except Exception as e:
            return str(e)

    def convert(self, s):
        if(s is None): 
            return
        s1 = '' 
        s1 += s[0].lower() 
        for i in range(1, len(s)): 
            if (s[i] == ' '): 
                s1 += s[i + 1].upper() 
                i += 1
            elif(s[i - 1] != ' '): 
                s1 += s[i] 
        return s1