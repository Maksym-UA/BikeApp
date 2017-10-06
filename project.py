#  show specific class of the bikes
from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from functools import wraps
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, BikeSpecs
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Bike Store Application"

# Connect to DB and create DB session
engine = create_engine('sqlite:///motorbikes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')  # http://0.0.0.0:5000/login
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits)for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Authorization via Facebook profile
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = (
        "https://graph.facebook.com/oauth/access_token?grant_type=" +
        "fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s"
        % (app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace the
        remaining quotes with nothing so that it can be used directly in
        the graph api calls
        '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = (
        "https://graph.facebook.com/v2.8/me?access_token=%s&fields=" +
        "name,id,email" % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = (
        "https://graph.facebook.com/v2.8/me/picture?access_token=%s&" +
        "redirect=0&height=200&width=200" % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (
        ' " style = "width: 150px; height: 150px;border-radius: 75px;' +
        '-webkit-border-radius: 75px;-moz-border-radius: 75px;"> ')

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = (
        'https://graph.facebook.com/%s/permissions?access_token=%s'
        % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Authorization via Google profile
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (
        ' " style = "width: 150px; height: 150px;border-radius: 75px;' +
        '-webkit-border-radius: 75px;-moz-border-radius: 75px;"> ')
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


#  login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash('Please, log in to your account')
            return redirect('/publicbikes')
    return decorated_function


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        #  del login_session['username']
        #  del login_session['email']
        #  del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API to view all bikes
@app.route('/bikes/JSON')
def allBikesJSON():
    bikes = session.query(BikeSpecs).all()
    return jsonify(bikes=[b.serialize for b in bikes])


# JSON API to view bikes of specific class
@app.route('/bikes/<string:class_name>/JSON')
def bikeClassJSON(class_name):
    class_name
    bikes = session.query(BikeSpecs).filter_by(bike_class=class_name).all()
    return jsonify(bikes=[b.serialize for b in bikes])


# JSON API to view specific bikes
@app.route('/bikes/<int:bike_id>/JSON')
def singleBikeJSON(bike_id):
    bike = session.query(BikeSpecs).filter_by(id=bike_id).one()
    return jsonify(bike=[bike.serialize])


#  landing page
@app.route('/')
@app.route('/index')
def allClasses():
    return render_template('allclasses.html')


#  Show bikes of specific class
@app.route('/bikes/<string:selected_class>')
@login_required
def selectedClass(selected_class):
    bikes = session.query(BikeSpecs).filter_by(bike_class=selected_class).all()
    author = session.query(
        User).filter_by(id=login_session['user_id']).one()
    return render_template(
        'selected_class.html', bikes=bikes, author=author.name,
        user_id=author.id)


# Show bikes when logged out
@app.route('/publicbikes')
def publicBikes():
    bikes = session.query(BikeSpecs).all()
    return render_template('publicbikes.html', bikes=bikes)


# Show all bikes
@app.route('/bikes')
@login_required
def allBikes():
    bikes = session.query(BikeSpecs).order_by(asc(BikeSpecs.bike_name))
    author = session.query(
            User).filter_by(id=login_session['user_id']).one()
    return render_template(
            'allbikes.html', bikes=bikes, author=author.name,
            user_id=author.id)


# Add a new bike
@app.route('/bikes/new/', methods=['GET', 'POST'])
@login_required
def addNewBike():
    if request.method == 'POST':
        author = login_session['user_id']
        newBike = BikeSpecs(
            bike_name=request.form['bike_name'], user_id=author,
            description=request.form['description'],
            price=request.form['price'], bike_class=request.form['bike_class'],
            img=request.form['image'])
        session.add(newBike)
        session.commit()
        flash("New Bike '%s' Successfully Added" % newBike.bike_name)
        return redirect(url_for('allBikes'))
    else:
        return render_template('new_bike.html')


# Edit bike specs
@app.route('/bikes/<int:bike_id>/edit/', methods=['GET', 'POST'])
@login_required
def editBikeSpecs(bike_id):
    editedBike = session.query(
        BikeSpecs).filter_by(id=bike_id).one()

    if editedBike.user_id != login_session['user_id']:
        return (
            "<script>function myFunction() {alert('You are not authorized" +
            "to edit this bike's specs. Please add a new bike in order to" +
            "edit.');}</script><body onload='myFunction()''>")
    if request.method == 'POST':
        if request.form['name']:
            editedBike.bike_name = request.form['name']
        if request.form['description']:
            editedBike.description = request.form['description']
        if request.form['price']:
            editedBike.price = request.form['price']
        if request.form['image']:
            editedBike.img = request.form['image']
        if request.form['bike_class']:
            editedBike.bike_class = request.form['bike_class']
        session.add(editedBike)
        session.commit()
        flash('The bike specs successfully edited')
        return redirect(url_for('allBikes'))
    else:
        image = editedBike.img
        return render_template(
            'editbike.html', bike_id=bike_id, editedBike=editedBike)


# Delete a bike
@app.route('/bikes/<int:bike_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteBike(bike_id):
    bikeToDelete = session.query(BikeSpecs).filter_by(id=bike_id).one()
    if login_session['user_id'] != bikeToDelete.user_id:
        return (
            "<script>function myFunction() {alert('You are not authorized" +
            "to delete this bike. Please add your own bike in order to " +
            "delete later.');}</script><body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(bikeToDelete)
        session.commit()
        flash('Bike %s Successfully Deleted' % bikeToDelete.bike_name)
        return redirect(url_for('allBikes'))
    else:
        return render_template(
            'delete_bike.html', bike_id=bike_id, bikeToDelete=bikeToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            # del login_session['gplus_id']
            # del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('allClasses'))
    else:
        flash("You were not logged in")
        return redirect(url_for('allClasses'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

