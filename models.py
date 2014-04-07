import datetime
from mongoengine import Document, BooleanField
from mongoengine import DateTimeField, StringField
from kcmweb_flask import db, mongodb, url_for, session
from flask_mongoengine.wtf import model_form as mongo_form
from wtforms.ext.sqlalchemy.orm import model_form
from flask_wtf import Form



#blahblah = '1'
#FinVizFinancial = db.Table('finviz_financial', metadata, info={'bind_key': 'finintel'}, autoload=True)
#FinVizOverview = db.Table('finviz_overview', metadata, info={'bind_key': 'finintel'}, autoload=True)
#FinVizValuation = db.Table('finviz_valuation', metadata, info={'bind_key': 'finintel'}, autoload=True)

class FinVizFinancial(db.Model):
    __tablename__ = 'finviz_financial'
    __bind_key__ = 'finintel'
    import_no = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.Text(10))
    market_cap = db.Column(db.Text(10))
    dividend_yield = db.Column(db.Text(10))
    return_on_assets = db.Column(db.Text(10))
    return_on_equity = db.Column(db.Text(10))
    return_on_investment = db.Column(db.Text(10))
    current_ratio = db.Column(db.Text(10))
    quick_ratio = db.Column(db.Text(10))
    long_term_debt_equity = db.Column(db.Text(10))
    debt_equity = db.Column(db.Text(10))
    gross_margin = db.Column(db.Text(10))
    operating_margin = db.Column(db.Text(10))
    profit_margin = db.Column(db.Text(10))
    next_earnings_date = db.Column(db.Text(25))
    last_price = db.Column(db.Text(10))
    last_change = db.Column(db.Text(10))
    last_volume = db.Column(db.Integer)

class FinVizOverview(db.Model):
    __tablename__ = 'finviz_overview'
    __bind_key__ = 'finintel'
    import_no = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.Text(10))
    company_name = db.Column(db.Text(100))
    company_sector = db.Column(db.Text(25))
    company_industry = db.Column(db.Text(50))
    company_country = db.Column(db.Text(30))
    market_cap = db.Column(db.Text(10))
    price_to_earnings = db.Column(db.Text(10))
    last_price = db.Column(db.Text(10))
    last_change = db.Column(db.Text(10))
    last_volume = db.Column(db.Integer)

class FinVizValuation(db.Model):
    __tablename__ = 'finviz_valuation'
    __bind_key__ = 'finintel'
    import_no = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.Text(10))
    market_cap = db.Column(db.Text(10))
    price_to_earnings = db.Column(db.Text(10))
    forward_price_to_earnings = db.Column(db.Text(10))
    price_earnings_growth = db.Column(db.Text(10))
    price_to_sales = db.Column(db.Text(10))
    price_to_book = db.Column(db.Text(10))
    price_to_cash = db.Column(db.Text(10))
    price_to_fcf = db.Column(db.Text(10))
    eps_growth_this_year = db.Column(db.Text(10))
    eps_growth_next_year = db.Column(db.Text(10))
    eps_growth_past_five_years = db.Column(db.Text(10))
    eps_growth_next_five_years = db.Column(db.Text(10))
    sales_growth_past_five_years = db.Column(db.Text(10))
    last_price = db.Column(db.Text(10))
    last_change = db.Column(db.Text(10))
    last_volume = db.Column(db.Integer)

class NewsArticles(db.Model):
    __tablename__ = 'news_articles'
    __bind_key__ = 'finintel'
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publication_name = db.Column(db.Text(20))
    publication_date = db.Column(db.Date)
    article_title = db.Column(db.Text(100))
    article_text = db.Column(db.Text(100000))
    article_tags = db.Column(db.Text(100))
    ticker = db.Column(db.Text(5))
    thoughts_response = db.Column(db.Text(500))

class Post(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    title = StringField(max_length=255, required=True)
    body = StringField(required=True)

    def __unicode__(self):
        return self.title

class Ticker(Document):
    ticker = StringField(required=True)
    cycle_position = StringField()
    macro_strategy = StringField()
    tactical_strategy = StringField()
    guidance = StringField()
    portfolio = BooleanField()
    watchlist = BooleanField()

NewsArticleForm = model_form(NewsArticles, db.session, Form)
PostForm = mongo_form(Post)
TickerForm = mongo_form(Ticker)

