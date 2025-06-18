from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
db = SQLAlchemy(app)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

with app.app_context():
    db.create_all()
 

    

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "id": new_user.id}), 201


@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/users/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    user = User.query.get(user_id)                
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})  
    return jsonify({"error": "User not found"}), 404


@app.route('/users/<int:user_id>', methods = ['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

@app.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    new_role = Role(name=data['name'])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({"message": "Role created", "id": new_role.id}), 201

@app.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{"id": role.id, "name": role.name} for role in roles])


@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = Role.query.get(role_id)
    if role:
        return jsonify({"id": role.id, "name": role.name})
    return jsonify({"error": "Role not found"}), 404

@app.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404
    data = request.json
    role.name = data.get('name', role.name)
    db.session.commit()
    return jsonify({"id": role.id, "name": role.name})

@app.route('/users/<int:user_id>/roles', methods=['POST'])
def assign_role_to_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    role = Role.query.get(data['role_id'])
    if not role:
        return jsonify({"error": "Role not found"}), 404
    
    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        return jsonify({"message": "Role assigned to user"})
    return jsonify({"message": "User already has this role"})

@app.route('/users/<int:user_id>/roles', methods=['GET'])
def get_user_roles(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user id": user.id, "username": user.name, "assign_role": [role.name for role in user.roles] })    
    

@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404
    db.session.delete(role)
    db.session.commit()
    return jsonify({"message": "Role deleted"})

if __name__ == '__main__':
    app.run(debug=True)
