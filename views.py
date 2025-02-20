from flask import render_template_string,render_template,request,jsonify
from flask_security import auth_required, current_user, roles_required, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from extensions import db

def create_views(app,user_datastore:SQLAlchemyUserDatastore):

    # home
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if not email or not password or role not in ['inst','stud']:
            return jsonify({"message" : "invalid input"})
        
        if user_datastore.find_user(email=email):
            return jsonify({"message":"User already exists"})
        
        active = False if role=='inst' else True
        try:
            user_datastore.create_user(email=email,password=hash_password(password),roles = [role],active=active)
            db.session.commit()
        except:
            print('error while creating')
            db.session.rollback()
            return jsonify({"message":"error while creating user"}), 408
        
        return jsonify({"message" : "user created"}), 200
    # profile
    @app.route('/profile')
    @auth_required('token', 'session')
    def profile():
        return render_template_string(
            """
                <h1> this is homepage </h1>
                <p> Welcome, {{current_user.email}}</p>
                <p> Role :  {{current_user.roles[0].description}}</p>
                <p><a href="/logout">Logout</a></p>
            """
        )
    
    @app.route('/inst-dashboard')
    @roles_required('inst')
    def inst_dashboard():
        return render_template_string(
            """
                <h1>this is intructor dashboard</h1>
                <p>This should only be accessable to inst</p>
            """
        )
    
    @app.route('/stud-dashboard')
    @roles_required('stud')
    def stud_dashboard():
        return render_template_string(
            """
                <h1>this is student dashboard</h1>
                <p>This should only be accessable to student</p>
            """
        )