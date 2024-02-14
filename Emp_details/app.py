from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
vj=Flask(__name__)
static_url_path='/static'
vj.secret_key="Vijay@006"
vj.config["MYSQL_HOST"]='localhost'
vj.config["MYSQL_USER"]='root'
vj.config["MYSQL_PASSWORD"]='Vijay@006'
vj.config["MYSQL_DB"]='emp_details'
mysql=MySQL(vj)
@vj.route("/index")
def home():
    cur=mysql.connection.cursor()
    cur.execute("select *from employees inner join signup on employees.Name=signup.username")
    data=cur.fetchone()
    cur.close()
    return render_template("emp.html",value=data)
@vj.route("/")
def homes():
    return render_template("index.html")
@vj.route("/add_employee",methods=["GET","POST"])
def add():
    if request.method=="POST":
        Name=request.form.get("Name")
        Mbl_No=request.form.get("Mbl_No")
        email=request.form.get("email")
        department=request.form.get("department")
        cur=mysql.connection.cursor()
        cur.execute("insert into employees (Name,Mbl_No,email,department) values (%s,%s,%s,%s)",(Name,Mbl_No,email,department))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("emp"))
    return render_template("add.html")
    
@vj.route("/edit/<string:emp_id>",methods=["GET","POST"])
def edit(emp_id):
    if request.method=="POST":
        Name=request.form.get("Name")
        Mbl_No=request.form.get("Mbl_No")
        email=request.form.get("email")
        department=request.form.get("department")
        cur=mysql.connection.cursor()
        cur.execute("update employees set Name=%s,Mbl_No=%s,email=%s,department=%s where emp_id=%s", (Name,Mbl_No,email,department,emp_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))
    cur=mysql.connection.cursor()
    cur.execute("select *from employees where emp_id=%s",(emp_id,))
    data=cur.fetchone
    cur.close()
    return render_template("edit.html",data=data)

@vj.route("/delete/<string:emp_id>",methods=["GET","POST"])
def delete(emp_id):
    cur=mysql.connection.cursor()
    cur.execute("delete from employees where emp_id=%s",(emp_id,))
    cur.connection.commit()
    cur.close()
    return redirect(url_for('home'))

@vj.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        User_Name=request.form.get("username")
        Pass_word=request.form.get("password")
        cur=mysql.connection.cursor()
        cur.execute("select *signup where username=%s,password=%s",(User_Name,Pass_word))
        data=cur.fetchall
        cur.connection.commit()
        cur.close()
        if data:
            session["username"]=User_Name
            return redirect(url_for('table'))
        else:
            return "Invalid password"
    return render_template("login.html")
# @vj.route("/user",methods=["GET","POST"])
# def user():
#     if request.method=="POST":
#         User_Name=request.form.get("username")
#         Pass_word=request.form.get("password")
#         cur=mysql.connection.cursor()
#         cur.execute("select *signup where username=%s,password=%s",(User_Name,Pass_word))
#         data=cur.fetchone
#         cur.connection.commit()
#         cur.close()
#         if data:
#             session["username"]=User_Name
#             return redirect(url_for('emp'))
#         else:
#             return "Invalid password"


@vj.route("/signup",methods=["GET","POST"])
def Signup():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        cur=mysql.connection.cursor()
        cur.execute("insert into signup (username,password) values (%s,%s)",(username,password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("login"))
    return render_template("signup.html")


if __name__=="__main__":
    vj.run(debug=True)

