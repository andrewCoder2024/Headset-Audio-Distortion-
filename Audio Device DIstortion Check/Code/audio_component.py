import stt, tts, multi


class audial:
    def __init__(self, isActing=False, sLang='en', lLang='en'):
        self.listener = stt.Listener()
        self.speaker = tts.Speaker()
        self.speaker_lang = sLang
        self.listener_lang = lLang

    def say(self, text, speed=1):
        self.speaker.speak(text, speed)

    def listen(self):
        try:
            response = self.listener.listens()
        except:
            response = "i didn't quite hear you, can you repeat it?"
        print("You:", response)
        return response.lower()

    def change_speaker_lang(self, lang='en'):
        self.speaker.change_lang(lang)
        self.speaker_lang = lang

    def change_listener_lang(self, lang='en'):
        self.listener.change_lang(lang)
        self.listener_lang = lang
