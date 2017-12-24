#Blog app initialization and framework

# ----------------- App config


#importing flask modules
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initiating app
app = Flask(__name__)
#Look for app configuration file and config based on it
app.config.from_pyfile('config.cfg')


# ----------------- Database


#init Database
db = SQLAlchemy(app)

#Database Table schema
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)



# ----------------- Routes

# home page routes
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template('index.html',posts=posts)

# about the author page
@app.route('/about')
def about():
    return render_template('about.html')

# Single Post page
@app.route('/post/<int:post_id>') # here the post_id is dinamic
def post(post_id):
    # given the post id look for it in the database and save it to the variable
    post = Post.query.filter_by(id=post_id).one()
    # Formating datetime to present it properly
    date_posted = post.date_posted.strftime('%B %d, %Y')
    # Rendering the template and sending the variables values
    return render_template('post.html', post=post,date_posted=date_posted)

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Adding a post page, this needs enhacement (adding a Medium-like editor)
@app.route('/add')
def add():
    return render_template('add.html')

# Adding a post to the database
@app.route('/addpost', methods=['POST']) # Remember t set the methods to Post!
def addpost():
    # these are the variables that define a Post given our Post Table
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    # Given what we retrieved from the form, add it to an object mapped by the Post class
    post = Post(title=title, author=author, content=content, date_posted=datetime.now())
    # Add this object to stage area
    db.session.add(post)
    # Commit it to the database! (how awesome is that?!)
    db.session.commit()
    # Send the User to home Page to check the new Post
    return redirect(url_for('index'))


# Run the app with debugger on
if __name__=='__main__':
    app.run(debug=True)
