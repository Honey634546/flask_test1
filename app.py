from flask import Flask, request, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import *
from wtforms.validators import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
app.config["WTF_CSRF_ENABLED"] = True
CsrfProtect(app)


class cityForm(FlaskForm):
    """
    签证中心城市表单
    """
    city = SelectField(label="签证中心位于",
                       validators=[DataRequired()],
                       choices=[(1, "Beijing"), (2, "Shanghai"), (3, "Hangzhou"), (4, "chengdu")],
                       coerce=int)
    submit = SubmitField(label=u"提交")


class categoryForm(FlaskForm):
    num = IntegerField(label="申请人数（最大为5）",
                       validators=[DataRequired(), NumberRange(0, 5, message="您填写的数字越界或者不是数字")])
    category = SelectField(label="签证类别",
                           validators=[DataRequired()],
                           choices=[(1, "General"), (2, "Wrok and Holiday Visa")],
                           coerce=int)
    submit = SubmitField("提交")


class emailForm(FlaskForm):
    email = StringField(label="电子邮箱地址",
                        validators=[DataRequired(), Email(message="邮箱格式不正确")])
    submit = SubmitField("提交")


class detailForm(FlaskForm):
    Passport_Number = StringField(label="Passport Number",
                                  validators=[DataRequired()])
    values = ["male", "female"]
    Gender = StringField(label="Gender",
                         validators=[DataRequired(), AnyOf(values=values, message="请在male和female之中填写一个")])
    Name = StringField(label="Name",
                       validators=[DataRequired()])
    Surname = StringField(label="Surname",
                          validators=[DataRequired()])
    Area_Code = StringField(label="Area_Code",
                            validators=[DataRequired()])
    Mobile_Number = StringField(label="Mobile_Number",
                                validators=[DataRequired()])
    submit = SubmitField(label="submit")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/city', methods=["GET", "POST"])
def city():
    form = cityForm()
    if form.validate_on_submit():
        print(form.city)
        city = form.city
        # city = request.form.get("city")
        print(1, city)
        return redirect(url_for("category"))
    else:
        return render_template("city.html", form=form)


@app.route('/category', methods=["GET", "POST"])
def category():
    form = categoryForm()

    if form.validate_on_submit():
        num = request.form.get("num")
        category = request.form.get("category")
        print(num, category)
        return redirect(url_for("email"))
    else:
        num = request.form.get("num")

        return render_template('category.html', form=form)


@app.route('/email', methods=["GET", "POST"])
def email():
    form = emailForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        print(email)
        return redirect(url_for("detail"))
    return render_template("email.html", form=form)


@app.route('/detail', methods=["GET", "POST"])
def detail():
    form = detailForm()
    if form.validate_on_submit():
        Passport_Number = request.form.get("Passport_Number")
        Gender = request.form.get("Gender")
        Name = request.form.get("Name")
        Surname = request.form.get("Surname")
        Area_Code = request.form.get("Area_Code")
        Mobile_Number = request.form.get("Mobile_Number")
        print(Passport_Number, Gender, Name, Surname, Area_Code, Mobile_Number)
        return redirect(url_for("end"))
    return render_template("detail.html", form=form)


@app.route('/end', methods=["GET", "POST"])
def end():
    return render_template("end.html")


if __name__ == '__main__':
    app.run()
