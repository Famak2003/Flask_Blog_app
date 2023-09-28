import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # Generates a random name for the image
    # This returns two values....It returns the file name without the extension e.g(pelumi), and returns the extension its self e.g(jpg)////// '_' means when you dont need the variable
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # "app.root_path" is the root path of this application all the way up to the package directory.....So what this line is doing is creating a path for the picture by joining all of them together
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # We resize the image to 125 X 125 before saving it
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) # Here, we save the picture to the created path

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email]) # This are the header of the mail
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)