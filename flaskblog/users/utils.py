import imghdr
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    """
    Get profile pic, get its extension, give it a random coded name
    and save it to the project subfolder
    :param form_picture: picture from UpdateAccountForm
    :return: random coded name given to the picture
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # --- resize image before saving
    output_size = (250, 250)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='admin@quant-analytics.net', recipients=[user.email])
    msg.body = f"To reset your password, visit the following link:\n" \
               f"{url_for('users.reset_token', token=token, _external=True)}\n" \
               f"If you did not make this request, then simply ignore this email and no changes will be made."
    mail.send(msg)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


