import spacy
from spacy.cli import download
import pandas as pd
import nltk, random, json , pickle
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
import csv, sys
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
        self.nouns ,self.verbs = self.get_nouns()
        self.noun_chunks = self.get_nounChunks()
        self.entities,self.back_entities = self.get_entitiy()
        self.columns = self.get_columns()
        self.conditions = []
    
    def tokens(self,text):
        tokens = word_tokenize(text)
        return tokens

    def processColumns(self):
        path = 'Data/IMDB_Movie_Data.csv'
        with open(path, newline='') as f:
            reader = csv.reader(f)
            try:
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
            if token.pos_ in ['NOUN','PROPN'] or token.tag_ in ['NN','NNS','NNP','NNPS','ADP']:
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
        if 'title' in self.columns and not 'director' in self.columns and not 'actors' in self.columns:
            print("Adding Actor")
            c = "imdb.actors LIKE \'%{actor}%\'".format(actor=p[1])
            self.conditions.append(c)
                     
                        
        if 'director' in self.columns:
            print("Adding Director")
            c = "imdb.director LIKE \'%{director}%\'".format(director=p[1])
            self.conditions.append(c)
            self.columns.remove('director')
                        
        if 'actors'in self.columns:
            c = "imdb.actors LIKE \'%{actor}%\'".format(actor=p[1])
            self.conditions.append(c)
            self.columns.remove('actors')
                    
    def unique_conditions(self,P):
        holder = []
        for x in P:
            if x not in P:
                holder.append(x)
        return holder

    def constructQuery(self,tag,pred_columns):
        print("NOUNS:",self.nouns)
        print("NOUN_Chunks:",self.noun_chunks)
        print("VERBS:",self.verbs)
        print("COLUMNS:",self.columns)
        print("ENTITIES:",self.entities)
        print("B_ENTITIES:",self.back_entities)
        print("Predicted columns:",pred_columns)
        
        if pred_columns != None:
            pred_cols = ""
            if ',' in pred_columns and ' ' not in pred_columns:
                pred_cols = pred_columns.split(',')
            if ' ' in pred_columns:
                pred_cols = pred_columns.replace(',',"")
                pred_cols = pred_cols.split()
            
            print("After token PREDICTED COLUMNS:",pred_cols)
            self.columns = list(set(self.columns)|set(pred_cols))
            print("AFter Union:",self.columns)
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

        set_cols = self.pred.count('[columns]')
        set_con = self.pred.count('[conditions]')
        col_len = len(self.columns)
        
        nums = ['metascore','revenue','rank','runtime','year','rating','votes']
        agg = ['avg','min','max','sum']
        if col_len > 1:
            co = ""
            if tag not in agg:
                for i in range(col_len):
                    if i == col_len-1:
                        co+=self.columns[i] 
                    else:
                        co+=self.columns[i] + ','
            else:
                for c in self.columns:
                    if c in nums:
                        self.pred = self.pred.replace('[columns]',c)
            
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
            self.pred = self.pred.replace("WHERE [conditions]","")
        
        print(self.pred)




        return self.pred


lemmatizer=WordNetLemmatizer()
context={}
class Testing:
    def __init__(self):
        #load the intent file
        self.intents = json.loads(open('intents.json').read())
        self.column_intents = json.loads(open('column_intents.json').read())
        
        #load the training_data file which contains training data
        self.model = None
        self.words = None
        self.classes = None
        self.tag = None
        
        self.column_model = None
        self.column_words = None
        self.column_classes = None
        self.pred_columns = None

        if os.path.exists('training_data'):
            data=pickle.load(open("training_data","rb"))
            self.words = data['words']
            self.classes = data['classes']
        
        if os.path.exists('learned_model.h5'):
            self.model = load_model('learned_model.h5')

        if os.path.exists('column_training_data'):
            data=pickle.load(open("column_training_data","rb"))
            self.column_words = data['words']
            self.column_classes = data['classes']
        
        if os.path.exists('column_learned_model.h5'):
            self.column_model = load_model('column_learned_model.h5')
        
        if self.column_model == None:
            print("MODEL NONE______________________________________")
        #set the probability threshold value
        self.prob_threshhold = 0.2
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
        
        if self.words != None:
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
        print("REGULAR MOD INPUT:",mod_input,"From sentence:",sentence)
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

    
    def column_process_input(self,sentence):
        
        special_chars = list(".'!@#$%^&*?")
        
        #tokenize the input sentence
        input_words = word_tokenize(sentence.lower())
        
        #lemmatize and remove special characters
        input_words = list(map(lemmatizer.lemmatize,input_words))
        input_words = list(filter(lambda x:x not in special_chars,input_words))
        
        if self.column_words != None:
            #Construct the vectorizer
            cv = CountVectorizer(tokenizer=self.tokens,analyzer="word",stop_words=None)
            input_words =' '.join(input_words)
            
            #Fit the vectorizer on the the words
            words = ' '.join(self.column_words)
            vectorize = cv.fit([words])
            
            # Create vector of input sentence
            word_vector = vectorize.transform([input_words]).toarray().tolist()[0]
            
            return(np.array(word_vector)) 

    def classify_columns(self,sentence):
        
        #Predict class of input sentence
        
        mod_input = [self.column_process_input(sentence)]
        
        print("Column MOD INPUT:",mod_input,"From sentence:",sentence)
        if self.column_model != None:
            results = self.column_model.predict(np.array(mod_input))[0]
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
            return_list.append((self.column_classes[i[0]],str(i[1])))
        
        return return_list
    
    
    
    def getQuery(self,sentence,intent):
        self.inputP = text_processing(sentence,intent['query'][0])
        query = self.inputP.constructQuery(self.tag,self.pred_columns)
        return query
    
    def results(self,sentence,userID):
        return self.classify(sentence)
    
    def Query(self,sentence):
        #Predict query tag
        query = None
        results = self.classify(sentence)
        col_results = self.classify_columns(sentence)
        print("Results:",sentence,":",results,":",col_results)


        if len(col_results) > 0:
            self.pred_columns = col_results[0][0]
        ans=""
        
        if len(results) > 0:
            self.tag = results[0][0]
            print(self.intents)
            intent = self.intents[self.tag]
            query = self.getQuery(sentence,intent)
       
            print("Query:",query)
        
                            
        return query
    
    
class manualTraining():
    def __init__(self, sentence):
        self.nlp = spacy.load('en_core_web_lg')
        self.inputStr = self.nlp(sentence)
        self.nlp2 = nltk.sent_tokenize(sentence)
        #self.cols = self.processColumns()
        self.nouns ,self.verbs = self.get_nouns()
        self.noun_chunks = self.get_nounChunks()
        self.entities,self.back_entities = self.get_entitiy()
        self.cols = ['rank','title','genre','description','director','actors','years','runtime','rating','votes','revenue','metascore']

        self.verb_patterns = [[{"POS":"AUX"}, {"POS":"VERB"}, {"POS":"ADP"}], 
                              [{"POS":"AUX"},{"POS":"VERB"}],[{"POS":"ADJ"}],
                              [{"POS":"NOUN"},{"POS":"VERB"}],
                              [{"POS": "PREP"},{"POS":"VERB"}],
                              [{"POS":"NOUN"},{"POS":"VERB"}, {"POS":"ADP"},{"POS":"NOUN"}],
                              [{"POS": "PREP"},{"POS":"VERB"},{"POS":"NOUN"}],
                              [{"POS":"VERB"}],
                              [{"POS":"NOUN"},{"POS":"ADP"}]
                              ]


    def process_train_columns(self,cols):
        cols = cols.lower()
        if ',' not in cols and ' ' not in cols:
            cols = [cols] 
        if ',' in cols and ' ' not in cols:
                cols = cols.split(',')
        if ' ' in cols:
                cols = cols.replace(',',"")
                cols = cols.split()
        
        cols.sort()
        cols = ",".join(cols)
        return cols

    def columns_process_Training_input(self):
        print(self.nouns)
        print(self.verbs)
        print(self.noun_chunks)
        #for n in self.noun_chunks
        print(self.entities,self.back_entities)
        patterns = []
        for n in self.nouns:
            print("NOUNS:",n)
            flag = True
            
            if len(self.entities) > 0 :
                print("Entitites:",self.entities[0][1],self.back_entities[0][1])
                for e in self.entities:
                    if n in e[1]:
                        flag = False
            
            if len(self.back_entities) > 0 :
                for e in self.back_entities:
                    if n in e[1]:
                        flag = False
            
            for c in self.cols:
                if n in c:
                    flag = True
            if n == 'movie':
                flag = False
            
            if n in ['what','for','be','of']:
                flag = False
            
            if flag == True:
                print("Appeding:",n)
                patterns.append(n)

        for v in self.verbs:
            patterns.append(v)
        
        for nc in self.noun_chunks:
            flag = True
            print("NC:",str(nc),type(nc),type(str(nc)))
            nc = str(nc)
            if len(self.entities) > 0 :
                for e in self.entities:
                    if nc in e[1]:
                        flag = False
            
            if len(self.back_entities) > 0 :
                for e in self.back_entities:
                    if nc in e[1]:
                        flag = False
           
            print("NC:",nc,flag)
            print("THE COLUMNS:",self.cols)
            if flag == True:
                print("Appeding:",nc)
                patterns.append(nc)
        
        vp, nouns = self.find_triplet()
        patterns.append(vp)
        
        print("PATTERNS:",patterns)
        return patterns

    def process_Training_input(self):
        print(self.nouns)
        print(self.verbs)
        print(self.noun_chunks)
        #for n in self.noun_chunks
        print(self.entities,self.back_entities)
        patterns = []
        for n in self.nouns:
            print("NOUNS:",n)
            flag = True
            
            if len(self.entities) > 0 :
                print("Entitites:",self.entities[0][1],self.back_entities[0][1])
                for e in self.entities:
                    if n in e[1]:
                        flag = False
            
            if len(self.back_entities) > 0 :
                for e in self.back_entities:
                    if n in e[1]:
                        flag = False
            
            for c in self.cols:
                if n in c:
                    flag = False
            if n == 'movie':
                flag = False

            if flag == True:
                print("Appeding:",n)
                patterns.append(n)
        
        for v in self.verbs:
            print("VERBS:",v)
            flag = True
            for c in self.cols:
                if v in c:
                    flag = False
            if flag == True:
                print("Appeding:",v)
                patterns.append(v)
        
        for nc in self.noun_chunks:
            flag = True
            print("NC:",str(nc),type(nc),type(str(nc)))
            nc = str(nc)
            if len(self.entities) > 0 :
                for e in self.entities:
                    if nc in e[1]:
                        flag = False
            
            if len(self.back_entities) > 0 :
                for e in self.back_entities:
                    if nc in e[1]:
                        flag = False
           
            print("NC:",nc,flag)
            print("THE COLUMNS:",self.cols)
            for c in self.cols:
                print("Checking:",c,nc)
                if c in nc:
                    nc = nc.replace(c,'')
            if flag == True:
                print("Appeding:",nc)
                patterns.append(nc)
        
        
        print("PATTERNS:",patterns)
        return patterns



    def get_nouns(self):
        nouns = []
        verbs = []
        for token in self.inputStr:
            print("Token:",token)
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
            if token.pos_ in ['NOUN','PROPN','ADP'] or token.tag_ in ['NN','NNS','NNP','NNPS','ADP']:
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
                    back_entities.append([chunk.label(),' '.join(c[0] for c in chunk)])
        for ent in self.inputStr.ents:
            entities.append([ent.label_,ent.text])
        return entities,back_entities


    def longer_verb_phrase(self,verb_phrases):
        longest_length = 0
        longest_verb_phrase = None
        for verb_phrase in verb_phrases:
            if len(verb_phrase) > longest_length:
                longest_verb_phrase = verb_phrase
        return str(longest_verb_phrase)

    def get_verb_phrases(self):
        verb_phrases = textacy.extract.matches.token_matches(self.inputStr, self.verb_patterns)
        new_vps = []
        
        for verb_phrase in verb_phrases:
            new_vps.append(verb_phrase)
        return new_vps
    
    def find_triplet(self):
        self.get_verb_phrases()
        verb_phrases = list(self.get_verb_phrases())
        verb_phrase = None
        if (len(verb_phrases) > 0 ):
            verb_phrase = self.longer_verb_phrase(list(verb_phrases))
            
        return verb_phrase, self.nouns
