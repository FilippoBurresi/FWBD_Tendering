from tkinter import *
from tkinter import ttk
import pandas as pd
from tkinter import filedialog

# def clear_data():
#     tv1.delete(*tv1.get_children())
#     return None

def makeform(root, fields, title="Lorem Ipsum", description="Lorem Ipsum description",view = False, file = False):
    def fileDialog():
        global filename
        filename = filedialog.askopenfilename(initialdir ="/", title = "Select a file") #, filetype = (('text files', 'txt'),)

    entries = {}
    row = Frame(root)
    row.pack(fill = X, padx = 5, pady = 5)
    lab = Label(row, text = title,font=(None, 15) )
    lab.pack(side=LEFT)
    row = Frame(root)
    row.pack(fill = X, padx = 5, pady = 5)
    lab = Label(row, text = description,font=(None, 10) )
    lab.pack(side=LEFT)
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=field+": ", anchor='w')
        ent = Entry(row, width=40)
        ent.insert(0,"0")
        row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
        lab.pack(side = LEFT,fill = X, padx = 10 , pady = 0)
        ent.pack(side = RIGHT, expand = YES, fill = X)
        entries[field] = ent
    if view:
        row = LabelFrame(root, text="Excel Data", height=250, width=600)
        sub_row1 = Frame(row)
        sub_row2 = Frame(row)
        tv1 = ttk.Treeview(sub_row1)   
        treescrolly = Scrollbar(sub_row1, orient="vertical", command=tv1.yview) 
        treescrollx = Scrollbar(sub_row2, orient="horizontal", command=tv1.xview) 
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

        row.pack(side = TOP, fill = X, expand = True,  padx = 5 , pady = 5) #,  padx = 5 , pady = 5
        sub_row1.pack(side = TOP, fill = X, expand = True,  padx = 5 , pady = 5)
        tv1.pack(side = LEFT, fill = X, expand = True,  padx = 5 , pady = 5) #, padx = 5 , pady = 5     
        treescrolly.pack(side="left", fill="y")
        #row.pack(side = BOTTOM, fill = X, padx = 5 , pady = 5) 
        sub_row2.pack(side = TOP, fill = X, expand = True,  padx = 5 , pady = 5)
        treescrollx.pack(side="bottom", fill="x")   

        entries['tv1'] = tv1
    # button to search a file
    if file:
        row = Frame(root)
        btn = Button(row, text = "File", height=2, width=12, command = fileDialog)
        row.pack(side=TOP, fill=X, expand = True)
        btn.pack(side= LEFT,padx = 5 , pady = 5)
        
    # button to call the
    row = Frame(root)
    btn = Button(row, text = "Call", height=2, width=12)
    row.pack(side=TOP, fill=X, expand = True)
    btn.pack(side= LEFT,padx = 5 , pady = 5)
    
    # button to call the function
    row = Frame(root)
    s = ttk.Separator(row, orient=HORIZONTAL )
    row.pack(fill=X,padx = 5 , pady = 5)
    s.pack(fill = X)
    
    

    return entries

# creating the main window
window = Tk()
window.title("Smart Contract Tendering")
window.geometry('500x750')

#creating tab
tab_parent = ttk.Notebook(window)

tab_pa = ttk.Frame(tab_parent)
tab_contractor = ttk.Frame(tab_parent)
tab_citizen = ttk.Frame(tab_parent)

tab_parent.add(tab_pa, text="Public Administration")
tab_parent.add(tab_contractor, text="Contractor")
tab_parent.add(tab_citizen, text="Citizen")

tab_parent.pack(expand=1, fill='both')
main_frame = Frame(tab_pa)
main_frame.pack(fill=BOTH, expand = 1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

second_frame = Frame(my_canvas)

my_canvas.create_window((0,0),window=second_frame, anchor ="nw")

# creating the function fo

ent1 = makeform (second_frame, ('primo', 'secondo', 'terzo'), view=True, file=  True)
ent2 = makeform (second_frame, ('primo', 'secondo', 'terzo'))
ent2 = makeform (second_frame, ('primo', 'secondo', 'terzo') )

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

ent1['tv1']["column"] = list(df.columns)
ent1['tv1']["show"] = "headings"
for column in ent1['tv1']["columns"]:
   ent1['tv1'].heading(column, text=column) # let the column heading = column name

df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
for row in df_rows:
   ent1['tv1'].insert("", "end", values=row)


window.mainloop()

