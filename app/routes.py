from app import app, models, db, forms, images
import flask, flask_login

@app.route('/')
def homepage():
    """
    Display homepage
    """
    all_posts = models.Post.query.order_by(models.Post.post_time.desc()).all()

    rendered = flask.render_template('homepage.jin', posts=all_posts)

    return rendered


@app.route('/azure')
def azure():
    """
    History of bike constructions
    """
    # Retrieving every posts with topic 'History'
    azure_posts = models.Post.query.filter_by(topic='microsoft azure').order_by(models.Post.post_time.desc()).all()
    return flask.render_template('azure.jin', posts=azure_posts)


@app.route('/aws')
def aws():
    aws_posts = models.Post.query.filter_by(topic='aws').order_by(models.Post.post_time.desc()).all()
    return flask.render_template('aws.jin', posts=aws_posts)


@app.route('/new-post', methods=('GET', 'POST'))
def newpost():

    # New post form
    post_form = forms.NewPost()

    if flask.request.method == 'POST':
        if post_form.validate_on_submit():

            #Post creation
            post = post_form.create_post_object()

            # Check if topic is history to redirect to the good page
            if post_form.topic.data.lower() == 'microsoft azure':  # Check case insensitive
                return flask.redirect(flask.url_for('azure'))

            elif post_form.topic.data.lower() == 'aws':
                return flask.redirect(flask.url_for('aws'))

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


@app.route('/<topic>/<int:post_id>', methods=('GET', 'POST'))
def post(topic, post_id):
    """
    :param post_id:
    :return: Specific post you clicked in the feed + comments to it
    """

    # Retreive the post user clicked at by receiving its id. post_id retrieves from 'history' page
    current_post = models.Post.query.filter_by(post_id=post_id).first()

    #Retreive all comments related to the current_post
    comments = current_post.comments

    comment_form = forms.NewComment()

    if flask.request.method == "POST":
        if comment_form.validate_on_submit():

            new_comment = comment_form.get_comment(post_id)
            current_post.add_comment(new_comment)
            flask_login.current_user.add_comment(new_comment)

        return flask.redirect(flask.url_for('post', topic=topic, post_id=post_id))

    return flask.render_template('post.jin', topic=topic, post=current_post, comments=comments, form=comment_form)


@app.route('/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):

    #Retrieve the post I want to edit
    post_el = models.Post.query.filter_by(post_id=post_id).first()

    #Form for updating the post
    edit_post_form = forms.UpdatePost()

    if flask.request.method == "POST":
        if edit_post_form.validate_on_submit():

            # ##### The commented code works but it seems to be not professional to do so ####
            # topic_n = edit_post_form.topic.data
            # heading_n = edit_post_form.heading.data
            # post_preview_n = edit_post_form.post_preview.data
            # post_text_n = edit_post_form.post_text.data
            # post_image_n = images.save(edit_post_form.image.data)
            #
            # post_el.update_post(topic_n, heading_n, post_preview_n, post_text_n, post_image_n)

            # return flask.redirect(flask.url_for('post', topic=post_el.topic, post_id=post_el.post_id))

            # Here I want to retrieve the updated post using the functions in forms.py and models.py
            updated_post = edit_post_form.sending_updated_data()

            return flask.redirect(flask.url_for('post', topic=updated_post.topic, post_id=updated_post.post_id))

    edit_post_form.retrieve(post_el.topic, post_el.heading, post_el.post_preview, post_el.post_text, post_el.post_image)

    return flask.render_template('editpost.jin', form=edit_post_form)


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
                return flask.redirect(flask.url_for('homepage'))
            else:
                return flask.redirect((flask.url_for('signin', form=signin_form)))

    return flask.render_template('signin.jin', form=signin_form)


@app.route('/sign-out')
def signout():
    """
    User Sign out
    """

    models.User.signout()

    return flask.redirect(flask.url_for('homepage'))
