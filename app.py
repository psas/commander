#!/usr/bin/env python
from flask import Flask, render_template
import yaml
import json
import os
import glob
app = Flask(__name__)

def slug(name):
    s = name.lower()
    s = s.replace(' ', '-')
    return s

# Find all .yml files
files_yml = glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles/*.yml"))

# Make lise of files + names
Profiles = []
for f in files_yml:
    with open(f, 'r') as y:
        p = yaml.load(y, Loader=yaml.Loader)
        Profiles.append({
            'name': p['title'],
            'slug': slug(p['title']),
            'uri': "/profiles/"+slug(p['title']),
            'file': f
        })

@app.route('/cmd/<profile>/<int:section>/<int:command>', methods=['POST'])
def cmd(profile, section, command):
    print profile, section, command
    return "{}"

@app.route('/')
def index():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles/default.yml")

    # Open file, parse
    with open(filename, 'r') as y:
        profile = yaml.load(y, Loader=yaml.Loader)
        sections = profile['sections']

    return render_template('index.html', layouts=Profiles, sections=sections)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
