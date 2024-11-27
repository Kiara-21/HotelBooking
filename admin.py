import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import time
from plyer import notification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/Desktop/Project/instance/hotel_booking.db'
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


def get_bookings():
    with app.app_context():
        print("Отримуємо бронювання...")
        bookings = db.session.execute(text("SELECT * FROM Booking WHERE status='pending'")).fetchall()
    return bookings


def refresh_bookings():
    print("Оновлюємо бронювання...")
    bookings = get_bookings()
    return bookings


def confirm_booking(booking_id):
    with app.app_context():
        booking = Booking.query.get(booking_id)
        if booking:
            booking.status = 'confirmed'
            db.session.commit()
            print(f"Бронювання {booking_id} підтверджено.")


def cancel_booking(booking_id):
    with app.app_context():
        booking = Booking.query.get(booking_id)
        if booking:
            booking.status = 'canceled'
            db.session.commit()
            print(f"Бронювання {booking_id} скасовано.")


def send_notification(message):
    notification.notify(
        title='З*явилось нове бронювання!',
        message=message,
        timeout=10
    )


def run_gui():
    last_booking_count = 0 

    def update_ui():
        nonlocal last_booking_count

        print("Оновлення...")
        bookings = refresh_bookings()

        if len(bookings) > last_booking_count:
            print("Знайдено нове бронювання")
            send_notification(f"Знайдено нове бронювання! Всього бронювань: {len(bookings)}")
            last_booking_count = len(bookings) 

        for row in tree.get_children():
            tree.delete(row)

        for booking in bookings:
            tree.insert("", "end", values=(booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7], booking[8], booking[9], booking[10]))

        root.after(5000, update_ui)

    def on_confirm():
        selected = tree.selection()
        if selected:
            booking_id = tree.item(selected[0])['values'][0]
            confirm_booking(booking_id)
            update_ui()

    def on_cancel():
        selected = tree.selection()
        if selected:
            booking_id = tree.item(selected[0])['values'][0]
            cancel_booking(booking_id)
            update_ui()

    root = tk.Tk()
    root.title("Панель адміністратора")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    columns = ("ID", "Name", "Phone", "Email", "Check-in Date", "Check-out Date", "Room Type", "Guests", "Services", "Comments", "Status")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    
    tree.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.pack(side="right", fill="y")
    tree.config(yscrollcommand=scroll.set)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    confirm_button = tk.Button(button_frame, text="Підтвердити", command=on_confirm)
    confirm_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Скасувати", command=on_cancel)
    cancel_button.pack(side=tk.LEFT, padx=10)

    refresh_button = tk.Button(button_frame, text="Оновити", command=update_ui)
    refresh_button.pack(side=tk.LEFT, padx=10)

    update_ui()

    root.mainloop()

if __name__ == "__main__":
    print("Запуск...")
    run_gui()
