# Rocket Commander

Configurable web app to send commands to the flight computer and other
subsystems.


## Concept

We have a couple of types of commands:

 - **Signal**
    - Asynchronous, singular commands.
    - _Example_: "ARM"
 - **Flip**
    - Commands with a logical negative, i.e. something that flips a state.
    - _Example_: RNH Port power (on ↔ off)

And need a convenient way to expose these commands to an interface somewhere.
We've chosen the browser as the most convenient way to make cross-device
interfaces quickly. We have multiple places to send commands and the exact
command set changes relatively often so an easy way of describing the grouping
and layout of our commands is necessary (a config file).
