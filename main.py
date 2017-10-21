from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:anewblog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


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

    the_post = post.id

    return redirect("/blog?id=" + str(the_post))



@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('posts.html', error=encoded_error and cgi.escape(encoded_error, quote=True))



app.secret_key = 'A&Zr^8I/3ye R~XtH!j*N]L!X/,?zU'

if __name__ == "__main__":
    app.run()