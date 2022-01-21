from flask import Flask, jsonify, request, make_response, abort
from flask_sqlalchemy import SQLAlchemy
# from flask_user import roles_required # for role based access to create and update user
#

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"


def ClassFactory(name):
    tabledict={'id':db.Column(db.Integer, primary_key = True),
               'username':db.Column(db.String(25), unique= True, nullable=False),
               'email':db.Column(db.String(60), nullable=False),
               }
    newclass = type(name, (db.Model,), tabledict)
    return newclass


@app.route("/create", methods=['POST'])
# @roles_required('Admin')
def create():
    """
    Create user with username and email address
    for simplicity limiting to username and email
    :return:
    """
    if not request.json or 'username' not in request.json or 'email' not in request.json:
        abort(400)
    user = User(username=request.json.get('username'), email=request.json.get('email'))
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify({'username': ''}), 400

    return jsonify({'username': request.json.get('username')}), 201


@app.route('/update', methods=['PUT'])
# @roles_required('Admin')
def update_user():
    # update user email
    if not request.json:
        abort(400)
    user = User.query.filter(User.username==request.json.get('username')).first()
    if not user:
        abort(404)
    user.email = request.json.get('email')
    db.session.commit()
    return jsonify(str(user)), 200


@app.route('/login', methods=['POST'])
def login_post():
    if not request.json or 'username' not in request.json or 'email' not in request.json:
        abort(400)
    # login code goes here
    username = request.form.get('username')
    email = request.form.get('email')

    user = User.query.filter(username=username).first()

    # check if the user actually exists
    if not user:
        return jsonify(str(user)), 404

    return jsonify(str(user)), 200


@app.route('/login', methods=['GET'])
def login_out():
    pass


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': [str(i) for i in User.query.all()]})


@app.route("/creategroup", methods=['POST'])
def creategroup():
    """
    create chat group, input - groupname
    create user table per group
    initialize it.
    """
    if not request.json or 'groupname' not in request.json:
        abort(400)

    # create new table with groupname and initialize it
    # if already existing return
    ClassFactory(request.json.get('groupname'))
    db.create_all()
    db.session.commit()

    return jsonify({'groupname': request.json.get('groupname')}), 201


@app.route("/joingroup", methods=['POST'])
def joingroup():
    """
    pass username and groupname to add to group
    :return:
    """
    if not request.json or 'groupname' not in request.json or 'username' not in request.json:
        abort(400)

    # add user to the group table
    pass


@app.route("/exitgroup", methods=['GET'])
def exitgroup():
    """
    pass username and groupname to remove from group
    :return:
    """
    if not request.json or 'groupname' not in request.json or 'username' not in request.json:
        abort(400)

    # remove user to the groupname
    pass


@app.route("/searchgroup", methods=['GET'])
def searchgroup():
    # search if the user exists in the given group
    pass


@app.route("/sendmessage", methods=['POST'])
def sendmessage():
    # search if the user exists in the given group
    pass


if __name__ == '__main__':
    app.run(debug=True)
