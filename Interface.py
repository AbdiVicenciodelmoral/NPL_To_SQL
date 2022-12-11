from tkinter import *
from tkinter import ttk
import json
import processInput as inputProc
import Training as trainModel
import imdb


BG_GRAY="#ABB2B9"
BG_COLOR ="#1C1C1C"
Black_Grey_COLOR ="#1C1C1C"
TEXT_COLOR="#FFF"
FONT="Calibri 14 bold"
FONT_BOLD="Calibri 13 bold"


class ChatBot:
    def __init__(self):
        self.window = Tk()
        self.test = inputProc.Testing()
        data_file=open('query_trainer.json').read()
        self.training_queries = json.loads(data_file)
        self.main_window()

    def run(self):
        self.window.mainloop()
    
    def main_window(self):

        #Interface Window Parameters
        self.window.title("IMDB Database Interface")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=1000,height=1000,bg="#1C1C1C")
        self.window.resizable(True, True)
        
        """s = ttk.Style()
        s.configure('My.TFrame', background='red')

        mail1 = Frame(self.window, style='My.TFrame')
        self.tab = ttk.Notebook(self.window)
        # Initialize style
        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame', background='green')
        style.configure("TNotebook", highlightbackground="#848a98")
        # Create style for the first frame
        s.configure('Frame1.TFrame', background='red')
        # Use created style in this frame
        #tab1 = ttk.Frame(mainframe, style='Frame1.TFrame')
        #mainframe.add(tab1, text="Tab1")

        # Create separate style for the second frame
       # s.configure('Frame2.TFrame', background='blue')
        # Use created style in this frame
        #tab2 = ttk.Frame(mainframe, style='Frame2.TFrame')
        #mainframe.add(tab2, text="Tab2")"""

        
        mygreen = "#d2ffd2"
        myred = "#dd0202"

        style = ttk.Style()

        style.theme_create( "yummy", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
                "TNotebook.Tab": {
                    "configure": {"padding": [5, 1], "background": "#1C1C1C", "foreground": "white" },
                    "map":       {"background": [("selected", '#ED872D')],
                                 "foreground": [("selected", "#1C1C1C")],
                                "expand": [("selected", [1, 1, 1, 0])] } } } )

        style.theme_use("yummy")

        style.configure('Frame1.TFrame', background=Black_Grey_COLOR)

        self.tab = ttk.Notebook(self.window)
        self.tab.pack(expand=1,fill='both')
        self.interface_frame = ttk.Frame(self.tab,width=520,height=520, style='Frame1.TFrame')
        self.train_frame = ttk.Frame(self.tab,width=520,height=520,style='Frame1.TFrame')
        self.tab.add(self.interface_frame,text='Movie Database'.center(100))
        self.tab.add(self.train_frame,text='Train Model'.center(100))
        
        #Add Tabs
        self.database_interface()
        self.train_interface()
        
    def database_interface(self):
        #Heading
        head_label = Label(self.interface_frame,bg='#ED872D',fg="#1C1C1C",text="Enter a Query",font=FONT_BOLD,pady=10)
        head_label.place(relwidth=1)
        line = Label(self.interface_frame,width=450,bg="#1C1C1C")
        line.place(relwidth=1,rely=0.07,relheight=0.012)

        #Text Area 
        self.text_widget = Text(self.interface_frame,width=20,height=2,bg="#696969",fg="#000",font=FONT,padx=5,pady=5)
        self.text_widget.place(relheight=0.745,relwidth=1,rely=0.08)
        self.text_widget.configure(cursor="arrow",state=DISABLED)

        #Scrollbar
        s = ttk.Style()
        s.configure("My.Vertical.TScrollbar", gripcount=0, background="#464647",troughcolor='#252526', borderwidth=2,
bordercolor='#252526', lightcolor='#252526', darkcolor='#252526')
        scrollbar= ttk.Scrollbar(self.text_widget,  style="My.Vertical.TScrollbar")
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        #Bottom label 
        bottom_label = Label(self.interface_frame,bg="#1C1C1C",height=80)
        bottom_label.place(relwidth=1,rely=0.825)
        
        #Entry Box
        self.msg_entry = Entry(bottom_label,bg="#696969",fg="#000",font=FONT)
        self.msg_entry.place(relwidth=0.788,relheight=0.06,rely=0.008,relx=0.008)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self.on_enter)
        
        #Bottom button
        send_button=Button(bottom_label,text="Send",font=FONT_BOLD,width=8,bg='#00a17b',command=lambda: self.on_enter(None))   
        send_button.place(relx=0.80,rely=0.008,relheight=0.06,relwidth=0.20)

    def train_interface(self):
        #Heading
        head_label=Label(self.train_frame,bg='#ED872D',fg="#1C1C1C",text="Query Train",font=FONT_BOLD,pady=10)
        head_label.place(relwidth=1)

        #Pattern Label
        patternlabel = Label(self.train_frame,bg="#696969",fg="#000",text="Pattern",font=FONT)
        patternlabel.place(relwidth=0.2,rely=0.14,relx=0.008)
        self.pattern = Entry(self.train_frame,bg="#696969",fg="#000",font=FONT)
        self.pattern.place(relwidth=0.7,relheight=0.06,rely=0.14,relx=0.22)

        #Training Buttons
        k1 = 'select_full'
        q1 = self.training_queries[k1]
        pos = 0
        select_button = Button(self.train_frame,text=q1,
                                    font=FONT_BOLD,width=len(q1),bg="#00a17b"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k1,q1))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos+0.01,relheight=0.06,relwidth=0.70)

        k2 = 'select'
        q2 = self.training_queries[k2]
        pos2 = 1
        select_button = Button(self.train_frame,text=q2,
                                    font=FONT_BOLD,width=len(q2),bg="#00a17b"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k2,q2))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos2+0.01,relheight=0.06,relwidth=0.70)

        k3 = 'count'
        q3 = self.training_queries[k3]
        pos3 = 2
        select_button = Button(self.train_frame,text=q3,
                                    font=FONT_BOLD,width=len(q3),bg="#00a17b"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k3,q3))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos3+0.01,relheight=0.06,relwidth=0.70)


        k4 = 'sum'
        q4 = self.training_queries[k4]
        pos4 = 3
        select_button = Button(self.train_frame,text=q4,
                                    font=FONT_BOLD,width=len(q4),bg="#00a17b"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k4,q4))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos4+0.01,relheight=0.06,relwidth=0.70)

        k5 = 'avg'
        q5= self.training_queries[k5]
        pos5 = 4
        select_button = Button(self.train_frame,text=q5,
                                    font=FONT_BOLD,width=len(q5),bg="#00a17b"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k5,q5))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos5+0.01,relheight=0.06,relwidth=0.70)

        k6 = 'min'
        q6 = self.training_queries[k6]
        pos6 = 5
        select_button = Button(self.train_frame,text=q6,
                                    font=FONT_BOLD,width=len(q6),bg="#00a17b"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k6,q6))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos6+0.01,relheight=0.06,relwidth=0.70)


        k7 = 'max'
        q7 = self.training_queries[k7]
        pos7 = 6
        select_button = Button(self.train_frame,text=q7,
                                    font=FONT_BOLD,width=len(q7),bg="#00a17b"
                                    ,command=lambda: self.train_on_query(self.pattern.get(),k7,q7))   
        select_button.place(relx=0.20,rely=0.28+0.08*pos7+0.01,relheight=0.06,relwidth=0.70)

    
    def train_on_query(self,pattern,key,query):
        print("Training:",pattern,key,query)
        #read intent file and append created class,pattern and queries from train_interface function
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






