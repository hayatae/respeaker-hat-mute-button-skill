from mycroft import MycroftSkill, intent_file_handler
from mycroft_bus_client import Message

try:
    import RPi.GPIO as GPIO
    """This is trapped so you can still run without RPi.GPIO
    GPIO will be checked before use
    """
    pi_interface = True
except:
    pi_interface = False
    pass

RESPEAKER_BUTTON = 26


class RespeakerHatMuteButton(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.isMuted = False
        if pi_interface:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(RESPEAKER_BUTTON, GPIO.IN)
            GPIO.add_event_detect(
                RESPEAKER_BUTTON, GPIO.BOTH, mute_button_handler)

    def mute_button_handler(self, channel):
        if GPIO.input(channel) == GPIO.HIGH:
            if self.isMuted:
                self.isMuted = False
                self.bus.emit(Message('mycroft.mic.unmute'))
                self.log.info("Unmuting microphone.")
            else:
                self.isMuted = True
                self.bus.emit(Message('mycroft.mic.mute'))
                self.log.info("Muting microphone.")


def create_skill():
    return RespeakerHatMuteButton()
