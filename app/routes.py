from app import app, models, db, forms
import flask


@app.route('/')
def homepage():
    rendered = flask.render_template('homepage.jin')

    return rendered


@app.route('/history')
def history():
    history_posts = models.Post.query.filter_by(topic='History').all()

    return flask.render_template('history.jin', posts=history_posts)


@app.route('/building')
def building():
    building_posts = models.Post.query.filter_by(topic='Building').all()

    return flask.render_template('building.jin', posts=building_posts)


@app.route('/new-post', methods=('GET', 'POST'))
def newpost():
    post = forms.NewPost()

    if flask.request.method == 'POST':
        if post.validate_on_submit():
            new_post = models.Post(topic=post.topic.data, heading=post.heading.data, post_text=post.post_text.data)
            db.session.add(new_post)
            db.session.commit()
            if post.topic.data == 'history' or post.topic.data == 'History':
                return flask.redirect(flask.url_for('history'))
            elif post.topic.data == 'building' or post.topic.data == 'Building':
                return flask.redirect(flask.url_for('building'))
        else:
            return flask.render_template('newpost.jin', form=post)

    return flask.render_template('newpost.jin', form=post)


@app.route('/history/<int:post_id>')
def post(post_id):
    current_post = models.Post.query.filter_by(post_id=post_id).first()

    return flask.render_template('post.jin', post=current_post)
