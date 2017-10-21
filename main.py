from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:anewblog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(120), unique=True)
#    password = db.Column(db.String(120))
    
  #  def __init__(self, email, password):
   #     self.email = email
    #    self.password = password

 #   def __repr__(self):
  #      return '<User %r>' % self.email

class Postings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_content = db.Column(db.String(255))

    def __init__(self, post_title, post_content):
        self.post_title = post_title
        self.post_content = post_content

    def __rpr__(self):
        return "<Post %r>" % self.post_title

def get_post_list():
    return Postings.query.all()


   

# @app.route("/register", methods=["POST","GET"])
#def register():
 #   if request.method == 'POST':
  #      email = request.form['email']
  #      password = request.form['password']
   #     verify = request.form['pass_verif']
    #    if not is_email(email):
     #       flash('Whoops. "' + email + '" does not seem like an email address')
  #          return redirect('/register')
   #     email_db_count = User.query.filter_by(email=email).count()
    #    if email_db_count > 0:
     #       flash('Oh noes. "' + email + '" is already taken and password reminders are not implemented')
      #      return redirect('/register')
  #      if password != verify:
   #         flash('passwords did not match')
    #        return redirect('/register')
     #   user = User(email=email, password=password)
      #  db.session.add(user)
 #       db.session.commit()
  #      session['user'] = user.email
   #     return redirect("/")
    #else:
     #   return render_template("new-user.html")

#@app.route("/login", methods=['POST', 'GET'])
#def login():
 #   if request.method == 'POST':
  #      email = request.form['email']
   #     password = request.form['password']
    #    users = User.query.filter_by(email=email)
     #   if users.count() == 1:
      #      user = users.first()
       #     if password == user.password:
        #        session['user'] = user.email
         #       flash('Hello again!, ' + user.email)
          #      return redirect("/")
  #      flash('Bad username or password, please try again')
   #     return redirect("/login")
    #elif request.method == 'GET':
     #   return render_template('user-login.html')


@app.route("/blog", methods=['GET'])
def posts_list():
    if request.args.get("id") == None:
        posts = get_post_list()
        return render_template("posts.html", posts=posts)        
    else:
        variable = int(request.args.get("id"))
        single_post = Postings.query.filter_by(id=variable).first()
        return render_template("post.html", post=single_post)
        


@app.route("/newpost", methods=["GET"])
def load_new_post():
    return render_template("new-post.html")

@app.route("/newpost", methods=["POST"])
def new_post():
    new_title = request.form["title"]
    new_content = request.form["content"]

    if (not new_title) or (new_title.strip() == "") or (not new_content) or (new_content.strip() == ""): 
        flash("Please inlcude both a title and the post content")
        return render_template("new-post.html")


    post = Postings(new_title,new_content)
    db.session.add(post)
    db.session.commit()

    return redirect("/blog")

#def is_email(string):
 #   atsign_index = string.find('@')
 #   atsign_present = atsign_index >= 0
 #   if not atsign_present:
  #      return False
  #  else:
   #     domain_dot_index = string.find('.', atsign_index)
   #     domain_dot_present = domain_dot_index >= 0
   #     return domain_dot_present

#@app.route("/logout", methods=['POST'])
#def logout():
#    del session['user']
 #   return redirect("/")

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('posts.html', error=encoded_error and cgi.escape(encoded_error, quote=True))


#endpoints_without_login = ['login', 'register']


#@app.before_request
#def require_login():
 #   if not ('user' in session or request.endpoint in endpoints_without_login):
 #       return redirect("/register")

app.secret_key = 'A&Zr^8I/3ye R~XtH!j*N]L!X/,?zU'

if __name__ == "__main__":
    app.run()