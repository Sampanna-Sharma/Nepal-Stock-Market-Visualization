from flask import Flask, redirect, jsonify
from flask import render_template
from flask import request
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'Stockdb.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
#e = create_engine('sqlite:///bookdatabase.db')


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    headline = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    def __init__(self, id, date, headline, link):
        self.date = date
        self.headline = headline
        self.link = link

class Company(db.Model):
    symbol = db.Column(db.String(10), primary_key=True, nullable=False)
    company_name = db.Column(db.String(255))

    def __init__(self, sym, name):
        self.symbol = sym
        self.company_name = name


class DailyPrices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(10),  db.ForeignKey(Company.__table__.c.symbol), nullable=False)
    closing_price = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

    def __init__(self, date, sym, cp, h, l, v):
        self.date = date
        self.symbol =sym
        self.closing_price = cp
        self.high = h
        self.low = l
        self.volume = v

class NewsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'headline', 'link')

class CompanySchema(ma.Schema):
    class Meta:
        fields = ('symbol', 'company_name')

class DailyPriceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'symbol', 'closing_price', 'high', 'low', 'volume')

news_schema = NewsSchema(strict = True)
mnews_schema = NewsSchema(many = True, strict =True)

company_schema = CompanySchema(strict = True)
companies_schema = CompanySchema(many = True, strict =True)

dailyprice_schema = DailyPriceSchema(strict = True)
dailyprices_schema = DailyPriceSchema(many = True, strict =True)


#         def __repr__(self):
#             return "<Title: {}>".format(self.title)


''' @app.route("/", methods=["GET", "POST"])
def home():
        #df = pd.read_csv("Nepse_index.csv")
        #df.to_sql(name='ds', con=e, if_exists='append')
        #temp = pd.read_sql_table(table_name='ds', con=e)
    with e.connect() as connection:
        query = "SELECT * FROM ds"
        result = connection.execute(query)

        s = list(result)
        return render_template('home.html', s=s)
        # connection.close()
 '''
@app.route("/DailyPrices",methods = ["GET", "POST"])
def daily_prices():
    if request.method == 'POST':
        date = request.json['date']
        symbol = request.json['symbol']
        closing_price = request.json['closing_price']
        high = request.json['high']
        low = request.json['low']
        volume = request.json['volume']
        new_dp = DailyPrices(date, symbol, closing_price, high, low, volume)
        db.session.add(new_dp)
        db.session.commit()
        return "Successful"
    else:
        dps = DailyPrices.query.all()
        result = dailyprices_schema.dump(dps)
        print(result.data)
        return jsonify(result.data)
        
     

if __name__ == "__main__":
    app.run(debug=True)
