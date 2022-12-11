import nltk, random, json , pickle
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import flatten
nltk.download('punkt');nltk.download('wordnet')

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adagrad



lemmatizer=WordNetLemmatizer()
class initializeModel:
    def __init__(self):
        # read and load the intent file which contains sql structure
        data_file=open('intents.json').read()
        self.intents=json.loads(data_file)


    def process_data(self):
        
        #Extract patterns 
        x = lambda x:x
        cls = list(x(self.intents))
        self.pattern = list(map(lambda x:self.intents[x]["patterns"],self.intents))
        self.words = list(map(word_tokenize,flatten(self.pattern)))
        
        #Create classes for target data
        self.classes = flatten( [[x]*len(y) for x,y in zip(cls,self.pattern)])
        
        #Create Training Data
        self.Data = list(map(lambda x,y:(x,y),self.words,self.classes))

        #Convert words list to lowercase and remove special characters
        self.spec_chars = list(".,!@#$%^&*?")
        self.words = list(map(str.lower,flatten(self.words)))
        self.words = list(filter(lambda x:x not in self.spec_chars,self.words))
        
        
        #lemmatize the words and sort the words to be used in the vectorizer            
        self.words = list(map(lemmatizer.lemmatize,self.words))
        self.words = sorted(list(set(self.words)))
         
        # sort the classes to be used in the vectorizer            
        self.classes=sorted(list(set(self.classes)))
        

    def tokens(self,text):
        tokens = word_tokenize(text)
        return tokens
    
    
    def construct_training_data(self):
        
        #Construct the vectorizer
        cv = CountVectorizer(tokenizer=self.tokens,analyzer="word",stop_words=None)
        
        #Construct the training sets
        training=[]
        for doc in self.Data:
            #print(doc)
            # Convert patterns to lowercase and lemmatize them
            word_patterns = list(map(str.lower,doc[0]))
            word_patterns = ' '.join(list(map(lemmatizer.lemmatize,word_patterns)))
            

            # Fit the vectorizer to the list of word
            #Then vectorize the word patterns
            vectorize = cv.fit([' '.join(self.words)])
            word_vector = vectorize.transform([word_patterns]).toarray().tolist()[0]
            
            #Construct output structure
            output_row = [0]*len(self.classes)
            
            # Map a 1 in the index of the class
            output_row[self.classes.index(doc[1])]=1

            #Append the vector with its assigned class into the 
            #training data
            training.append([word_vector,output_row])

        #shuffle training
        random.shuffle(training)
        training= np.array(training,dtype=object)
        
        
        if len(training)>0:
            # Features
            self.train_X = list(training[:,0])
            # Targets
            self.train_y = list(training[:,1])
        else:
            self.train_X = []
            self.train_y = []

        

    def build_model(self):
        # Construct a Sequential model with 3 layers.
        if len(self.train_X) > 0 and len(self.train_y) == len(self.train_X):
            model=Sequential()
            
            #input layer with latent dimension of 128 neurons and ReLU activation function 
            model.add(Dense(128,input_shape=(len(self.train_X[0]),),activation='relu'))
            model.add(Dropout(0.5)) #Dropout to avoid overfitting
            
            #second layer with the latent dimension of 64 neurons
            model.add(Dense(64,activation='relu')) 
            model.add(Dropout(0.5))
            
            #fully connected output layer with softmax activation function
            model.add(Dense(len(self.train_y[0]),activation='softmax')) 
            
            # Using the adagrad optimizer
            ada = Adagrad(learning_rate=0.1, initial_accumulator_value=0.1, epsilon=1e-07)
            
            model.compile(loss='categorical_crossentropy',optimizer=ada,metrics=['accuracy'])
            
            hist=model.fit(np.array(self.train_X),np.array(self.train_y),epochs=200,batch_size=10,verbose=1)
            # save model 
            model.save('learned_model.h5',hist)
            # save words and classes
            pickle.dump({'words':self.words,'classes':self.classes,'train_x':self.train_X,'train_y':self.train_y},
                        open("training_data","wb"))

        else:
            print("NO TRAINING DATA AVAILABLE")




def main():
    T = initializeModel()
    T.process_data()
    T.construct_training_data()
    T.build_model()

if __name__ == '__main__':
    main()


