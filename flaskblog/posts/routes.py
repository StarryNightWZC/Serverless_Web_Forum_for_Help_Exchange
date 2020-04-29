from flask import (render_template, url_for, flash,redirect, request, abort, Blueprint, session, current_app)
#from flask_login import current_user, login_required
from flask_googlemaps import get_coordinates

#from flaskblog import db
from flaskblog.models import Post, Posts, Users
from flaskblog.posts.forms import PostForm
from datetime import datetime
from flask_googlemaps import GoogleMaps, Map
from flask_googlemaps import get_address, get_coordinates

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
def new_post():
    if 'user' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('users.login'))
    form = PostForm()
    posts_table = Posts()
    if form.validate_on_submit():
        # post = Post(title=form.title.data, type=form.type.data, phone=form.phonember.data,emailaddress=form.emailaddress.data,
        #             address=form.address.data,content=form.content.data, author=session['user']['username'])
        # db.session.add(post)
        # db.session.commit()
        try:
            place = get_coordinates(current_app.config['GOOGLEMAPS_KEY'],form.address.data)
        except:
            form.address.data=None
            flash("Your address is not valid","warning")
            return render_template('create_post.html', title='New Post',
                                   form=form, legend='New Request')
        posts_table.put_post(title=form.title.data, type=form.type.data, phone=form.phonember.data,
                             email=form.emailaddress.data,
                             address=form.address.data,
                             content=form.content.data,
                             username=session['user']['username'],
                             sdate=form.sdate.data.strftime('%Y-%m-%d'),
                             fdate=form.fdate.data.strftime('%Y-%m-%d'),
                             lat=place['lat'],
                             lng=place['lng']
                            )

        flash('Your request has been created!', 'success')
        return redirect(url_for('main.offerhelp'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Request')


@posts.route("/post/<string:post_id>")
def post(post_id):
    if 'user' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('users.login'))

    post=Posts()
    post=post.get_post(post_id)
    print("_-----------------")
    print(session)
    print(session['user']['user_current_location'])
    locations = []  # long list of coordinates
    #place = get_coordinates(current_app.config['GOOGLEMAPS_KEY'], session['user']['user_current_location'])
    place={}
    try:
        place['lat'] = session['user']['user_current_location'][0]
        place['lng'] = session['user']['user_current_location'][1]
        place['icon'] = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
        place['infobox'] = "<b>Your Current Location</b>"
        locations.append(place)
    except:
        flash("Your location shows error, Please input your location in search bar","warning")
        return redirect(url_for('main.offerhelp'))
    place1={}
    place1 = get_coordinates(current_app.config['GOOGLEMAPS_KEY'], post.address)
    place1['icon'] = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
    place1['infobox'] = "<b>Target Location</b>"
    locations.append(place1)

    print(locations)

    map_offerhelp = Map(
        identifier="map_offerhelp",
        style=(
            "height:350px;"
            "width:730px;"
        ),
        lat=locations[0]['lat'],
        lng=locations[0]['lng'],
        markers=[(loc['lat'], loc['lng'], loc['infobox'],loc['icon']) for loc in locations],
        fit_markers_to_bounds=True
    )
    print(post.timestamp)
    user_table = Users()
    #post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post,user_table=user_table,map_offerhelp=map_offerhelp)
#>>>>>>> e6da0986ad809f643f141827cb64633cc9d0c652


@posts.route("/post/<string:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    if 'user' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('users.login'))
    post_table=Posts()
    post = post_table.get_post(post_id)
    if post.username != session['user']['username']:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.type=form.type.data
        post.sdate=datetime.strftime(form.sdate.data,'%Y-%m-%d')
        post.fdate = datetime.strftime(form.fdate.data, '%Y-%m-%d')
        #post.fdate=form.fdate.data
        post.address=form.address.data
        post.email=form.emailaddress.data
        post.phone=form.phonember.data
        post.content = form.content.data
        post.type = form.type.data
        #db.session.commit()
        post_table.update_post(post)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.type.data=post.type
        form.fdate.data=datetime.strptime(post.fdate, '%Y-%m-%d')
        form.sdate.data = datetime.strptime(post.sdate, '%Y-%m-%d')
        form.phonember.data=post.phone
        form.address.data=post.address
        form.emailaddress.data=post.email
        form.content.data = post.content
        form.type.data=post.type
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<string:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    if 'user' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('users.login'))
    post_table = Posts()
    post = post_table.get_post(post_id)
    if post.username != session['user']["username"]:
        abort(403)
    post_table.delete_post(post_id)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
