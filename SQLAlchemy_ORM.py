@app.route('/create_user')
def create_user():
    new_user = User(username='john_doe', email='john@example.com')
    db.session.add(new_user)
    db.session.commit()
    return "User created!"

@app.route('/create_order/<user_id>')
def create_order(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found!"
    new_order = Order(product_name='Laptop', price=1000.0, user=user)
    db.session.add(new_order)
    db.session.commit()
    return "Order created!"
