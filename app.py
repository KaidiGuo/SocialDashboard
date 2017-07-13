from flask import Flask
from flask import flash
from flask import json
from flask import render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'WIND327976003'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/iotemplate")
def iotemplate():
    return render_template("iotemplate.html")
@app.route('/bar')
def bar():
    return render_template("herosidbar.html")

@app.route('/test/')
def test():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "select * from tbl_user"

    cursor.execute(sql)
    result = cursor.fetchall()
    outputlist = []
    for something in result:
        outputlist.append(int(something[1]))
    # flash('New entry was successfully posted')
    return render_template('test.html', todos = outputlist)


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
    sql = "select * from tbl_user"

    cursor.execute(sql)
    result = cursor.fetchall()
    outputlist =[]
    for something in result:
        outputlist.append(int(something[1]))

    # flash('New entry was successfully posted')

    return render_template("plot.html",food = outputlist)


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

