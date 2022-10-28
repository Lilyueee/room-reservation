# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 19:02:08 2021

@author: jqy
"""

import csv
import pandas as pd

from pandas import Series, DataFrame
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk

df_rooms=pd.read_csv('Rooms.csv', index_col='Name')
df_book=pd.read_csv('Book.csv',index_col='Name')


##Display in a window
window=tk.Tk()
window.title('Room-booking System')


##BOOK FUNCTION

#create an upper frame
frame_up=tk.Frame(window, bg='lightyellow')
frame_up.pack()
##user input the room
tk.Label(frame_up, bg='lightyellow', 
         font=tkFont.Font(family='Arial', size=11, weight=tkFont.BOLD),
         text='Welcome!\nPlease enter the name of the room:').pack()
e=tk.Entry(frame_up, show=None, width=35)
e.pack(side=tk.LEFT, padx=5, pady=5)

##when clicking button "confirm"
def enter_button():
    user_input=e.get() 
    #detect error
    if user_input not in df_rooms.index:
        tk.messagebox.showerror(title='ERROR',message='Please enter the right name!')

    details=df_rooms.loc[user_input]
    
    #show the details in a separate window
    show_detail=tk.Tk()
    show_detail.title(user_input)
    msg=tk.Label(show_detail,
                 text='See the details of {}:\n {}'.format(user_input,details),
                 bg='green',
                 font=('Arial',10),
                 )
    msg.pack()
    
    ##book or not
    #when clicking the button "book"
    def book_button():
        #check if the room is available
        if_avail=df_rooms.at[user_input, 'Availability']
        if if_avail=='Available':
            #choose the time slot
            #open a new window
            show_detail.destroy()
            choose_time=tk.Tk()
            choose_time.title('Choose Your Time Slot')
            choose_time.focus_force()
            #the interface for booking
            words=tk.Label(choose_time, text='Time slots available for you:')
            words.pack()
                
            
            #when clicking "choose this time slot"    
            def time_selection():
                time_chosen=lb.get(lb.curselection())
                if df_book.at[user_input, time_chosen]==0:
                    df_book.at[user_input,time_chosen]=1
                    df_book.to_csv('Book.csv',encoding='utf-8')
                    tk.messagebox.showinfo(title='Success!',
                                           message='You have booked {} for {}.'.format(user_input, time_chosen))
                else:
                    tk.messagebox.showerror(title='Fail!',
                                                message='Action Denied.')
                    
            #create a button for choosing time slot
            bb = tk.Button(choose_time, text='choose this time slot', width=15,
                               height=2, command=time_selection)
            bb.pack()
                
            #create a list of timeslots
            lb = tk.Listbox(choose_time)
            lb.insert(1, '8:00-9:00')
            lb.insert(2, '9:00-10:00')
            lb.insert(3, '10:00-11:00')
            lb.insert(4, '11:00-12:00')
            lb.insert(5, '12:00-13:00')
            lb.insert(6, '13:00-14:00')
            lb.pack()
                
            choose_time.mainloop()
            
        #if the room is not available    
        else:
            tk.messagebox.showinfo(title='Failure',
                                   message='The room is not available.')
            
        
    ##create the button "book"
    b_book=tk.Button(show_detail,
                 text='Book',
                 width=15, height=2,
                 command=book_button)
    b_book.pack()
    
    show_detail.mainloop()
   
    
#create the "confirm" button in the index window    
b1=tk.Button(frame_up,
             text='Confirm',
             width=10,height=1,
             command=enter_button)
b1.pack(side=tk.LEFT, padx=5, pady=5)




###SEARCH FUNCTION
tk.Label(window, text='Search by:',
         font=tkFont.Font(family='Arial', size=10, weight=tkFont.BOLD),
         pady=10).pack()

#create a lower frame
frame_low=tk.Frame(window)
frame_low.pack()


##search the room by TIME SLOTS
time_intro=tk.Label(frame_low, pady=5, padx=10,
                      text='Time Slots',
                      fg='DarkSlateBlue')
time_intro.grid(row=0)
#create a comcobox
com_time=ttk.Combobox(frame_low)
com_time['value']=("8:00-9:00","9:00-10:00","10:00-11:00","11:00-12:00",
              "12:00-13:00","13:00-14:00")
com_time['state']="readonly"
com_time.current(0)

#search by time slot function
Name_list=df_rooms.index
def search_time(event):     
    time_searched=com_time.get()
    time_window=tk.Tk()
    time_window.title('Results')
    tk.Label(time_window,
             text='Rooms available at {}'.format(time_searched),
             fg='MediumPurple',
             font=16).pack()
    frm=tk.Frame(time_window, width=150, height=80, 
                 relief=tk.RAISED, borderwidth=5)
    frm.pack(padx=10, pady=10)

    for name in Name_list:
        if df_book.at[name, time_searched]==0:
            tk.Label(frm, text='{}\n'.format(name)).pack()
    time_window.mainloop()
      
com_time.bind("<<ComboboxSelected>>",search_time)
com_time.grid(row=0,column=1, pady=5)


##search the room by TYPE
type_intro=tk.Label(frame_low, pady=5, padx=10,
                      text='Types',
                      fg='DarkSlateBlue')
type_intro.grid(row=1)
#create a comcobox
com_type=ttk.Combobox(frame_low)
com_type['value']=("Tiered","Teaching","Flat","Boardroom","Flexible")
com_type['state']="readonly"
com_type.current(0)
#search by type
def search_type(event):
    type_searched=com_type.get()
    type_window=tk.Tk()
    type_window.title('Results')
    tk.Label(type_window, text='Rooms available of type "{}"'.format(type_searched),
             fg='MediumPurple', font=16).pack()
    frm=tk.Frame(type_window, width=150, height=80,
                 relief=tk.RAISED, borderwidth=5)
    frm.pack(padx=10, pady=10)
    
    for name in Name_list:
        type_all=df_rooms.at[name,'Type']
        if type_searched in type_all:
            tk.Label(frm, text='{}\n'.format(name)).pack()
    type_window.mainloop()

com_type.bind("<<ComboboxSelected>>",search_type)
com_type.grid(row=1, column=1, pady=5)


##search the room by EQUIPMENT
equip_intro=tk.Label(frame_low, padx=10, pady=5, 
                     fg='DarkSlateBlue',
                     text='Equipments')
equip_intro.grid(row=2)
#search button function
def select_equipment(label):
    equip_selected=label.get()
    
    equip_window=tk.Tk()
    equip_window.title('Results')
    tk.Label(equip_window, text='Rooms available with {}'.format(equip_selected),
             fg='MediumPurple', font=16).pack()
    frm=tk.Frame(equip_window, width=150, height=80,
                 relief=tk.RAISED, borderwidth=5)
    frm.pack(padx=10, pady=10)
    
    equip_list=[]
    for name in Name_list:        
        equip_all=df_rooms.at[name, 'Equipment']      
        equip_list.append(equip_all)
        if equip_selected in equip_all:
            tk.Label(frm, text='{}\n'.format(name)).pack()

    equip_window.mainloop()
                
def search_equipment():
    label=tk.StringVar()
    e_equip=tk.Entry(frame_low, textvariable=label)
    e_equip.grid(row=2,column=1, pady=5)
   
    
    select_btn=tk.Button(frame_low, padx=10, pady=5,
                         text='search', width=5, height=1,
                         command=lambda:select_equipment(label))
    select_btn.grid(row=2, column=2, pady=5)
search_equipment()


##search the room by BUILDING
build_intro=tk.Label(frame_low, padx=10, pady=5,
                     fg='DarkSlateBlue',
                     text='Building')
build_intro.grid(row=3)
#create a comcobox
com_build=ttk.Combobox(frame_low)
com_build['value']=("Arts Centre","Faculty of Arts","Humanities",
                    "Library","Ramphal","Westwood-Avon Building")
com_build['state']="readonly"
com_build.current(0)
#search by building
def search_build(event):
    build_searched=com_build.get()
    build_window=tk.Tk()
    build_window.title('Results')
    tk.Label(build_window, text='Rooms available of building "{}"'.format(build_searched),
             fg='MediumPurple', font=16).pack()
    frm=tk.Frame(build_window, width=150, height=80,
                 relief=tk.RAISED, borderwidth=5)
    frm.pack(padx=10, pady=10)
    
    for name in Name_list:
        build_all=df_rooms.at[name,'Building']
        if build_searched in build_all:
            tk.Label(frm, text='{}\n'.format(name)).pack()
    build_window.mainloop()

com_build.bind("<<ComboboxSelected>>",search_build)
com_build.grid(row=3, column=1, pady=5)

window.mainloop()            


##check if the room is available
def if_available(name):
    avail_list=[]
    for i in range(1,7):
        avail_list.append(df_book.loc[name][i])
    if 0 not in avail_list:
        df_rooms.at[name, 'Availability']='Not Available'
        df_rooms.to_csv('Rooms.csv',encoding='utf-8')

for name in Name_list:
    if_available(name)
    
    




   