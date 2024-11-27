from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Room(db.Model):
    __tablename__ = 'Room'

    id = db.Column(db.Integer, primary_key=True) 
    room_type = db.Column(db.Integer, nullable=False) 
    description = db.Column(db.String(255))  
    price_per_night = db.Column(db.Float, nullable=False)  
    is_available = db.Column(db.Boolean, default=True)  

    def __repr__(self):
        return f"<Room {self.id} - Type {self.room_type}>"

class Booking(db.Model):
    __tablename__ = 'Booking'

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    phone = db.Column(db.String(20), nullable=False) 
    email = db.Column(db.String(100), nullable=False)  
    checkin_date = db.Column(db.String(10), nullable=False)  
    checkout_date = db.Column(db.String(10), nullable=False)  
    room_type = db.Column(db.Integer, nullable=False)  
    guests = db.Column(db.Integer, nullable=False)  
    services = db.Column(db.String(255))  
    comments = db.Column(db.String(255))  
    status = db.Column(db.String(20), default='pending') 

    def __repr__(self):
        return f"<Booking {self.id} - {self.name}>"

class Service(db.Model):
    __tablename__ = 'Service'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False) 
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Service {self.id} - {self.name}>"


@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')
@app.route('/story')
def story():
    return render_template('story.html')


@app.route('/rooms', methods=['GET', 'POST'])
def book_room():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        checkin_date = request.form['checkin_date']
        checkout_date = request.form['checkout_date']
        room_type = request.form['room_type']
        guests = request.form['guests']
        services = request.form.getlist('services')
        comments = request.form['comments']

        booking = Booking(
            name=name,
            phone=phone,
            email=email,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            room_type=room_type,
            guests=guests,
            services=",".join(services),
            comments=comments
        )
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for('thank_you'))

    return render_template('rooms.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
