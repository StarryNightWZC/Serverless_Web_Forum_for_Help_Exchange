import traceback
from datetime import timedelta

from flask_googlemaps import get_coordinates

from flaskblog.templates import *
from flask import render_template, url_for, flash, redirect, request, Blueprint, session, current_app
#from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import bcrypt
from flaskblog.models import User, Post, Users, Posts
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email
import boto3
import os
import shutil




users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    try:
        if 'user' in session:
            return redirect(url_for('main.home'))

        form = RegistrationForm()
        users_table = Users()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # user = User2(username=form.username.data, email=form.email.data, password=hashed_password)
            #db.session.add(user)
            #db.session.commit()
            username = form.username.data
            email = form.email.data
            password = hashed_password
            address=form.address.data
            try:
                place = get_coordinates(current_app.config['GOOGLEMAPS_KEY'], address)
            except:
                flash("Your address is invalid","warning")
                return render_template('register.html', title='Register', form=form)

            user=users_table.get_user(username)
            user_emails=users_table.query_email(email)
            if user!=None and len(user_emails)!=0:
                flash("Username already exists", "danger")
            elif user!=None:
                flash("Username already exists", "danger")
            elif len(user_emails)!=0:
                if user_emails!=None:print(user_emails)
                flash("Email already exists", "danger")
            else:
                users_table.put_user(username,email,password,address)
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('users.login'))
        return render_template('register.html', title='Register', form=form)

    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return render_template('error.html')
    return ' '


@users.route("/login", methods=['GET', 'POST'])
def login():
    s3 = boto3.client('s3')
    #default_image_path = os.path.join(current_app.config['APP_ROOT'], 'static/img/default.jpg')

#     #s3.upload_file(default_image_path, 'ece1779-final', '/tmp/default/default.jpg')
#
#     #target_image_path = os.path.join(current_app.config['APP_ROOT'], 'static/profile_pics')
#     #shutil.rmtree(target_image_path)
#     #os.mkdir(os.path.join(current_app.config['APP_ROOT'], 'static/profile_pics'))
#
#     #s3.download_file('ece1779-final', '/tmp/default/default.jpg','/tmp/default.jpg')

    if 'user' in session:
        return redirect(url_for('main.home'))
    form = LoginForm()
    users_table = Users()
    if form.validate_on_submit():
        email=form.email.data
        users=users_table.query_email(email)
        if len(users)==0:#users空
            print("!!!")
            flash("You should register first",'danger')
        else:
            user=users[0]
            print(user)
            if len(user['image_file'])==0:
                user['image_file']='https://covid19blog.s3.amazonaws.com/default/default.jpg'
            # else :
            #     if (user['image_file']!='default.jpg'):
            #       #print(target_image_path + '/' + user['image_file'])
            #       # s3.download_file('ece1779-final',
            #       #                '/tmp/'+ user['email'] + '/user_images/{}'.format(user['image_file']),
            #       #                '/tmp/'+user['image_file'])
            if user and bcrypt.check_password_hash(user['password'], form.password.data):
                #print(user['image_file'])
                try:
                    place = get_coordinates(current_app.config['GOOGLEMAPS_KEY'], user['address'])
                    place['infobox'] = "<b>Hello World</b>"
                    user_current_location = [place['lat'], place['lng']]
                except:
                    user_current_location = None
                session.permanent = True
                session['user'] = {
                    'username': user['username'],
                    'email': user['email'],
                    'image_file': user['image_file'],
                    'user_current_location':user_current_location
                }
                next_page = request.args.get('next')
                #flash('Login Successful', 'message')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
def account():
    s3 = boto3.client('s3');
    profile_img_folder = '/tmp'
    if 'user' not in session:
        return redirect(url_for('main.login'))
    form = UpdateAccountForm()
    users_table = Users()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            target_img_path="/".join([profile_img_folder,picture_file])
            s3.upload_file(target_img_path, 'ece1779-final', '/tmp/'+ session['user']['email'] + '/user_images/{}'.format(picture_file))
            url = s3.generate_presigned_url('get_object',
                                            Params={
                                                'Bucket': 'ece1779-final',
                                                'Key': '/tmp/'+ session['user']['email'] + '/user_images/{}'.format(picture_file)
                                            },
                                            ExpiresIn=604800)

            users_table.update_imagefile(session['user']['username'],url,picture_file)
# =======
#             users_table.update_imagefile(session['user']['username'],url)
# >>>>>>> 708ef730537a1e160d1903d5d876ac41188ffdda
            session['user']['image_file'] = url
            flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = session['user']['username']
        form.email.data = session['user']['email']


    image_file = '/tmp/'+ session['user']['image_file']
    #print(session['user']['image_file'])
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    # page = request.args.get('page', 1, type=int)
    # user = User.query.filter_by(username=username).first_or_404()
    # posts = Post.query.filter_by(author=user)\
    #     .order_by(Post.date_posted.desc())\
    #     .paginate(page=page, per_page=5)
    post_table=Posts();
    #list of Post objects
    posts = post_table.query_post_by_username(username)
    length=len(posts)
    print("here",posts)
    user_table=Users()
    return render_template('user_posts.html', posts=posts, user_table=user_table,username=username,length=length)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if 'user' in session:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user=Users()
        user=user.query_email(email=form.email.data)
        if len(user)==0:
            flash('Your account does not exist', 'error')
            return redirect(url_for('users.reset_password'))
        email=user[0]['email']
        username=user[0]['username']
        image_file=user[0]['image_file']
        user=User(email=email,username=username,image_file=image_file)
        #user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if 'user' in session:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        #db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
