@app.route('/orders', methods=['GET', 'POST'])
@login_required
def manage_orders():
    if request.method == 'POST':    
        pass
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=orders)
