#!/usr/bin/env python
from flask import Flask, render_template
import yaml
import json
import os
import glob
import socket
from psas_packet import network
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

def do_command(defn):
    if defn['connection'] == 'FC-tcp':
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', 0))
            sock.connect(('127.0.0.1', 2223))
            sock.send(defn['payload'])
            data = sock.recv(512)
            print data
        except:
            print "borp"
        finally:
            sock.close()


@app.route('/cmd/<profile>/<int:section>/<int:command>', methods=['POST'])
def cmd(profile, section, command):
    print profile, section, command

    for p in Profiles:
        if profile == p['slug']:
            #print p['sections'][section]['commands'][command]
            do_command(p['sections'][section]['commands'][command])
    return "{}"


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
