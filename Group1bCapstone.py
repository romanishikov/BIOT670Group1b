#######################################################
#############BIOT 670 Capstone Group 1b################
#######################################################


#################Creation of the GUI###################
#import GUI library
import tkinter as tk
import pysam
#Create instance
win = tk.Tk()
#Create title
win.title("Python GUI")
#Start GUI
win.mainloop()

samfile = pysam.AlignmentFile("ombined.sam.bam", "rb")
