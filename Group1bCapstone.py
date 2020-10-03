import pysam
import tkinter as tk
from tkinter import *
# Looks for text and highlights it
def search(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword,pos,END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx,len(keyword))
        text_widget.tag_add(tag,idx,pos)

win = Tk()
win.title("BAM View")
#win.geometry("1000x750") # Size of window

frame1 = Frame(win)
frame1.pack(side = LEFT)
scrollbar = Scrollbar(frame1, orient='horizontal')
scrollbar.grid(row=1, column=0, sticky=N+S+E+W)

frame2 = Frame(win)
frame2.pack(side = RIGHT)
scrollbar2 = Scrollbar(frame2, orient='horizontal')
scrollbar2.grid(row=1, column=1, sticky=N+S+E+W)

samfile = pysam.AlignmentFile("ADAMC-PARK7.sam.sorted.bam", "rb")

for read in samfile:
    print("Query Name: " + str(read.query_name))
    print("Seq: " + str(read.seq))
    print("Length: " + str(read.query_length))
    # print("Cigar: " + str(read.cigar))
    print("Position: " + str(read.pos))
    print("Flag: " + str(read.flag))
    print("RName: " + str(read.rname))
    print("MapQ: " + str(read.mapq))
    print("RNext: " + str(read.rnext))
    print("PNext: " + str(read.pnext))
    print("Tlen: " + str(read.tlen))
    # print("Bin: " + str(read.query_qualities))
    # print("Tag: " + str(read.tags))

print("")

gene1 = [];
gene1Names = [];
gene1Length = [];
gene1Pos = [];
gene1Seq = [];

gene2 = [];
gene2Names = [];
gene2Length = [];
gene2Pos = [];
gene2Seq = [];

# Get the details of the samfile
results = samfile.fetch()
for read in results:
    if read.pos not in gene1Pos and len(gene1Pos) == 0:
        gene1Pos.append(read.pos)
        gene1Length.append(read.query_length)
    elif read.pos not in gene1Pos and read.pos not in gene2Pos:
        gene2Pos.append(read.pos)
        gene2Length.append(read.query_length)

    if read.pos in gene1Pos:
        gene1Names.append(read.query_name)
        gene1Seq.append(read.seq)
    elif read.pos in gene2Pos:
        gene2Names.append(read.query_name)
        gene2Seq.append(read.seq)


print("Position gene 1: " + str(gene1Pos))
print("Length gene 1: " + str(gene1Length))
for x in range(len(gene1Names)):
    print(gene1Names[x])
    print(gene1Seq[x])

print("")

print("Position gene 2: " + str(gene2Pos))
print("Length gene 2: " + str(gene2Length))
for x in range(len(gene2Names)):
    print(gene2Names[x])
    print(gene2Seq[x])

print("")

# Highlight the matching sections of each gene
if gene1Length[0] > gene2Length[0]:
    for x in range(len(gene1Seq)):
        if gene1Seq[x].endswith(gene2Seq[x]):
            print("Gene 2 matches ending of gene 1!")
        elif gene1Seq[x].startswith(gene2Seq[x]):
            print("Gene 2 matches start of gene 1!")
elif gene1Length[0] < gene2Length[0]:
    for x in range(len(gene2Seq)):
        if gene2Seq[x].endswith(gene1Seq[x]):
            print("Gene 1 matches ending of gene 2!")
        elif gene2Seq[x].startswith(gene1Seq[x]):
            print("Gene 1 matches start of gene 2!")

#w = tk.Label(frame1,text=gene1Seq[0])
#w.pack()

text = Text(frame1, width = 60, height = 40, wrap = NONE, xscrollcommand = scrollbar.set)
scrollbar.config(command=text.xview)
text.grid(row=0, column=0)
text.insert(END, gene1Seq[0])

text.tag_config(gene1Seq[0], background = 'red')
text.config(state = DISABLED)

text2 = Text(frame2, width = 60, height = 40, wrap = NONE, xscrollcommand = scrollbar2.set)
scrollbar2.config(command=text2.xview)
text2.grid(row=0, column=1)
text2.insert(INSERT, gene2Seq[0])

text2.tag_config(gene1Seq[0], background = 'red')
text2.config(state = DISABLED)

search(text,gene1Seq[0],gene1Seq[0])
search(text2,gene1Seq[0],gene1Seq[0])

win.mainloop()

samfile.close()
