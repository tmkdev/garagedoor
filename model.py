import web

db = web.database(dbn="sqlite", db="database/garage.db")

def createDatabase():
	db.query("CREATE TABLE IF NOT EXISTS users (id integer primary key AUTOINCREMENT, name text, code text, enabled int , permission int);")
	db.query("CREATE TABLE IF NOT EXISTS log ( name text, doorstatus int, tstamp int DEFAULT CURRENT_TIMESTAMP);")

def getUserAuth(name, code):
	return db.select('users', locals(), where="name = $name and code = $code and enabled = 1", 
		what='enabled, permission').list()

def listUsers():
	return db.select('users')

def deleteuser(id):
	return db.delete('users', where="id=$id", vars=locals())

def insertuser(username, usercode):
	return db.insert('users', name=username, code=usercode, enabled=1, permission=0)

def toggleenabled(id):
	return db.query("UPDATE users SET enabled=not enabled where id=%s;" % id)

def log(user, doorstatus):
	return db.insert('log', name=user, doorstatus=doorstatus)
