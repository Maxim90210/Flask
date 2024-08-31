from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
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



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return render_template('register.html', message="Користувач з таким іменем або email вже існує.")


        new_user = User(username=username, email=email,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']


        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message="Неправильне ім'я користувача або пароль.")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/reviews', methods=['GET', 'POST'])
@login_required
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
@login_required
def get_reviews():
    reviews = Review.query.all()
    return jsonify(
        [{'trainer_id': review.trainer_id, 'rating': review.rating, 'comment': review.comment} for review in reviews])


@app.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])


@app.route('/api/register', methods=['POST'])
def api_register_user():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/orders', methods=['GET'])
@login_required
def get_orders():
    orders = Order.query.all()
    return jsonify(
        [{'id': order.id, 'user_id': order.user_id, 'phone_number': order.phone_number, 'cod_amount': order.cod_amount}
         for order in orders])


@app.route('/order/<int:id>', methods=['GET'])
@login_required
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(
        {'id': order.id, 'user_id': order.user_id, 'phone_number': order.phone_number, 'cod_amount': order.cod_amount})


if __name__ == '__main__':
    app.run(debug=True)
