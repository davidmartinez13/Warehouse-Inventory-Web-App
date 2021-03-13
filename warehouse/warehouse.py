 
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    nam = db.Column("name", db.String(100))
    quant = db.Column("quantity", db.String(100))

    def __init__(self,nam,quant):
        self.nam = nam
        self.quant = quant



class Form(FlaskForm):
    name = StringField('Name')
    quantity = StringField('Quantity')

@app.route ("/view")#to view the entered items in the database enter /view
def view():
    return render_template("view.html", values = users.query.all())

@app.route('/', methods=['GET', 'POST'])
def form():
    form = Form()

    if form.validate_on_submit():# if the request is submitted then do
        n= users(form.name.data,form.quantity.data)#data entry
        db.session.add(n)
        db.session.commit()#save entries
        #return '<h1>The name is {}. The quantity is {}.'.format(form.name.data, form.quantity.data) #show user which values were added
    return render_template('form.html', form=form)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)