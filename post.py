@app.route('/reviews/add', methods=['POST'])
@login_required
def add_review():
    trainer_id = request.form['trainer_id']
    rating = request.form['rating']
    comment = request.form.get('comment')
    new_review = Review(trainer_id=trainer_id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('get_reviews'))


@app.route('/reviews/edit', methods=['POST'])
@login_required
def edit_review():
    review_id = request.form['review_id']
    review = Review.query.get_or_404(review_id)
    if review:
        review.rating = request.form['rating']
        review.comment = request.form.get('comment')
        db.session.commit()
        return redirect(url_for('get_reviews'))
    return jsonify({'message': 'Review not found'}), 404


@app.route('/reviews/delete', methods=['POST'])
@login_required
def delete_review():
    review_id = request.form['review_id']
    review = Review.query.get_or_404(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return redirect(url_for('get_reviews'))
    return jsonify({'message': 'Review not found'}), 404
