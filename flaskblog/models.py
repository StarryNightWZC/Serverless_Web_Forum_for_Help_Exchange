from datetime import datetime

from flask_login._compat import text_type
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
#from flaskblog import db, login_manager

import boto3

import time
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime


dynamodb = boto3.resource('dynamodb')

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class Users:
    table = dynamodb.Table('users')
    def get_user(self, username):
        response = self.table.get_item(
            Key={
                'username': username
            }
        )
        user = None
        if 'Item' in response:
            user = response['Item']
        return user
    def query_email(self,email):
        response = self.table.scan(
            FilterExpression=Attr('email').eq(email)
        )
        items = response['Items']
        print(items)
        return items

    def get_all_users(self):
        response = self.table.scan(
            TableName="users"
        )
        items = response['Items']
        return items

    def put_user(self,username, email, password,address):
        user = {
            'username': username,
            'password': password,
            'email': email,
            'image_file':'https://covid19blog.s3.amazonaws.com/default/default.jpg',
            'address':address,
            'image_name':'default.jpg'
        }
        self.table.put_item(
            Item=user
        )
    def update_imagefile(self,username,imagefile,picture_file):
        self.table.update_item(
            Key={
                'username': username,
            },
            UpdateExpression='SET image_file = :val1,'
                             'image_name=:val2',
            ExpressionAttributeValues={
                ':val1': imagefile,
                ':val2': picture_file
            }
        )
    def update_imagefile2(self,username,imagefile):
        self.table.update_item(
            Key={
                'username': username,
            },
            UpdateExpression='SET image_file = :val1',
            ExpressionAttributeValues={
                ':val1': imagefile,
            }
        )
    def get_user_imagefile(self,username):
        response = self.table.get_item(
            Key={
                'username': username
            }
        )
        user = None
        if 'Item' in response:
            user = response['Item']
        return user['image_file']

    def get_user_address(self,username):
        response = self.table.get_item(
            Key={
                'username': username
            }
        )
        user = None
        if 'Item' in response:
            user = response['Item']
        return user['address']

class User:
    'user object'
    def __init__(self,email,username,image_file):
        self.email=email,
        self.image_file=image_file,
        self.username=username

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'username': self.username}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            username = s.loads(token)['usernmae']
        except:
            return None
        return User.query.get(user_id)

class Posts:
    table = dynamodb.Table('posts')
#post id: timestamp
    #返回post object
    def get_post(self, post_id):
        response = self.table.get_item(
            Key={
                'post_id': post_id
            }
        )
        post = None
        if 'Item' in response:
            item = response['Item']
            post=Post(post_id=item['post_id'],title=item['title'],type=item['type'],phone=item['phone'],
                       email=item['email'],address=item['address'],content=item['content'],username=item['username'],timestamp=item['timestamp'],
                      sdate=item['sdate'],fdate=item['fdate'],lat=float(item['lat']),lng=float(item['lng']))
        return post

    def query_post_email(self, username):
        response = self.table.scan(
            FilterExpression=Attr('username').eq(username)
        )
        items = response['Items']
        print(items)
        return items

    def get_all_posts(self):
        response = self.table.scan(
            TableName="posts"
        )
        items = response['Items']
        posts_list=[]
        for item in items:
            print(item['post_id'])
            post=Post(item['post_id'],item['title'],item['type'],item['phone'],
                       item['email'],item['email'],item['content'],item['username'],item['timestamp'],
                      item['sdate'],item['fdate'],float(item['lat']),float(item['lng']))
            posts_list.append(post)
           # print(post)
        #print(posts_list)
        #重写排序
        posts_list.sort(reverse=True)
        #print(posts_list)
        return posts_list

    def put_post(self, title, type, phone, email,address,content,username,sdate,fdate,lat,lng):
        timestamp = str(datetime.timestamp(datetime.now()))
        inttimestamp=int(float(timestamp))
        time=str(datetime.now())
        print(timestamp)
        post = {
            'post_id': str(inttimestamp),
            'title':title,
            'type':type,
            'phone':phone,
            'email':email,
            'address':address,
            'content':content,
            'username':username,
            'timestamp':time[0:-7],
            'sdate':sdate,
            'fdate':fdate,
            'lat':str(lat),
            'lng':str(lng),
            'isactive':True
        }
        print(post)
        self.table.put_item(
            Item=post
        )

    def update_post(self,post_obj):#传入post obj
        #print(post_obj.type)
        self.table.update_item(
            Key={
                'post_id': post_obj.post_id,
            },
            UpdateExpression='SET #title = :val1,'
                             '#type = :val2,'
                             '#email = :val3,'
                             '#address = :val4,'
                             '#content = :val5,'
                             '#phone = :val6,'
                             '#sd = :val7,'
                             '#fd = :val8',
            ExpressionAttributeValues={
                ':val1': post_obj.title,
                ':val2': post_obj.type,
                ':val3': post_obj.email,
                ':val4': post_obj.address,
                ':val5': post_obj.content,
                ':val6': post_obj.phone,
                ':val7': post_obj.sdate,
                ':val8': post_obj.fdate,
            },
            ExpressionAttributeNames={
                "#title":"title",
                "#type" :"type",
                "#email" :"email",
                "#address":"address",
                "#content":"content",
                "#phone": "phone",
                "#sd":"sdate",
                "#fd":"fdate"
            }
        )
    def delete_post(self,post_id):
        self.table.update_item(
            Key={
                'post_id': post_id,
            },
            UpdateExpression='SET #isactive = :val1',
            ExpressionAttributeValues={
                ':val1': False,
            },
            ExpressionAttributeNames={
                "#isactive": "isactive",
            }

        )

    def query_post_by_username(self,username):
        response = self.table.scan(
            FilterExpression=Attr('username').eq(username)
        )
        items = response['Items']
        posts_list = []
        for item in items:
            print(item['post_id'])
            post=Post(item['post_id'],item['title'],item['type'],item['phone'],
                       item['email'],item['address'],item['content'],item['username'],item['timestamp'],item['sdate'],item['fdate'],
                      float(item['lat']),float(item['lng']))
            posts_list.append(post)
        print(posts_list)
        #重写排序
        posts_list.sort(reverse=True)
        print(posts_list)
        return posts_list

    def query_post_by_address(self,location):
        response = self.table.scan(
            FilterExpression=Attr('address').eq(location)
        )
        items = response['Items']
        posts_list = []
        for item in items:
            print(item['post_id'])
            post=Post(item['post_id'],item['title'],item['type'],item['phone'],
                       item['email'],item['address'],item['content'],item['username'],item['timestamp'],item['sdate'],item['fdate'],
                      float(item['lat']),float(item['lng']))
            posts_list.append(post)
        return posts_list
    def query_post_by_type(self,type):
        response = self.table.scan(
            FilterExpression=Attr('type').eq(type)
        )
        items = response['Items']
        posts_list = []
        for item in items:
            print(item['post_id'])
            post=Post(item['post_id'],item['title'],item['type'],item['phone'],
                       item['email'],item['address'],item['content'],item['username'],item['timestamp'],item['sdate'],item['fdate'],
                      float(item['lat']),float(item['lng']))
            posts_list.append(post)
        return posts_list
    def query_post_by_sdate(self,sdate):
        response = self.table.scan(
            FilterExpression=Attr('sdate').gte(str(sdate))
        )
        items = response['Items']
        posts_list = []
        for item in items:
            print(item['post_id'])
            post=Post(item['post_id'],item['title'],item['type'],item['phone'],
                       item['email'],item['address'],item['content'],item['username'],item['timestamp'],item['sdate'],item['fdate'],
                      float(item['lat']),float(item['lng']))
            posts_list.append(post)
        #print("*********************")
        #print(posts_list)
        return posts_list

    def query_post_by_fdate(self,fdate):
        response = self.table.scan(
            FilterExpression=Attr('fdate').lte(str(fdate))
        )
        items = response['Items']
        posts_list = []
        for item in items:
            print(item['post_id'])
            post=Post(item['post_id'],item['title'],item['type'],item['phone'],
                       item['email'],item['address'],item['content'],item['username'],item['timestamp'],item['sdate'],item['fdate'],
                      float(item['lat']),float(item['lng']))
            posts_list.append(post)
        return posts_list



class Post:
    'post object'

    def __repr__(self) -> str:
        return f"Post('id:{self.post_id},\n" \
               f"title:{self.title},\n" \
               f"type:{self.type},\n" \
               f"phone:{self.phone},\n" \
               f"email:{self.email},\n" \
               f"address:{self.address},\n" \
               f"content:{self.content},\n" \
               f"distance:{self.distance},\n" \
               f"lat:{self.lat},\n" \
               f"lng:{self.lng},\n" \
               f"username:{self.username}')"

    def __init__(self,post_id,title,type,phone,email,address,content,username,timestamp,sdate,fdate,lat,lng):
        self.post_id=post_id
        self.title=title
        self.type=type
        self.phone=phone
        self.email=email
        self.address=address
        self.content=content
        self.username=username
        self.timestamp=timestamp
        self.sdate=sdate
        self.fdate=fdate
        self.distance=None
        self.lat=lat
        self.lng=lng

    def __lt__(self, other):
        return self.post_id < other.post_id

    def __eq__(self, other):
        return self.post_id == other.post_id

    def __hash__(self):
        return hash(self.post_id)

