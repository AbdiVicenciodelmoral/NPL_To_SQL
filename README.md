# CS580_Database_Project
 NLP to SQL using Deep Learning
 
 Create a working directory
Save files to directory

Create Envronment
    Create Environment: python3-mvenv database_proj
    
    Activate envrinment: database_proj\Scripts\activate

Install Libraries:
    pip install nltk
    pip install numpy
    pip install -U scikit-learn
    pip install tensorflow
    pip install -U spacy
    pip install textacy
    pip install gensim
    ** You may need to install other ones as well but start with these**

Run this command in terminal to download corpus:
    python -m spacy download en_core_web_lg
    
    
You should now be able to run the program:
    python Interface.py
    
There will be no initial model, you will need to train the model, by clicking on the train model tab
