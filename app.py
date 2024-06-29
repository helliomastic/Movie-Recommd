from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy 
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    release_date = db.Column(db.String(10))
    rating = db.Column(db.Float)

    def __init__(self, title, description, image, genre, director, release_date, rating):
        self.title = title
        self.description = description
        self.image = image
        self.genre = genre
        self.director = director
        self.release_date = release_date
        self.rating = rating

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']
        genre = request.form['genre']
        director = request.form['director']
        release_date = request.form['release_date']
        rating = float(request.form['rating'])

        image.save(f'static/images/{image.filename}')

        new_movie = Movie(title=title, description=description, image=image.filename,
                          genre=genre, director=director, release_date=release_date, rating=rating)
        db.session.add(new_movie)
        db.session.commit()

        flash('Movie added successfully!', 'success')
        return redirect(url_for('show_movie', movie_id=new_movie.id))

    return render_template('admin.html')

@app.route('/movie/<int:movie_id>')
def show_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie.html', movie=movie)

@app.route('/movie')
def all_movies():
    movies = Movie.query.all()
    return render_template('movie_list.html', movies=movies)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/details')
def details():
    return render_template('movie-details.html')

@app.route('/recommd')
def recommd():
    return render_template('recom.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()
        return render_template('dashboard.html', user=user)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            flash('Please login', 'success')
            return redirect('/')
        else:
            error = 'Invalid email or password'
            flash(error, 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error = 'Email address already exists'
            flash(error, 'error')
            return render_template('register.html')
        
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect('/login')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
