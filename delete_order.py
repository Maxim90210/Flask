@app.route('/orders/delete', methods=['POST'])
@login_required
def delete_order():
    order_id = request.form['order_id']
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('get_orders'))
