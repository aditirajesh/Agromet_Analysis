from flask import Flask,render_template,request,session,redirect,url_for,flash
from new_main import Customer,crop_gdd_timeline,chemical_fertilizer_soil,fertilizer_practice,main_notification_irrigation,main_weather,harvesting
import pandas as pd
import os
from message import send_message

app = Flask(__name__)
app.secret_key = os.urandom(24)
cust = Customer('Udantika','Test','example@123','9090909','passwd','chennai',50,50,30,'jute','18-07-2023',2)

@app.route('/')
def index():
    return redirect('/signup') 
'''------------------------------------------------------------------------'''
@app.route('/signup',methods = ['POST','GET'])
def signup():
    if request.method =='POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('mail')
        ph = request.form.get('phno')
        password = request.form.get('passwd')

        df = pd.read_csv('data.csv')
        if email in list(df['mail']):
            flash('Email already exists.')

        elif ph in list(df['phno']):
            flash('Phone number already exists.')
        
        else:
            session["fname"] = fname
            session["lname"] = lname 
            session["mail"] = email 
            session["phno"] = ph
            session["passwd"] = password
            return redirect('/input')
    return render_template('website.html')

'''---------------------------------------------------------------------------'''

@app.route('/input',methods = ['POST','GET'])
def input():
    if request.method=='POST':
        n = request.form.get('n')
        p = request.form.get('p')
        k = request.form.get('k')
        crop = request.form.get('crop')
        location = request.form.get('location')
        area = request.form.get('area')
        dos = request.form.get('dos')

        session["n"] = n 
        session["p"] = p 
        session["k"] = k 
        session["location"] = location 
        session["crop"] = crop 
        session["area"] = area 
        session["dos"] = dos

        if list(session.keys()).sort() == ['fname','lname','mail','phno','passwd','n','p','k','location','crop','area'].sort() and dos != '':
            df = pd.read_csv('data.csv')
            row = {'fname':session["fname"],'lname':session["lname"],'mail':session["mail"],'phno':session["phno"],'passwd':session["passwd"],'location':session['location'],'n':session['n'],'p':session['p'],'k':session['k'],'crop':session['crop'],'area':session['area']}
            df = df.append(row,ignore_index='True')
            df.to_csv('data.csv',index=False)
            return redirect('/home')
        
        else:
            flash('all inputs not registered')
            return redirect('/input')
    return render_template('input.html')
'''----------------------------------------------------------------------------'''

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        df = pd.read_csv('data.csv',index_col=False)
        if email in list(df['mail']):
            if password in list(df[df['mail']==email]['passwd']):
                person = df[df['mail']==email] 
                session["fname"] = list(person["fname"])[0]
                session["lname"] = list(person["lname"])[0]
                session["mail"] = list(person["mail"])[0]
                session["phno"] = list(person["phno"])[0]
                session["passwd"] = list(person["passwd"])[0]
                session["location"] = list(person["location"])[0]
                session["n"] = list(person["n"])[0]
                session["p"] = list(person["p"])[0]
                session["k"] = list(person["k"])[0]
                session["crop"] = list(person["crop"])[0]
                session["dos"] = list(person["dos"])[0]
                session["area"] = list(person["area"])[0]


                return redirect('/home')        


    return render_template('website2.html')

@app.route('/home')
def home():
    title = 'Agromet analysis'
    
    if "fname" in session:
        fname = session["fname"]
        lname = session["lname"]
        mail = session["mail"]
        phno = session["phno"]
        passwd = session["passwd"]
        n = session['n']
        p = session['p']
        k = session['k']
        location = session["location"]
        crop = session['crop']  #none type value 
        dos = session['dos']   #none type value(?)
        area = session['area']
        customer_login = Customer(fname,lname,mail,phno,passwd,location,n,p,k,crop,dos,area)
        l = harvesting(customer_login.dos,customer_login.crop)
        return render_template('index.html',title = title,user = f'{customer_login.fname} {customer_login.lname}',dos = customer_login.dos,doh = l[0],p = l[1] )
    
    else:
        return redirect(url_for("login"))

'''-----------------------------------------------------------------------------------------'''

@app.route('/fertilizers')
def fert():
    title = 'Agromet analysis'
    if "fname" in session:
        fname = session["fname"]
        lname = session["lname"]
        mail = session["mail"]
        phno = session["phno"]
        passwd = session["passwd"]
        location = session["location"]
        n = session['n']
        p = session['p']
        k = session['k']
        crop = session['crop']
        dos = session['dos']
        area = session['area']
        customer_login = Customer(fname,lname,mail,phno,passwd,location,n,p,k,crop,dos,area)
        return render_template('dashboard-fertilizers.html',title = title, c = fertilizer_practice(customer_login))

    else:
        return redirect(url_for("login"))
    

'''--------------------------------------------------------------------------------------------'''

@app.route('/notification')
def notification():
    title = 'Agromet analysis'
    if "fname" in session:
        fname = session["fname"]
        lname = session["lname"]
        mail = session["mail"]
        phno = session["phno"]
        passwd = session["passwd"]
        location = session["location"]
        n = session['n']
        p = session['p']
        k = session['k']
        crop = session['crop']
        dos = session['dos']
        area = session['area']
        
        customer_login = Customer(fname,lname,mail,phno,passwd,location,n,p,k,crop,dos,area)
        l = main_notification_irrigation(customer_login)
        s = ''
        for i in l:
            s+=i
        send_message(s,'12345')
        return render_template('dashboard-notif.html',title = title, dats = main_notification_irrigation(customer_login) )
    
    else:
        return redirect(url_for("login"))

'''---------------------------------------------------------------------------------------------'''

@app.route('/settings')
def setting():
    title = 'Agromet analysis'
    if "fname" in session:
        fname = session["fname"]
        lname = session["lname"]
        mail = session["mail"]
        phno = session["phno"]
        passwd = session["passwd"]
        location = session["location"]
        n = session['n']
        p = session['p']
        k = session['k']
        crop = session['crop']
        dos = session['dos']
        area = session['area']
        customer_login = Customer(fname,lname,mail,phno,passwd,location,n,p,k,crop,dos,area)
        return render_template('dashboard-settings.html',title = title )
    
    else:
        return redirect(url_for("login"))

'''-----------------------------------------------------------------------------------------------'''

@app.route('/weather')
def weather():
    title = 'Agromet analysis'
    if "fname" in session:
        fname = session["fname"]
        lname = session["lname"]
        mail = session["mail"]
        phno = session["phno"]
        passwd = session["passwd"]
        location = session["location"]
        n = session['n']
        p = session['p']
        k = session['k']
        crop = session['crop']
        dos = session['dos']
        area = session['area']
        customer_login = Customer(fname,lname,mail,phno,passwd,location,n,p,k,crop,dos,area)
        wid = main_weather(customer_login)
        return render_template('dashboard-weather.html',title = title, wd = wid )
    
    else:
        return redirect(url_for("login"))
'''-------------------------------------------------------------------------------------------------'''


@app.route('/crop')
def crop():
    title = 'Agromet analysis'
    return render_template('dashboard-crop-stage.html',title = title, datas = crop_gdd_timeline(cust) )

'''--------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------'''

if __name__=='__main__':
    app.run(debug=True)