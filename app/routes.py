from app import app, models, db, forms
import flask

@app.route('/')
def homepage():
    """
    Display homepage
    """
    rendered = flask.render_template('homepage.jin')

    return rendered


@app.route('/history')
def history():
    """
    History of bike constructions
    """
    # Retrieving every posts with topic 'History'
    history_posts = models.Post.query.filter_by(topic='history').all()
    return flask.render_template('history.jin', posts=history_posts)


@app.route('/building')
def building():
    building_posts = models.Post.query.filter_by(topic='Building').all()
    return flask.render_template('building.jin', posts=building_posts)


@app.route('/new-post', methods=('GET', 'POST'))
def newpost():

    # Create new post form
    post_form = forms.NewPost()

    if flask.request.method == 'POST':
        if post_form.validate_on_submit():

            #Post creation
            post = post_form.create_post_object()

            # Check if topic is history to redirect to the good page
            if post_form.topic.data.lower() == 'history':  # Check case insensitive
                return flask.redirect(flask.url_for('history'))

            elif post_form.topic.data.lower() == 'building':
                return flask.redirect(flask.url_for('building'))

            # Maybe return flask.redirect(flask.url_for(post.topic.lower()))) --> If name of the endpoint is always
            # the name of the topic

            #TODO: when there will be many tabs/topics, dictionary with endpoints approach should be used
            # If the endpoint is not always the same: Use a dictionary to map between topic and endpoint
            # endpoints = {
            #     'building': 'building-function',
            #     'history': 'history-function'
            #  }
            # return flask.redirect(flask.url_for(endpoints[post.topic.lower()]))

        else:
            return flask.render_template('newpost.jin', form=post_form)

    return flask.render_template('newpost.jin', form=post_form)


@app.route('/history/<int:post_id>')
def post(post_id):
    current_post = models.Post.query.filter_by(post_id=post_id).first()

    return flask.render_template('post.jin', post=current_post)


@app.route('/sign-up', methods=('GET', 'POST'))
def signup():
    """
    Sign up form for users
    """

    #Creates Sign Up form
    sign_up = forms.SignUp()

    if flask.request.method == 'POST':
        if sign_up.validate_on_submit():

            #Creates new user
            new_user = sign_up.create_user()

            return flask.redirect(flask.url_for('homepage'))

    return flask.render_template('signup.jin', form=sign_up)

@app.route('/sign-in', methods=('GET', 'POST'))
def signin():
    """
    Sign in form for those who was already signed up before
    """
    signin_form = forms.SignIn()

    if flask.request.method == 'POST':
        if signin_form.validate_on_submit():

            success = signin_form.signin_user()

            if success:
                flask.redirect(flask.url_for('homepage'))
            else:
                return flask.redirect((flask.url_for('signin', form=signin_form)))

    return flask.render_template('signin.jin', form=signin_form)
