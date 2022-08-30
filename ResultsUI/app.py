import os
import os.path as op
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

import flask_admin as admin
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla


# create application
app = Flask(__name__)

# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'paper'

# secrey key so sessions could be used
app.config['SECRET_KEY'] = '1234567890'

# database configuration
app.config['DATABASE_FILE'] = 'email_scraper.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# database models
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_domain = db.Column(db.Text)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.Text, unique=True)


@app.route('/add/', methods=['POST'])
def add():
    email = request.form['email']
    domain = request.form['domain']
    item = Email(first_domain=domain, email=email)
    db.session.add(item)
    db.session.commit()
    return ''


# customized model admin
class PostAdmin(sqla.ModelView):
    can_create = False 
    can_edit = False
    can_export = True
    export_max_rows = 1000000
    export_types = ['csv', 'tsv']



# Create admin
admin = admin.Admin(app, name='Scraped Emails', template_mode='bootstrap3', url='/')

# Add views
admin.add_view(PostAdmin(Email, db.session))

def build_sample_db():
    """
    database creation
    """

    import random
    import datetime

    db.drop_all()
    db.create_all()
    db.session.commit()
    return

if __name__ == '__main__':
    # Build db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
