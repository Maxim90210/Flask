from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    cod_amount = db.Column(db.Float, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/reviews', methods=['GET', 'POST'])
def review_trainer():
    if request.method == 'POST':
        trainer_id = request.form['trainer_id']
        rating = request.form['rating']
        comment = request.form.get('comment')
        new_review = Review(trainer_id=trainer_id, rating=rating, comment=comment)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('review.html')

@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{'trainer_id': review.trainer_id, 'rating': review.rating, 'comment': review.comment} for review in reviews])

if __name__ == '__main__':
    app.run(debug=True)
