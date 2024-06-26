from flask import Flask,render_template
 
app=Flask(__name__)
app.secret_key='someone is lazy'

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


if __name__ == '__main__':
    app.run(debug=True)