#from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np
from flask import *
from twilio.rest import Client

app = Flask(__name__)

model=pickle.load(open('model.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    t1=request.form.get('dat',False)
    print("jhbjcbhdjbc",t1)
    dist=request.form.get('district',False)
    print("jhbjcbhdjbc",dist)
    month=t1[5:7]
    day=t1[8:10]
    time=t1[11:13]
    int_features=[]
    int_features.append(month)
    int_features.append(day)
    int_features.append(time)
    int_features.append(dist)
    num=request.form['phno']
    num=int(num)
    print(int_features) 
    final=[np.array(int_features,dtype=int)]
    print(final)
    output=model.predict(final)
    print(output)
    print(num)
    if output==0:
        pred='Less crime ,Happy journey (crime less than 13) {}'.format(output)
        sendsms(num,pred)
        return render_template('home.html',pred='Less crime ,Happy journey (crime less than 13) {}'.format(output))
    elif output==1:
        pred='Moderate crime, be precautious {}'.format(output)
        sendsms(num,pred)
        return render_template('home.html',pred='Moderate crime, be precautious {}'.format(output))
    else:
        pred='High crime rate,change your time travel {}'.format(output)
        sendsms(num,pred)
        return render_template('home.html',pred='High crime rate,change your time travel {}'.format(output))
        

def sendsms(phno,content):
    
    account_sid = 'AC238bf3dcdf3f9565401efd6c853e994e' 
    auth_token = 'f8fd6c89933f5d762a3c82fe5a803133' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(  
        messaging_service_sid='MG4943bef71ae4aac352e1f469b1000d4b',
        body=content,      
        to='+91'+str(phno)
        )
    print(message.sid)
    
    
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
