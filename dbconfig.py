##from flaskext.mysql import MySQL

##mysql = MySQL()

server = 'quations.database.windows.net' ##'azure-jbatty.database.windows.net'
database = 'questionnairedb'
username = 'qadmin'
password = 'Debugger1$'
port = 1433
driver = '{ODBC Driver 17 for SQL Server}'

connstr = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=no'
