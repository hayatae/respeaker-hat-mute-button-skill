from mycroft import MycroftSkill, intent_file_handler


class RespeakerHatMuteButton(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('button.mute.hat.respeaker.intent')
    def handle_button_mute_hat_respeaker(self, message):
        self.speak_dialog('button.mute.hat.respeaker')


def create_skill():
    return RespeakerHatMuteButton()

