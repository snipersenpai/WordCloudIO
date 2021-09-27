from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '500')
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty,ObjectProperty,BooleanProperty
from kivy.uix.popup import Popup
import os

import wordcloud

def generate_freq(text):
    # Here is a list of punctuations and uninteresting words you can use to process your text
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]

    # LEARNER CODE START HERE
    freq = {}
    cur_wrd = ''
    for char in text:
        if char in punctuations:
            continue
        if char==' ':
            if (len(cur_wrd)>0) and (cur_wrd not in uninteresting_words) :
                freq[cur_wrd] = freq.get(cur_wrd,0)+1
            cur_wrd = ''
            continue
        cur_wrd += char.lower()
    return freq
def verify_file(file):
    content = False
    #check if file exit
    if os.path.exists(file):
        #check if file is txt
        if os.path.splitext(file)[1] == '.txt':
            content = open(file,'r').read()
    print('content: ',content)
    return content
class ErrorPopUp(Popup):
    text = StringProperty('')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    pass
class FileChoosePopUp(Popup):
    ref = ObjectProperty()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def Open(self,path,selection):
        print(path,selection)
        verified_file = verify_file(selection[0])
        if verified_file:
            self.ref.from_file_path = selection[0]
            self.ref.text = verified_file
            self.dismiss()
        else:
            ErrorPopUp(text='Invalid Input File').open()
            pass
        return
    pass
class WORDCLOUD(AnchorLayout):
    from_file_path = StringProperty('')
    to_path = StringProperty('Untitled.png')
    text = ''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.file_chooser_popup = FileChoosePopUp(ref=self)
    def on_from_file_path(self,ins,val):
        self.from_file_path_input.text = self.from_file_path
        return
    def set_to_path(self,text):
        self.to_path = text
        return
    def generate(self):
        cloud = wordcloud.WordCloud()
        if self.text:
            freq=generate_freq(self.text)
            img = cloud.generate_from_frequencies(freq)
            image = img.to_image()
            if self.to_path:
                if not self.to_path.endswith('.png'):
                    self.to_path+='.png'
            else:
                self.to_path = 'Untitled.png'
            image.save(self.to_path)
            image.show()
            print(freq)
        else:
            ErrorPopUp(text='Input File (.txt) Field Cannot be empty').open()
            return
        pass
    pass

class MainApp(App):
    def build(self):
        return WORDCLOUD()
if __name__ == '__main__':
    MainApp().run()
