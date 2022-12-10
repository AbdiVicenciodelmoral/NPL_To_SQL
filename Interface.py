#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import ttk
import json
#import the training.py
#and testing.py file
import processInput as inputProc
import Training as trainModel
import imdb

# In[2]:


BG_GRAY="#ABB2B9"
BG_COLOR="#000"
TEXT_COLOR="#FFF"
FONT="Calibri 14"
FONT_BOLD="Calibri 13 bold"


# In[3]:


class ChatBot:
    def __init__(self):
        #initialize tkinter window
        self.window = Tk()
        self.test = inputProc.Testing()
        # read and load the trainer file which contains sql structure
        data_file=open('query_trainer.json').read()
        self.training_queries = json.loads(data_file)

        self.main_window()

        
        
    #run window
    def run(self):
        self.window.mainloop()
    
    def main_window(self):
        #add title to window and configure it
        self.window.title("ChatBot")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=520,height=520,bg=BG_COLOR)
        self.window.resizable(True, True)
        
        #add tab for Chatbot and Train Bot in Notebook frame
        self.tab = ttk.Notebook(self.window)
        self.tab.pack(expand=1,fill='both')
        self.bot_frame = ttk.Frame(self.tab,width=520,height=520)
        self.train_frame = ttk.Frame(self.tab,width=520,height=520)
        self.tab.add(self.bot_frame,text='Movie Database'.center(100))
        self.tab.add(self.train_frame,text='Train Model'.center(100))
        
        self.add_bot()
        self.add_train()
        
    def add_bot(self):
        #Add heading to the Chabot window
        head_label=Label(self.bot_frame,bg='#ADD8E6',fg=TEXT_COLOR,text="Enter a Query",font=FONT_BOLD,pady=10)
        head_label.place(relwidth=1)
        
        line = Label(self.bot_frame,width=450,bg='#ADD8E6')
        line.place(relwidth=1,rely=0.07,relheight=0.012)

        #create text widget where conversation will be displayed
        self.text_widget=Text(self.bot_frame,width=20,height=2,bg="#fff",fg="#000",font=FONT,padx=5,pady=5)
        self.text_widget.place(relheight=0.745,relwidth=1,rely=0.08)
        self.text_widget.configure(cursor="arrow",state=DISABLED)

        #create scrollbar
        scrollbar=Scrollbar(self.text_widget)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        #create bottom label where message widget will placed
        bottom_label=Label(self.bot_frame,bg='#ADD8E6',height=80)
        bottom_label.place(relwidth=1,rely=0.825)
        #this is for user to put query
        self.msg_entry=Entry(bottom_label,bg="#F5F5DC",fg="#000",font=FONT)
        self.msg_entry.place(relwidth=0.788,relheight=0.06,rely=0.008,relx=0.008)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self.on_enter)
        #send button which will call on_enter function to send the query
        send_button=Button(bottom_label,text="Send",font=FONT_BOLD,width=8,bg="#6ECFE4",command=lambda: self.on_enter(None))   
        send_button.place(relx=0.80,rely=0.008,relheight=0.06,relwidth=0.20)

    def add_train(self):
        head_label=Label(self.train_frame,bg=BG_COLOR,fg=TEXT_COLOR,text="Query Train",font=FONT_BOLD,pady=10)
        head_label.place(relwidth=1)

        #class Label and Entry for intents class. 
        """classlabel=Label(self.train_frame,fg="#000",text="Class",font=FONT)
        classlabel.place(relwidth=0.2,rely=0.14,relx=0.008)
        self.query_class=Entry(self.train_frame,bg="#fff",fg="#000",font=FONT)
        self.query_class.place(relwidth=0.7,relheight=0.06,rely=0.14,relx=0.22)"""

        #Pattern Label and Entry for pattern to our Class.
        
        
        patternlabel = Label(self.train_frame,fg="#000",text="Pattern",font=FONT)
        patternlabel.place(relwidth=0.2,rely=0.14,relx=0.008)
        self.pattern = Entry(self.train_frame,bg="#fff",fg="#000",font=FONT)
        self.pattern.place(relwidth=0.7,relheight=0.06,rely=0.14,relx=0.22)

        """#Query Label and Entry for query to the pattern.
        self.query=[]
        
        querylabel=Label(self.train_frame,fg="#000",text="Query",font=FONT)
        querylabel.place(relwidth=0.2,rely=0.50+0.08,relx=0.008)
        self.query = Entry(self.train_frame,bg="#fff",fg="#000",font=FONT)
        self.query.place(relwidth=0.7,relheight=0.06,rely=0.50+0.08,relx=0.22)"""


        select = self.training_queries['select']
        print(self.training_queries.keys())
        #to train our bot create Train Bot button which will call on_train function
        #select_label=Label(self.train_frame,fg="#000")
        #select_label.place(relwidth=1,rely=0.825)
        #select_button = Button(self.train_frame,text=select,font=FONT_BOLD,width=12,bg="Gray",command=lambda: self.train_on_query(None))
        #select_button.place(relx=0.20,rely=0.9,relheight=0.06,relwidth=0.60)



        #Pattern Label and Entry for pattern to our tag.
        """self.query_buttons = []
        for i in range(len(self.training_queries.keys())):
            pos = i+1
            key = list(self.training_queries.keys())
            print(key[i],self.training_queries[key[i]])

            k = key[i]
            q = self.training_queries[key[i]]"""
        
        k1 = 'select_full'
        q1 = self.training_queries[k1]
        pos = 0
        select_button = Button(self.train_frame,text=q1,
                                    font=FONT_BOLD,width=len(q1),bg="Gray"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k1,q1))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos+0.01,relheight=0.06,relwidth=0.70)

        k2 = 'select'
        q2 = self.training_queries[k2]
        pos2 = 1
        select_button = Button(self.train_frame,text=q2,
                                    font=FONT_BOLD,width=len(q2),bg="Gray"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k2,q2))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos2+0.01,relheight=0.06,relwidth=0.70)

        k3 = 'count'
        q3 = self.training_queries[k3]
        pos3 = 2
        select_button = Button(self.train_frame,text=q3,
                                    font=FONT_BOLD,width=len(q3),bg="Gray"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k3,q3))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos3+0.01,relheight=0.06,relwidth=0.70)


        k4 = 'sum'
        q4 = self.training_queries[k4]
        pos4 = 3
        select_button = Button(self.train_frame,text=q4,
                                    font=FONT_BOLD,width=len(q4),bg="Gray"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k4,q4))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos4+0.01,relheight=0.06,relwidth=0.70)

        k5 = 'avg'
        q5= self.training_queries[k5]
        pos5 = 4
        select_button = Button(self.train_frame,text=q5,
                                    font=FONT_BOLD,width=len(q5),bg="Gray"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k5,q5))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos5+0.01,relheight=0.06,relwidth=0.70)

        k6 = 'min'
        q6 = self.training_queries[k6]
        pos6 = 5
        select_button = Button(self.train_frame,text=q6,
                                    font=FONT_BOLD,width=len(q6),bg="Gray"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k6,q6))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos6+0.01,relheight=0.06,relwidth=0.70)


        k7 = 'max'
        q7 = self.training_queries[k7]
        pos7 = 6
        select_button = Button(self.train_frame,text=q7,
                                    font=FONT_BOLD,width=len(q7),bg="Gray"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k7,q7))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos7+0.01,relheight=0.06,relwidth=0.70)

            #self.query_buttons.append(select_button)
            #self.query_buttons[i].place(relx=0.20,rely=0.28+0.08*i+0.01,relheight=0.06,relwidth=0.70)
            
            #patternlabel=Label(self.train_frame,fg="#000",text="Pattern%d"%(i+1),font=FONT)
            #patternlabel.place(relwidth=0.2,rely=0.28+0.08*i,relx=0.008)
            #self.pattern.append(Entry(self.train_frame,bg="#fff",fg="#000",font=FONT))
            #self.pattern[i].place(relwidth=0.7,relheight=0.06,rely=0.28+0.08*i,relx=0.22)
        
        """#to train our bot create Train Bot button which will call on_train function
        bottom_label=Label(self.train_frame,bg=BG_GRAY,height=80)
        bottom_label.place(relwidth=1,rely=0.825)

        train_button=Button(bottom_label,text="Train Model",font=FONT_BOLD,width=12,bg="Gray",command=lambda: self.on_train(None))
        train_button.place(relx=0.20,rely=0.008,relheight=0.06,relwidth=0.60)"""
    
    def train_on_query(self,pattern,key,query):
        print("ERERERERRRRRRRRRRR",pattern,key,query)
        #read intent file and append created class,pattern and queries from add_train function
        with open('intents.json','r+') as json_file:
            file_data=json.load(json_file)
            

            if key in file_data:
                file_data[key]['patterns'].append(pattern)

            else:
                file_data[key] = {"patterns": [pattern],
                                  "query": [query]}
            json_file.seek(0)
            json.dump(file_data, json_file, indent = 1)
        
        
        
        self.pattern.delete(0, END)

        #run and retrain model.
        T = trainModel.initializeModel()
        T.process_data()
        T.construct_training_data()
        T.build_model()
        print("Trained Successfully")
        self.test = inputProc.Testing()


    def on_train(self,event):
        #read intent file and append created class,pattern and queries from add_train function
        print("IN ON TRAIN***********************************************")
        with open('intents.json','r+') as json_file:
            file_data=json.load(json_file)
            
            print(file_data,'\n',type(file_data))

            print(file_data.keys())
            
            print("Query Class:",self.query_class.get())
            if file_data[self.query_class.get()]:
                file_data[self.query_class.get()]['patterns'].append(self.pattern.get())

            else:
                file_data[self.query_class.get()] = {"patterns": [self.pattern.get()],
                                                 "query": [self.query.get()]}
            json_file.seek(0)
            json.dump(file_data, json_file, indent = 1)
        
        
        self.query_class.delete(0, END)
        self.pattern.delete(0, END)
        self.query.delete(0, END)

        #run and retrain model.
        T = trainModel.initializeModel()
        T.f_data()
        T.construct_training_data()
        T.build_model()
        print("Trained Successfully")
        self.test = inputProc.Testing()

        
    def on_enter(self,event):
        user_input = self.msg_entry.get()
        self.user_input(user_input,"Input")
        self.interface_query(user_input,"Query")
        
    def interface_query(self,user_input,sender):
        self.text_widget.configure(state=NORMAL)
        #get the query for the user's query from testing.py file
        q = self.test.Query(user_input)
        
        if q == None:
            self.text_widget.insert(END, "No query formed. Please rephrase query or Train Model" +"\n\n")
            self.text_widget.configure(state=DISABLED)
            self.text_widget.see(END)

        else:
            print("THE QUERY IS: ",q)
            sql = imdb.IMDB_Connect(q)
            sql.connect()
            self.text_widget.insert(END,"Query: " + q +"\n\n")
            for i in sql.rows:
                print(i)
                self.text_widget.insert(END, i +"\n")
            self.text_widget.configure(state=DISABLED)
            self.text_widget.see(END)
    
    def user_input(self,inputQuery,sender):
        if not inputQuery:
            return
        self.msg_entry.delete(0,END)
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END,str(sender)+" : " + str(inputQuery)+"\n\n")
        self.text_widget.configure(state=DISABLED)
        


def main():
    bot = ChatBot()
    bot.run()


# run the file
if __name__=="__main__":
    main()






