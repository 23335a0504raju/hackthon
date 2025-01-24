
print("Content-type:text/html\n\n");
from flask import Flask, request, render_template,url_for
import joblib
import pandas as pd
import webbrowser
import mysql.connector as my
def open():
       webbrowser.open('http://127.0.0.1:5000')

def connector():
    conn = my.connect(host="localhost",user="root",password="",database="heart")
    cursor = conn.cursor()
    return conn,cursor

app1 = Flask(__name__)

@app1.route('/')
def registers():
    return render_template('heart1.html')

@app1.route('/sample2', methods=['GET', 'POST'])
def sample2():
       if request.method == 'POST':
              age = request.form['age']
              sex = request.form['sex']
              if sex == 'Male':
                     sex = 0
              else:
                     sex = 1
              cp = request.form['cp']
              if cp == '0':
                     cp = 0
              elif cp == '1':
                     cp = 1
              elif cp == '2':
                     cp = 2
              else:
                     cp = 3
              trestbps = request.form['trestbps']
              chol = request.form['chol']
              fbs = request.form['fbs']
              if fbs == '1':
                     fbs = 1
              else:
                     fbs = 0
              restecg = int(request.form['restecg'])
              thalach = request.form['thalach']
              exang = int(request.form['exang'])
              oldpeak = request.form['oldpeak']
              slope = request.form['slope']
              ca = request.form['ca']
              thal = int(request.form['thal'])

            
              val = [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), 
                     float(restecg), float(thalach), float(exang), float(oldpeak), 
                     float(slope), float(ca), float(thal)]

              import numpy as np
              from sklearn.model_selection import train_test_split
              from sklearn.ensemble import RandomForestClassifier
              from sklearn.preprocessing import StandardScaler
              import pandas as pd

              data = pd.read_csv("heart.xls")
              X = data.drop(columns='target', axis=1)
              Y = data['target']
              X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

              sc = StandardScaler()
              X_train = sc.fit_transform(X_train)  
              X_test = sc.transform(X_test)

              model = RandomForestClassifier()
              model.fit(X_train, Y_train)

           
              result = model.predict([val])

            
              conn, cursor = connector()
              query = """INSERT INTO heart_params (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
              values = (int(age), int(sex), int(cp), int(trestbps), int(chol), int(fbs), int(restecg), 
                        int(thalach), int(exang), float(oldpeak), int(slope), int(ca), int(thal), int(result[0]))

              cursor.execute(query, values)
              conn.commit()  
              cursor.close()
              conn.close()

        
              if result[0] == 0:
                     resultss = 'No heart disease'
              else:
                     resultss = 'Heart disease detected'

              return render_template("/resultss.html", results=resultss)

       else:
              return render_template('heart1.html')


if __name__ == '__main__':
       open()
       app1.run(debug=False)
