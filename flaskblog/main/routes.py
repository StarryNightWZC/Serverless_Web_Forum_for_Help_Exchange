import requests
from flask import render_template, request, Blueprint, redirect, url_for, session
from flaskblog.models import Post,Posts,Users
from flaskblog.posts.forms import SearchForm
from flask import (render_template, url_for, flash, current_app,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
#from flaskblog import db
from flask_googlemaps import GoogleMaps, Map
from flask_googlemaps import get_address, get_coordinates

from geopy.distance import great_circle
import boto3
import os,io
from botocore.exceptions import ClientError
import requests

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home')

def extra_same_elem(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    iset = set1.intersection(set2)
    return list(iset)


def imgisexist(imgname,folder):
    if os.path.isfile(folder+'/'+imgname):
        return False
    else:
        return True




@main.route("/offerhelp",methods=['GET', 'POST'])
def offerhelp():
    form=SearchForm()
    post_table=Posts()
    users=Users()
    s3 = boto3.client('s3')
    target_image_path='/tmp'

    allusers = users.get_all_users()
    for user in allusers:
        url=user['image_file']
        r = requests.get(url)
        if r.status_code == 403:
            url = s3.generate_presigned_url('get_object',
                                            Params={
                                                'Bucket': 'ece1779-final',
                                                'Key': '/tmp/' + session['user']['email'] + '/user_images/{}'.format(
                                                    user['image_name'])
                                            },
                                            ExpiresIn=604800)
            users.update_imagefile2(user['username'],url)
    for user in allusers:
        if (imgisexist(user['image_file'],target_image_path)):
            #print('ece1779-final', user['email'] + '/user_images/{}'.format(user['image_file']))
            #print(target_image_path + '/' + user['image_file'])
            print(user['image_file'])
            # s3.download_file('ece1779-final','/tmp/'+user['email'] + '/user_images/{}'.format(user['image_file']),
            #              target_image_path + '/' + user['image_file'])

    if form.validate_on_submit():
        #locations=post_table.query_post_by_address(form.location.data)
        types = post_table.get_all_posts()
        if form.type.data!="All":
            #print(form.type.data)
            types=post_table.query_post_by_type(form.type.data)
        sdates=post_table.query_post_by_sdate(form.sdate.data)
        fdates=post_table.query_post_by_fdate(form.fdate.data)
        search_results=extra_same_elem(types,sdates)
        search_results=extra_same_elem(search_results, fdates)
        #print(search_results)

        #####################################################################
        locations = []  # long list of coordinates
        place = get_coordinates(current_app.config['GOOGLEMAPS_KEY'], form.location.data)
        place['infobox'] = "<b>Hello World</b>"
        locations.append(place)
        for item in search_results:
            #print(item)
            temp={}
            temp['lat']=item.lat
            temp['lng']=item.lng
            temp['infobox'] = "<b>Hello World from other place</b>"
            locations.append(temp)
        print(locations)
        temp_results=[]
        i=1
        user_current_location = [locations[0]['lat'], locations[0]['lng']]
        session['user']['user_current_location']=user_current_location
        #print(session['user']['user_current_location'])
        for item in search_results:
            post_location = [locations[i]['lat'], locations[i]['lng']]
            i+=1
            item.distance=great_circle(user_current_location, post_location).km
            print("Distance:{}km".format(item.distance))
            if form.distance.data>=item.distance:
                temp_results.append([item.distance,item.post_id])
            #print(second_search_results)
        temp_results.sort()
        #print(temp_results)
        search_results.clear()
        for item in temp_results:
            post=post_table.get_post(item[1])
            search_results.append(post)
            if len(search_results)>4:
                break
        #####################################################################
        print(search_results)
        user_table = Users()

        return render_template('offerhelp.html', posts=search_results, user_table=user_table, form=form, legend='Filter Request')
    else:
        post_table = Posts()
        # list of Post objects
        posts = post_table.get_all_posts()
        user_table = Users()
        return render_template('offerhelp.html', posts=posts, user_table=user_table, form=form, legend='Filter Request')


@main.route("/about")
def about():
    return render_template('about.html', title='About')
