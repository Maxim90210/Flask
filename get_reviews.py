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
        return redirect(url_for('review_trainer'))
    reviews = Review.query.filter_by(trainer_id=current_user.id).all()
    return render_template('review.html', reviews=reviews)
