from hermes_python.hermes import Hermes
from gpiozero import DigitalOutputDevice


MQTT_ADDR = "localhost:1883"        # Specify host and port for the MQTT broker

# Outputs for each amplifier set here
left_amplifier = DigitalOutputDevice(pin=17, active_high=True, inital_value=False)
right_amplifier = DigitalOutputDevice(pin=18, active_high=True, inital_value=False)


def speaker_toggle(state, side='both'):
    if state == 'toggle':
        # Check current status of amplifier pins
        right_on = bool(right_amplifier.value)
        left_on = bool(left_amplifier.value)

        # Switch amplifier on if currently off, defaults to switching off if unsure
        if not right_on:
            right_amplifier.on()
        else:
            right_amplifier.off()

        if not left_on:
            left_amplifier.on()
        else:
            left_amplifier.off()

    elif state == 'on':
        if side == 'left':
            left_amplifier.on()
        elif side == 'right':
            right_amplifier.on()
        else:
            left_amplifier.on()
            right_amplifier.on()
    elif state == 'off':
        if side == 'left':
            left_amplifier.off()
        elif side == 'right':
            right_amplifier.off()
        else:
            left_amplifier.off()
            right_amplifier.off()


# Defining callback functions to handle an intent that asks for the weather.
def subscribe_speaker_toggle_callback(hermes, intent_message):
    side = 'both'
    state = intent_message.slots.state.first().value
    if len(intent_message.slots.side) != 0:
        side = intent_message.slots.side.first().value
    print("Parsed intent : {}".format(intent_message.intent.intent_name))
    print("Setting {} speaker(s) to {}".format(side, state))
    speaker_toggle(state, side)


with Hermes(MQTT_ADDR) as h:  # Initialization of a connection to the MQTT broker
    # Registering callback functions to handle the searchWeatherForecast intent
    h.subscribe_intent("speakerToggle", subscribe_speaker_toggle_callback) \
        .start()
    # We get out of the with block, which closes and releases the connection.
