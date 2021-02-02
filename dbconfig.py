##from flaskext.mysql import MySQL

##mysql = MySQL()

server = 'LAPTOP-52PJGRUU\SQLEXPRESS' ##'azure-jbatty.database.windows.net'
database = 'questionnairedb'
username = 'admin'
password = 'Debugger1$'
port = 1433
driver = '{ODBC Driver 17 for SQL Server}'

connstr = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=no'
