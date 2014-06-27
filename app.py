#!/usr/bin/env python
from flask import Flask, render_template
import yaml
import json
import os
import glob
import socket
import json
from psas_cmdr import commands
app = Flask(__name__)

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
    response = conn.send(defn['payload'])
    print response
    return

@app.route('/cmd/<profile>/<int:section>/<int:command>', methods=['POST'])
def cmd(profile, section, command):
    print profile, section, command

    for p in Profiles:
        if profile == p['slug']:
            do_command(p['sections'][section]['commands'][command])
    return json.dumps({'result': "success"})

@app.route('/TEST/cmd/<profile>/<int:section>/<int:command>', methods=['POST'])
def test_cmd(profile, section, command):
    for p in Profiles:
        if profile == p['slug']:
            do_command(p['sections'][section]['commands'][command], test=True)
    return json.dumps({'result': "success"})



@app.route('/')
@app.route('/profiles/<profile>')
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
