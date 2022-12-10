
import spacy
from spacy.cli import download
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets') 
nltk.download('maxent_ne_chunker')
nltk.download('words')
import textacy
import gensim
from gensim.models import Word2Vec
import gensim.downloader as api
#from gensim.test.utils import common_texts

import csv, sys
import nltk, random, json , pickle
#nltk.download('punkt');nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.feature_extraction.text import CountVectorizer
import os.path

class text_processing:
    def __init__(self, sentence,prediction):
        self.nlp = spacy.load('en_core_web_lg')
        
        self.inputStr = self.nlp(sentence)
        self.nlp2 = nltk.sent_tokenize(sentence)
        self.pred = prediction
        self.cols = self.processColumns()
        #!python -m spacy download en_core_web_md --user
        #nlp =  spacy.load('en_core_web_sm')
        
        self.nouns ,self.verbs = self.get_nouns()
        self.noun_chunks = self.get_nounChunks()
        self.entities,self.back_entities = self.get_entitiy()
        self.columns = self.get_columns()
        self.conditions = []
    
    def processColumns(self):
        path = 'Data/IMDB_Movie_Data.csv'
        with open(path, newline='') as f:
            reader = csv.reader(f)
            try:
                #for row in reader:
                #    print(row)
                cols = next(reader)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
        
        cols = [x.lower() for x in cols]
        return cols
    
    def get_nouns(self):
        nouns = []
        verbs = []
        for token in self.inputStr:
            #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
            if token.pos_ in ['NOUN','PROPN'] or token.tag_ in ['NN','NNS','NNP','NNPS']:
                nouns.append(token.lemma_)
            if token.pos_ in ['VERB'] or token.tag_ in ['VB','VBG','VBD','VBN','VBP','VBZ','JJ']:
                verbs.append(token.lemma_)
        return nouns,verbs
    
    def get_nounChunks(self):
        chunks = []
        for noun_chunks in self.inputStr.noun_chunks:
            chunks.append(noun_chunks)
        return chunks
    
    def get_entitiy(self):
        entities = []
        back_entities =[]

        for sent in self.nlp2:
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label'):
                    print(chunk.label(), ' '.join(c[0] for c in chunk))
                    back_entities.append([chunk.label(),' '.join(c[0] for c in chunk)])
        for ent in self.inputStr.ents:
            #print(ent.text, ent.label_)
            entities.append([ent.label_,ent.text])
        return entities,back_entities
    
    def get_columns(self):
        columns = []
        for n in self.nouns:
            if n in self.cols:
                columns.append(n)
            if 'movie' in n or 'title' in n or 'film' in n:
                columns.append('title')
            if 'act' in n:
                columns.append('actors')
            if 'direct' in n:
                columns.append('director')
        
        for v in self.verbs:
            if 'direct' in v:
                columns.append('director')
            if 'rat' in v:
                columns.append('rate')
                
        columns = list(set(columns))
        return columns
    
    def add_person(self,p):
        if 'title' in self.columns and not 'director' in self.columns and not 'actor' in self.columns:
            print("Adding Actor")
            c = "imdb.actors LIKE \'%{actor}%\'".format(actor=p[1])
            self.conditions.append(c)
                     
                        
        if 'director' in self.columns:
            print("Adding Director")
            c = "imdb.director LIKE \'%{director}%\'".format(director=p[1])
            self.conditions.append(c)
            self.columns.remove('director')
                        
        if 'actor'in self.columns:
            c = "imdb.actors LIKE \"%{actor}%\"".format(actor=p[1])
            self.conditions.append(c)
            self.columns.remove('actor')
                    
    def unique_conditions(self,P):
        holder = []
 
        # traverse for all elements
        for x in P:
            # check if exists in unique_list or not
            if x not in P:
                holder.append(x)
        return holder

    def constructQuery(self):
        print("NOUNS:",self.nouns)
        print("VERBS:",self.verbs)
        print("COLUMNS:",self.columns)
        print("ENTITIES:",self.entities)
        print("B_ENTITIES:",self.back_entities)

        
        people = []

        for e in self.entities:
            print(e)
            if 'PERSON' in e:
                people.append(e)
                

        for b in self.back_entities:
            print(b)
            if 'PERSON' in b:
                if b not in people:
                    people.append(b)
        
        
     
        print("People:",people)
        for p in people:
            self.add_person(p)

        #self.conditions = list(set(self.conditions))
        set_cols = self.pred.count('[columns]')
        set_con = self.pred.count('[conditions]')
        col_len = len(self.columns)
        
        if col_len > 1:
            co = ""
            for i in range(col_len):
                if i == col_len-1:
                    co+=self.columns[i] 
                else:
                    co+=self.columns[i] + ','
            
            self.pred = self.pred.replace('[columns]',co)
        else:
            self.pred = self.pred.replace('[columns]',self.columns[0])
        
        print("CONDTIONS:",self.conditions)
        if len(self.conditions) >= 1:
            for i in range(len(self.conditions)):
                print("Replacing")
                self.pred = self.pred.replace('[conditions]',self.conditions[i])
        else:
            print("NO CONDITIONs")
            self.pred.replace("WHERE [conditions]","")
        
        print(self.pred)
        return self.pred








lemmatizer=WordNetLemmatizer()
context={};
class Testing:
    def __init__(self):
        #load the intent file
        self.intents = json.loads(open('intents.json').read())
        
        #load the training_data file which contains training data
        data=pickle.load(open("training_data","rb"))
        self.words = data['words']
        self.classes = data['classes']
        self.model = None
        if os.path.exists('learned_model.h5'):
            self.model = load_model('learned_model.h5')

        
        #set the probability threshold value
        self.prob_threshhold = 0.5
        

    def tokens(self,text):
        tokens = word_tokenize(text)
        return tokens
    
    def process_input(self,sentence):
        
        special_chars = list(".'!@#$%^&*?")
        
        #tokenize the input sentence
        input_words = word_tokenize(sentence.lower())
        
        #lemmatize and remove special characters
        input_words = list(map(lemmatizer.lemmatize,input_words))
        input_words = list(filter(lambda x:x not in special_chars,input_words))
        
        
        #Construct the vectorizer
        cv = CountVectorizer(tokenizer=self.tokens,analyzer="word",stop_words=None)
        input_words =' '.join(input_words)
        

        #Fit the vectorizer on the the words
        words = ' '.join(self.words)
        vectorize = cv.fit([words])
        
        # Create vector of input sentence
        word_vector = vectorize.transform([input_words]).toarray().tolist()[0]
        
        return(np.array(word_vector)) 

    
    def classify(self,sentence):
        
        #Predict class of input sentence
        mod_input = [self.process_input(sentence)]
        if self.model != None:
            results = self.model.predict(np.array(mod_input))[0]
        else:
            results = []
        
        print("results:",results)
        
        #Create list of class and probability
        full_results = list(map(lambda x: [x[0],x[1]], enumerate(results)))
        
        print("fullresults:",full_results)
        
        #Retain the classes with higher probability
        top_results = list(filter(lambda x: x[1]> self.prob_threshhold ,full_results))

        print("fullresults:",top_results)
        
        #Sort in descending order
        top_results.sort(key=lambda x: x[1], reverse=True)
        
        print("TOP:",top_results)
        return_list = []

        for i in top_results:
            print(i)
            return_list.append((self.classes[i[0]],str(i[1])))
        
        return return_list
    
    
    def getQuery(self,sentence,intent):
        self.inputP = text_processing(sentence,intent['query'][0])
        query = self.inputP.constructQuery()
        return query
    
    def results(self,sentence,userID):
        return self.classify(sentence)
    
    def Query(self,sentence):
        #get class of users query
        query = None
        results = self.classify(sentence)
        print("Test.py Results:",sentence,results)
        #store random query to the query
        ans=""
        
        if len(results) > 0:
            tag = results[0][0]
            intent = self.intents[tag]
            query = self.getQuery(sentence,intent)
       
            print("Query:",query)
                            
        return query
