from flask import Flask,render_template,request,url_for,redirect,flash,session
from flask_mysqldb import MySQL
import re
app=Flask(__name__)
app.secret_key='someone is lazy'

#CREATE A CONNECTION TO THE DATABASE, database configuration
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='portfolio'

#calling the mysql function
mysql=MySQL(app)

#Validation phonenumber
def is_valid_phone(phone):
    pattern= r'^2547\d{8}$'
    return re.match(pattern,phone)

#Validate email address
def is_valid_email(email):
    pattern= r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern,email)

#search route
@app.route('/search',methods=['POST'])
def search():
    if request.method=='POST':
        value=request.form['value']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE name LIKE %s OR phonenumber LIKE %s OR email LIKE %s OR message LIKE %s", (value,value,value,value))
        data=cur.fetchall()
        cur.close()
        return render_template('search_results.html',contactsr=data)

#END OF SEARCH

#INSERT
@app.route('/insert' , methods=['POST'])
def insert():
    if request.method=='POST':
        flash("Data updated successfully")
        name=request.form['name']
        phone=request.form['phonenumber']
        email=request.form['email']
        message=request.form['message']

        #check for duplicates
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE phonenumber=%s AND email=%s",(phone,email))
        contact=cur.fetchone()
        cur.close()
        
        if not(contact):
            if not(name and email and phone and message):
                flash("All fields are required")
                return redirect(url_for('contact_me'))
            if not(len(name)>=3 and len(email)>=3 and len(message)>=0):
                flash("Textfield values must be greater than or equal to three")
                return redirect(url_for('contact_me'))
            if not phone.isdigit():
                flash("The phonenumber must be numeric")
                return redirect(url_for('contact_me'))
            if not is_valid_phone(phone):
                flash("The phonenumber formart is invalid")
                return redirect(url_for('contact_me'))
            if not is_valid_email(email):
                flash("Email adress format is invalid")
                return redirect(url_for('contact_me'))
        
            else:
                    #Open a connection to database
                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO contacts(name,phonenumber,email,message) VALUES(%s,%s,%s,%s)",(name,phone,email,message))
                mysql.connection.commit()
                flash("Data saved successfully")
                return redirect(url_for('contact_me'))
        else:
            flash("Duplicate entries")
            return redirect(url_for('contact_me'))



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact_me')
def contact_me():
    return render_template('contact.html')

#LOGIN page
@app.route('/login')
def login():
    return render_template("login.html")

#loging in
@app.route('/login_admin', methods=['POST'])
def login_admin():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM admins WHERE email = %s AND password = %s",(email,password))
        user=cur.fetchone()
        cur.close()

        if user :
            session['user_id']=user[0]
            session["user_name"]=user[1]
            return redirect(url_for('admin'))
        
        else :
            flash("Invalid Credentials")
            return redirect(url_for('login'))
        
#logging out
@app.route('/logmeout', methods=['POST'])
def logmeout():
    if request.method == 'POST':
        session.pop('user_id', None)
        session.pop('user_name', None)
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'user_id' in session :
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts")
        data=cur.fetchall()
        cur.close()
        return render_template('admin.html', contactsr=data)
    else :
        flash("Failed !! Login Required")
        return redirect(url_for('login'))

@app.route('/update', methods=["POST"])
def update():
    if request.method == "POST" :
        flash("Data updated successfully")
        id=request.form["id"]
        name=request.form["fullname"]
        phone=request.form["phonenumber"]
        email=request.form["email"]
        message=request.form["message"]
        cur=mysql.connection.cursor()
        cur.execute("""UPDATE contacts SET name=%s, phonenumber=%s, email=%s, message=%s WHERE id=%s""", (name,phone,email,message,id))
        mysql.connection.commit()
        return redirect(url_for("admin"))
    
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        flash("Success!! One record deleted")
        id=request.form['id']
        cur=mysql.connection.cursor()
        cur.execute("""DELETE FROM contacts WHERE id=%s""",(id,))
        mysql.connection.commit()
        return redirect(url_for('admin'))







if __name__ == '__main__':
    app.run(debug=True)