@app.route('/orders/edit', methods=['POST'])
@login_required
def edit_order():
    order_id = request.form['order_id']
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    order.phone_number = request.form['phone_number']
    order.cod_amount = request.form['cod_amount']
    db.session.commit()
    return redirect(url_for('get_orders'))
