@app.route('/orders/add', methods=['POST'])
@login_required
def add_order():
    phone_number = request.form['phone_number']
    cod_amount = request.form['cod_amount']
    new_order = Order(user_id=current_user.id, phone_number=phone_number, cod_amount=cod_amount)
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('get_orders'))
