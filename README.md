# Rocket Commander

Configurable web app to send commands to the flight computer and other
subsystems.


## Concept

And need a convenient way to expose commands to an interface somewhere.
We've chosen the browser as the most convenient way to make cross-device
interfaces quickly. We have multiple places to send commands and the exact
command set changes relatively often so an easy way of describing the grouping
and layout of our commands is necessary (a config file).


# Install

To install make sure you have libffi-dev. Make a virtual environment and install
python dependences via pip.

    $ sudo apt-get install python-dev libffi-dev
    $ pip install -r requirements.txt

The first time you need to generate secrets. Run

    $ ./init.py

And fill in an admin password.


# Run

To run in debug mode:

    $ python app.py

To run in production (on port 80):

    $ sudo ./run.py

### Optional: Run debug TCP listener

In tests there is a simple tcp listener that will respond to commands when in
'test mode'.

    $ cd tests
    $ ./listener.py
