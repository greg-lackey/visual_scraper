from flask import render_template, flash, redirect, url_for, request
from flask import send_from_directory
from app import app, db
from app.forms import LoginForm, ScraperForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Documents, PrevDoc
from werkzeug.urls import url_parse
from sqlalchemy.sql.expression import func
from datetime import datetime
import os

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    scraped_docs = Documents.query.filter_by(scraped=True).count()
    not_scraped_docs = Documents.query.filter_by(scraped=False).count()
    curr_user = User.query.filter_by(username=current_user.username).first()
    users = User.query.all()
    return render_template('index.html',  title = 'Scraping Page', curr_user=curr_user,
                          scraped_docs = scraped_docs, not_scraped_docs =
                          not_scraped_docs, users=users)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        #Assing a current document immediately upon login
        curr_doc = Documents.query.filter_by(scraped=False).filter_by(user_id=None).order_by(func.random()).first()
        curr_doc.user_id = current_user.id
        curr_doc.in_use = True
        #Grab the only previous doc for the user
        prev_doc = PrevDoc.query.filter_by(user_id=current_user.id).first()
        prev_doc.in_use = True
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In', form=form)

@app.route('/logout')
def logout():
    #See if a document has in_use = True and set to false
    curr_doc = Documents.query.filter_by(in_use=True).filter_by(user_id=current_user.id).first()
    curr_doc.user_id = None
    curr_doc.in_use = False
    #Grab the only previous doc for the user
    prev_doc = PrevDoc.query.filter_by(in_use=True).filter_by(user_id=current_user.id).first()
    prev_doc.in_use = False
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/scraper/', methods=['GET', 'POST'])
@login_required
def scraper():
    curr_doc = Documents.query.filter_by(in_use=True).filter_by(user_id=current_user.id).first()
    prev_doc = PrevDoc.query.filter_by(in_use=True).filter_by(user_id=current_user.id).first()
    form = ScraperForm(test_date = curr_doc.test_date)
    if form.validate_on_submit():
        #Set current doc for update
        curr_doc.test_date = form.test_date.data    
        curr_doc.init_bradenhead_pressure = form.init_bradenhead_pressure.data 
        curr_doc.init_intermediate_1_pressure = form.init_intermediate_1_pressure.data 
        curr_doc.init_intermediate_2_pressure = form.init_intermediate_2_pressure.data 
        curr_doc.init_casing_pressure = form.init_casing_pressure.data 
        curr_doc.init_tubing_pressure = form.init_tubing_pressure.data 
        curr_doc.fin_bradenhead_pressure = form.fin_bradenhead_pressure.data 
        curr_doc.fin_intermediate_1_pressure = form.fin_intermediate_1_pressure.data 
        #curr_doc.fin_intermediate_2_pressure = form.fin_intermediate_2_pressure.data 
        curr_doc.fin_casing_pressure = form.fin_casing_pressure.data 
        curr_doc.bradenhead_buildup_pressure = form.bradenhead_buildup_pressure.data 
        curr_doc.intermediate_1_buildup_pressure = form.intermediate_1_buildup_pressure.data 
        #curr_doc.intermediate_2_buildup_pressure = form.intermediate_2_buildup_pressure.data 
        curr_doc.shut_in = form.shut_in.data
        curr_doc.water_flow = form.water_flow.data
        curr_doc.oil_flow = form.oil_flow.data
        curr_doc.scraped = True
        curr_doc.scraper_id = current_user.id
        curr_doc.scraper_name = current_user.username
        curr_doc.comment = form.comment.data 
        curr_doc.date_scraped = datetime.utcnow()
        curr_doc.user_id = None
        curr_doc.in_use = False
        #Set previous doc for update
        prev_doc.doc_id = curr_doc.id
        prev_doc.doc_path = curr_doc.doc_path
        prev_doc.doc_name = curr_doc.doc_name
        prev_doc.api_numb = curr_doc.api_number
        prev_doc.test_date = form.test_date.data
        prev_doc.init_bradenhead_pressure = form.init_bradenhead_pressure.data 
        prev_doc.init_intermediate_1_pressure = form.init_intermediate_1_pressure.data 
        prev_doc.init_intermediate_2_pressure = form.init_intermediate_2_pressure.data 
        prev_doc.init_casing_pressure = form.init_casing_pressure.data 
        prev_doc.init_tubing_pressure = form.init_tubing_pressure.data 
        prev_doc.fin_bradenhead_pressure = form.fin_bradenhead_pressure.data 
        prev_doc.fin_intermediate_1_pressure = form.fin_intermediate_1_pressure.data 
        #prev_doc.fin_intermediate_2_pressure = form.fin_intermediate_2_pressure.data 
        prev_doc.fin_casing_pressure = form.fin_casing_pressure.data 
        prev_doc.bradenhead_buildup_pressure = form.bradenhead_buildup_pressure.data 
        prev_doc.intermediate_1_buildup_pressure = form.intermediate_1_buildup_pressure.data 
        #prev_doc.intermediate_2_buildup_pressure = form.intermediate_2_buildup_pressure.data 
        prev_doc.shut_in = form.shut_in.data
        prev_doc.water_flow = form.water_flow.data
        prev_doc.oil_flow = form.oil_flow.data
        prev_doc.scraped = True
        prev_doc.scraper_id = current_user.id
        prev_doc.scraper_name = current_user.username
        prev_doc.comment = form.comment.data 
        prev_doc.date_scraped = datetime.utcnow()
        db.session.commit()
        flash(str(curr_doc.doc_name)+' Successfully Submitted!')
        #Adding a new current document
        curr_doc = Documents.query.filter_by(scraped=False).filter_by(user_id=None).order_by(func.random()).first()
        curr_doc.user_id = current_user.id
        curr_doc.in_use = True
        db.session.commit()
        return redirect(url_for('scraper'))

    return render_template('scraper.html', title='Scraper', curr_doc=curr_doc, form = form)


@app.route('/prevscraper/', methods=['GET', 'POST'])
@login_required

def prev_scraper():
    #If the go back button is pressed. The curr_doc will still be the one from
    #the previous page
    curr_doc = Documents.query.filter_by(in_use=True).filter_by(user_id=current_user.id).first()
    curr_doc.user_id = None
    curr_doc.in_use = False
    db.session.commit()
    #Tie the current doc to the previous doc!
    prev_doc = PrevDoc.query.filter_by(user_id=current_user.id).first()
    curr_doc = Documents.query.filter_by(id=prev_doc.doc_id).first()
    curr_doc.user_id = current_user.id
    curr_doc.in_use = True
    db.session.commit()
    form = ScraperForm(test_date = prev_doc.test_date,
                       init_bradenhead_pressure=prev_doc.init_bradenhead_pressure,
                       init_intermediate_1_pressure=prev_doc.init_intermediate_1_pressure,
                       init_intermediate_2_pressure=prev_doc.init_intermediate_2_pressure,
                       init_casing_pressure=prev_doc.init_casing_pressure,
                       init_tubing_pressure=prev_doc.init_tubing_pressure,
                       fin_bradenhead_pressure = prev_doc.fin_bradenhead_pressure,
                       fin_intermediate_1_pressure = prev_doc.fin_intermediate_1_pressure,
                       fin_intermediate_2_pressure = prev_doc.fin_intermediate_2_pressure,
                       fin_casing_pressure = prev_doc.fin_casing_pressure,
                       fin_tubing_pressure = prev_doc.fin_tubing_pressure,
                       bradenhead_buildup_pressure = prev_doc.bradenhead_buildup_pressure,
                       intermediate_1_buildup_pressure = prev_doc.intermediate_1_buildup_pressure,
                       intermediate_2_buildup_pressure = prev_doc.intermediate_2_buildup_pressure,
                       shut_in = prev_doc.shut_in,
                       water_flow=prev_doc.water_flow, oil_flow =
                       prev_doc.oil_flow, comment=prev_doc.comment)

    if form.validate_on_submit():
        #Set current doc for update
        curr_doc.test_date = form.test_date.data
        curr_doc.init_bradenhead_pressure = form.init_bradenhead_pressure.data
        curr_doc.init_intermediate_1_pressure = form.init_intermediate_1_pressure.data 
        curr_doc.init_intermediate_2_pressure = form.init_intermediate_2_pressure.data 
        curr_doc.init_casing_pressure = form.init_casing_pressure.data 
        curr_doc.init_tubing_pressure = form.init_tubing_pressure.data 
        curr_doc.fin_bradenhead_pressure = form.fin_bradenhead_pressure.data 
        curr_doc.fin_intermediate_1_pressure = form.fin_intermediate_1_pressure.data 
        #curr_doc.fin_intermediate_2_pressure = form.fin_intermediate_2_pressure.data 
        curr_doc.fin_casing_pressure = form.fin_casing_pressure.data 
        curr_doc.bradenhead_buildup_pressure = form.bradenhead_buildup_pressure.data 
        curr_doc.intermediate_1_buildup_pressure = form.intermediate_1_buildup_pressure.data 
        #curr_doc.intermediate_2_buildup_pressure = form.intermediate_2_buildup_pressure.data 
        curr_doc.shut_in = form.shut_in.data
        curr_doc.water_flow = form.water_flow.data
        curr_doc.oil_flow = form.oil_flow.data
        curr_doc.scraped = True
        curr_doc.scraper_id = current_user.id
        curr_doc.scraper_name = current_user.username
        curr_doc.comment = form.comment.data 
        curr_doc.date_scraped = datetime.utcnow()
        curr_doc.user_id = None
        curr_doc.in_use = False
        #Set previous doc for update
        prev_doc.doc_id = curr_doc.id
        prev_doc.doc_path = curr_doc.doc_path
        prev_doc.doc_name = curr_doc.doc_name
        prev_doc.api_numb = curr_doc.api_number
        prev_doc.test_date = form.test_date.data
        prev_doc.init_bradenhead_pressure = form.init_bradenhead_pressure.data
        prev_doc.init_intermediate_1_pressure = form.init_intermediate_1_pressure.data 
        prev_doc.init_intermediate_2_pressure = form.init_intermediate_2_pressure.data 
        prev_doc.init_casing_pressure = form.init_casing_pressure.data 
        prev_doc.init_tubing_pressure = form.init_tubing_pressure.data 
        prev_doc.fin_bradenhead_pressure = form.fin_bradenhead_pressure.data 
        prev_doc.fin_intermediate_1_pressure = form.fin_intermediate_1_pressure.data 
        #prev_doc.fin_intermediate_2_pressure = form.fin_intermediate_2_pressure.data 
        prev_doc.fin_casing_pressure = form.fin_casing_pressure.data 
        prev_doc.bradenhead_buildup_pressure = form.bradenhead_buildup_pressure.data 
        prev_doc.intermediate_1_buildup_pressure = form.intermediate_1_buildup_pressure.data 
        #prev_doc.intermediate_2_buildup_pressure = form.intermediate_2_buildup_pressure.data 
        prev_doc.shut_in = form.shut_in.data
        prev_doc.water_flow = form.water_flow.data
        prev_doc.oil_flow = form.oil_flow.data
        prev_doc.scraped = True
        prev_doc.scraper_id = current_user.id
        prev_doc.scraper_name = current_user.username
        prev_doc.comment = form.comment.data 
        prev_doc.date_scraped = datetime.utcnow()
        db.session.commit()
        flash(str(curr_doc.doc_name)+' Successfully Submitted!')
        #Adding a new current document
        curr_doc = Documents.query.filter_by(scraped=False).filter_by(user_id=None).order_by(func.random()).first()
        curr_doc.user_id = current_user.id
        curr_doc.in_use = True
        db.session.commit()
        return redirect(url_for('scraper'))


    return render_template('scraper.html', title='Scraper', curr_doc=curr_doc, form = form)



