import smtplib
import pyrebase
import RPi.GPIO as GPIO
import time

# setting GPIO pins
GPIO.setmode(GPIO.BCM)
motion_pin = 17
button_pin = 18

# SMTP details 
sender_email = "smartshop.3765@gmail.com"
recipient_email = "shravelrishyan@gmail.com"
subject = "Mail Posted!"
body = "A new Mail has been posted on your mailbox"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "smartshop.3765@gmail.com"
smtp_password = "gzumvlddihunutku"

# On push button
def on_button_press(channel):
    button_press()
    print("Button pressed!")
    
# on Motion detected
def on_motion_detected(channel):
    mail_detected()

# GPIO setuos
GPIO.setup(motion_pin, GPIO.IN)
GPIO.add_event_detect(motion_pin, GPIO.RISING, callback=on_motion_detected)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=on_button_press, bouncetime=200)

# Firebase configuration
firebase_config = {
  "apiKey": "AIzaSyCOFOCT6fF9PhB6TXB_fiZWjeOJNHUmyb4",
  "authDomain": "mailbox-2b829.firebaseapp.com",
  "databaseURL": "https://mailbox-2b829-default-rtdb.firebaseio.com",
  "projectId": "mailbox-2b829",
  "storageBucket": "mailbox-2b829.appspot.com",
  "messagingSenderId": "1012165531027",
  "appId": "1:1012165531027:web:59152dd7001516cd7f4466",
  "measurementId": "G-G0ZKDPKN37"
};


firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# sending the mail and incrementing the Real time database
def mail_detected() :
	server = smtplib.SMTP(smtp_server, smtp_port)
	server.starttls()
	server.login(smtp_username, smtp_password)
	server.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{body}")
	print("Email sent successfully!")

	mails_ref = db.child("mails")
	current_value = mails_ref.get().val() 

	if current_value is None:
		current_value = 0

	new_value = current_value + 1
	db.child("mails").set(new_value)

	print(f"Successfully incremented 'mails/count' variable. New value: {new_value}")
def button_press():
    db.child("mails").set(0)
    
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()

