import nltk 
from nltk.corpus import wordnet 
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
import random


class MegaNLP:
    def __init__(self):
        print('loading the wordnet corpus...')
        wordnet.ensure_loaded()
        print('loading done')
        self.numbers = ['one','two','three','four','five','six','seven','eight','nine','zero','ten','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety']
        self.nlp = spacy.load('en')
        self.nlp.add_pipe(WordnetAnnotator(self.nlp.lang), after='tagger')
        f= open('sorted_first_names.txt','r')
        lines = f.readlines()
        self.first_name_array = []
        for line in lines:
           line = line.rstrip()
           self.first_name_array.append(line)
        f= open('sorted_last_names.txt','r')
        lines = f.readlines()
        self.last_name_array = []
        for line in lines:
           line = line.rstrip()
           self.last_name_array.append(line)
        f= open('bad_words.txt','r')
        lines = f.readlines()
        self.profane_words_array = []
        for line in lines:
           line = line.rstrip()
           self.profane_words_array.append(line)

        f= open('states.txt','r')
        lines = f.readlines()
        self.states_array = []
        for line in lines:
           line = line.rstrip()
           line = line.lower()
           self.states_array.append(line)

        f= open('random_addresses.txt','r')
        lines = f.readlines()
        self.random_addresses_array = []
        for line in lines:
           line = line.rstrip()
           line = line.lower()
           self.random_addresses_array.append(line)

    def random_first_name(self):
        l = len(self.first_name_array)
        i = random.randint(1,l)
        return self.first_name_array[i]

    def random_last_name(self):
        l = len(self.last_name_array)
        i = random.randint(1,l)
        return (self.last_name_array[i]).lower()
   
    def random_ssn(self):
        ret = ''
        for i in range(0,10):
             n = random.randint(0,10)
             ret = ret + ' ' + self.numbers[n]
        return ret
     
    def random_phone(self):
        ret = ''
        for i in range(0,10):
             n = random.randint(0,10)
             ret = ret + ' ' + self.numbers[n]
        return ret

    def random_address(self):
        l = len(self.random_addresses_array)
        i = random.randint(1,l)
        return self.random_addresses_array[i]

    def binarySearch(self ,arr, x): 
        l = 0
        r = len(arr) -1
        while (l <= r): 
            m = l + ((r - l) // 2) 
            #print('l= ',l,' ; r= ',r,' ; m= ',m)
            # Check if x is present at mid 
            if ( x.lower() == arr[m].lower() ): 
                return m - 1
      
            # If x greater, ignore left half 
            if ( x.lower() > arr[m].lower()): 
                l = m + 1
      
            # If x is smaller, ignore right half 
            else: 
                r = m - 1
      
        return -1
  
    def is_first_name(self, name):
       result = self.binarySearch(self.first_name_array, name) 
       if (result == -1): 
          return False
       else:
          return True 

    def is_last_name(self, name):
       result = self.binarySearch(self.last_name_array, name) 
       if (result == -1): 
          return False
       else:
          return True 

    def is_profane_word(self, name):
       name = name.replace('\'','')
       result = self.binarySearch(self.profane_words_array, name) 
       if (result == -1): 
          return False
       else:
          return True 
    def find_first_names(self, mystr):
       sent = mystr.split()
       sent = self.remove_common_words(sent)
       names = []
       for word in sent:
           if( self.is_first_name(word)):
               names.append(word)
       return names

    def find_profane_words(self, mystr):
       sent = mystr.split()
       sent = self.remove_common_words(sent)
       names = []
       for word in sent:
           if( self.is_profane_word(word)):
               names.append(word)
       return names

    def find_last_names(self, mystr):
       sent = mystr.split()
       sent = self.remove_common_words(sent)
       names = []
       for word in sent:
           if( self.is_first_name(word)):
               names.append(word)
       return names
    def remove_common_words(self, words):
        commonwords = ['i','the','is','a','an','am','are','was','were' ,'have','has','had','will','going','she','he','they','can','may','might','should','could','can','would','please','thanks','then','to','for','with','upon','on','in','from','since','after','before','want','need','there','here','be','my','your','her','his','mine','yours','hers']
        new_words = [word for word in words if word not in commonwords]
        return new_words


    def contain_domain(self, sentence,domain): 
        domains = []
        words = sentence.split()
        words = self.remove_common_words(words)
        for word in words:
            token = self.nlp(word)[0]
            tmp_domains = token._.wordnet.wordnet_domains()
            for dom in tmp_domains:
                 domains.append(dom)
    
        domains = list(set(tmp_domains))
        print(domains)
        for dom in domains:
            if( dom == domain):
                return True
        return False
    
    def find_synonym(self, word, sentence):	
        synonyms = [] 
        answers = []
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 
                synonyms.append(l.name()) 
        synonyms = list(set(synonyms))
        words = sentence.split()
        words = self.remove_common_words(words)
        for myword in words:
           simpleword = WordNetLemmatizer().lemmatize(myword)
           for synonym in synonyms:
               simple_syn = WordNetLemmatizer().lemmatize(synonym)
               if (simpleword==synonym):
                   answers.append(myword)
        return answers

    def find_antonyms(self, word, sentence):	
        antonyms = [] 
        synonyms = [] 
        answers = []
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 
                synonyms.append(l.name()) 
                if l.antonyms(): 
        	        antonyms.append(l.antonyms()[0].name()) 
        
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 
                synonyms.append(l.name()) 
        synonyms = list(set(antonyms))
        words = sentence.split()
        word = self.remove_common_words(words)
        for myword in words:
           simpleword = WordNetLemmatizer().lemmatize(myword)
           for synonym in synonyms:
               simple_syn = WordNetLemmatizer().lemmatize(synonym)
               if (simpleword==synonym):
                   answers.append(myword)
        return answers

    def find_similar(self, word, sentence):	
        similars = []
        synsets_word = wordnet.synsets(word)
        words = sentence.split()
        words = self.remove_common_words(words)
        for myword in words:
           synsets_myword = wordnet.synsets(myword)
           for mysyn in synsets_myword :
               for syn in synsets_word:
                   sim = mysyn.wup_similarity(syn)
                   #print('similarity of',syn,', ', mysyn,' is ', sim)
                   if (sim is not None):
                       if (sim > 0.6):
                           similars.append(myword)
        similars = list(set(similars))
        return similars
   
    def is_number(self,word):
        if word in self.numbers:
            return True
        return False

    def find_high_digits_number(self, mystr):
       sent = mystr.split()
       sent = self.remove_common_words(sent)
       nums = []
       n_digits = 0
       for word in sent:
           if( self.is_number(word)):
               nums.append(word)
               n_digits = n_digits + 1
       if(n_digits >8):
           return nums
       else:
           return ""
       return ""

    def find_phone_number(self, mystr):
       ret = self.find_high_digits_number(mystr)
       return ret
    
    def find_ssn(self, mystr):
       ret = self.find_high_digits_number(mystr)
       return ret

    def is_state(self,word):
        if word in self.states_array:
            return True
        else:
            return False
    
    def find_us_address(self,mystr):
       address = ""
       sent = mystr.split()
       l = len(sent)
       first_num_index = -1
       state_index = -2
       print(sent)

       for i in range(0,l):
           if(self.is_number(sent[i])):
               first_num_index = i
               break
       for i in range(0,l):
           if(self.is_state(sent[i])):
               state_index = i
               break
       print(first_num_index,state_index)
       if(first_num_index<0):
          return address
       if(state_index<first_num_index):
          return address
       for i in range(first_num_index,state_index+1):
          address = address + sent[i] + " "
       address.rstrip(" ")
       return address
       
