from lib import knotGUI as gui
import tkinter as tk

print("")
print("Knot Transcription Application")
print("© 2020, Sam Wolk and Violet Dennison")
print("--------------------------------------")
print('loading GUI...')

root = tk.Tk()
gui = gui.KnotGUI(root,800,800)
root.state('zoomed')
root.mainloop()

print('closed GUI... goodbye!')
print("--------------------------------------")
