#!/usr/bin/env python
from base64 import b64encode
from random import SystemRandom
import bcrypt

# Make secret key
rand = SystemRandom()
randstring = b64encode(bytes(rand.getrandbits(128)))
with open('session.secret', 'w') as out:
    out.write(randstring)

# Set password
passwd = raw_input('admin password: ').strip()
with open('passwd.secret', 'w') as out:
    hashedpw = bcrypt.hashpw(passwd, bcrypt.gensalt())
    out.write(hashedpw)
