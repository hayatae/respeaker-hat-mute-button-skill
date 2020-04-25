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
        self.isButtonPressed = False
        if pi_interface:
            self.log.info("Pi GPIO interface installed. Binding to button.")
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(RESPEAKER_BUTTON, GPIO.IN)
            GPIO.add_event_detect(
                RESPEAKER_BUTTON, GPIO.BOTH, self.mute_button_handler)
        else:
            self.log.info("Pi GPIO interface is not installed.")

    def mute_button_handler(self, channel):
        previousState = self.isButtonPressed

        if GPIO.input(channel) == GPIO.HIGH:
            # released
            if self.isButtonPressed:
                self.isButtonPressed = False
        else:
            # pressed
            if not self.isButtonPressed:
                self.isButtonPressed = True

        if self.isButtonPressed == False and previousState == True:
            if self.isMuted:
                self.isMuted = False
                self.bus.emit(Message('mycroft.mic.unmute'))
                self.log.info("Unmuting microphone.")
                self.speak_dialog('Unmuted')
            else:
                self.isMuted = True
                self.bus.emit(Message('mycroft.mic.mute'))
                self.log.info("Muting microphone.")
                self.speak_dialog('Muted')

    def shutdown(self):
        if pi_interface:
            GPIO.cleanup()


def create_skill():
    return RespeakerHatMuteButton()
