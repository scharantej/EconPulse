
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///economic_events.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

# Create the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    indicators = db.Column(db.String(120), nullable=False)

# Create the EconomicEvent model
class EconomicEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    impact = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)

# Create the database tables
db.create_all()

# Define the home route
@app.route('/')
def home():
    # Fetch upcoming economic events
    events = EconomicEvent.query.all()

    # Render the home page
    return render_template('index.html', events=events)

# Define the subscribe route
@app.route('/subscribe')
def subscribe():
    # Render the subscribe page
    return render_template('subscribe.html')

# Define the profile route
@app.route('/profile')
def profile():
    # Fetch the user's subscriptions
    user = User.query.filter_by(email=current_user.email).first()

    # Render the profile page
    return render_template('profile.html', user=user)

# Define the subscribe submit route
@app.route('/subscribe/submit', methods=['POST'])
def subscribe_submit():
    # Get the user's email address and selected indicators
    email = request.form['email']
    indicators = request.form.getlist('indicators')

    # Check if the user already exists
    user = User.query.filter_by(email=email).first()

    # If the user does not exist, create a new user
    if not user:
        user = User(email=email, indicators=','.join(indicators))
        db.session.add(user)
        db.session.commit()

    # Otherwise, update the user's indicators
    else:
        user.indicators = ','.join(indicators)
        db.session.commit()

    # Flash a message to the user
    flash('You have successfully subscribed to the selected indicators.')

    # Redirect the user to the home page
    return redirect(url_for('home'))

# Define the profile update route
@app.route('/profile/update', methods=['POST'])
def profile_update():
    # Get the user's new indicators
    indicators = request.form.getlist('indicators')

    # Fetch the user
    user = User.query.filter_by(email=current_user.email).first()

    # Update the user's indicators
    user.indicators = ','.join(indicators)
    db.session.commit()

    # Flash a message to the user
    flash('Your subscriptions have been updated.')

    # Redirect the user to the profile page
    return redirect(url_for('profile'))

# Define the events Upcoming route
@app.route('/events/upcoming')
def events_upcoming():
    # Fetch upcoming economic events
    events = EconomicEvent.query.all()

    # Convert events to JSON format
    events_json = []
    for event in events:
        event_json = {
            'title': event.title,
            'impact': event.impact,
            'date': event.date
        }
        events_json.append(event_json)

    # Return the JSON response
    return jsonify(events_json)

# Define the events Subscribe route
@app.route('/events/subscribe')
def events_subscribe():
    # Get the event id and user email
    event_id = request.args.get('event_id')
    email = request.args.get('email')

    # Check if the user already subscribed to the event
    subscription = Subscription.query.filter_by(event_id=event_id, email=email).first()

    # If the user is not already subscribed, create a new subscription
    if not subscription:
        subscription = Subscription(event_id=event_id, email=email)
        db.session.add(subscription)
        db.session.commit()

    # Flash a message to the user
    flash('You have successfully subscribed to the event.')

    # Redirect the user to the home page
    return redirect(url_for('home'))

# Define the events Unsubscribe route
@app.route('/events/unsubscribe')
def events_unsubscribe():
    # Get the event id and user email
    event_id = request.args.get('event_id')
    email = request.args.get('email')

    # Fetch the subscription
    subscription = Subscription.query.filter_by(event_id=event_id, email=email).first()

    # If the subscription exists, delete it
    if subscription:
        db.session.delete(subscription)
        db.session.commit()

    # Flash a message to the user
    flash('You have successfully unsubscribed from the event.')

    # Redirect the user to the home page
    return redirect(url_for('home'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
