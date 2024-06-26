from tkinter import *
import tkinter.messagebox
import re

import webbrowser

# from chat import get_response

from bot import getresponse,get_predicted_value , get_disease_predictions

from tkinter.simpledialog import askstring


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self.outputs = []
        self.days = 0
        self._get_name()

        
    def run(self):
        self.window.mainloop()
    
    def giveanswer(self,dises,ans):
        self.text_widget.tag_config('blue', foreground="#FDD20E")
        self.msg_entry.delete(0, END)
        sender = self.name_entry.get().split(" ")[0]
        msg1 = f"{sender} : "
        msg2 = f"{dises} -> {ans} \n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1.capitalize(), 'blue')
        self.text_widget.insert(END, msg2.capitalize())
        self.text_widget.configure(state=DISABLED)

    # ask for how many days 
    def _suffering_days(self):
        no_of_days = askstring(f"Please respond only in days [1,2,3 ....]", f"You suffering from how many days ? ")
        if no_of_days is None:
            self.msg_warning(f"Wrong Input ","Please respond only in [1,2,3,....] format.Do not cancel because it's important.")
            self._suffering_days()
        elif no_of_days.isnumeric() is True and int(no_of_days) > 0:
            self.giveanswer("You suffering from how many days ? ",no_of_days)
            # print(type(no_of_days))
            self.days += int(no_of_days)
        else:
            self.msg_warning(f"Wrong Input ","Please respond only in [1,2,3,....] format.Do not cancel because it's important.")
            self._suffering_days()


    # ask question to the user 
    def ask_box(self,desid):
        prompt = askstring(f"Please respond only with (Yes/No)", f"Are you suffering from a ' {desid} ' ? ")
        if prompt == None:
            self.msg_warning(f"{desid} Wrong Input ","Please respond only in (yes/no) format.Do not cancel because it's important.")
            self.ask_box(desid)
        elif prompt.lower() == "no" or prompt.lower() == "yes":
            self.giveanswer(desid,prompt)
            if prompt.lower() == "yes" :
                self.outputs.append(desid)
        else:
            self.msg_warning(f"{desid} Wrong Input ","Please give the answer only in (yes/no)")
            self.ask_box(desid)
        



    def _get_name(self):
        self.window.title("Welcome to Health Care Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=500, height=500, bg=BG_COLOR)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, y=0, relheight=0.002)


        self.name = Label(self.window, bg="RED", fg=TEXT_COLOR,
                           text="Please Enter Your name", font=FONT_BOLD, pady=10)
        self.name.place(relwidth=1,y=57.3)

        # entry label
        name_name_label = Label(self.window, bg=BG_COLOR, height=80)
        name_name_label.place(relheight=0.09, relwidth=1,y=105.9)

        # message entry box 
        self.name_entry = Entry(name_name_label, bg=BG_GRAY, fg="BLACK", font=FONT_BOLD)
        self.name_entry.place(relheight=0.85,relwidth=0.74, x=65)
        self.name_entry.focus()
        self.name_entry.bind("<Return>", self.get_name_after_click)

        #button lable
        name_box_label = Label(self.window, bg=BG_COLOR, height=80)
        name_box_label.place(relheight=0.09, relwidth=1,y=150.9)

        # # send button
        name_send_button = Button(name_box_label, text="Submit", fg=TEXT_COLOR, font=FONT_BOLD, width=20, bg="RED",
                             command=lambda: self.get_name_after_click(None))
        name_send_button.place(relheight=1,relwidth=0.24, x=190)

    

        # menu button 
        menu = Menu(self.window,bg=BG_COLOR,borderwidth=0,fg=TEXT_COLOR,font="bold")
        self.window.config(menu=menu, bd=5)


        # File menu 
        File = Menu(menu, tearoff=0,font="bold",activebackground="#FFFFFF")
        menu.add_cascade(label="File", menu=File,font="bold")
        File.add_command(label="Clear Chat",command=self.clear_chat,font="bold")
        File.add_command(label="Exit",command=None,font="bold")

        # About menu 
        about = Menu(menu, tearoff=0,font="bold",activebackground="#FFFFFF")
        menu.add_cascade(label="About", menu=about,font="bold")

        about.add_command(label="Develpoers", command=lambda: self.msg_showinfo(f"Bot Develpoers ",f"Project Lead - A.LakshmiReddy \n\n Group Members \n\n 1. B.Venkata Lakshmi (O180024) \n 2.R.Yogeeswari (O180077) \n 3.N.Preveena (O180074) \n"),font="bold")
        about.add_command(label="About Bot", command=lambda: self.msg_showinfo(f"Bot V1.0.0 ",f" \tAbout Bot \n\n This is a bot which is used to predict similar diseases using a machine learning model and give the diseases information and their prevention."))

        # Quit menu 
        menu.add_command(label ='Quit!',font="bold", command=lambda: self.msg_msg_askcancle(f"Ok Quit "," Are You sure? "))



    # check the name must be written 
    def get_name_after_click(self,name):
        # print(len(self.name_entry.get()))
        if len(self.name_entry.get()) >= 2:
            self._setup_main_window()
            self.coming_msg()
        else:
            self.msg_warning("Message Regarding Name Error","Please enter at least two words of a name.")
            



    # Main Window 
    def _setup_main_window(self):
        self.window.title("Welcome to Health Care Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=1200, height=640, bg=BG_COLOR)

        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, y=0, relheight=0.012)
        
        

        # left side label 
        leftside_label = Label(self.window, bg=BG_COLOR, height=80,border=1)
        leftside_label.place(relheight=1, relwidth=0.2519,y=3 )

        
        # sidebox name lable
        self.name = Label(leftside_label, bg=BG_COLOR, fg=TEXT_COLOR,
                           text=self.name_entry.get().capitalize(), font=FONT_BOLD, pady=10)
        self.name.place(relheight=0.07, relwidth=1,y=1)

        # sidebox Help box
        self.help = Label(leftside_label, bg="red", fg=TEXT_COLOR,
                           text="Help Search (Similar diseases)", font=FONT_BOLD, pady=10)
        self.help.place(relheight=0.07, relwidth=1,y=48)


        # seach label
        search_label = Label(leftside_label, bg=TEXT_COLOR, height=80)
        search_label.place(relheight=0.07, relwidth=1,y=94)

        # message entry box 
        self.help_entry = Entry(search_label, bg=BG_GRAY, fg="BLACK", font=FONT_BOLD)
        self.help_entry.place(relheight=0.85,relwidth=0.74, y=2.4)
        self.help_entry.focus()
        self.help_entry.bind("<Return>", self._on_enter_help_search)
        
        # send button
        help_send_button = Button(search_label, text="Search", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_help_search(None))
        help_send_button.place(relheight=0.85,relwidth=0.24,y=2.4, x=224)

        #Searchbox
        self.search = Text(leftside_label, width=20, height=2, bg="#00003d", fg=TEXT_COLOR,
                                font=FONT, padx=8, pady=8)
        self.search.place(relheight=.779, relwidth=1,y=140)
        self.search.configure(cursor="arrow", state=DISABLED)
        # scroll bar for search
        scrollsearch = Scrollbar(self.search)
        scrollsearch.place(relheight=1, relx=0.97)
        scrollsearch.configure(command=self.search.yview)

        # righ sider lebel

        rightside_label = Label(self.window, bg=BG_COLOR, height=80,border=1)
        rightside_label.place(relheight=1, relwidth=0.75,y=3 ,x=300)


        # text widget
        self.text_widget = Text(rightside_label, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        # self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.place(relheight=0.893, relwidth=1,y=0 ,x=0)

        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.99)
        scrollbar.configure(command=self.text_widget.yview)

        
        # bottom label
        bottom_label = Label(rightside_label, bg="#17202A", height=80)
        bottom_label.place(relwidth=1,relheight=.1,x=1, y=563.7 )
        
        # message entry box #2C3E50
        self.msg_entry = Entry(bottom_label, bg="#1161A8", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relheight=0.85,relwidth=0.82,x=5, y=4)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relheight=0.85, relwidth=0.15,x=745,y=4)

    # get help search Diesies
    def _on_enter_help_search(self,event):
        dis_list = ['itching', 'skin rash', 'nodal skin eruptions', 'continuous sneezing', 'shivering', 'chills', 'joint pain', 'stomach pain', 'acidity', 'ulcers on tongue', 'muscle wasting', 'vomiting', 'burning micturition', 'spotting urination', 'fatigue', 'weight gain', 'anxiety', 'cold hands and feets', 'mood swings', 'weight loss', 'restlessness', 'lethargy', 'patches in throat', 'irregular sugar level', 'cough', 'high fever', 'sunken eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish skin', 'dark urine', 'nausea', 'loss of appetite', 'pain behind the eyes', 'back pain', 'constipation', 'abdominal pain', 'diarrhoea', 'mild fever', 'yellow urine', 'yellowing of eyes', 'acute liver failure', 'fluid overload', 'swelling of stomach', 'swelled lymph nodes', 'malaise', 'blurred and distorted vision', 'phlegm', 'throat irritation', 'redness of eyes', 'sinus pressure', 'runny nose', 'congestion', 'chest pain', 'weakness in limbs', 'fast heart rate', 'pain during bowel movements', 'pain in anal region', 'bloody stool', 'irritation in anus', 'neck pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen legs', 'swollen blood vessels', 'puffy face and eyes', 'enlarged thyroid', 'brittle nails', 'swollen extremeties', 'excessive hunger', 'extra marital contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
        inp = self.help_entry.get()
        pred_list=[]
        if len(inp) > 0:
            regexp = re.compile(inp)
            for item in dis_list:
                if regexp.search(item):
                    pred_list.append(item)
        self.help_entry.delete(0, END)
        if len(pred_list) > 0:
            msg1 = ""
            for i in range(len(pred_list)):
                msg1 += f"{i+1})  {pred_list[i]} \n"
        else:
            msg1 = "Ohh!! There were no similar diseases discovered."
        self.search.configure(state=NORMAL)
        self.search.delete("1.0",END)
        self.search.insert(END, msg1)
        self.search.configure(state=DISABLED)

    def coming_msg(self):

        self.text_widget.tag_config('red', foreground="red")
        good_name  = self.name_entry.get().split(" ")[0]
        msg2 = f"Hey! {good_name} , Are you not feeling well? Please tell me what symptoms you are suffering from here are some examples:\n --> fever\n --> cold\n --> cough\n --> headache\n --> stomach_pain\n --> abdominal_pain\n --> dehydration\n --> swelling\n --> acidity\n --> internal_itching\n --> sneezing\n --> vomiting\n --> anxiety , etc \n Note: Please use underscore (  _  ) in place of spacing in the name of disease.\n\n"
        msg1 = f"bot : "
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1.capitalize(),"red")
        self.text_widget.insert(END, msg2.capitalize())
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg)
        
    def _insert_message(self, msg):
        if not msg:
            return

        # delete the entery whtich is in entry box 
        self.msg_entry.delete(0, END)

        # sender msg or user msg 
        sender = self.name_entry.get().split(" ")[0]
        msg1 = f"{sender} : "
        msg2 = f"{msg}\n"

        self._user_instet_msg(msg1,msg2)

        quit_msg = ["quit","exit","bye","bye bye"]        
        if len([i for i in quit_msg if i == msg.lower()]) == 1:
            self.msg_msg_askcancle(f"Ok Quit "," Are You sure? ")
        
        # get msg form response from bot 
        else:
            chat_hear = getresponse(msg)

            if len(chat_hear) == 1 :
                msg4 = f"{chat_hear[0]} \n\n"
                self._bot_insert(msg4)

            elif len(chat_hear) > 1 :
                msg4 = f"{chat_hear[0]} \n \t Please give input on the diseases. \n\n"
                self._bot_insert(msg4)

                self.days *= 0
                self._suffering_days()

                self.outputs.clear()
                for i in chat_hear[1]:
                    self.ask_box(i)

                msg4 = f"You may also have diseases like \n"
                if len(self.outputs) > 0 :
                    # print(self.outputs)
                    for i in range(len(self.outputs)):
                        msg4 += f"\t {i+1} ) : {self.outputs[i]}\n"
                    msg4 += f"\n"
                else:
                    # print(self.outputs)
                    msg4 += f"\t 1 ) : {chat_hear[0]}\n\n"

                self._bot_insert(msg4)
                # print(self.outputs)

                # no of days 
                if self.days > 10:
                    self._bot_insert("Reach to the nearest hospital and take this medicines \n")

                # get answer 
                final_dieses = get_predicted_value(self.outputs)
                try:
                    diesese_is =  get_disease_predictions(final_dieses)
                except:
                    diesese_is = f"Sorry no diese get {final_dieses}"
                self._bot_insert(diesese_is)

                # open webbrowser
                if self.days > 1:
                    ask_to_web = tkinter.messagebox.askokcancel("Permition to open Google Map", "Do you want to open Google Map in Your Default Browser \n ")
                    if ask_to_web is True:
                        webbrowser.open_new_tab('https://www.google.com/maps/search/hospital+near+me/')
                        self._bot_insert("\n opening Google Map \n")
            else:
                pass
            # print(final_dieses)
            # self.msg_showinfo("predict_des",chat_hear[1])
    # clear chat
    # 

    def clear_chat(self):
        self.text_widget.config(state=NORMAL)
        self.text_widget.delete(1.0, END)
        self.text_widget.delete(1.0, END)
        self.text_widget.config(state=DISABLED)

    def _user_instet_msg(self,usr,msg):
        self.text_widget.tag_config('blue', foreground="#FDD20E")
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, usr.capitalize(), 'blue')
        self.text_widget.insert(END, msg.capitalize())
        self.text_widget.configure(state=DISABLED)

    def _bot_insert(self,msg):
        self.text_widget.tag_config('red', foreground="#F93822")
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, "Bot : ","red")
        self.text_widget.insert(END, msg)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        
    def msg_showinfo(self,title,msg):
        tkinter.messagebox.showinfo(title,msg)
    def msg_warning(self,title,msg):
        tkinter.messagebox.showwarning(title,msg)
    def msg_msg_askcancle(self,title,msg):
        msg_data = tkinter.messagebox.askokcancel(title, msg)
        if msg_data == True:
            self.window.destroy()
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()
