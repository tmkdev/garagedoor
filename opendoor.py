import web
from web import form
import re
import base64
from subprocess import Popen
import pprint
import model
import links

web.config.debug = False
pp = pprint.PrettyPrinter(depth=6)

urls = (
    '/opendoor', 'opendoor',
    '/door', 'door',
    '/edit', 'edit',
    '/login', 'login',
    '/logout', 'logout',
    '/enable/(.*)', 'enable',
    '/delete/(.*)', 'delete',
    '/favicon.ico', 'icon',
    '/*', 'login',
)

web.config.session_parameters['cookie_name'] = 'garagedoor_session_id'
web.config.session_parameters['secret_key'] = '6u4ZkTIChQ'

app = web.application(urls, globals())

#Init database
model.createDatabase()

#Session
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store,
                              initializer={'login': 0, 'privilege': 0, 'user': ''})

#Globals
globals = { 'context': session, 'links': links.links } 
render = web.template.render('templates', globals=globals, base='layout')

def IsAuthorized(function):
	def wrapper(*args, **kwargs):
		if session.login == 0:
			web.seeother('/login')
		return function(*args, **kwargs)
	return wrapper

class icon:
	def GET(self):
		raise web.seeother("/static/house.ico")

class login:
    loginform = form.Form(
    		form.Textbox('username', description="Username:"),
    		form.Password('password', description="Password:"),
    		form.Button('submit', type="submit", class_="form_control btn btn-primary", description="Login"),
    )

    def GET(self):
	f = self.loginform()
	return render.login(f)

    def POST(self):
	f = self.loginform()
	f.validates()
	print f.d.username
	print f.d.password
	allow = model.getUserAuth(name=f.d.username, code=f.d.password)
        if not (len(allow) == 1 and allow[0]['enabled'] == 1) :
		session.login=0
		return render.login(f)
	        
	session.login=1
	session.privilege=allow[0]['permission']
	session.user=f.d.username
	
	web.seeother('/door')

class logout:
	def GET(self):
		session.login=0
		session.privilege=0
		session.user=''
		web.seeother('/login')

class edit:        
    newuser = form.Form(
	        form.Textbox('username', description="Username:"),
                form.Password('password', description="Password:"),
                form.Password('password2', description="Password (Again):"),
                form.Button('submit', type="submit", class_="form_control btn btn-primary", description="Add User" ), 
		validators = [
        		form.Validator("Passwords did't match", lambda i: i.password == i.password2)]
    )

    @IsAuthorized
    def GET(self):
	f = self.newuser()
	users = model.listUsers()
        return render.edit(users,f)

    @IsAuthorized 
    def POST(self):
	users = model.listUsers()
	f = self.newuser()
        if not f.validates():
		print f.render_css()
		return render.edit(users,f)
	else:
		success = model.insertuser( f.d.username, f.d.password )
		web.seeother('/door')
	
class enable:
    @IsAuthorized
    def GET(self, id):
        if not id:
	    web.seeother('/edit')
	model.toggleenabled(id)	
	web.seeother('/edit')

class delete:
    @IsAuthorized
    def GET(self, id):
        if not id:
	    web.seeother('/door')
	model.deleteuser(id)	
	web.seeother('/edit')

class door:
    @IsAuthorized 
    def GET(self):
	return render.door()

class opendoor:
    @IsAuthorized
    def GET(self):
	if session.login==1:
		model.log(session.user, 0)
		Popen(["opendoor"])
	web.seeother('/door')

if __name__ == "__main__":
    app.run()
