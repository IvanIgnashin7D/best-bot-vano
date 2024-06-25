from googletrans import Translator

translator = Translator()
txt = 'поезда'
translated = translator.translate(txt, src='ru')
print(translated.text)
