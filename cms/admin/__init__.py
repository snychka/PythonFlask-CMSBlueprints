from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
# from flask import request, redirect, url_for, flash
# from flask import redirect, url_for, flash
from cms.admin.models import Type, Content, Setting, User, db

# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint
# https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints
# admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

# https://flask.palletsprojects.com/en/1.1.x/blueprints/#my-first-blueprint
def requested_type(type):
    types = [row.name for row in Type.query.all()]
    return True if type in types else False

@admin_bp.route('/', defaults = {'type': 'page'})
@admin_bp.route('/<type>')
def content(type):
    if requested_type(type):
        content = Content.query.join(Type).filter(Type.name == type)
        return render_template('admin/content.html', type=type, content=content)
    else:
        abort(404)

# https://stackoverflow.com/questions/22947905/flask-example-with-post
@admin_bp.route('/admin/create/<type>', methods=['POST', 'GET'])
def create(type):
    if requested_type(type):
        # https://stackoverflow.com/questions/42018603/handling-get-and-post-in-same-flask-view
        if request.method == 'POST':
            # https://stackoverflow.com/questions/42154602/how-to-get-form-data-in-flask
            # get doesn't pass
            # title = request.form.get('title')
            title = request.form['title']
            slug = request.form['slug']
            type_id = request.form['type_id']
            body = request.form['body']
            error = None
            # if title == '' :
            # if title is None:
            if not title: 
                error = 'title is empty'
            # elif type == '':
            # elif type is None:
            # WRONG?? should be type??
            elif not type_id:
                error = 'type is empty'
            if error is None:
                content = Content(title=title, slug=slug, type_id=type_id, body=body)
                db.session.add(content)
                db.session.commit()
                # https://flask.palletsprojects.com/en/1.1.x/api/#flask.url_for
                # remember type as an arg.  sigh
                return redirect(url_for('admin.content', type=type))
            flash(error)
        types = Type.query.all()
        return render_template('admin/content_form.html', title='Create', types=types, type_name=type)
    else:
        abort(404)

@admin_bp.route('/admin/users')
def users():
    users = User.query.all()
    return render_template('admin/users.html', title='Users', users=users)

@admin_bp.route('/admin/settings')
def settings():
    settings = Setting.query.all()
    return render_template('admin/settings.html', title='Settings', settings=settings)

@admin_bp.route('/admin/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    content = Content.query.get_or_404(id)
    # should be type?  instead of type_id tests/test_module2.py:410
    # type = Type.query.get(content.type)
    type = Type.query.get(content.type_id)
    types = Type.query.all()
    if request.method == 'POST':
        content.id = request.form['id']
        content.title = request.form['title']
        content.slug = request.form['slug']
        content.type_id = request.form['type_id']
        content.type = request.form['type']
        content.body = request.form['body']
        # content.created_at = request.form['created_at']
        content.updated_at = datetime.utcnow()
        error = None
        if not request.form['title']:
            error = 'title is empty'
        if error is None:
            db.session.commit()
            return redirect(url_for('admin.content', content=content, type=type.name))
        flash(error)
    return render_template('admin/content_form.html', types = types, title = 'Edit'  , item_title = content.title , slug = content.slug , type_name = type.name  , type_id = content.type_id  , body = content.body )
