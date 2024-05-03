from .types import Translators

#  This needs to have a key and work diferent YandexTranslator, QCRI
# I could use this to automate the translations single_detection, batch_detection

def translate_generator(Generator, text:str, source= 'auto', target= 'english'):
    return Generator(source, target).translate(text)

def translate_text_factory(translator, text: str, source: str= 'auto', target: str= 'english'):
    print('translator')
    print(translator)
    tranlated_text:str = translate_generator(translator, text, source, target)
    # match translator:
    #     case 'google':
    #         tranlated_text = 
    #     case 'pons':
    #         tranlated_text = translate_generator(PonsTranslator, text, source, target)
    #     case 'linguee':
    #         tranlated_text = translate_generator(LingueeTranslator, text, source, target)
    #     case 'myMemory':
    #         tranlated_text = translate_generator(MyMemoryTranslator, text, source, target)
                        
    
    return tranlated_text
