from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from utils import *
import os

filename = "/"

# User interface
def makeform(root, fields, title="Lorem Ipsum", description="Lorem Ipsum description",view = False, file = False):
    
    def fileDialog(v):
        filename = filedialog.askopenfilename(initialdir =os.getcwd(), title = "Select a file") #, filetype = (('text files', 'txt'),)
        v.set(filename)

    entries = {}
    row = Frame(root)
    row.pack(fill = X, padx = 5, pady = 5)
    lab = Label(row, text = title,font=(None, 15) ,)
    lab.pack(side=LEFT)
    row = Frame(root)
    row.pack(fill = X, padx = 5, pady = 5)
    lab = Label(row, text = description,font=(None, 10), wraplength = 580, justify = LEFT )
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
        #row = LabelFrame(root, text="Data", height=250, width=600)
        sub_row1 = Frame(root)
        sub_row2 = Frame(root)
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
        v = StringVar()
        lab = Label(row, textvariable = v)
        entries["link"]=lab
        btn = Button(row, text = "File", height=2, width=12, command = lambda arg1=v : fileDialog(arg1))
        row.pack(side=TOP, fill=X, expand = True)
        btn.pack(side= LEFT,padx = 5 , pady = 5)
        lab.pack(side=LEFT)

        
    # button to call the
    row = Frame(root)
    btn = Button(row, text = "Call", height=2, width=12)
    row.pack(side=TOP, fill=X, expand = True)
    btn.pack(side= LEFT,padx = 5 , pady = 5)
    entries["btn"]=btn
    
    # button to call the function
    row = Frame(root)
    s = ttk.Separator(row, orient=HORIZONTAL )
    row.pack(fill=X,padx = 5 , pady = 5)
    s.pack(fill = X)
    
    return entries

def main_loop(web3,contract,function_info):
    account_list = web3.eth.accounts
    window = Tk()
    window.title("Smart Contract Tendering")
    window.geometry('600x750')
    
    #creating tabS
    tab_parent = ttk.Notebook(window)
    
    tab_login = ttk.Frame(tab_parent)
    tab_pa = ttk.Frame(tab_parent)
    tab_contractor = ttk.Frame(tab_parent)
    tab_citizen = ttk.Frame(tab_parent)
    
    tab_parent.add(tab_login, text="Login")
    tab_parent.add(tab_pa, text="Public Administration")
    tab_parent.add(tab_contractor, text="Contractor")
    tab_parent.add(tab_citizen, text="Notice Board")
    tab_parent.pack(expand=1, fill='both')
    
    # login interface
    def set_account():
        web3.eth.defaultAccount = account_tkvariable.get().split()[1]
        messagebox.showinfo("Account Changed", "The current account is {}".format(account_tkvariable.get().split()[2]))
    
    account_id_list = [str(i) for i in range(10)]
    account_name_list = ['Public Administration', '1','2','3','4','5','6','7','8','Citizen']
    selection_list = [' '.join(i) for i in zip(account_id_list, account_list, account_name_list)]
    account_tkvariable = StringVar()
    account_tkvariable.set(selection_list[0])
    lab = Label(tab_login, text="Here you can change account, select the desired one and click on 'set account'")
    lab.pack(side = TOP, padx = 5, pady = 20)
    drop = OptionMenu(tab_login, account_tkvariable, *selection_list)
    drop.pack(padx = 10, pady = 10)
    button = Button(tab_login,text = "Set Account", command = set_account)
    button.pack(pady = 20)
    
    # make each tab scrollable (PA)
    main_frame_PA = Frame(tab_pa)
    
    main_frame_PA.pack(fill=BOTH, expand = 1)
    
    my_canvas_PA = Canvas(main_frame_PA)
    my_canvas_PA.pack(side=LEFT, fill=BOTH, expand=1)
    
    my_scrollbar_PA = ttk.Scrollbar(main_frame_PA, orient=VERTICAL, command=my_canvas_PA.yview)
    my_scrollbar_PA.pack(side=RIGHT, fill=Y)
    
    my_canvas_PA.configure(yscrollcommand=my_scrollbar_PA.set)
    my_canvas_PA.bind('<Configure>', lambda e: my_canvas_PA.configure(scrollregion = my_canvas_PA.bbox("all")))
    
    second_frame_PA = Frame(my_canvas_PA)
    
    
    my_canvas_PA.create_window((0,0),window=second_frame_PA, anchor ="nw")
    
    # (CONTRACTOR)
    
    main_frame_contractor = Frame(tab_contractor)
    main_frame_contractor.pack(fill=BOTH, expand = 1)
    
    my_canvas_contractor = Canvas(main_frame_contractor)
    my_canvas_contractor.pack(side=LEFT, fill=BOTH, expand=1)
    
    my_scrollbar_contractor = ttk.Scrollbar(main_frame_contractor, orient=VERTICAL, command=my_canvas_contractor.yview)
    my_scrollbar_contractor.pack(side=RIGHT, fill=Y)
    
    my_canvas_contractor.configure(yscrollcommand=my_scrollbar_contractor.set)
    my_canvas_contractor.bind('<Configure>', lambda e: my_canvas_contractor.configure(scrollregion = my_canvas_contractor.bbox("all")))
    
    second_frame_contractor = Frame(my_canvas_contractor)
    
    my_canvas_contractor.create_window((0,0),window=second_frame_contractor, anchor ="nw")
    
    # (CITIZEN)
    
    main_frame_citizen = Frame(tab_citizen)
    main_frame_citizen.pack(fill=BOTH, expand = 1)
    
    my_canvas_citizen = Canvas(main_frame_citizen)
    my_canvas_citizen.pack(side=LEFT, fill=BOTH, expand=1)
    
    my_scrollbar_citizen = ttk.Scrollbar(main_frame_citizen, orient=VERTICAL, command=my_canvas_citizen.yview)
    my_scrollbar_citizen.pack(side=RIGHT, fill=Y)
    
    my_canvas_citizen.configure(yscrollcommand=my_scrollbar_citizen.set)
    my_canvas_citizen.bind('<Configure>', lambda e: my_canvas_citizen.configure(scrollregion = my_canvas_citizen.bbox("all")))
    
    second_frame_citizen = Frame(my_canvas_citizen)
    
    my_canvas_citizen.create_window((0,0),window=second_frame_citizen, anchor ="nw")
    
    # creating link the function to the user interface
    #CreateTender
    title = "Create Tender"
    create_tender_fields = ('tender name','description','n seconds to send hash','n seconds to send file','weight price', 'weight time', 'weight environment')
    elem_1= makeform(second_frame_PA, create_tender_fields, title=title, description=function_info[title])
    btn_1 = elem_1["btn"]
    btn_1['command'] = lambda arg1=web3, arg2=contract, arg3=elem_1: create_tender(arg1,arg2,arg3)
    
    #placeBid
    title = 'Place Bid'
    place_bid_fields = ('tender id','price','time','environment')
    elem_2 = makeform(second_frame_contractor, place_bid_fields,title=title, description=function_info[title])
    btn_2 = elem_2['btn']
    btn_2['command'] = lambda arg1=web3, arg2=contract, arg3=elem_2: send_bid(arg1,arg2,arg3)
    
    #concludeBid
    title = 'Conclude Bid'
    conclude_bid_fields = ()
    elem_3 = makeform(second_frame_contractor, conclude_bid_fields, title=title, description=function_info[title],file= True)
    btn_3 = elem_3['btn']
    btn_3['command'] = lambda arg1=web3, arg2= contract, arg3 = elem_3: send_unencrypted(arg1, arg2, arg3)
    
    # #getTenderStatus
    # title = 'getTenderStatus'
    # elem_4 = makeform(second_frame_citizen, (),title=title,description=function_info[title],view=True)
    # btn_4 = elem_4['btn']
    # btn_4['command'] = lambda arg1=web3, arg2=contract, arg3=elem_4: get_tenders_status(arg1, arg2, arg3)
    
    #see_active_tenders
    title = "See Active Tenders"
    see_active_tenders_fields = ()
    elem_5 = makeform(second_frame_citizen,see_active_tenders_fields,title=title, description=function_info[title], view=True)
    btn_5 = elem_5['btn']
    btn_5['command'] = lambda arg1=web3, arg2=contract, arg3=elem_5:see_active_tenders(arg1,arg2,arg3)
    
    #see_closed_tenders
    title = 'See Closed Tenders'
    see_closed_tenders_fields = ()
    elem_6 = makeform(second_frame_citizen,see_closed_tenders_fields, title = title, description=function_info[title], view = True)
    btn_6 = elem_6['btn']
    btn_6['command'] = lambda arg1=web3, arg2=contract, arg3=elem_6:see_closed_tenders(arg1,arg2,arg3)
    
    #PA give permission to contractor to place bid
    title = 'Allow Companies'
    allow_companies_fields = ('allowed companies',)
    elem_7 = makeform(second_frame_PA, allow_companies_fields, title = title, description= function_info[title])
    btn_7 = elem_7['btn']
    btn_7['command'] = lambda arg1=web3, arg2=contract, arg3=elem_7: allowed_companies_ids(arg1, arg2, arg3)
    
    #PA see offer given tender id
    title = "Get Bids Details"
    get_bids_details_fields = ('tender id',)
    elem_8 = makeform(second_frame_citizen, get_bids_details_fields, title=title, description=function_info[title], view=True)
    btn_8 = elem_8['btn']
    btn_8['command'] = lambda arg1=web3, arg2=contract, arg3=elem_8: get_bids_details(arg1, arg2, arg3)
    
    #declare the winner
    title = 'Assign Winner'
    assing_winner_fields = ('tender id',)
    elem_9 = makeform(second_frame_PA, assing_winner_fields, title=title, description=function_info[title])
    btn_9 = elem_9['btn']
    btn_9['command'] = lambda arg1=web3, arg2=contract, arg3=elem_9: assign_winner(arg1, arg2, arg3)
    
    window.mainloop()
