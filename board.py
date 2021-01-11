import tkinter as tk
#from TictacPlayer import *


class Application(tk.Tk):

    def __init__(self):
        
        tk.Tk.__init__(self)
        self.geometry('500x600')
        self._frame = None
        self.swap_frame(Home)

    def swap_frame(self, page_name):
        new_frame = page_name(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0)


class Home(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.welcome = tk.Label(
            text='Welcome to Ultimate Tic-Tac-Toe! \nPress the start button to begin playing against your AI opponent.')
        self.welcome.grid(row=0, column=1)
        tk.Button(text='Start!', command=lambda: master.swap_frame(Game)).grid(row=2,column=1)
        #self.start.grid(row=1, column=0)


class Game(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.ttp=TictacPlayer()
        frame=tk.Frame()
        newlabel = tk.Label(text='good luck!')
        newlabel.grid(row=0,column=0)
        x1 = 0
        y1 = 100
        for x in range(3):
            row = tk.Frame()
            for y in range(3):
                row = tk.Frame()
                row.grid(row=x, column=y)
                label=tk.Label(text=str(self.ttp.board[x][y].state),master=row)
                label.pack()
                
            #row.pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()