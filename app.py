from flask import Flask, render_template, request, redirect, url_for
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, confirm_login, fresh_login_required
import bcrypt
import yaml
import json
import os
import glob
import socket
import json
from psas_cmdr import commands

app = Flask(__name__)

# Read secret key for session managment
try:
    with open('session.secret', 'r') as fin:
        app.config.update(SECRET_KEY=fin.read())
except:
    print "Secret key missing, run `./init.py` first!"
    exit(1)

# Read admin password for session managment
try:
    with open('passwd.secret', 'r') as fin:
        PWHASH = fin.read()
except:
    print "Password hash missing, run `./init.py` first!"
    exit(1)

login_manager = LoginManager()
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id

USERS = { 1: User(u"admin", 1) }

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

login_manager.setup_app(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        testpass = request.form.get('password').encode('ascii')
        if bcrypt.hashpw(testpass, PWHASH) == PWHASH:
            login_user(USERS[1], remember=False)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', failure=True)
    else:
        return render_template('login.html', failure=False)

def slug(name):
    s = name.lower()
    s = s.replace(' ', '-')
    return s

# Find all .yml files
files_yml = sorted(glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles/*.yml")))

# Make lise of files + names
Profiles = []
for f in files_yml:
    with open(f, 'r') as y:
        p = yaml.load(y, Loader=yaml.Loader)
        Profiles.append({
            'name': p['title'],
            'slug': slug(p['title']),
            'uri': "/profiles/"+slug(p['title']),
            'file': f,
            'sections': p['sections'],
        })

def do_command(defn, test=False):
    # get connection class
    if test:
        conn = commands.CONNECTIONS['TEST'][defn['type']]
    else:
        conn = commands.CONNECTIONS[defn['connection']][defn['type']]
    success, response = conn.send(defn['payload'])
    return success, response


@app.route('/cmd/<profile>/<int:section>/<int:command>', methods=['POST'])
def cmd(profile, section, command):

    success = None
    response = "Unknown"
    for p in Profiles:
        if profile == p['slug']:
            success, response = do_command(p['sections'][section]['commands'][command])

    if success is not None:
        return json.dumps({'result': "success", 'data': response})

    return json.dumps({'result': "failure", 'reason': response})


@app.route('/TEST/cmd/<profile>/<int:section>/<int:command>', methods=['POST'])
def test_cmd(profile, section, command):

    success = None
    response = "Unknown"
    for p in Profiles:
        if profile == p['slug']:
            success, response = do_command(p['sections'][section]['commands'][command], test=True)

    if success is not None:
        return json.dumps({'result': "success", 'data': response})

    return json.dumps({'result': "failure", 'reason': response})



@app.route('/')
@app.route('/profiles/<profile>')
@login_required
def index(profile=None):
    if profile is None:
        profile = 'default'
    for p in Profiles:
        if profile == p['slug']:
            profile = p

    return render_template('index.html', layouts=Profiles, sections=profile['sections'], slug=profile['slug'])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
