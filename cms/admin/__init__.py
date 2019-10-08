from flask import Blueprint, render_template, abort, request
from flask import request
from cms.admin.models import Type, Content, Setting, User

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

