import tkinter as tk
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
style.use('ggplot')
import pandas as pd
import numpy as np
from esp32wifitest import *

class tkinterApp(tk.Tk):
     
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Spike counter')
        container = tk.Frame(self) 
        container.pack()

        self.frames = {} 
  
        for F in (LoginPage, Page1):
  
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(LoginPage)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

  
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, height=512, width=1024, bg="#263D42")
        canvas.place(x=0,y=0)
        canvas.create_text(500, 50, text="Login Page", fill="white", font=('Helvetica 40 bold'))

        self.userName = tk.StringVar()
        global userName1
        userName1 = str(self.userName)
        userNameBox = tk.Entry(self, textvariable=self.userName)
        userNameBox.place(x=400, y=100)

        newUser = tk.Button(self, text="Create User", padx=10, pady=5, fg="black", bg="#263D42",
        command = lambda : controller.show_frame(Page1))
        newUser.place(x=425, y=150)

        userName = tk.StringVar()
        userNameBox = tk.Entry(self, textvariable=userName)
        userNameBox.place(x=400, y=250)

        newUser = tk.Button(self, text="Login", padx=10, pady=5, fg="black", bg="#263D42",
        command = lambda : controller.show_frame(Page1))
        newUser.place(x=450, y=300)

class Page1(tk.Frame):
    
    def __init__(self, parent, controller):
        global userName1
        global esp32;

        esp32 = esp32() ## loaded from esp32wifitest

        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, height=512, width=1024, bg="#263D42")
        canvas.grid(row = 0, column = 0, padx = 10, pady = 10)
        canvas.create_text(520, 100, text="Spike Count", fill="white", font=('Helvetica 60 bold'))

        self.str1 = tk.StringVar()
        self.counter = tk.Label(self, textvariable=self.str1, bg="#263D42", fg="white", font=('Helvetica 180'))
        self.counter.place(relx=0.45, rely=0.3)

        self.userLabel = tk.Label(self, text="User: ", bg="#263D42", fg="white", font=('Helvetica 40'))
        self.userLabel.place(relx=0.4, rely=0.04)

        self.userLabel = tk.Label(self, textvariable=userName1, bg="#263D42", fg="white", font=('Helvetica 40'))
        self.userLabel.place(relx=0.5, rely=0.04)

        start_button = tk.Button(self, text="Start", padx=10, pady=5, fg="black", bg="#263D42",
                          command = self.readCount)
        start_button.place(relx = 0.25, rely=0.8)

        end_button = tk.Button(self, text="Pause", padx=10, pady=5, fg="black", bg="#263D42",
                          command=self.endCounter)
        end_button.place(relx=0.45, rely=0.8)

        reset_button = tk.Button(self, text="Reset", padx=10, pady=5, fg="black", bg="#263D42",
                               command = self.restart)
        reset_button.place(relx=0.65, rely=0.8)

        self.f = Figure(figsize=(5, 4), dpi=100)
        self.a = self.f.add_subplot(1,1,1)
        self.plot = FigureCanvasTkAgg(self.f)

    def animate(self):
        global ax
        global ay
        global az

        self.a.clear()
        self.a.plot(np.arange(0, 25, 1), ax, label='aX') # used to be 50
        self.a.plot(np.arange(0, 25, 1), ay, label='aY')
        self.a.plot(np.arange(0, 25, 1), az, label='aZ')
        self.a.legend(loc='upper right')

    def spikeCount(self):
        global spikeName
        global count
        global spikes
        global fileHeight
        global ax
        global ay
        global az

        if count > 9: # Need to change for the real run
            exit(1)
        file = pd.read_csv("Data/live_data.csv", header=None)
        file1 = file.iloc[:, 0:76] # 151 -> 76
        fileHeight_curr = file.shape[0]
        if fileHeight == fileHeight_curr:
            return spikes, ax, ay, az
        if fileHeight < fileHeight_curr:
            ax = file1.iloc[count, 1::3]
            ay = file1.iloc[count, 2::3]
            az = file1.iloc[count, 3::3]

            label = file.iloc[count, 76] # 151-> 76

            if (label == spikeName):
                spikes += 1
            count += 1
            # fileHeight = fileHeight_curr
            # print(ax)
            return spikes, ax, ay, az

    def readCount(self):
        global readInterval
        global spikes
        global ax
        global ay
        global az

        esp32.run();

        spikes, ax, ay, az = self.spikeCount()
        self.animate()
        self.plot.draw()
        self.plot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.str1.set(spikes)
      
        #if stopCounter:
        #    print ("counter stopped")
        #    return

        self.counter.after(readInterval*1000, self.readCount)

    def endCounter(self):
        global stopCounter
        stopCounter = True

    def restart(self):
        global stopCounter
        global spikes
        global count
        stopCounter = False
        spikes = 0
        count = 0
        self.a.clear()
        self.plot.draw()
        self.counter.destroy()
        self.str1 = tk.StringVar()
        self.counter = tk.Label(self, textvariable=self.str1, bg="#263D42", fg="white", font=('Helvetica 180'))
        self.counter.place(relx=0.4, rely=0.3)
        esp32 = esp32()

if __name__ == "__main__":
    stopCounter = False
    spikes = 0
    count = 0 # line counter
    spikeName = 'shake'
    readInterval = 3 # read csv every 1 second
    fileHeight = 0
    userName1 = ''

    ax = []
    ay = []
    az = []

    app = tkinterApp()
    app.mainloop()