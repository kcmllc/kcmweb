import functools
import httplib2
import oauth2client
from bson import *
from bson.json_util import dumps
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials, Credentials
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, session, g, redirect, url_for, flash, send_file, make_response, jsonify, render_template
from flask_mongomyadmin import MongoMyAdmin
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_googleauth import GoogleFederated
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask.ext.csrf import csrf
from rauth.service import OAuth2Service

from settings import *
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
import json

app = Flask(__name__)
app.config.from_object('settings')
#toolbar = DebugToolbarExtension(app)
Bootstrap(app)
db = SQLAlchemy(app)
mongodb = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(mongodb)
m = MongoMyAdmin(app)
csrf(app)
from models import *
db.create_all()

scope = ['https://www.googleapis.com/auth/plus.login',
         'https://www.googleapis.com/auth/plus.me', 'https://www.googleapis.com/auth/userinfo.profile',
         'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/admin.directory.group',
         'https://www.googleapis.com/auth/admin.directory.group.member', 'https://www.googleapis.com/auth/tasks']
http = ''

@app.route('/oauth2callback')
def authorized():
    code = request.args['code']
    if code:
        # exchange the authorization code for user credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, scope, redirect_uri=request.base_url)
        try:
            credentials = flow.step2_exchange(code)
            session['credentials'] = credentials.to_json()
        except Exception as e:
            print "Unable to get an access token because ", e.message
            flash(e.message)
            return redirect(url_for('index'))
        # store these credentials for the current user in the session
        # This stores them in a cookie, which is insecure. Update this
        # with something better if you deploy to production land
        http = httplib2.Http()
        http = credentials.authorize(http)
        user = build('oauth2', 'v2', http=http).userinfo().get().execute(http=http)
        taskservice = build('tasks', 'v1').tasks().list(tasklist='@default').execute(http=http)
        session['tasklists'] = taskservice.get('items', [])
        adminservice = build('admin', 'directory_v1', http=http).members().list(groupKey='admin@knightcapllc.com', roles='admin').execute(http=http)
        adminlist = adminservice.get('members', [])
        for member in adminlist:
            admins = []
            admins.append(member['email'])
        if user['email'] not in admins:
            session['privilege'] = 'user'
            session['name'] = user['name']
        else:
            session['privilege'] = 'admin'
            session['name'] = user['name']
        print session['privilege']

        return redirect(url_for('index'))

@app.route('/refreshtasks', methods=['GET', 'POST'])
def refreshtasks():
    oauth = OAuth2Credentials.from_json(session['credentials'])
    http = httplib2.Http()
    http = oauth.authorize(http)
    taskservice = build('tasks', 'v1').tasks().list(tasklist='@default').execute(http=http)
    tasks = taskservice.get('items', [])
    return json.dumps(tasks)

@app.route('/addtask', methods=['POST'])
def addtask():
    oauth = OAuth2Credentials.from_json(session['credentials'])
    http = httplib2.Http()
    http = oauth.authorize(http)
    taskservice = build('tasks', 'v1').tasks().list(tasklist='@default').execute(http=http)
    session['tasklists'] = taskservice.get('items', [])
    return redirect(request.referrer)

@app.route('/login')
def login():

    flow = OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                               redirect_uri='http://www.knightcapllc.com' + url_for('authorized'),
                               scope=scope)
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)

@app.route('/logout')
def logout():
    session.pop('privilege', None)
    session.pop('name', None)
    session.pop('tasklists', None)
    session.pop('credentials', None)
    return redirect(url_for('index'))

def authrequired(fn):
        """Request decorator. Forces authentication."""
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            if 'privilege' in session and session['privilege'] != 'admin':
                flash('You do not have access to view this page')
                return redirect(url_for('index'))
            elif 'privilege' not in session:
                flash('You do not have access to view this page')
                return redirect(url_for('index'))
            return fn(*args, **kwargs)
        return decorated

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/finintel', methods=['GET', 'POST'])
@authrequired
def searchfinintel():
    if request.method == 'POST':
        ticker = request.form['ticker']
        return redirect(url_for('finintel', ticker=ticker))
    else:
        return render_template('search_finintel.html')

@app.route('/finintel/<ticker>', methods=['GET', 'POST'])
def finintel(ticker):
    #overview = FinVizOverview.select(ticker=ticker).first()
    overview = FinVizOverview.query.filter_by(ticker=ticker)
    try:
        test = overview[0]
    except Exception, e:
        flash("Ticker not found!")
        return redirect(url_for('searchfinintel'))
    else:
        financial = FinVizFinancial.query.filter_by(ticker=ticker)
        valuation = FinVizValuation.query.filter_by(ticker=ticker)
        articlelist = NewsArticles.query.filter_by(ticker=ticker)
        try:
            mapping = Ticker.objects.get(ticker=ticker.upper())
        except Exception, e:
            mapping = Ticker(ticker=ticker.upper())
        return render_template('finintel.html', overview=overview, financial=financial,
                               valuation=valuation, articlelist=articlelist, mapping=mapping)

@app.route('/article/<id>', methods=['GET','POST'])
def getarticle(id):
    articlemodel = NewsArticles.query.get(id)
    articleform = NewsArticleForm(request.form, articlemodel)
    #articleform = NewsArticleForm(request.form, obj=articlemodel)
    if articleform.validate_on_submit():
        # articlemodel.article_text = articleform.article_text.data
        # articlemodel.publication_name = articleform.publication_name.data
        # articlemodel.publication_date = articleform.publication_date.data
        # articlemodel.article_title = articleform.article_title.data
        # articlemodel.article_text = articleform.article_text.data
        # articlemodel.article_tags = articleform.article_tags.data
        # articlemodel.ticker = articleform.ticker.data
        # articlemodel.thoughts_response = articleform.thoughts_response.data
        articleform.populate_obj(articlemodel)
        db.session.merge(articlemodel)
        db.session.commit()
        flash("Article updated")
        return redirect(url_for('getarticle', id=id))
    return render_template("editarticle.html", form=articleform, articlemodel=articlemodel)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    articlemodel = NewsArticles()
    articleform = NewsArticleForm(request.form, articlemodel)

    if articleform.validate_on_submit():
        articleform.populate_obj(articlemodel)
        print articlemodel.article_title
        db.session.add(articlemodel)
        db.session.commit()
        flash("Article Added!")
        return redirect(url_for("articles"))
    return render_template('articles.html', form=articleform)

@app.route('/research', methods=['GET', 'POST'])
def research():
    return render_template('research.html')

@app.route('/blog', methods=['GET','POST'])
def blog():
    posts = Post.objects.all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/create', methods=['GET','POST'])
def createpost():
    post = Post()
    postform = PostForm(request.form)
    if postform.validate_on_submit():
        postform.populate_obj(post)
        post.save()
        return redirect(url_for('blog'))
    return render_template('create_post.html', postform=postform)

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'GET':
        return render_template('journal.html')
    if request.method == 'POST':
        created_at = request.json.get('created_at')
        title = request.json.get('title')
        body = request.json.get('body')
        post = Post(created_at=created_at, title=title, body=body).save()
        return post.to_json()

@app.route('/journal/<id>', methods=['PUT','DELETE'])
def getentry(id):
    if request.method == 'PUT':
        id = request.json.get('_id.$oid')
        post = Post.objects(_id=id)
        post.from_json(request.json)
        post.update()
    if request.method == 'DELETE':
        post = Post.objects(id=ObjectId(id))
        post.delete()

@app.route('/journalentries',methods=['GET', 'POST'])
def getentries():
    posts = Post.objects.all().order_by('-created_at').to_json()
    return posts

@app.route('/strategymap', methods=['GET','POST'])
def strategymap():
    if request.method == 'POST':

        #data = request.get_json(force=True)
        #print request.content_type
        #print data
        ticker = request.json.get('ticker')
        try:
            mapping = Ticker.objects.get(ticker=ticker)
            mapping.cycle_position = request.json.get('cycle_position') if request.json.get('cycle_position') else mapping.cycle_position
            mapping.macro_strategy = request.json.get('macro_strategy') if request.json.get('macro_strategy') else mapping.macro_strategy
            mapping.tactical_strategy = request.json.get('tactical_strategy') if request.json.get('tactical_strategy') else mapping.tactical_strategy
            mapping.guidance = request.json.get('guidance') if request.json.get('guidance') else mapping.guidance
            mapping.portfolio = request.json.get('portfolio') if request.json.get('portfolio') else mapping.portfolio
            mapping.watchlist = request.json.get('watchlist') if request.json.get('watchlist') else mapping.watchlist
            mapping.save()
            return ticker
        except:
            mapping = Ticker(ticker=request.json.get('ticker'), cycle_position=request.json.get('cycle_position'),
                             macro_strategy=request.json.get('macro_strategy'), tactical_strategy=request.json.get('tactical_strategy'),
                             guidance=request.json.get('guidance'), portfolio=request.json.get('portfoko'),
                             watchlist=request.json.get('watchlist')).save()
    else:
        return redirect(url_for('strategymap'))

if __name__ == '__main__':
    app.run(debug=True)
