#CHRISTINE BERNA E. CELICIOUS
# PRINCESS JOY SALINAS
# BS STATISTICS 

import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
import tkinter.messagebox
import sqlite3
import time
import datetime
from PIL import Image, ImageTk
from tkinter import Label, RIDGE
from tkinter import messagebox

conn = sqlite3.connect('Attendance_Management.db')
cursor = conn.cursor()


class Attendance(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Activity, Course, Student):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Activity)

    def show_frame(self, page_number):

        frame = self.frames[page_number]
        frame.tkraise()
        
    

class Activity(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Attendance Management System")
        centercolor = tk.Label(self,height = 9,width=600, bg="#000000")
        centercolor.place(x=0,y=5)
    
        titleheading = tk.Label(self, text="Attendance Management System", font = ('Times', 45, 'bold'), foreground = '#E3FF94', background = '#000000')
        titleheading.place(x=350, y=35)

        title2=Label(self, text = "College of Science and Mathematics", font = ('Arial', 19, 'bold'), foreground = 'white', background = '#000000')
        title2.place(x=555, y=15)

        title2=Label(self, text = "excellencia est norma", font = ('Roman', 17, 'bold'), foreground = 'white', background = '#000000')
        title2.place(x=650, y=110)
        
        img2 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\logo_1.jpg")
        img2 = img2.resize((130, 130), Image.BICUBIC)

        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblimg = Label(self, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=200, y=15, width=130, height=130)


        
#========= BUTTONS =========#
        Activitybutton = tk.Button(self, text="Activity",font=("Arial",13,"bold"),bd=0,
                            width = 7,
                            bg="#A30505", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Activity))
        Activitybutton.place(x=1250,y=100)
        Activitybutton.config(cursor= "hand2")
        
        Coursebutton= tk.Button(self, text="Course",font=("Arial",13, "bold"),bd=0,
                            width = 7,
                            bg="#A30505", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Course))
        Coursebutton.place(x=1346,y=100)
        Coursebutton.config(cursor= "hand2")
        
        Studbutton= tk.Button(self, text="Student",font=("Arial",13, "bold"),bd=0,
                            width = 7,
                            bg="#A30505", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Student))
        Studbutton.place(x=1440,y=100)
        Studbutton.config(cursor= "hand2")

        ActName = StringVar()
        AcadYear = StringVar()
        Semester = StringVar()
        Duration = StringVar()
        Location = StringVar()
        SearchBarVar = StringVar()


 #========= FUNCTIONS =========#
        def connectActivity():
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS activity (ActName TEXT, AcadYear TEXT,Semester TEXT, Duration TEXT, Location TEXT );") 
            conn.commit() 
            conn.close()
            
        def addActivity():
            if ActName.get()=="": 
                tkinter.messagebox.showinfo("Attendance Management System", "Please fill up the Box correctly")
            else:
                conn = sqlite3.connect("Attendance_Management.db")
                c = conn.cursor() 
                c.execute("INSERT INTO activity(ActName,AcadYear,Semester,Duration,Location) VALUES (?,?,?,?,?)",\
                          (ActName.get(),AcadYear.get(),Semester.get(),Duration.get(),Location.get()))        
                conn.commit()           
                conn.close()
                ActName.set('') 
                tkinter.messagebox.showinfo("Attendance Management System", "Activity Recorded Successfully")
                displayActivity()   
                
        def displayActivity():
            treeactivity.delete(*treeactivity.get_children())
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM activity")
            rows = cur.fetchall()
            for row in rows:
                treeactivity.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateActivity():
            for selected in treeactivity.selection():
                conn = sqlite3.connect("Attendance_Management.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE activity SET ActName=?, AcadYear=?, Semester=?, Duration=?,Location=? WHERE ActName=?", \
                            (ActName.get(), AcadYear.get(), Semester.get(), Duration.get(), Location.get(), treeactivity.set(selected, '#1')))  
                conn.commit()
                tkinter.messagebox.showinfo("Attendance Management System", "Activity Updated Successfully")
                displayActivity()
                conn.close()
                
        def editActivity():
            x = treeactivity.focus()
            if x == "":
                tkinter.messagebox.showerror("Attendance Management System", "Please select a record from the table.")
                return
            values = treeactivity.item(x, "values")
            ActName.set(values[0])
            AcadYear.set(values[1])
            Semester.set(values[2])
            Duration.set(values[3])
            Location.set(values[4])
            
                    
        def deleteActivity(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("Attendance Management System", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Attendance_Management.db")
                    cur = con.cursor()
                    x = treeactivity.selection()[0]
                    id_no = treeactivity.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM activity WHERE ACtName = ?",(id_no,))                   
                    con.commit()

                    treeactivity.delete(x)
                    tkinter.messagebox.showinfo("Attendance Management System", "Activity Deleted Successfully")
                    displayActivity()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Attendance Management System", "Students still attended the activity")
                
        def searchActivity():
            activityName = SearchBarVar.get()
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM activity WHERE ActName = ?", (activityName,))
            rows = cur.fetchall()
            treeactivity.delete(*treeactivity.get_children())
            for row in rows:
                treeactivity.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()

 
        def Refresh():
            pass
            displayActivity()
        
        def clear():
            ActName.set('')
            AcadYear.set('')
            Semester.set('')
            Duration.set('')
            Location.set('')

#========= ENTRY AND CLOCK =========#

        ManageFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#3A302A")
        ManageFrame.place(x=0, y=146,width=300, height=645)
        
        DisplayFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#750505")
        DisplayFrame.place(x=300, y=190,width=1240, height=600)
        
        SmallFrame=Frame(self,relief=GROOVE, borderwidth=1, bg = "#120000")
        SmallFrame.place(x=300, y=145,width=1240, height=45)
        
        RightFrame=Frame(self,relief=GROOVE, borderwidth=1, bg = "#8B795E")
        RightFrame.place(x=1250, y=145,width=300, height=645)
        
        def time1():
            time_string = time.strftime("%H:%M:%S")
            date_string = time.strftime("%d:%m:%y")
            clock.config(text="Time: "+time_string+"\n""Date: "+date_string, font =('Arial', 15, 'bold'))
            clock.after(200, time1)

        clock = Label(ManageFrame, font = ('Times', 14, 'bold'), width = 15, relief = RIDGE, background = "#000000", foreground = 'white')
        clock.place(x = 20, y = 10, width = 250)
        time1()
        
        
        img15 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\greetings.jpg")
        img15 = img15.resize((250, 600), Image.BICUBIC)

        self.photoimg15 = ImageTk.PhotoImage(img15)
        lblimg = Label(RightFrame, image=self.photoimg15, bd=0, relief=RIDGE)
        lblimg.place(x=14, y=20, width=250, height=600)
        
        
#========= LABEL, DISPLAY AND ENTRY BOXES =========#
        
        self.lblActNAme = Label(ManageFrame, font=("Arial",14), justify='center',fg="white", bg="#3A302A", text="Activity Name:", padx=5, pady=5)
        self.lblActNAme.place(x=10,y=70)
        self.txtActName = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=ActName, width=14)
        self.txtActName.place(x=150,y=77)
        
        self.lblAcadYear = Label(ManageFrame, font=("Arial",14), justify='center',fg="white", bg="#3A302A", text="Academic Year:", padx=5, pady=5)
        self.lblAcadYear.place(x=10,y=100)
        self.txtAcadYear = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=AcadYear, width=14)
        self.txtAcadYear.place(x=150,y=108)
        
        self.lblSemester = Label(ManageFrame, font=("Arial",14), justify='center',fg="white", bg="#3A302A", text="Semester:", padx=5, pady=5)
        self.lblSemester.place(x=10,y=130)
        self.txtSemester = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=Semester, width=14)
        self.txtSemester.place(x=150,y=138)
        
        self.lblDuration = Label(ManageFrame, font=("Arial",14), justify='center',fg="white", bg="#3A302A", text="Duration:", padx=5, pady=5)
        self.lblDuration.place(x=10,y=160)
        self.txtDuration = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=Duration, width=14)
        self.txtDuration.place(x=150,y=168)
        
        self.lblLocation = Label(ManageFrame, font=("Arial",14), justify='center',fg="white", bg="#3A302A", text="Location:", padx=5, pady=5)
        self.lblLocation.place(x=10,y=190)
        self.txtLocation = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=Location, width=14)
        self.txtLocation.place(x=150,y=198)
        
        self.SearchBar = Entry(SmallFrame, font=("Arial",12), justify='center', textvariable=SearchBarVar, width=25)
        self.SearchBar.place(x=600,y=10)
        

#========= TREE =========#
        
        scrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
        scrollbar.place(x=900,y=50,height=500)

        treeactivity = ttk.Treeview(DisplayFrame,
                                        columns=("Activity Name","Academic Year", "Semester", "Duration", "Location"),
                                        height = 16,
                                        yscrollcommand=scrollbar.set)

        treeactivity.heading("Activity Name", text="Activity Name", anchor=W)
        treeactivity.heading("Academic Year", text="Academic Year",anchor=W)
        treeactivity.heading("Semester", text="Semester",anchor=W)
        treeactivity.heading("Duration", text="Duration",anchor=W)
        treeactivity.heading("Location", text="Location",anchor=W)
        treeactivity['show'] = 'headings'

        treeactivity.column("Activity Name", width=300, anchor=W, stretch=False)
        treeactivity.column("Academic Year", width=100, stretch=False)
        treeactivity.column("Semester", width=100, stretch=False)
        treeactivity.column("Duration", width=150, stretch=False)
        treeactivity.column("Location", width=250, stretch=False)


        treeactivity.place(x=25,y=50, height = 500, width = 850)
        scrollbar.config(command=treeactivity.yview)
            
#========= BUTTONS =========#

        self.btnAddAct = Button(ManageFrame, text="Add", font=('Arial', 10, 'bold'), height=1, width=15,
                                bg="#E3FF9A", fg="black", command=addActivity)
        self.btnAddAct.place(x=10,y=240)
        
        self.btnUpdate = Button(ManageFrame, text="Update", font=('Arial', 10, 'bold'), height=1, width=15,
                                bg="#E3FF9A", fg="black", command=updateActivity) 
        self.btnUpdate.place(x=150,y=240)
        
        self.btnClear = Button(ManageFrame, text="Clear", font=('Arial', 10, 'bold'), height=1, width=15,
                                bg="#E3FF9A", fg="black", command=clear)
        self.btnClear.place(x=10,y=280)
        
        self.btnDelete = Button(ManageFrame, text="Delete", font=('Arial', 10, 'bold'), height=1, width=15,
                                bg="#E3FF94", fg="black", command=deleteActivity)
        self.btnDelete.place(x=150,y=280)
        
        self.btnSelect = Button(ManageFrame, text="Select", font=('Arial', 10, 'bold'), height=1, width=15,
                              bg="#E3FF94", fg="black", command=editActivity)
        self.btnSelect.place(x=80,y=320)
        
        search_icon = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\search bar.png")
        search_icon = search_icon.resize((20, 20), Image.BICUBIC)
        self.photoimg_search = ImageTk.PhotoImage(search_icon)
        
        self.btnSearch = Button(SmallFrame, text="Search", font=('Arial', 10, 'bold'), height=18, width=30,
                               image=self.photoimg_search, bg="#E3FF94", fg="black", command=searchActivity)
        self.btnSearch.place(x=565,y=10)
        
        self.btnRefresh = Button(SmallFrame, text="Show All", font=('Arial', 10, 'bold'), height=1, width=10,
                              bg="#E3FF94", fg="black", command=Refresh)
        self.btnRefresh.place(x=845,y=8)
        
        connectActivity()
        displayActivity()
        

class Course(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Attendance Management System")
        centercolor = tk.Label(self,height = 9,width=600, bg="#000000")
        centercolor.place(x=0,y=5)
     
        titleheading = tk.Label(self, text="Attendance Management System", font = ('Times', 45, 'bold'), foreground = '#E3FF94', background = '#000000')
        titleheading.place(x=350, y=35)

        title2=Label(self, text = "College of Science and Mathematics", font = ('Arial', 19, 'bold'), foreground = 'white', background = '#000000')
        title2.place(x=555, y=15)

        title2=Label(self, text = "excellencia est norma", font = ('Roman', 17, 'bold'), foreground = 'white', background = '#000000')
        title2.place(x=650, y=110)
        
        img2 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\logo_2.jpg")
        img2 = img2.resize((130, 130), Image.BICUBIC)

        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblimg = Label(self, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=200, y=15, width=130, height=130)


#========= BUTTONS =========#
        Activitybutton = tk.Button(self, text="Activity",font=("Arial",13,"bold"),bd=0,
                            width = 7,
                            bg="#A30505", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Activity))
        Activitybutton.place(x=1250,y=100)
        Activitybutton.config(cursor= "hand2")
        
        Coursebutton = tk.Button(self, text="Course",font=("Arial",13,"bold"),bd=0,
                            width = 7,
                            bg="#000000", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Course))
        Coursebutton.place(x=1346,y=100)
        Coursebutton.config(cursor= "hand2")
        
        Studbutton= tk.Button(self, text="Student",font=("Arial",13, "bold"),bd=0,
                            width = 7,
                            bg="#A30505", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Student))
        Studbutton.place(x=1440,y=100)
        Studbutton.config(cursor= "hand2")

        Code = StringVar()
        Cname = StringVar()
        SearchBarVar = StringVar()


 #========= FUNCTIONS =========#
        def connectCourse():
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS ccode (Code TEXT PRIMARY KEY, Cname TEXT);") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            if Code.get()=="" or Cname.get()=="": 
                tkinter.messagebox.showinfo("Attendance Management System", "Please fill up the Box correctly")
            else:
                conn = sqlite3.connect("Attendance_Management.db")
                c = conn.cursor() 
                c.execute("INSERT INTO ccode(Code,Cname) VALUES (?,?)",\
                          (Code.get(),Cname.get()))        
                conn.commit()           
                conn.close()
                Code.set('')
                Cname.set('') 
                tkinter.messagebox.showinfo("Attendance Management System", "Course Recorded Successfully")
                displayCourse()
                
                
              
        def displayCourse():
            treecourse.delete(*treecourse.get_children())
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM ccode")
            rows = cur.fetchall()
            for row in rows:
                treecourse.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in treecourse.selection():
                conn = sqlite3.connect("Attendance_Management.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE ccode SET Code=?, Cname=? WHERE Code=?", \
                            (Code.get(),Cname.get(), treecourse.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Attendance Management System", "Course Updated Successfully")
                displayCourse()
                conn.close()
                
        def editCourse():
            x = treecourse.focus()
            if x == "":
                tkinter.messagebox.showerror("Attendance Management System", "Please select a record from the table.")
                return
            values = treecourse.item(x, "values")
            Code.set(values[0])
            Cname.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("Attendance Management System", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Attendance_Management.db")
                    cur = con.cursor()
                    x = treecourse.selection()[0]
                    id_no = treecourse.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM ccode WHERE Code = ?",(id_no,))                   
                    con.commit()

                    treecourse.delete(x)
                    tkinter.messagebox.showinfo("Attendance Management System", "Course Deleted Successfully")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Attendance Management System", "Students are still enrolled in this course")
                
        def searchCourse():
            Code = SearchBarVar.get()                
            con = sqlite3.connect("Attendance_Management.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM ccode WHERE Code = ?",(Code,))
            con.commit()
            treecourse.delete(*treecourse.get_children())
            rows = cur.fetchall()
            for row in rows:
                treecourse.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
 
        def Refresh():
            pass
            displayCourse()
        
        def clear():
            Code.set('')
            Cname.set('') 

#========= ENTRY AND CLOCK =========#

        ManageFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#3A302A")
        ManageFrame.place(x=0, y=146,width=300, height=645)
        
        DisplayFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#750505")
        DisplayFrame.place(x=300, y=190,width=1240, height=600)
        
        SmallFrame=Frame(self,relief=GROOVE, borderwidth=1, bg = "#120000")
        SmallFrame.place(x=300, y=145,width=1240, height=45)
        
        RightFrame=Frame(self,relief=GROOVE, borderwidth=1, bg = "#8B795E")
        RightFrame.place(x=1250, y=145,width=300, height=645)
        

        def time1():
            time_string = time.strftime("%H:%M:%S")
            date_string = time.strftime("%d:%m:%y")
            clock.config(text="Time: "+time_string+"\n""Date: "+date_string, font =('Arial', 15, 'bold'))
            clock.after(200, time1)

        clock = Label(ManageFrame, font = ('Times', 14, 'bold'), width = 15, relief = RIDGE, background = "#000000", foreground = 'white')
        clock.place(x = 20, y = 10, width = 250)
        time1()
        
        img3 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\math.png")
        img3 = img3.resize((100, 100), Image.BICUBIC)

        self.photoimg3 = ImageTk.PhotoImage(img3)
        lblimg = Label(RightFrame, image=self.photoimg3, bd=0, relief=RIDGE)
        lblimg.place(x=40, y=18, width=100, height=100)
        
        img4 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\koral.jpg")
        img4 = img4.resize((100, 100), Image.BICUBIC)

        self.photoimg4 = ImageTk.PhotoImage(img4)
        lblimg = Label(RightFrame, image=self.photoimg4, bd=0, relief=RIDGE)
        lblimg.place(x=140, y=18, width=100, height=100)
        
        img5 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\ering.jpg")
        img5 = img5.resize((100, 100), Image.BICUBIC)

        self.photoimg5 = ImageTk.PhotoImage(img5)
        lblimg = Label(RightFrame, image=self.photoimg5, bd=0, relief=RIDGE)
        lblimg.place(x=40, y=118, width=100, height=100)
        
        img6 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\chart.png")
        img6 = img6.resize((100, 100), Image.BICUBIC)

        self.photoimg6 = ImageTk.PhotoImage(img6)
        lblimg = Label(RightFrame, image=self.photoimg6, bd=0, relief=RIDGE)
        lblimg.place(x=140, y=118, width=100, height=100)
        
        img7 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\circle star.jpg")
        img7 = img7.resize((100, 100), Image.BICUBIC)

        self.photoimg7 = ImageTk.PhotoImage(img7)
        lblimg = Label(RightFrame, image=self.photoimg7, bd=0, relief=RIDGE)
        lblimg.place(x=40, y=218, width=100, height=100)
        
        img8 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\microscope.jpg")
        img8 = img8.resize((100, 100), Image.BICUBIC)

        self.photoimg8 = ImageTk.PhotoImage(img8)
        lblimg = Label(RightFrame, image=self.photoimg8, bd=0, relief=RIDGE)
        lblimg.place(x=140, y=218, width=100, height=100)
        
        img9 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\isda.png")
        img9 = img9.resize((100, 100), Image.BICUBIC)

        self.photoimg9 = ImageTk.PhotoImage(img9)
        lblimg = Label(RightFrame, image=self.photoimg9, bd=0, relief=RIDGE)
        lblimg.place(x=40, y=318, width=100, height=100)
        
        img10 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\nature.png")
        img10 = img10.resize((100, 100), Image.BICUBIC)

        self.photoimg10 = ImageTk.PhotoImage(img10)
        lblimg = Label(RightFrame, image=self.photoimg10, bd=0, relief=RIDGE)
        lblimg.place(x=140, y=318, width=100, height=100)
        
        img11 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\balay.png")
        img11 = img11.resize((100, 100), Image.BICUBIC)

        self.photoimg11 = ImageTk.PhotoImage(img11)
        lblimg = Label(RightFrame, image=self.photoimg11, bd=0, relief=RIDGE)
        lblimg.place(x=140, y=418, width=100, height=100)
        
        img12 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\libro.png")
        img12 = img12.resize((100, 100), Image.BICUBIC)

        self.photoimg12 = ImageTk.PhotoImage(img12)
        lblimg = Label(RightFrame, image=self.photoimg12, bd=0, relief=RIDGE)
        lblimg.place(x=40, y=418, width=100, height=100)
        
        img13 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\Nagtudlo.png")
        img13 = img13.resize((100, 100), Image.BICUBIC)

        self.photoimg13 = ImageTk.PhotoImage(img13)
        lblimg = Label(RightFrame, image=self.photoimg13, bd=0, relief=RIDGE)
        lblimg.place(x=140, y=518, width=100, height=100)
        
        img14 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\laptop.png")
        img14 = img14.resize((100, 100), Image.BICUBIC)

        self.photoimg14 = ImageTk.PhotoImage(img14)
        lblimg = Label(RightFrame, image=self.photoimg14, bd=0, relief=RIDGE)
        lblimg.place(x=40, y=518, width=100, height=100)
        
#========= LABEL, DISPLAY AND ENTRY BOXES =========#
        
        self.lblCourseCode = Label(ManageFrame, font=("Arial",15), justify='center',fg="white", bg="#3A302A", text="Course Code:", padx=5, pady=5)
        self.lblCourseCode.place(x=10,y=70)
        self.txtCourseCode = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=Code, width=30)
        self.txtCourseCode.place(x=10,y=100)
        

        self.lblCourseName = Label(ManageFrame, font=("Arial",15), justify='center',fg="white", bg="#3A302A", text="Course Name:", padx=5, pady=5)
        self.lblCourseName.place(x=10,y=125)
        self.txtCourseName = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=Cname, width=30)
        self.txtCourseName.place(x=10,y=155)
        
        self.SearchBar = Entry(SmallFrame, font=("Arial",12), justify='center', textvariable=SearchBarVar, width=25)
        self.SearchBar.place(x=600,y=10)

#========= TREE =========#
        
        scrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
        scrollbar.place(x=900,y=50,height=500)

        treecourse = ttk.Treeview(DisplayFrame,
                                        columns=("Course Code","Course Name"),
                                        height = 16,
                                        yscrollcommand=scrollbar.set)

        treecourse.heading("Course Code", text="Course Code", anchor=W)
        treecourse.heading("Course Name", text="Course Name",anchor=W)
        treecourse['show'] = 'headings'

        treecourse.column("Course Code", width=200, anchor=W, stretch=False)
        treecourse.column("Course Name", width=690, stretch=False)

        treecourse.place(x=25,y=50, height = 500, width = 850)
        scrollbar.config(command=treecourse.yview)
      
#========= BUTTONS =========#

        self.btnAddID = Button(ManageFrame, text="Add", font=('Arial', 10,'bold'), height=1, width=15,
                                bg="#E3FF9A", fg="black", command=addCourse)
        self.btnAddID.place(x=10,y=200)
        
        self.btnUpdate = Button(ManageFrame, text="Update", font=('Arial', 10,'bold'), height=1, width=15,
                                bg="#E3FF9A", fg="black", command=updateCourse) 
        self.btnUpdate.place(x=150,y=200)
        
        self.btnClear = Button(ManageFrame, text="Clear", font=('Arial', 10,'bold'), height=1, width=15,
                                bg="#E3FF9A", fg="black", command=clear)
        self.btnClear.place(x=10,y=240)
        
        self.btnDelete = Button(ManageFrame, text="Delete", font=('Arial', 10,'bold'), height=1, width=15,
                                bg="#E3FF94", fg="black", command=deleteCourse)
        self.btnDelete.place(x=150,y=240)
        
        self.btnSelect = Button(ManageFrame, text="Select", font=('Arial', 10,'bold'), height=1, width=15,
                              bg="#E3FF94", fg="black", command=editCourse)
        self.btnSelect.place(x=75,y=280)
        
        search_icon = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\search bar.png")
        search_icon = search_icon.resize((20, 20), Image.BICUBIC)
        self.photoimg_search = ImageTk.PhotoImage(search_icon)
        
        self.btnSearch = Button(SmallFrame, text="Search", font=('Arial', 10, 'bold'), height=18, width=30,
                               image=self.photoimg_search, bg="#E3FF94", fg="black", command=searchCourse)
        self.btnSearch.place(x=565,y=10)
        
        self.btnRefresh = Button(SmallFrame, text="Show All", font=('Arial', 10, 'bold'), height=1, width=10,
                              bg="#E3FF94", fg="black", command=Refresh)
        self.btnRefresh.place(x=845,y=8)
        
        connectCourse()
        displayCourse()
        
           

class Student(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Attendance Management System")
        centercolor = tk.Label(self,height = 9,width=600, bg="#000000")
        centercolor.place(x=0,y=5)
        apptitle = tk.Label(self, text="Attendance Management System", font = ('Times', 45, 'bold'), foreground = '#E3FF94', background = '#000000')
        apptitle.place(x=350,y=35)
    
        title2=Label(self, text = "College of Science and Mathematics", font = ('Arial', 19, 'bold'), foreground = 'white', background = '#000000')
        title2.place(x=555, y=15)

        title2=Label(self, text = "excellencia est norma", font = ('Roman', 17, 'bold'), foreground = 'white', background = '#000000')
        title2.place(x=650, y=110)
        
        img2 = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\logo_1.jpg")
        img2 = img2.resize((130, 130), Image.BICUBIC)

        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblimg = Label(self, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=200, y=15, width=130, height=130)


#========= INITIAL BUTTONS =========#
        Activitybutton = tk.Button(self, text="Activity",font=("Arial",13,"bold"),bd=0,
                            width = 7,
                            bg="#A30505", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Activity))
        Activitybutton.place(x=1250,y=100)
        Activitybutton.config(cursor= "hand2")
        
        Coursebutton = tk.Button(self, text="Course",font=("Arial",13,"bold"),bd=0,
                                width = 7,
                                bg="#A30505",
                                fg="white",
                                command=lambda: controller.show_frame(Course))
        Coursebutton.place(x=1346,y=100)
        Coursebutton.config(cursor= "hand2")
            
        Studbutton= tk.Button(self, text="Student",font=("Arial", 13, "bold"),bd=0,
                                width = 7,
                                bg="#000000",
                                fg="white",
                                command=lambda: controller.show_frame(Student))
        Studbutton.place(x=1440,y=100)
        Studbutton.config(cursor= "hand2")
        
        
#========= FUNCTIONS =========#
        ActName = StringVar()
        AcadYear = StringVar()
        ID = StringVar()
        FName = StringVar()
        MName = StringVar()
        SName = StringVar()
        YLevel = StringVar()
        Gender = StringVar()
        Searchbar=StringVar()
        CCode = StringVar()
        SignIn =StringVar()
        SignOut = StringVar()

        def connect():
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS studopt (ActName TEXT, AcadYear TEXT, ID TEXT, FName TEXT, "
                        "MName TEXT, SName TEXT, CCode TEXT, YLevel TEXT, Gender TEXT, "
                        "SignIn TEXT DEFAULT CURRENT_TIMESTAMP, SignOut TEXT DEFAULT CURRENT_TIMESTAMP, "
                        "FOREIGN KEY(CCode) REFERENCES ccode(Code) ON UPDATE CASCADE)")
            conn.commit()
            conn.close()

        def addData():
            if ActName.get() == "" or AcadYear.get() == "" or ID.get() == "" or FName.get() == "" or MName.get() == "" or SName.get() == "" or CCode.get() == "" or YLevel.get() == "" or Gender.get() == "":
                messagebox.showinfo("Attendance Management System", "Please fill up the Box correctly")
            else:
                ID1 = ID.get()
                ID1_list = []
                for i in ID1:
                    ID1_list.append(i)
                a = ID1.split("-")
                if len(a) >= 2 and len(a[1]) == 4:
                    if "-" in ID1_list:
                        while True:
                            try:
                                conn = sqlite3.connect("Attendance_Management.db")
                                c = conn.cursor() 
                                c.execute("PRAGMA foreign_keys = ON")
                                # Insert the record into the table with empty strings for Sign In and Sign Out
                                c.execute("INSERT INTO studopt(ActName, AcadYear, ID, FName, MName, SName, CCode, YLevel, Gender, SignIn, SignOut) \
                                            VALUES (?,?,?,?,?,?,?,?,?,?,?)", \
                                            (ActName.get(), AcadYear.get(), ID.get(), FName.get(), MName.get(), SName.get(), CCode.get(), \
                                            YLevel.get(), Gender.get(), '', ''))
                                conn.commit() 
                                messagebox.showinfo("Attendance Management System", "Student Recorded")
                                clear()
                                displayData()
                                break  # Exit the while loop on successful insertion
                            except sqlite3.OperationalError as e:
                                print("Error:", e)
                                time.sleep(0.1)  # Wait for a brief period
                                continue
                            finally:
                                conn.close()
                    else:
                        messagebox.showerror("Attendance Management System", "ID is invalid")
                else:
                    messagebox.showerror("Attendance Management System", "ID is Invalid")

         
        def sign_in_student():
            selected_item = tree.focus()
            if not selected_item:
                tkinter.messagebox.showerror("Attendance Management System", "Please select a student from the table.")
                return

            # Get the selected student's ID
            student_id = tree.item(selected_item)["values"][2]

            # Update the sign-in timestamp in the database
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("UPDATE studopt SET SignIn=? WHERE ID=?", (timestamp, student_id))
            conn.commit()
            conn.close()

            # Update the sign-in timestamp in the display
            tree.set(selected_item, "Sign In", timestamp)


        def sign_out_student():
            selected_item = tree.focus()
            if not selected_item:
                tkinter.messagebox.showerror("Attendance Management System", "Please select a student from the table.")
                return

            # Get the selected student's ID
            student_id = tree.item(selected_item)["values"][2]

            # Update the sign-out timestamp in the database
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("UPDATE studopt SET SignOut=? WHERE ID=?", (timestamp, student_id))
            conn.commit()
            conn.close()

            # Update the sign-out timestamp in the display
            tree.set(selected_item, "Sign Out", timestamp)


        def displayData():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("Attendance_Management.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM studopt")
            rows = cur.fetchall()
            for row in rows:
                # Replace None values with empty strings for Sign In and Sign Out columns
                row = ['' if value is None else value for value in row]
                tree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()

        def updateData():
            for selected in tree.selection():
                conn = sqlite3.connect("Attendance_Management.db")
                cur = conn.cursor()
                try:
                    act_name = ActName.get()
                    acad_year = AcadYear.get()
                    student_id = ID.get()
                    fname = FName.get()
                    mname = MName.get()
                    sname = SName.get()
                    ccode = CCode.get()
                    y_level = YLevel.get()
                    gender = Gender.get()

                    cur.execute("UPDATE studopt SET ActName = ?, AcadYear = ?, FName = ?, MName = ?, SName = ?, "
                                "CCode = ?, YLevel = ?, Gender = ? WHERE ID = ?",
                                (act_name, acad_year, fname, mname, sname, ccode, y_level, gender, student_id))
                    conn.commit()
                    messagebox.showinfo("Attendance Management System", "Student information updated successfully.")
                    displayData()
                except sqlite3.Error as e:
                    print("Error:", e)
                    messagebox.showerror("Attendance Management System", "Failed to update student information.")
                finally:
                    cur.close()
                    conn.close()



        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Attendance Management System", "Do you want to delete this record?")
                if messageDelete == True:   
                    con = sqlite3.connect("Attendance_Management.db")
                    cur = con.cursor()
                    x = tree.selection()[0]
                    id_no = tree.item(x)["values"][2]
                    cur.execute("DELETE FROM studopt WHERE ID = ?",(id_no,))                   
                    con.commit()
                    tree.delete(x)
                    tkinter.messagebox.showinfo("Attendance Management System", "Student is successfully deleted")
                    displayData()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            ID = Searchbar.get()
            try:  
                con = sqlite3.connect("Attendance_Management.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM studopt WHERE ID = ?",(ID,))
                con.commit()
                tree.delete(*tree.get_children())
                rows = cur.fetchall()
                for row in rows:
                    tree.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("Attendance Management System", "ID is invalid")
                            
        def editData():
            x = tree.focus()
            if x == "":
                tkinter.messagebox.showerror("Attendance Management System", "Please select a record from the table.")
                return
            values = tree.item(x, "values")
            ActName.set(values[0])
            AcadYear.set(values[1])
            ID.set(values[2])
            FName.set(values[3])
            MName.set(values[4])
            SName.set(values[5])
            CCode.set(values[6])
            YLevel.set(values[7])
            Gender.set(values[8])
            SignIn.set(values[9])
            SignOut.set(values[10])

            
        def Refresh():
            displayData()
        
        def clear():
            ActName.set('')
            AcadYear.set('')
            ID.set('')
            FName.set('')
            MName.set('')
            SName.set('')
            CCode.set('')
            YLevel.set('')
            Gender.set('')
            SignIn.set('')
        
        con = sqlite3.connect("Attendance_Management.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM activity")
        books = cur.fetchall()
        bookid_actname = []
        for book in books:
             bookid_actname.append(book[0])
             
        con = sqlite3.connect("Attendance_Management.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM activity")
        books = cur.fetchall()
        bookid_acadyear = []
        for book in books:
             bookid_acadyear.append(book[1])

        con = sqlite3.connect("Attendance_Management.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM ccode")
        books = cur.fetchall()
        bookid_course = []
        for book in books:
             bookid_course.append(book[0])
             
#========ENTRY AND CLOCK======#

        ManageFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#3A302A")
        ManageFrame.place(x=0, y=146,width=300, height=645)
        
        DisplayFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#750505")
        DisplayFrame.place(x=300, y=190,width=1240, height=600)
        
        SmallFrame=Frame(self,relief=GROOVE, borderwidth=1, bg = "#120000")
        SmallFrame.place(x=300, y=145,width=1240, height=45)
        

        def time1():
            time_string = time.strftime("%H:%M:%S")
            date_string = time.strftime("%d:%m:%y")
            clock.config(text="Time: "+time_string+"\n""Date: "+date_string, font =('Arial', 15, 'bold'))
            clock.after(200, time1)

        clock = Label(ManageFrame, font = ('Times', 14, 'bold'), width = 15, relief = RIDGE, background = "#000000", foreground = 'white')
        clock.place(x = 20, y = 10, width = 250)
        time1()
        

#========= LABEL AND ENTRY BOXES =========#

        self.lblActNAme = Label(ManageFrame, font=("Arial",14),fg="white", bg="#3A302A", text="Activity Name:", padx=5, pady=5)
        self.lblActNAme.place(x=17,y=65)
        self.txtActName = ttk.Combobox(ManageFrame, value=bookid_actname,state="readonly", justify='center', font=("Arial", 13), textvariable=ActName, width=26)
        self.txtActName.place(x=17,y=95)
        
        self.lblAcadYear = Label(ManageFrame, font=("Arial",15), justify='center',fg="white", bg="#3A302A", text="Academic Year:", padx=5, pady=5)
        self.lblAcadYear.place(x=17,y=120)
        self.txtAcadYear = ttk.Combobox(ManageFrame, value=bookid_acadyear,state="readonly",justify='center', font=("Arial", 13), textvariable=AcadYear, width=26)
        self.txtAcadYear.place(x=17,y=150)
        
        self.StudentID = Label(ManageFrame, font=("Arial",14),fg="snow", bg="#3A302A", text="Student ID:", padx=5, pady=5)
        self.StudentID.place(x=17,y=175)
        self.StudentIDEntry = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=ID, width=28)
        self.StudentIDEntry.place(x=17,y=205)
        self.StudentIDEntry.insert(2,'YYYY-NNNN')
        

        self.Firstname = Label(ManageFrame, font=("Arial",14),fg="white", bg="#3A302A", text="First Name:", padx=5, pady=5)
        self.Firstname.place(x=17,y=230)
        self.FirstnameEntry = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=FName, width=28)
        self.FirstnameEntry.place(x=17,y=260)

        self.Midname = Label(ManageFrame, font=("Arial",14),fg="white", bg="#3A302A", text="Middle Name:", padx=5, pady=5)
        self.Midname.place(x=17,y=285)
        self.MidnameEntry = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=MName, width=28)
        self.MidnameEntry.place(x=17,y=315)

        self.Surname = Label(ManageFrame, font=("Arial",14),fg="white", bg="#3A302A",text="Surname:", padx=5, pady=5)
        self.Surname.place(x=17,y=340)
        self.SurnameEntry = Entry(ManageFrame, font=("Arial", 13), justify='center', textvariable=SName, width=28)
        self.SurnameEntry.place(x=17,y=370)

        self.Course = Label(ManageFrame, font=("Arial",14), fg="white", bg="#3A302A",text="Course:", padx=5, pady=5)
        self.Course.place(x=17,y=395)
        self.CourseEntry =ttk.Combobox(ManageFrame,value=bookid_course,state="readonly", justify='center', font=("Arial", 13), textvariable=CCode, width=26)
        self.CourseEntry.place(x=17,y=425)
        

        self.StudentYearLevel = Label(ManageFrame, font=("Arial",14),fg="white", bg="#3A302A", text="Year Level:", padx=5, pady=5)
        self.StudentYearLevel.place(x=17,y=451)
        self.StudentYearLevelEntry = ttk.Combobox(ManageFrame,
                                                value=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
                                                state="readonly", justify='center', font=("Arial", 13), textvariable=YLevel,
                                                width=26)
        self.StudentYearLevelEntry.place(x=17,y=480)
        

        self.Gender = Label(ManageFrame, font=("Arial",14),fg="white", bg="#3A302A", text="Gender:", padx=5, pady=5)
        self.Gender.place(x=17,y=505)
        self.GenderEntry = ttk.Combobox(ManageFrame, value=["Male", "Female","Prefer not to say"], font=("Arial'", 13),
                                             state="readonly", justify='center', textvariable=Gender, width=26)
        self.GenderEntry.place(x=17,y=535)

        self.SearchBar = Entry(SmallFrame, font=("Arial'",12), justify='center', textvariable=Searchbar, width=25)
        self.SearchBar.place(x=600,y=10)
        self.SearchBar.insert(2,'YYYY-NNNN')
        
       
#========= TREE =========#
        
        scrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
        scrollbar.place(x=1190,y=50,height=500)

        tree = ttk.Treeview(DisplayFrame,
                            columns=("Activity Name", "Academic Year", "ID Number", "First Name","Mid Initial","Surname", "Course", "Year Level", "Gender", "Sign In", "Sign Out"),
                            height = 16,
                            yscrollcommand=scrollbar.set)

        tree.heading("Activity Name", text="Activity Name", anchor="center")
        tree.heading("Academic Year", text="Academic Year", anchor="center")
        tree.heading("ID Number", text="ID Number", anchor="center")
        tree.heading("First Name", text="First Name",anchor="center")
        tree.heading("Mid Initial", text="Middle Name",anchor="center")
        tree.heading("Surname", text="Surname",anchor="center")
        tree.heading("Course", text="Course",anchor="center")
        tree.heading("Year Level", text="Year Level",anchor="center")
        tree.heading("Gender", text="Gender",anchor="center")
        tree.heading("Sign In", text="Sign In",anchor="center")
        tree.heading("Sign Out", text="Sign Out",anchor="center")
        tree['show'] = 'headings'

        tree.column("Activity Name", width=127, anchor=W, stretch=False)
        tree.column("Academic Year", width=100, anchor=W, stretch=False)
        tree.column("ID Number", width=100, anchor=W, stretch=False)
        tree.column("First Name", width=127, stretch=False)
        tree.column("Mid Initial", width=80, stretch=False)
        tree.column("Surname", width=100, stretch=False)
        tree.column("Course", width=80, anchor=W, stretch=False)
        tree.column("Year Level", width=60, anchor=W, stretch=False)
        tree.column("Gender", width=100, anchor=W, stretch=False)
        tree.column("Sign In", width=120, anchor=W, stretch=False)
        tree.column("Sign Out", width=120, anchor=W, stretch=False)

        tree.place(x=20,y=50, height = 500, width = 1170)
        scrollbar.config(command=tree.yview)
        
#========= BUTTONS =========#
        
        btnAddStudent = Button(ManageFrame, text="Add", font=('Arial', 10,'bold'), height=1, width=10, bg="#E3FF9A", fg="black", command=addData)
        btnAddStudent.place(x=10,y=567)
        
        btnUpdate = Button(ManageFrame, text="Update", font=('Arial', 10,'bold'), height=1, width=10, bg="#E3FF9A", fg="black", command=updateData)
        btnUpdate.place(x=105,y=567)
        btnUpdate.config(cursor= "hand2")
        
        btnClear = Button(ManageFrame, text="Clear", font=('Arial', 10,'bold'), height=1, width=10, bg="#E3FF9A", fg="black", command=clear)
        btnClear.place(x=200,y=567)

        btnDelete = Button(ManageFrame, text="Delete", font=('Arial', 10,'bold'), height=1, width=10, bg="#E3FF9A", fg="black", command=deleteData)
        btnDelete.place(x=60,y=600)
        
        btnSelect = Button(ManageFrame, text="Select", font=('Arial', 10,'bold'), height=1, width=10, bg="#E3FF94", fg="black", command=editData)
        btnSelect.place(x=155,y=600) 
        
        btnSignIn = Button(SmallFrame, text="Sign In", font=('Arial', 10, 'bold'), height=1, width=10, bg="#E3FF9A", fg="black",
                   command=sign_in_student)
        btnSignIn.place(x=1025, y=8)
        btnSignIn.config(cursor="hand2")
        
        btnSignOut = Button(SmallFrame, text="Sign Out", font=('Arial', 10, 'bold'), height=1, width=10, bg="#E3FF9A", fg="black",
                    command=sign_out_student)
        btnSignOut.place(x=1125, y=8)
        btnSignOut.config(cursor="hand2")
        
        search_icon = Image.open(r"C:\Users\keenh\OneDrive\Documents\Final Project in CCC151_ Salinas&Berna\search bar.png")
        search_icon = search_icon.resize((20, 20), Image.BICUBIC)
        self.photoimg_search = ImageTk.PhotoImage(search_icon)
        
        btnSearch = Button(SmallFrame, text="Search", font=('Arial', 12,'bold'), height=18, width=30,
                           image=self.photoimg_search, bg="#E3FF94", fg="black", command=searchData)
        btnSearch.place(x=565,y=10)
       
        
        btnDisplay = Button(SmallFrame, text="Show All", font=('Arial', 10,'bold'), height=1, width=10, bg="#E3FF94", fg="black", command=Refresh)
        btnDisplay.place(x=845,y=8)
        btnDisplay.config(cursor= "hand2")
        connect()
        displayData()
        
attendance = Attendance()
attendance.geometry("1540x790+0+0")
attendance.resizable(False,False)
attendance.mainloop()