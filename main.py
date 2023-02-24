from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MY_APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-cafes-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), unique=False, nullable=False)
    open = db.Column(db.String(250), unique=False, nullable=False)
    close = db.Column(db.String(250), unique=False, nullable=False)
    coffee = db.Column(db.String(250), unique=False, nullable=False)
    wifi = db.Column(db.String(250), unique=False, nullable=False)
    power = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return f'<Cafe {self.name}>'


with app.app_context():
    db.create_all()


# new_cafe = Cafe(name="Mare Street Market", location="https://goo.gl/maps/ALR8iBiNN6tVfuAA8", open="8AM", close="13PM",
#                 coffee="☕☕", wifi="💪💪💪", power="🔌🔌🔌")
# db.session.add(new_cafe)
# db.session.commit()


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Location URL', validators=[DataRequired(), URL()])
    open_time = StringField(label='open time', validators=[DataRequired()])
    closing_time = StringField(label='closing time', validators=[DataRequired()])
    coffee_rating = SelectField(label='coffee rating', choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField(label='wifi rating', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_outlet_rating = SelectField(label='power outlet rating', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=all_cafes)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    new_row = form.cafe.data, form.location.data, form.open_time.data, form.closing_time.data, form.coffee_rating.data, form.wifi_rating.data, form.power_outlet_rating.data
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.cafe.data, location=form.location.data, open=form.open_time.data, close=form.closing_time.data,
                        coffee=form.coffee_rating.data, wifi=form.wifi_rating.data, power=form.power_outlet_rating.data)
        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
