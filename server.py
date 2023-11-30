from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    filename = db.Column(db.String(255))

def create_upload_folder():
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

@app.route('/')
def index():
    with app.app_context():
        photos = Photo.query.all()
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['POST'])
def upload():
    create_upload_folder()  # Ensure the upload folder exists

    if 'photo' in request.files:
        photo = request.files['photo']
        description = request.form['description']

        if photo and allowed_file(photo.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(filename)

            with app.app_context():
                new_photo = Photo(description=description, filename=photo.filename)
                db.session.add(new_photo)
                db.session.commit()

    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
