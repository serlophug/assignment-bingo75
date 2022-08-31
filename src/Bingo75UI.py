
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
import threading

class Bingo75UI (threading.Thread):
    
    BingoMaster = None
    root = None
    N_players = None
    view1_mainFrame = None
    view1_entry_createBingoCards= None
    view1_label_createBingoCards_error = None

    view2_mainFrame= None
    view2_label_lastNumber = None
    view2_grid_oldNumbers = None
    #view2_label_oldNumbers_firstTime = True
    view2_prev_number=None
    view2_button_view2_distribute = None
    view2_button_view2_start = None

    aux = 0
    def __init__(self, N_players, BingoMaster):
        self.BingoMaster = BingoMaster
        self.N_players = N_players
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):   
        self.root = Tk()        
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        #icon = PhotoImage(file = 'src/images/bingo-icon.png')

        self.root.title('MPI Bingo')

        #self.root.iconphoto(False, icon)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        #self.root.geometry("1360x768")

        self.setup_view1()

        self.root.mainloop()
       

    def setup_view1(self):
        self.view1_mainFrame = Frame( self.root )
        self.view1_mainFrame.grid()
        #label_tittle = Label(self.view1_mainFrame, text="MPI BINGO App - Start page")
        #label_tittle.grid(row=0, column=0, columnspan=3)

        top_center = Frame(self.view1_mainFrame, width=200, height=200)
        top_center.grid(row=1, column=0, columnspan=3)   
        canvas_for_image = Canvas(top_center, height=200, width=200, borderwidth=0, highlightthickness=0) 
        canvas_for_image.grid(row=0, column=0, sticky='nesw', padx=0, pady=0)
        image = Image.open('src/images/bingo-icon.png')
        canvas_for_image.image = ImageTk.PhotoImage(image.resize((200, 200), Image.ANTIALIAS))
        canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')

        #label_createBingoCards = Label(self.view1_mainFrame, text="Number of Bingo Cards (one for each MPI workers)")
        #self.view1_entry_createBingoCards = Entry(self.view1_mainFrame)
        #self.view1_entry_createBingoCards.insert(0, "0")
        #self.view1_label_createBingoCards_error = Label(self.view1_mainFrame, text="")
        #label_createBingoCards.grid(column=0, row=1)   
        #self.view1_entry_createBingoCards.grid(column=1, row=1)   
        #self.view1_label_createBingoCards_error.grid(column=1, row=2)   

        #label_winning_condition = Label(self.view1_mainFrame, text="Select the winning condition:")
        #label_winning_condition.grid(row=1, column=0) 
        #self.view1_combobox_winner_condition = ttk.ComboBox(self.view1_mainFrame, values=self.winner_condition_choices)
        #self.view1_combobox_winner_condition.grid(row=1, column=0,columnspan=2) 
        
        button_createBingoCards=Button(self.view1_mainFrame, text="Create Bingo Cards", command=self.ui_view1_button_addBingoCards)
        button_createBingoCards.grid(column=0, row=3, sticky="NSWE", columnspan=3)

    def ui_view1_button_addBingoCards(self):
        '''self.view1_label_createBingoCards_error.config(text = "")
        if not self.view1_entry_createBingoCards.get().isdigit():
            print("boton pulsado con valor %s" % self.view1_entry_createBingoCards.get()) 
            self.view1_label_createBingoCards_error.config(fg="red")
            self.view1_label_createBingoCards_error.config(text="You should introduce an integer value")
        else:
            self.setup_view2()
        '''
        self.BingoMaster.ui_user_trigger_bingoCards_generation()
        self.setup_view2()
    
    def setup_view2(self):
        MIDDLE_HEIGHT = 200
        self.view1_mainFrame.destroy()
        self.view2_mainFrame = Frame( self.root )
        self.view2_mainFrame.grid()
        #label_tittle = Label(self.view2_mainFrame, text="MPI BINGO App - Start playing")
        #label_tittle.grid(row=0, column=0, columnspan=3)
        
        top = Frame(self.view2_mainFrame)
        top.grid(row=0, column=1, columnspan=2)

        self.view2_button_view2_distribute=Button(top, text="Distribute the BingoCards to players", command=self.ui_view2_distribute)
        self.view2_button_view2_distribute.grid(row=0, column=0, sticky="NSWE")
        self.view2_button_view2_start=Button(top, text="Start the Bingo Game", command=self.ui_view2_start, state = DISABLED)
        self.view2_button_view2_start.grid(row=0, column=1, sticky="NSWE")

        middle_left = Frame(self.view2_mainFrame, width=200, height=MIDDLE_HEIGHT)
        middle_left.grid(row=0, column=0)   
        canvas_for_image = Canvas(middle_left, height=MIDDLE_HEIGHT, width=200, borderwidth=0, highlightthickness=0) 
        canvas_for_image.grid(row=0, column=0, sticky='nesw', padx=0, pady=0)
        image = Image.open('src/images/bingo-icon.png')
        canvas_for_image.image = ImageTk.PhotoImage(image.resize((200, MIDDLE_HEIGHT), Image.ANTIALIAS))
        canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')

        '''
        DEBUG
        button_createaddNumber=Button(middle_left, text="Take one number", command=self.ui_view2_button_addNumber)
        button_createaddNumber.grid(column=0, row=1, sticky="NSWE")

        '''     


        label_lastNumber_tittle  = Label(self.view2_mainFrame, text="Current number", font=("Arial", 15))
        self.view2_label_lastNumber = Label(self.view2_mainFrame, text="-", font=("Arial", 60), width=15)
        label_lastNumber_tittle.grid(row=1, column=1)
        self.view2_label_lastNumber.grid(row=2, column=1)

        frame_olderNumbers = Frame(self.view2_mainFrame, width=200)
        frame_olderNumbers.grid(row=2, column=2, rowspan=2)  
        self.view2_grid_oldNumbers = []
        for i in range(15):
            self.view2_grid_oldNumbers.append([None, None, None, None, None])

        start = 1
        
        for j in range (5):
            for i in range(15):
                self.view2_grid_oldNumbers[i][j] = Label(frame_olderNumbers, text=str( start + i ), font=("Arial", 15), fg="gray")
                self.view2_grid_oldNumbers[i][j].grid(row=i, column=j)
            start += 15

        label_olderNumbers_tittle  = Label(self.view2_mainFrame, text="Older numbers", font=("Arial", 15))
        label_olderNumbers_tittle.grid(row=1, column=2)

        max_players_per_row = 8
        frame_players = Frame(self.view2_mainFrame, width=200)
        frame_players.grid(row=3, column=0, columnspan=3) 
        label_players_tittle = Label(frame_players, text="Players", font=("Arial", 25))
        label_players_tittle.grid(row=0, column=0, columnspan=max_players_per_row)

        person_icon = Image.open('src/images/person.jpg')
        
        i = 1
        j = 0
        for p in range(self.N_players):
            if j >= max_players_per_row:
                j = 0
                i += 2
            canvas_for_image = Canvas(frame_players, height=50, width=50, borderwidth=0, highlightthickness=0) 
            canvas_for_image.grid(row=i, column=j, sticky='nesw', padx=0, pady=0)  
            canvas_for_image.image = ImageTk.PhotoImage(person_icon.resize((50, 50), Image.ANTIALIAS))
            canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')
            Label(frame_players, text="Player %s"%(str(p+1)), font=("Arial", 15)).grid(row=i+1, column=j)
            j += 1

        self.view2_label_state = Label(self.view2_mainFrame, text="", font=("Arial", 20), fg="red")
        self.view2_label_state.grid(row=5, column=0, columnspan=3)


        #self.view2_label_oldNumbers = Label(self.view2_mainFrame, font=("Arial", 25), width=20, text="-")

        #Label()
        
        #self.view2_label_oldNumbers.grid(row=1, column=2)

        #self.view2_mainFrame.tkraise()

    def ui_view2_start(self):
        self.view2_button_view2_start['state'] = DISABLED
        self.BingoMaster.ui_user_trigger_start()
        self.view2_label_state.config(text ="MPI master is taking the numbers from the rotating drum.")

    def ui_view2_distribute(self):
        self.view2_button_view2_distribute['state'] = DISABLED
        self.view2_button_view2_start['state'] = NORMAL
        self.view2_label_state.config(text ="Distribution of the bingo cards by MPI master to the players (MPI workers) done")
        self.BingoMaster.ui_user_trigger_bingoCard_distribution()

    def ui_view2_updateNewNumber(self, new_number):
        if self.view2_prev_number:
            col = int((int(self.view2_prev_number) / 15))
            row = (int(self.view2_prev_number) % 15)-1 
            if row < 0:
                row = 14
                col -= 1
            self.view2_grid_oldNumbers[row][col].config(bg="blue")

        self.view2_prev_number=new_number
        self.view2_label_lastNumber.config(text=new_number)

        col = int((int(new_number) / 15))
        row = (int(new_number) % 15)-1
        if row < 0:
            row = 14
            col -= 1
        self.view2_grid_oldNumbers[row][col].config(bg="orange")
        self.view2_grid_oldNumbers[row][col].config(fg="white")

    def ui_view2_updateWinner(self, winner, card=None):
        
        t = "The winner is Player " + str(winner)   
        self.view2_label_state.config(text=t)

         
        if card:
            card = card[0:12] + card[13:]
            for n in card:
                col = int((int(n) / 15))
                row = (int(n) % 15)-1
                if row < 0:
                    row = 14
                    col -= 1
                self.view2_grid_oldNumbers[row][col].config(bg="red")

    def ui_view2_button_addNumber(self):
        new_number = "{:^3s}".format( str(random.randint(1, 75)) )
        self.ui_view2_updateNewNumber(new_number)
        self.aux += 1
        if self.aux>10:
            self.ui_view2_updateWinner("ANTONIO", card=True)

        


