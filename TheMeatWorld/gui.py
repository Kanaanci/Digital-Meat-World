import tkinter as tk
import threading
import logging
import os

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.startBot = tk.Button(self, text="Start", command=self.runBot())
		self.startBot.pack(side="top")

		self.quit = tk.Button(self, text="Quit", bg="blue", command=self.master.destroy)
		self.quit.pack(side="bottom")

	def runBot(self):
		os.system("python3 TheMeatWorld.py -n 20 -i 120 --handles @SadSocrates @philosophytweet @existentialcoms")

root = tk.Tk()
root.title("Twitter Bot")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("550x250+%d+%d" % (screen_width/2-275, screen_height/2-125))
root.lift()


app = Application(master=root)
app.mainloop()

#https://stackoverflow.com/questions/1198262/tkinter-locks-python-when-an-icon-is-loaded-and-tk-mainloop-is-in-a-thread
#https://py2app.readthedocs.io/en/latest/implementation.html#run-build-command