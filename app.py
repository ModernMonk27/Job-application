from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message


app = Flask(__name__)

app.config["SECRET_KEY"] = "aravind123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smpt.gmail.com"
app.config["MAIL_PASSWORD"] = "offhtakpzwweuvvm"
app.config["MAIL_USERNAME"] = "lakshmiaravind.atom@gmail.com"
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_PORT"] = 465

db = SQLAlchemy(app)
mail = Mail(app)

class Form(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80))
    last = db.Column(db.Integer)

    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))
@app.route("/", methods=["GET", "POST"])
def home():
    print(request.method)
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        date = request.form["date"]
        date_obj = datetime.strptime(date,"%Y-%m-%d")
        occupation = request.form["occupation"]
        print(occupation)
        form = Form(first=name,email=email,date=date_obj,occupation = occupation)
        db.session.add(form)
        db.session.commit()
        message_body="hi"

        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[mail],
                          body=message_body)
        mail.send(message)
        flash(f"{name} your application is sent succesfully", "success")


    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)


