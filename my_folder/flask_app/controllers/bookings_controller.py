from flask_app import app
from flask import redirect, request, session, url_for, flash  # Import flash to display success messages
import os
import smtplib
from email.message import EmailMessage
from flask_app.models.users import User
from flask_app.models.bookings import Booking

@app.route('/book', methods=["POST"])
def book():
    if session['user_id'] == 5:
        return redirect('/')
    if not Booking.validate(request.form):
        return redirect(url_for("index") + "#book_form")
    data = {
        **request.form,
        'user_id': session['user_id'],
        'hotel_name': request.form.get('hotel_name', 'N/A')  # Ensure hotel_name is included
    }
    user = User.get_one_user({"id": session['user_id']})
    reciever = user.email
    EMAIL_ADDRESS = os.environ.get("DB_USER")
    EMAIL_PASSWORD = os.environ.get("DB_PASS")
    location = request.form['where_to']
    guests = request.form['how_many']
    arrival = request.form['arrival_date']
    departure = request.form['departure_date']
    hotel = request.form.get('hotel_name', 'N/A')  # Safely retrieve hotel_name or use 'N/A' if missing
    msg = EmailMessage()
    msg['Subject'] = 'Congratulations! Your trip is booked.'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = reciever
    msg.set_content(f"Your trip to {location} for {guests} guests from {arrival} to {departure} and your hotel {hotel} is now confirmed. Thank you for booking with us!")
    print(reciever)
    print(EMAIL_ADDRESS)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    flash("Email sent successfully to your registered email ID!", "success")  # Add success message
    Booking.save(data)
    return redirect('/')
