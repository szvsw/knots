from lib import knotGUI as gui
import tkinter as tk

print("")
print("Knot Transcription Application")
print("© 2020, Sam Wolk and Violet Dennison")
print("--------------------------------------")
print('loading GUI...')

root = tk.Tk()
gui = gui.KnotGUI(root,450,800)
root.mainloop()

print('closed GUI... goodbye!')
print("--------------------------------------")
