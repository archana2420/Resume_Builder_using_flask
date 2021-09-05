from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask_session import Session
from form import Register_form,Login_form,Resume_details
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required

app=Flask(__name__)

app.config['SECRET_KEY']='c82cfac7bef4767e84e74f03dafb1a62'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)
    resume_information=db.relationship('Resume_info',backref='user',uselist=False)

    def __repr__(self):
        return f"User('{self.id}','{self.email}')"

class Resume_info(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    res_id = db.Column(db.Integer,db.ForeignKey(User.id),unique=True)
    name = db.Column(db.String(20),nullable=False)
    phone_no = db.Column(db.String(20),nullable=False)
    workEmail = db.Column(db.String(20), nullable=False)
    linkedIn = db.Column(db.String(20),nullable=False)
    education = db.Column(db.String(200),nullable=False)
    skills = db.Column(db.String(200),nullable=False)
    project_1 = db.Column(db.String(50),nullable=False)
    project_2 = db.Column(db.String(50),nullable=False)


    def __repr__(self):
        return f"User('{self.id}','{self.name}'.'{self.phone_no}')"




@app.route("/")
def home():
    session['curr_id']=None
    return render_template('index.html')

@app.route("/signup",methods=['get','post'])
def signup():
    form = Register_form()

    if request.method == "POST":
        if form.validate_on_submit():
            new_user_name = request.form.get('email')
            new_user_passw = request.form.get('password')
            print(new_user_name,new_user_passw)
            if new_user_name and new_user_passw:
                new_user=User(email=new_user_name,password=new_user_passw)
                db.session.add(new_user)
                db.session.commit()
                user=User.query.filter_by(email=new_user_name).first()
                session['curr_id'] = user.id
                print(session['curr_id'])
            return redirect(url_for('resume_builder'))
    return render_template('sign_up.html',form=form)

@app.route("/login",methods=['get','post'])
def login():
    form = Login_form()
    if request.method == "POST":
        if form.validate_on_submit():
            existing_user = request.form.get('email')
            existing_passw = request.form.get('password')
            print(existing_user,existing_passw)
            user = User.query.filter_by(email=existing_user).first()
            verify = True if (user.password==existing_passw) else False
            if user and verify:
                login_user(user)
                resume = Resume_info.query.filter_by(res_id=user.id)
                session['curr_id']=user.id
                print(session['curr_id'])
                if resume:
                    return redirect(url_for('builder'))
                else:
                    return redirect(url_for('resume_builder'))
            flash('Your username or password is wrong','danger')

    return render_template('login.html', form=form)





@app.route("/resume_builder",methods=['get','post'])
def resume_builder():
    form=Resume_details()

    if request.method == "POST":
        if form.validate_on_submit():
            res_name = request.form.get('name')
            res_phone_no = request.form.get('phone_no')
            res_work_email = request.form.get('work_email')
            res_linkedIn = request.form.get('linkedIn')
            res_edu = request.form.get('education')
            res_skills = request.form.get('skills')
            res_project1 = request.form.get('project_1')
            res_project2 = request.form.get('project_2')
            resume1 = Resume_info(res_id=session['curr_id'],name=res_name,phone_no=res_phone_no,workEmail=res_work_email,linkedIn=res_linkedIn,education=res_edu,skills=res_skills,project_1=res_project1,project_2=res_project2)
            db.session.add(resume1)
            db.session.commit()
            return redirect(url_for('builder'))
    # print(session['curr_id'])
    # if session['curr_id'] != 0:
    #     existing_resume = Resume_info.query.filter_by(res_id=session['curr_id'])
    #     print(existing_resume)
    #     if existing_resume:
    #         return redirect(url_for('builder'))
    return render_template('resume_builder.html',form=form)

@app.route("/builder",methods=['get','post'])
def builder():
    user = Resume_info.query.filter_by(res_id=session['curr_id']).first()
    return render_template('builder2.html',user=user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)