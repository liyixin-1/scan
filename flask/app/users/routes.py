from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt)
from app import db
from app.users import users_bp
from app.users.models import User
from app.users.schema import UserSchema
from app.utils.responses import response_with
from app.utils import responses as resp

@users_bp.route('/newpasswd',methods=['POST'])
def newpasswd():
  try:
    data = request.get_json()
    user = data['username']
    fetched = User.find_by_username(username=user)
    newpad= User.generate_hash(data['password'])
    current_user = User.updatepasswd(fetched,user,newpad)
    #print(current_user.username)
    return resp.SUCCESS_201
  except Exception as e:
    print(e)
    return response_with(resp.INVALID_INPUT_422)


# 注册
@users_bp.route('/register',methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        data['password'] = User.generate_hash(data['password'])
        user_schema = UserSchema()
        users = user_schema.load(data)
        result = user_schema.dump(users.create())
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return response_with(resp.SUCCESS_201)
        #return response_with(resp.SUCCESS_201,value={"user":result,"access_token":access_token,"refresh_token":refresh_token})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@users_bp.route('/<int:id>',methods=['PUT'])
def update_users_detail(id):
    data = request.get_json()
    get_users = User.query.get_or_404(id)
    get_users.username = data['username']
    get_users.password = User.generate_hash(data['password'])
    get_users.phonenumber=data['phonenumber']
    get_users.email=data['email']
    get_users.role = data['role']
    db.session.add(get_users)
    db.session.commit()
    user_schema = UserSchema()
    users = user_schema.dump(get_users)
    return response_with(resp.SUCCESS_200,value={"users":users})


# 登录
@users_bp.route('/login',methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data['password'],current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return response_with(resp.SUCCESS_201,value={"access_token":access_token,"refresh_token":refresh_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_users(id):
    get_user = User.query.get_or_404(id)
    db.session.delete(get_user)
    db.session.commit()
    return response_with(resp.SUCCESS_201)

@users_bp.route('/list',methods=['GET'])
def get_ipscan_detail():
    fetched = User.query.all()
    result_schema = UserSchema(many=True,only=['id','username','password','phonenumber','email','role'])
    results = result_schema.dump(fetched)
    #fprint(results)
    return response_with(resp.SUCCESS_200,value={"results":results})

@users_bp.route('/result',methods=['GET'])
@jwt_required()
def get_userinfo():
    current_user=get_jwt_identity()
    fetched = User.find_by_username(username=current_user)
    return response_with(resp.SUCCESS_200,
            value={"data":{"username":fetched.username,"roles":fetched.role}})
