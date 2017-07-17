# -*- coding: UTF-8 -*-
from flask import Flask
from flask import flash
from flask import json
from flask import render_template, request
from flaskext.mysql import MySQL
from django.utils.safestring import mark_safe

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'WIND327976003'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/iotemplate")
def iotemplate():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "select platform2,count(*) from wbdata group by platform2 order by count(*) desc limit 10;"

    cursor.execute(sql)
    result = cursor.fetchall()
    def structure_result(myresult):
        datalist = []
        textlist = []
        outputdata = []
        for something in myresult:
            datalist.append(int(something[1]))
            textlist.append(something[0])
        outputdata.append(datalist)
        outputdata.append(textlist)
        return outputdata

    datalist = structure_result(result)[0]
    textlist = structure_result(result)[1]

    sql_country_data_count = "select keyword, count(*) from wbdata group by keyword order by count(*) desc;"
    cursor.execute(sql_country_data_count)
    sql_country_data_count_result = cursor.fetchall()
    country_list = structure_result(sql_country_data_count_result)[0]
    country_list_name = structure_result(sql_country_data_count_result)[1]

    sql_total_gender_rank = "select gender,count(*) from wbdata group by gender;"
    cursor.execute(sql_total_gender_rank)
    sql_total_gender_rank_value = cursor.fetchall()
    gender_list_value = structure_result(sql_total_gender_rank_value)[0]
    gender_list = structure_result(sql_total_gender_rank_value)[1]


    return render_template("iotemplate.html",datalist = datalist, textlist = mark_safe(textlist), country_list = country_list, country_list_name = mark_safe(country_list_name), gender_list= mark_safe(gender_list), gender_list_value=gender_list_value)

@app.route('/bar')
def bar():
    return render_template("herosidbar.html")

@app.route('/test/')
def test():

    return render_template('test.html', )


@app.route('/delete/<string:todo_id>')
def delete(todo_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "delete from tbl_user where user_name=" + str(todo_id)
    cursor.execute(sql)

    research = cursor.execute("select * from tbl_user")

    result = cursor.fetchall()
    outputlist = []
    for something in result:
        outputlist.append(int(something[1]))


    return render_template("test.html", todos=outputlist)

@app.route('/test/<parameter>')
def showtest(parameter):
    return render_template('test.html', renderitem = parameter)


@app.route('/plot')
def showplot():
    return render_template('plot.html')

@app.route('/plotdata')
def plotdata():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "select platform2,count(*) from wbdata group by platform2 order by count(*) desc limit 5;"

    cursor.execute(sql)
    result = cursor.fetchall()

    def structure_result(myresult):
        datalist = []
        textlist = []
        outputdata = []
        for something in myresult:
            datalist.append(int(something[1]))
            textlist.append(something[0])
        outputdata.append(datalist)
        outputdata.append(textlist)
        return outputdata

    datalist = structure_result(result)[0]
    textlist = structure_result(result)[1]
    # texts = ["beef","milk","chess"]
    return render_template("plot.html", datalist = datalist, textlist = mark_safe(textlist) )


@app.route('/list')
def shopping():
    food = ["beef","milk","chess"]
    return render_template("shopping.html",food=food)



@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)

