import flask, flask.views
import os ,uuid
from flask.ext.mail import Mail, Message
#from flask_mail import Message,Mail
import functools
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
#import flask_sijax
app = flask.Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)
app.secret_key = "1234"

gdb = GraphDatabase("http://localhost:7474/db/data/")

people = gdb.labels.create("People")		#label of user 
diaries = gdb.labels.create("Diaries")		#label of khaterat
wrote = gdb.labels.create("Wrote")		#label of relation between user and khaterat
friend = gdb.labels.create("Friend")		#label of relation between user and her friend

fdiaries = gdb.labels.create("Fdiaries")	#label of friend diaries
fridiaries = gdb.labels.create("Fridiaries")	#label of relation between user and friend diaries

public = gdb.labels.create("Public")		#label of public diaries
publicrel = gdb.labels.create("Publicrel")	#label of relation friend diaries

like = gdb.labels.create("Like")		#label of like
likerel = gdb.labels.create("Likerel")		#label of rel like

comment = gdb.labels.create("Comment")		#label of comment
commentrel = gdb.labels.create("Commentrel")	#label of rel comment

Image = gdb.labels.create("Image")		#label of comment
imagerel = gdb.labels.create("imagerel")	#label of rel comment

app.config['UPLOAD_FOLDER'] = '/home/malihe/tinder/test/asli/static/img/media'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

DEBUG = True
SECRET_KEY = 'hidden'
USERNAME = 'secret'
PASSWORD = 'secret'

MAIL_SERVER='imap.gmail.com'
MAIL_PORT=993
MAIL_USE_TLS = False
MAIL_USE_SSL= True
MAIL_USERNAME = 'happysnake.2014@gmail.com'
MAIL_PASSWORD = 'wormgame'

mail = Mail(app)
#app.config["MAIL_SERVER"] = "smtp.gmail.com"
#app.config["MAIL_PORT"] = 465
#app.config["MAIL_USE_SSL"] = True
#app.config["MAIL_USERNAME"] = 'happysnake.2014@gmail.com'
#app.config["MAIL_PASSWORD"] = 'wormgame'

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('main.html')
    
    def post(self):

	#user = flask.request.form['username']
        #passwd = flask.request.form['password']
	#user1 = flask.request.form['username1']
	#print user
	#print passwd
	#print user1
	if 'sign in' in flask.request.form:
		user = flask.request.form['username']
        	passwd = flask.request.form['password']

		q="""match (p:People { username : "%s"}) return p.password""" % user
		result = gdb.query(q=q)

		if (len(result)==0):
			print "your username is invalid!you must sign up."
			flask.flash("your username is invalid!you must sign up.")
        		return flask.redirect(flask.url_for('main'))

		if (result[0][0]==passwd):
			flask.session['username'] = user
			return flask.redirect(flask.url_for('home'))
        	else:
         		flask.flash("your password is incorrect")
        		return flask.redirect(flask.url_for('main'))

	if 'reset' in flask.request.form:

		return flask.redirect(flask.url_for('home'))
	
	if 'send' in flask.request.form:

		passwd1 = flask.request.form['password1']
		user1 = flask.request.form['username1']

		if(flask.request.form['username1']!="" and flask.request.form['password1']!="" and flask.request.form['a_password']!="" and flask.request.form['mail']!="" and flask.request.form['year']!="" and flask.request.form['month']!="" and flask.request.form['day']
!=""):

			q="""match (p:People { username : "%s"}) return p.password""" % user1
			results = gdb.query(q=q) 
			print "result",results,"len= ",len(results)
			if len(results)!=0:

				flask.flash("your username is repetitive.please change your username")
				print "your username is repetitive.please change your username"
				return flask.redirect(flask.url_for('main'))

			elif len(str(flask.request.form['password1']))<=5:

				flask.flash("your password must more than 5 character ! please change your password")
				print "your password must more than 5 character ! please change your password"
				return flask.redirect(flask.url_for('main'))

			elif flask.request.form['password1']!=flask.request.form['a_password']:

				flask.flash("your password and confirm password is not equal ")
				print "your password and confirm password is not equal"
				return flask.redirect(flask.url_for('main'))
			
			#elif (year<=0 or month<=0 or day<=0 or month>12 or day>31):
				#print year ,month ,day
			#	flask.flash("your birthday's date is invalid ")
			#	print "your birthday's date is invalid"
			#	return flask.redirect(flask.url_for('signup'))


			else:
				flask.session['username'] = user1
				#msg = Message("welcom to tinder group!",sender="happysnake.2014@gmail.com.com",recipients=["m.hajihosseini95@gmail.com"])
				#mail.send(msg)

				print flask.request.form['username1']
				print flask.request.form['password1']
				print flask.request.form['a_password']
				print flask.request.form['year']
				print flask.request.form['month']
				print flask.request.form['day']
				print flask.request.form['mail']

				#q=""" create (s:People{username:"%s",password:"%s"}) """%(flask.request.form['username'],flask.request.form['password'])

				q=""" create (s:People{username:"%s",password:"%s",a_password:"%s",mail:"%s",year:"%s",month:"%s",day:"%s",firstname:"%s",lastname:"%s",age:"%s",gender:"%s",country:"%s",education:"%s",work:"%s",college:"%s",school:"%s",biography:"%s",imageaddress:"%s"}) """ %(flask.request.form['username1'],flask.request.form['password1'],flask.request.form['a_password'],flask.request.form['mail'],flask.request.form['year'],flask.request.form['month'],flask.request.form['day'],"-","-","-","-","-","-","-","-","-","-","/static/img/media/profile.jpg")

				result = gdb.query(q=q)
				

				if os.path.exists('/home/malihe/tinder/test/asli/static/img/media/'+str(flask.request.form['username1'])):
    					pass
				else:
    					os.mkdir('/home/malihe/tinder/test/asli/static/img/media/'+str(flask.request.form['username1']))

			
				if os.path.exists('/home/malihe/tinder/test/asli/static/img/media/'+str(flask.request.form['username1'])+str("/khatere")):
    					pass
				else:
    					os.mkdir('/home/malihe/tinder/test/asli/static/img/media/'+str(flask.request.form['username1'])+str("/khatere"))



				return flask.redirect(flask.url_for('home'))
		

		else:
			flask.flash("you must fill all the blanks!")
		      	return flask.redirect(flask.url_for('main'))



#****************************************email******************************************

def send_mail():
    msg = Message(
      'Hello',
       sender='happysnake.2014@gmail.com',
       recipients=
       ['m.hajihosseini95@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Sent"



#**********************************************************************************

def login_required(method):
	@functools.wraps(method)
	def wrapper(*args,**kwargs):

		if 'username' in flask.session:

			return method(*args,**kwargs)
		else:
			print "A login is required to see the page!"
			flask.flash("A login is required to see the page!")
			return flask.redirect(flask.url_for('main'))
	return wrapper


#****************************************home******************************************

class home(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']		
		q = """match (k:People{username:"%s"})-[r:fridiaries]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title,d.ID """%user 
		result = gdb.query(q=q)
		

		dfriends=[]
		#comments = [('text',"khatere"),('name',"malihe"),('image',"/static/img/media/profile.jpg")]
		for i in range(len(result)):

			#q=""" match (d:Diaries{ID:"%s"})-[r:commentrel]->(c:Comment) return c.name,c.image,c.text """%result[i][6]
			#com = gdb.query(q=q)
			#comen = []
			#for j in range(len(com)):
			#	y = dict([('text',com[j][2]),('name',com[j][0]),('image',com[j][1])])#comment haye har khatere ra neshan midahad.
			#	comen.append[y]
			
			
			q=""" match (k:People{username:"%s"}) return k.imageaddress"""%result[i][1]
			picture = gdb.query(q=q)				#ax usery ke khatere ra neveshte
			
			q = """ match (d:Like{ID:"%s"}) return d.count""" %(result[i][6])	#tedad like haye har khatere
			like = gdb.query(q=q)

			#q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
			q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]->(i:Image) return i.address""" %result[i][6] #ax haie ke ba khatere ferestade
			img = gdb.query(q=q)
			print "$$$$$$$$$$$$$$$$$$$$$$$$$"
			print "333333333333333333= ",img[0][0]


			x = dict([('text',result[i][0]),('user',result[i][1]),('userimage',picture[0][0]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]) , ('feel',"laugh") ,('images',img[0][0]),('like',like[0][0]),('id',result[i][6]),('image',picture[0][0])])
			dfriends.append(x)
		print dfriends
		return flask.render_template('home.html',posts=dfriends)

	@login_required
	def post(self):

		user = flask.session['username']

		q=""" match (d:Diaries) return d.ID """
		resultl = gdb.query(q=q)

 
		if "btnmenusignout" in flask.request.form:
			flask.session.pop('username',None)
			return flask.redirect(flask.url_for('main'))

		if "submitsearch" in flask.request.form:
			flask.session['txtsearch'] = flask.request.form['txtsearch']
			return flask.redirect(flask.url_for('friendprofile'))
		
		Id = request.form('postid')
		txt = request.form('text')
		
		#if txt=='like':
		#	q=""" (g:Like{ID:"%s"}) return g.count"""
		#	result = gdb.query(q=q)

		#	q=""" (g:Like{ID:"%s"}) set g.count="%s" """(user,int(result[0][0]+1)
		#	result = gdb.query(q=q)

		#else:
		#	q = """ match (p:People{'username':"%s"}) return p.imageaddress"""
		#	result=gdb.query(q=q)
			
 		#	q="""match (d:Diaries{ID:"%s"}), CREATE (c:Comment{text:"%s",name:"%s",image:"%s"}) , CREATE (d)-[:commentrel]->(c) """ % (Id,txt,user,result[0][0])
		#	result = gdb.query(q=q)
		#for i in resultl:
		

		#if 'click' in flask.request.form:
		#	print "likkkkkkkkkkkkkkkk:"
			#q=""" (l:Like{IDL:"%s"}) return l.count """%(i)
			#like = gdb.query(q=q)
			#print "int(like[0][0])+1",int(like[0][0])+1
			#q=""" (l:Like{IDL:"%s"}) set l.count="%s" """%(i,int(like[0][0])+1)
			#like = gdb.query(q=q)
				
		
#		for i in resultl:
#			if i in flask.request.form:
#				m = str(i)
#				q=""" (p:People{username:"%s"}) return p.imageaddress """%( flask.session['username'])
#				result = gdb.query(q=q)
#
#				q=""" (d:Diaries{IDC:"%s"}) create (c:Comment{text:"%s",name:"%s",image:"%s"})  create (d)-[:commentrel]->(c) """%(i,flask.request.form[i],flask.session['username'],result[0][0])
#				comment = gdb.query(q=q)

				
		





#****************************************profile******************************************
class profile(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
	
		q="""match (p:People { username : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.education,p.work,p.college,p.school,p.biography , p.imageaddress""" % user
		result = gdb.query(q=q)

		return flask.render_template('profile.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender =result[0][3] ,mail=result[0][4],country=result[0][5],education = result[0][6],work = result[0][7],college = result[0][8],school = result[0][9],biography=result[0][10],filename=result[0][11])

	@login_required
	def post(self):
		pass

#****************************************friendprofile******************************************
class friendprofile(flask.views.MethodView):
	@login_required
	def get(self):

		ser = flask.session['txtsearch']
		
		q="""match (p:People { username : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.education,p.work,p.college,p.school,p.biography,p.imageaddress""" % ser
		result = gdb.query(q=q)
		if len(result)==0:
			print "this username is invalid"
			flask.flash("this username is invalid")
			return flask.render_template('home.html')
		
		q = """match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.username,k.imageaddress """ % ser
		a = gdb.query(q=q)
		friends=[]

		for i in range(len(a)):
			x = dict([('username',a[i][0]),('images',a[i][1])])
			friends.append(x)
		return flask.render_template('friendprofile.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender =result[0][3] ,mail=result[0][4],country=result[0][5],education = result[0][6],work = result[0][7],college = result[0][8],school = result[0][9],biography=result[0][10],filename=result[0][11],relations=friends)


	@login_required
	def post(self):
				

		if "add" in flask.request.form:

			user = flask.session['username']
			ser = flask.session['txtsearch']
		
			q="""start n=node(*) match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.username""" % user
			result = gdb.query(q=q)
			count=0
			for r in result:
				if r[0]==ser:
					count+=1

			if (count==0):
				q="""MATCH (p:People{username:"%s"}),(q:People{username:"%s"}) CREATE (p)-[:friend]->(q) """ % (user,ser)
				result = gdb.query(q=q)

				return flask.redirect(flask.url_for('home'))	

			
			return flask.redirect(flask.url_for('home'))

#****************************************upload******************************************

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload():
	print "lllllllllmmmmm" 
	user = flask.session['username']
	print "user:        ",user
    	f = flask.request.files['file']
	print "sssssssssssssssss= ",f.filename
    	if f and allowed_file(f.filename):
        	filename = secure_filename(f.filename)
	
       		f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(user), filename))
        	#return flask.redirect(url_for('profile'))

#def uploaded_file(filename):
#	return send_from_directory(app.config['UPLOAD_FOLDER'],
 #                              filename)


#****************************************writing******************************************

class writing(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.firstname,k.lastname,k.imageaddress,p.imageaddress """ % user
		result = gdb.query(q=q)
		friends=[]

		for i in range(len(result)):
			x=dict([('firstname',result[i][0]),('lastname',result[i][1]),('images',result[i][2])])
			friends.append(x)
		for friend in friends:
			print friend['firstname']
		print "friends",friends
		return flask.render_template('writing.html',friends=friends)


	@login_required
	def post(self):
		y = flask.request.form['year']
		m = flask.request.form['month']
		da = flask.request.form['day']
		titl = flask.request.form['title']
		user=flask.session['username']
		
		if 'save' in flask.request.form:
			
			if (y!="" and m!="" and da!=""):
				if flask.request.form['privacy']=="private":
					
					q = """ match (g:ID) return g.count """
					count = gdb.query(q=q)


					q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s",writer:"%s",ID:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (user,flask.request.form['text'],user,count[0][0],y,m,da,titl)
					result = gdb.query(q=q)

				
					f = flask.request.files['file']

					print "5555555555555555555555= ",f.filename
					if (f.filename != ""):
						addres = "/static/img/media/" + str(user) +"/khatere/"+ str(f.filename)

						q="""match(d:Diaries{ID:"%s"})  create (i:Image{address:"%s"})  create(d)-[:imagerel]->(i) """ % (count[0][0],addres)
						picture = gdb.query(q=q)

	    				if f and allowed_file(f.filename):
						filename = secure_filename(f.filename)
		
			       		f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(user)+str("/khatere"), filename))
					f.close()

					q = """ match (g:ID) set g.count="%s" """%(str(int(count[0][0])+1))
					result = gdb.query(q=q)


					q="""MATCH (d:Diaries{diarie:"%s"}) CREATE (l:Like{count:"0",ID:"%s"}) CREATE (d)-[:likerel]->(l) """ % (flask.request.form['text'],count[0][0])
					result = gdb.query(q=q)



				if flask.request.form['privacy']=="friends":
					
					q = """ match (g:ID) return g.count """
					count = gdb.query(q=q)


					q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s",writer:"%s",ID:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (user,flask.request.form['text'],user,count[0][0],y,m,da,titl)
					result = gdb.query(q=q)
				

					f = flask.request.files['file']

					print "5555555555555555555555= ",f.filename
					if (f.filename != ""):
						addres = "/static/img/media/" + str(user) +"/khatere/"+ str(f.filename)

						q="""match(d:Diaries{ID:"%s"})  create (i:Image{address:"%s"})  create(d)-[:imagerel]->(i) """ % (count[0][0],addres)
						picture = gdb.query(q=q)

	    				if f and allowed_file(f.filename):
						filename = secure_filename(f.filename)
		
			       		f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(user)+str("/khatere"), filename))
					f.close()



					q = """ match (g:ID) set g.count="%s" """%(str(int(count[0][0])+1))
					result = gdb.query(q=q)


					q="""MATCH (d:Diaries{diarie:"%s"}) CREATE (l:Like{count:"0",ID:"%s"}) CREATE (d)-[:likerel]->(l) """ % (flask.request.form['text'],count[0][0])
					result = gdb.query(q=q)



					q="""MATCH (p:People{username:"%s"})-[r:friend]-> (k:People) return k.username """ % (user)
					results = gdb.query(q=q)
					
					if (len(results)!=0):
						#q=""" create (r:Fdiaries{diarie:"%s",writer:"%s"}) """ %(flask.request.form['text'],user) 
						#result = gdb.query(q=q)

						for i in range(len(results)):
							print results[i][0]
							#q="""MATCH (p:People {username:"%s"}),(d:Fdiaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:fridiaries{year:"%s",month:"%s",day:"%s",titile:"%s"}]->(d) """ % (results[i][0],flask.request.form['text'],y,m,da,titl)

							q="""MATCH (p:People {username:"%s"}),(d:Diaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:fridiaries{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (results[i][0],flask.request.form['text'],user,y,m,da,titl)
							results1 = gdb.query(q=q)




				if flask.request.form['privacy']=="public":
					#ul = uuid.uuid4()
					#uc = uuid.uuid4()

					q = """ match (g:ID) return g.count """
					count = gdb.query(q=q)
					print "qqqqqqqqqqqqqqqq= ",count[0][0]

					q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s",writer:"%s",ID:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (user,flask.request.form['text'],user,count[0][0],y,m,da,titl)
					result = gdb.query(q=q)


					q="""MATCH (d:Diaries{diarie:"%s"}) CREATE (l:Like{count:"0",ID:"%s"}) CREATE (d)-[:likerel]->(l) """ % (flask.request.form['text'],count[0][0])
					result = gdb.query(q=q)


					f = flask.request.files['file']

					print "5555555555555555555555= ",f.filename
					if (f.filename != ""):
						addres = "/static/img/media/" + str(user) +"/khatere/"+ str(f.filename)

						q="""match(d:Diaries{ID:"%s"})  create (i:Image{address:"%s"})  create(d)-[:imagerel]->(i) """ % (count[0][0],addres)
						picture = gdb.query(q=q)

	    				if f and allowed_file(f.filename):
						filename = secure_filename(f.filename)
		
			       		f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(user)+str("/khatere"),filename))
					f.close()


					q = """ match (g:ID) set g.count="%s" """%(str(int(count[0][0])+1))
					result = gdb.query(q=q)

					q="""MATCH (p:People{username:"%s"})-[r:friend]-> (k:People) return k.username """ % (user)
					results = gdb.query(q=q)
					print "len= ",len(results)
					if (len(results)!=0):
						#q=""" create (r:Fdiaries{diarie:"%s",writer:"%s"}) """ %(flask.request.form['text'],user) 
						#result = gdb.query(q=q)

						for i in range(len(results)):
							print "!1111111111",results[i][0]
							print results[i][0]
							q="""MATCH (p:People {username:"%s"}),(d:Diaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:fridiaries{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (results[i][0],flask.request.form['text'],user,y,m,da,titl)
							results1 = gdb.query(q=q)





					#q=""" create (r:Public{diarie:"%s",writer:"%s"}) """ %(flask.request.form['text'],user) 
					#result = gdb.query(q=q)

					q="""MATCH (p:People) return p.username """ 
					result = gdb.query(q=q)

					for i in range(len(result)):
						print result[i][0]
						q="""MATCH (p:People {username:"%s"}),(d:Diaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:publicrel{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (result[i][0],flask.request.form['text'],user,y,m,da,titl)
						results = gdb.query(q=q)
				return flask.redirect(flask.url_for('writing'))
		
			else:
				flask.flash("you must write date!")
				print("you must write date!")
				return flask.redirect(flask.url_for('writing'))
				
#		if 'tag' in flask.request.form:
#			q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",titile:"%s"}]->(d) """ % (user,flask.request.form['text'],y,m,da,titl)
#			result = gdb.query(q=q)
			
#			q="""MATCH (p:People{username:"%s"})-[r:friend]-> (k:People) return k.username """ % (user)
#			result = gdb.query(q=q)
#			d = gdb.nodes.create(diarie=flask.request.form['text'])
#			frienddiaries.add(d)

		if 'cancel' in flask.request.form:
			return flask.redirect(flask.url_for('writing'))


#****************************************mydiary******************************************
class mydiary(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('mydiary.html')
	@login_required
	def post(self):

		if 'januery' in flask.request.form:
 			return flask.redirect(flask.url_for('diary1'))

		if 'febuery' in flask.request.form:
 			return flask.redirect(flask.url_for('diary2'))
	
		if 'march' in flask.request.form:
 			return flask.redirect(flask.url_for('diary3'))

		if 'april' in flask.request.form:
 			return flask.redirect(flask.url_for('diary4'))

		if 'may' in flask.request.form:
 			return flask.redirect(flask.url_for('diary5'))

		if 'june' in flask.request.form:
 			return flask.redirect(flask.url_for('diary6'))

		if 'july' in flask.request.form:
 			return flask.redirect(flask.url_for('diary7'))

		if 'august' in flask.request.form:
 			return flask.redirect(flask.url_for('diary8'))

		if 'september' in flask.request.form:
 			return flask.redirect(flask.url_for('diary9'))

		if 'october' in flask.request.form:
 			return flask.redirect(flask.url_for('diary10'))

		if 'november' in flask.request.form:
 			return flask.redirect(flask.url_for('diary11'))

		if 'december' in flask.request.form:
 			return flask.redirect(flask.url_for('diary12'))

#****************************************diary1******************************************

class diary1(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(1)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary1.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary1.html')
		

#****************************************diary2******************************************

class diary2(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(2)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary2.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary2.html')
		

#****************************************diary3******************************************

class diary3(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(3)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary3.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary3.html')
		

#****************************************diary4******************************************

class diary4(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(4)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary4.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary4.html')
		

#****************************************diary5******************************************

class diary5(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(5)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary5.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary5.html')
		
#****************************************diary6******************************************

class diary6(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(6)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary6.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary6.html')
		

#****************************************diary7******************************************

class diary7(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(7)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary7.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary7.html')
		
#****************************************diary8******************************************

class diary8(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(8)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary8.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary8.html')
		

#****************************************diary9******************************************

class diary9(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(9)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary9.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary9.html')
		

#****************************************diary10******************************************

class diary10(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(10)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary10.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary10.html')
		

#****************************************diary11******************************************

class diary11(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(11)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary11.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary11.html')
		

#****************************************diary12******************************************

class diary12(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title ,d.ID """%user 
		result = gdb.query(q=q)
		
		diary=[]
		#comments = ['a','b','c']

		for i in range(len(result)):
			if (result[i][3]==str(12)):
				q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
				pic = gdb.query(q=q)

				x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
				diary.append(x)
		return flask.render_template('diary12.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary12.html')
		
#****************************************friends******************************************

class friends(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']

		q = """match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.username,k.imageaddress """ % user
		result = gdb.query(q=q)
		friends=[]

		for i in range(len(result)):
			x = dict([('username',result[i][0]),('images',result[i][1])])
			friends.append(x)
		
		#q=""" match (p:People)-[r:friend]-> (k:People{username:"%s"}) return p.username,p.imageaddress """%user
		#result = gdb.query(q=q)
		#flowers=[]

		#for i in range(len(result)):
		#	y=dict([('username',result[i][0]),('images',result[i][1])])
		#	flowers.append(y)
		return flask.render_template('friends.html',friends = friends)
	@login_required
	def post(self):

		return flask.render_template('friends.html')
	

#****************************************flowers******************************************

class followers(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']
		q=""" match (p:People)-[r:friend]-> (k:People{username:"%s"}) return p.username,p.imageaddress """%user
		
		result = gdb.query(q=q)
		flowers=[]

		for i in range(len(result)):
			print result[i][0]
			y=dict([('username',result[i][0]),('images',result[i][1]),('id',result[i][0])])
			flowers.append(y)
		return flask.render_template('followers.html',followers=flowers)
	@login_required
	def post(self):

		return flask.render_template('followers.html')
	

#****************************************welcome******************************************
class welcome(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('welcome.html')
	@login_required
	def post(self):
		return flask.render_template('welcome.html')

#****************************************settings******************************************

class settings(flask.views.MethodView):
	def get(self):
		user = flask.session['username']
		q="""match (p:People { username : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.biography, p.imageaddress""" % user
		result = gdb.query(q=q)

		return flask.render_template('settings.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender =result[0][3] ,mail=result[0][4],country=result[0][5],biography=result[0][6],filename=result[0][7])


	@login_required
	def post(self):
		user = flask.session['username']
		if 'remove image'in flask.request.form :
			q="""match (p:People { username : "%s"}) set p.imageaddress="%s" """ % (user,"/static/img/media/profile.jpg")
			result = gdb.query(q=q)
			return flask.redirect(flask.url_for('profile'))			
		
		if 'reset' in flask.request.form:
			return flask.redirect(flask.url_for('settings'))
		


		if 'send' in flask.request.form:

			f = flask.request.files['file']
			print "5555555555555555555555= ",f.filename
			if (f.filename != ""):

				addres = "/static/img/media/" + str(user) +"/"+ str(f.filename)
				q="""match (p:People { username : "%s"}) set p.imageaddress="%s" """ % (user,addres)
				result = gdb.query(q=q)

	    			if f and allowed_file(f.filename):
					filename = secure_filename(f.filename)
	
		       		f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(user), filename))
				f.close()
			a=[flask.request.form['firstname'],flask.request.form['lastname'],flask.request.form['mail'],flask.request.form['age'],flask.request.form['country'],flask.request.form['male']]			

			if (a[2]!="" and (a[5]=="female" or a[5]=="male")):
				for i in range(6):
					if a[i]=="":
						a[i]="--"


				q="""match (p:People { username : "%s"}) set p.firstname="%s",p.lastname="%s",p.mail="%s",p.age="%s",p.country="%s",p.gender="%s" """ % (user,a[0],a[1],a[2],a[3],a[4],a[5])
				result = gdb.query(q=q)

				return flask.redirect(flask.url_for('profile'))			
			else:
				flask.flash("you must enter your mail")
				print "you must enter your mail"
				return flask.redirect(flask.url_for('settings'))			




#****************************************password******************************************
class password(flask.views.MethodView):
	@login_required
	def get(self):
		
		return flask.render_template('password.html')
	@login_required
	def post(self):
		user = flask.session['username']
		if 'send' in flask.request.form:
			q = """ match (p:People{username:"%s"}) return p.password"""%user
			result = gdb.query(q=q)
			if flask.request.form['oldpass']==result[0][0]:
				if flask.request.form['newpass']==flask.request.form['confirmpass']:
					q = """ match (p:People{username:"%s"}) set p.password="%s" , p.a_password="%s" """%(user , flask.request.form['newpass'],flask.request.form['newpass'])
					result = gdb.query(q=q)
					return flask.redirect(flask.url_for('settings'))			
				else:
					flask.flash("new password and confirm password is not equal")
					print "new password and confirm password is not equal"
					return flask.redirect(flask.url_for('settings'))
			else:			
				flask.flash("your old password is incorrect")
				print "your old password is incorrect"
				return flask.redirect(flask.url_for('settings'))
		return flask.render_template('password.html')


#****************************************work******************************************
class work(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']
		q="""match (p:People { username : "%s"}) return p.education,p.work,p.college,p.school""" % user
		result = gdb.query(q=q)
		return flask.render_template('work.html',education=result[0][0],work=result[0][1],college=result[0][2],school=result[0][3])

	@login_required
	def post(self):
		user = flask.session['username']
		if 'send' in flask.request.form:

			q="""match (p:People { username : "%s"}) set p.education="%s",p.work="%s",p.college="%s",p.school="%s" """ % (user,flask.request.form['education'],flask.request.form['work'],flask.request.form['college'],flask.request.form['school'])
			result = gdb.query(q=q)
			return flask.redirect(flask.url_for('profile'))
			
		if 'reset' in flask.request.form:
			return flask.redirect(flask.url_for('work'))			



#****************************************public******************************************

class public(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:publicrel]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title,d.ID """ %user
		result = gdb.query(q=q)
		
		publics=[]
		#comments = ['a','b','c']
		for i in range(len(result)):
			q=""" match (p:People{username:"%s"}) return p.imageaddress """%(result[i][1])
			pic = gdb.query(q=q)
				
			x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',pic[0][0])])
			publics.append(x)
		return flask.render_template('public.html',omumies=publics)
	@login_required
	def post(self):
		return flask.render_template('public.html')


#****************************************public_user******************************************

class public_user(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']

		q="""match (k:People{username:"%s"})-[r:publicrel]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title,d.ID """ %user
		result = gdb.query(q=q)
	
		#comments = ['a','b','c']
		publics=[]
		for i in range(len(result)):
		#	print "lennnnnnnnnnnn= ",len(result)
		#	print result[i][0]
			q=""" match (p:People{username:"%s"}) return p.imageaddress """% result[i][1]
			img = gdb.query(q=q)

			q=""" match (d:Diaries{ID:"%s"})-[r:imagerel]-(i:Image) return i.address  """%result[i][6]
			pic = gdb.query(q=q)
			
		#	print "22222222222222= ",pic[0][0]
			x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]),('image',img[0][0]),('images',pic[0][0])])
		#	print "xxxxxxxxxxxxxxxxxxxxxxxxxxxx= ",x
			publics.append(x)
		#	print "33333333333333333333333333333333= ",publics
		#print "44444444444444444444444444444444444444= ",publics
		return flask.render_template('public_user.html',posts=publics)
	@login_required
	def post(self):
		return flask.render_template('public_user.html')


#****************************************test******************************************
class test(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('test.html')
	@login_required
	def post(self):
		return flask.render_template('test.html')


app.add_url_rule('/',
                 view_func =  Main.as_view('main'),
                 methods = ['GET','POST'])


app.add_url_rule('/home/',
                 view_func =  home.as_view('home'),
                 methods = ['GET','POST'])

app.add_url_rule('/public/',
                 view_func =  public.as_view('public'),
                 methods = ['GET','POST'])


app.add_url_rule('/home/public_user/',
                 view_func =  public_user.as_view('public_user'),
                 methods = ['GET','POST'])


app.add_url_rule('/home/writing/',
                 view_func =  writing.as_view('writing'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/writing/test/',
                 view_func =  test.as_view('test'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/welcome/',
                 view_func =  welcome.as_view('welcome'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/profile/',
                 view_func =  profile.as_view('profile'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/friends/',
                 view_func =  friends.as_view('friends'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/friends/followers/',
                 view_func =  followers.as_view('followers'),
                 methods = ['GET','POST'])


app.add_url_rule('/home/mydiary/',
                 view_func =  mydiary.as_view('mydiary'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary1/',
                 view_func =  diary1.as_view('diary1'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary2/',
                 view_func =  diary2.as_view('diary2'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary3/',
                 view_func =  diary3.as_view('diary3'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary4/',
                 view_func =  diary4.as_view('diary4'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary5/',
                 view_func =  diary5.as_view('diary5'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary6/',
                 view_func =  diary6.as_view('diary6'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary7/',
                 view_func =  diary7.as_view('diary7'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary8/',
                 view_func =  diary8.as_view('diary8'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary9/',
                 view_func =  diary9.as_view('diary9'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary10/',
                 view_func =  diary10.as_view('diary10'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary11/',
                 view_func =  diary11.as_view('diary11'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/mydiary/diary12/',
                 view_func =  diary12.as_view('diary12'),
                 methods = ['GET','POST'])


app.add_url_rule('/home/friendprofile/',
                 view_func =  friendprofile.as_view('friendprofile'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/settings/',
                 view_func =  settings.as_view('settings'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/settings/password/',
                 view_func =  password.as_view('password'),
                 methods = ['GET','POST'])

app.add_url_rule('/home/settings/work/',
                 view_func =  work.as_view('work'),
                 methods = ['GET','POST'])


#app.add_url_rule('/home/public/',
#                 view_func =  public.as_view('public'),
 #                methods = ['GET','POST'])


app.debug = True
app.run(host="0.0.0.0")











