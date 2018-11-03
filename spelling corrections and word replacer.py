####################### class to check spelling mistakes ################
import enchant
from nltk.metrics import edit_distance

class SpellingReplacer(object):
    
    def __init__(self, dict_name='en', max_dist=2):
        
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist
        
    def replace(self, word):
        
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)
        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word

replacer = SpellingReplacer()
print(replacer.replace('fasttext'))  #'cookbook'
###################### class to replace repetetive words###################

import re
from nltk.corpus import wordnet

class RepeatReplacer(object):
    def __init__(self):
            
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'
        
    def replace(self, word):
        if wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


replacer = RepeatReplacer()
print(replacer.replace('looooove'))
print(replacer.replace('goose'))


######################### class to replace negations with antonyms ###########

#from nltk.corpus import wordnet

class AntonymReplacer(object):
    def replace(self, word, pos=None):
        antonyms = set()
        for syn in wordnet.synsets(word, pos=pos):
                for lemma in syn.lemmas():
                    for antonym in lemma.antonyms():
                        antonyms.add(antonym.name())
        if len(antonyms) == 1:
            return antonyms.pop()
        else:
            return None

    def replace_negations(self, sent):
        i, l = 0, len(sent)
        words = []
        while i < l:
            word = sent[i]
            if word == 'not' and i+1 < l:
                ant = self.replace(sent[i+1])
                if ant:
                    words.append(ant)
                    i += 2
                    continue
            words.append(word)
            i += 1
        return words
    
replacer = AntonymReplacer()
sent = ["let's", 'not', 'do', 'that','bad', 'code']
print(replacer.replace_negations(sent))

############# 

class WordReplacer(object):
    def __init__(self, word_map):
            self.word_map = word_map
            
    def replace(self, word):
        return self.word_map.get(word, word)


replacer = WordReplacer({'bday': 'birthday'})
print(replacer.replace('bday'))
print(replacer.replace('happy'))

########
class AntonymWordReplacer(WordReplacer, AntonymReplacer):
    pass

replacer = AntonymWordReplacer({'evil': 'good'})
print(replacer.replace_negations(['good', 'is', 'not', 'evil']))

###########################################################################

