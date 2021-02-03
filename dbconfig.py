##from flaskext.mysql import MySQL

##mysql = MySQL()

server = 'questionsft.database.windows.net' ##'azure-jbatty.database.windows.net'
database = 'questionnairedb'
username = 'qftadmin'
password = 'Th!sMyFirstSqlSrv'
port = 1433
driver = '{ODBC Driver 17 for SQL Server}'

connstr = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=no'
