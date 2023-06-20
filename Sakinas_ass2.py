from tkinter import*
import tkinter as ssis
from tkinter import ttk
import tkinter.messagebox
import sqlite3

#________APPDATABASE________#

class AppDatabase(ssis.Tk):

    def __init__(self):
        ssis.Tk.__init__(self)
        self.config(bg="#B99470")
        Table = ssis.Frame(self)
        Table.pack(side="top", fill="both", expand = True)
        Table.rowconfigure(0, weight=1)
        Table.columnconfigure(0, weight=1)
        self.frames = {}

        for i in (Home, Student, Course):
            frame = i(Table, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.ShowFrame(Home)

    def ShowFrame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()
        

#HOME
        
class Home(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self, parent)
        
        leftcolor = ssis.Label(self,height = 60,width=200, bg="#B99470")
        leftcolor.place(x=0,y=0)
        label = ssis.Label(self, text = "MSU-IIT STUDENT INFORMATION SYSTEM",bd=6,relief=RIDGE, font=("Garamond",40,"bold"),bg="white smoke", fg="maroon")
        label.place(x=110,y=40)
        
        ttlstudents = StringVar() 
        totalcourses = StringVar()

#________HOME FUNCTIONS________#
        def Totalcourse():
            try:
                conn = sqlite3.connect("StudentDatabase")
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                rows = cur.fetchall()
                totalcourses.set(len(rows))
                self.totalenrolled = Label(self, font=("Arial Black", 35 ,"bold"),textvariable = totalcourses, bg = "#B99470", fg = "maroon")
                self.totalenrolled.place(x=650,y=300)
                self.after(1000,Totalcourse)
                conn.commit()            
                conn.close()
            except:
                pass
            
        def Totalstudents():
            try:
                conn = sqlite3.connect("StudentDatabase")
                cur = conn.cursor()
                cur.execute("SELECT * FROM studdatabase")
                rows = cur.fetchall()
                ttlstudents.set(len(rows))
                self.totalenrolled = Label(self, font=("Arial Black", 35, "bold"),textvariable = ttlstudents, bg = "#B99470", fg = "maroon")
                self.totalenrolled.place(x=1100,y=300)
                self.after(1000,Totalstudents)
                conn.commit()            
                conn.close()
            except:
                pass
            

#________WINDOW BUTTONS________#
        
        Button1 =ssis.Button(self, text="Course",font=("Garamond",25,"bold"),bd=10,width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Course))
        Button1.place(x=70,y=350)
        Button2 = ssis.Button(self, text="Home",font=("Garamond",25,"bold"),bd=10,width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Home))
        Button2.place(x=70,y=550)
        Button3 =ssis.Button(self, text="Students",font=("Garamond",25,"bold"),bd=10, width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=70,y=450)

        self.totalstudents=Label(self, font=("Inter Black",25,"bold"),height=1, width = 20, bd=5,text="Total No. of Students",anchor=CENTER, bg="#EAE2B7",fg="saddle brown")
        self.totalstudents.place(x=900,y=230)
        
        self.totalcourse=Label(self, font=("Inter Black", 25,"bold"),height =1, width = 20, bd=5, text="Total No. of Course/s",anchor=CENTER, bg="#EAE3B7",fg="saddle brown")
        self.totalcourse.place(x=450,y=230)
        
    
        Totalcourse()
        Totalstudents()
        

#________COURSE FUNCTIONS________#

class Course(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("MSU-IIT STUDENT INFORMATION SYSTEM")

        leftcolor = ssis.Label(self,height = 60,width=200, bg="#B99470")
        leftcolor.place(x=0,y=0)
        label = ssis.Label(self, text = "Course List",bd=6,relief=RIDGE, font=("Garamond",40,"bold"),bg="white smoke", fg="maroon")
        label.place(x=550,y=30)
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def connectCourse():
            conn = sqlite3.connect("StudentDatabase")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            conn = sqlite3.connect("StudentDatabase")
            c = conn.cursor()                
            c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",\
                      (Course_Code.get(),Course_Name.get()))        
            conn.commit()           
            conn.close()
            Course_Code.set('')
            Course_Name.set('') 
            tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Successfully added!")
            displayCourse()
              
        def displayCourse():
            self.courselist.delete(*self.courselist.get_children())
            conn = sqlite3.connect("StudentDatabase")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", ssis.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in self.courselist.selection():
                conn = sqlite3.connect("StudentDatabase")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", \
                            (Course_Code.get(),Course_Name.get(), self.courselist.set(selected, '#1')))    
                conn.commit()
                tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully updated!")
                displayCourse()
                clear()
                conn.close()
                
        def editCourse():
            x = self.courselist.focus()
            if x == "":
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Please select a record.")
                return
            values = self.courselist.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("MSU-IIT STUDENT INFORMATION SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase")
                    cur = con.cursor()
                    x = self.courselist.selection()[0]
                    id_no = self.courselist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.courselist.delete(x)
                    tkinter.messagebox.askyesno("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully deleted!")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "This student already exist in the record")
                
        def searchCourse():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("StudentDatabase")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.courselist.delete(*self.courselist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", ssis.END, text=row[0], values=row[0:])
            con.close()
 
        def Refresh():
            displayCourse()
        
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.courselist.selection()[0]
            values = self.courselist.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
            
#________WINDOW BUTTONS________#

        Button1 =ssis.Button(self, text="Course",font=("Garamond",25,"bold"),bd=10,width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Course))
        Button1.place(x=265,y=550)
        Button2 = ssis.Button(self, text="Home",font=("Garamond",25,"bold"),bd=10,width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Home))
        Button2.place(x=525,y=550)
        Button3 =ssis.Button(self, text="Students",font=("Garamond",25,"bold"),bd=10, width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=790,y=550)
        
#________LABELS AND ENTRIES________#
        
        self.lblCourseCode = Label(self, font=("Palatino roman", 22, "bold"), text="Course Code:", padx=5, pady=5, bg = "#B99470", fg = "black")
        self.lblCourseCode.place(x=30,y=155)
        self.txtCourseCode = Entry(self, font=("Garamond", 25), textvariable=Course_Code, width=15, fg = "#B99470", bg = "white")
        self.txtCourseCode.place(x=290,y=160)

        self.lblCourseName = Label(self, font=("Palatin roman", 22,"bold"), text="Course Name:", padx=5, pady=5, bg = "#B99470", fg = "black")
        self.lblCourseName.place(x=30,y=215)
        self.txtCourseName = Entry(self, font=("Garamond", 25), textvariable=Course_Name, width=15, fg = "#B99470", bg = "white")
        self.txtCourseName.place(x=290,y=220)

        self.SearchBarlbl = Label(self, font=("Palatino roman", 18,"bold"), text="Course Code:", padx=5, pady=5, bg = "#B99470", fg = "black")
        self.SearchBarlbl.place(x=610,y=150)
        self.SearchBar = Entry(self, font=("Garamond", 21), textvariable=SearchBar_Var,width=17, fg = "#B99470", bg = "white" )
        self.SearchBar.place(x=790,y=155)

#________TREEVIEW________#
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1320,y=206,height=262)
        self.courselist = ttk.Treeview(self,columns=("Course Code","Course Name"),height = 12,  yscrollcommand=scrollbar.set)
        self.courselist.heading("Course Code", text="COURSE CODE")
        self.courselist.heading("Course Name", text="COURSE NAME")
        self.courselist['show'] = 'headings'
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Source code",18,"bold"),foreground="saddle  brown")
        style.configure("Treeview",font=("Source code",15))
        style.map('Treeview', background=[('selected', 'burlywood1')], foreground=[('selected', 'saddle brown')])
        self.courselist.column("Course Code", width=200, anchor=W)
        self.courselist.column("Course Name", width=500)
        self.courselist.bind("<Double-1> ", OnDoubleclick)
        self.courselist.place(x=610,y=205)
        scrollbar.config(command=self.courselist.yview)
        
#________COURSE BUTTONS________#

        ButtonFrame=Frame(self, bd=4, bg="#B99470", relief = GROOVE)
        ButtonFrame.place(x=40,y=300, width=500, height=170)
        
        self.btnAddID = Button(ButtonFrame, text="Add", font=("Palatino roman", 20, "bold" ), height=1, width=10, bd=1,bg="burlywood1", fg="black",command=addCourse)
        self.btnAddID.place(x=40,y=10)
        self.btnUpdate = Button(ButtonFrame, text="Update", font=("Palatino roman", 20, "bold"), height=1, width=10, bd=1,bg="burlywood1", fg="black", command=updateCourse) 
        self.btnUpdate.place(x=280,y=10)
        self.btnClear = Button(ButtonFrame, text="Clear", font=("Palatino roman", 20, "bold"), height=1, width=10, bd=1,bg="burlywood1", fg="black", command=clear)
        self.btnClear.place(x=40,y=90)
        self.btnDelete = Button(ButtonFrame, text="Delete", font=("Palatino roman", 20, "bold"), height=1, width=10, bd=1,bg="burlywood1", fg="black", command=deleteCourse)
        self.btnDelete.place(x=280,y=90)
        self.btnSearch = Button(self,text= "Search",font=("Palatino roman", 14,"bold"), height =1, width=10, bg = "burlywood1", fg = "black", command=searchCourse)
        self.btnSearch.place(x=1030,y=155)
        self.btnRefresh = Button(self, text="Refresh", font=('Palatino roman', 14, "bold"), height=1, width=10, bg="burlywood1", fg="black", command=Refresh)
        self.btnRefresh.place(x=1180,y=155)
        
        connectCourse()
        displayCourse()
        
#_______STUDENT FUNCTION________#

class Student(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("STUDENT INFORMATION")

        leftcolor = ssis.Label(self,height = 60,width=200, bg="#B99470")
        leftcolor.place(x=0,y=0)
        label = ssis.Label(self, text = "Student's Information",bd=6,relief=RIDGE, font=("Garamond",40,"bold"),bg="white smoke", fg="maroon")
        label.place(x=430,y=30)

        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()

        def connect():
            conn = sqlite3.connect("StudentDatabase")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS studdatabase (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def addData():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Completely fill the fields")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Oops! Invalid ID Number")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Oops! Invalid ID Number")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("StudentDatabase")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO studdatabase(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully added!")
                                    conn.commit() 
                                    clear()
                                    displayData()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("StudentDatabase")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM studdatabase")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    print(ids)
                                    if ID in ids:
                                       tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "This ID already exist")
                                    else: 
                                       tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                else:
                    tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                 
        def updateData():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("StudentDatabase")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE studdatabase SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully Updated!")
                    displayData()
                    clear()
                    conn.close()
        
        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("MSU-IIT STUDENT INFORMATION SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM studdatabase WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully Deleted!")
                    displayData()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("StudentDatabase")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM studdatabase")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", ssis.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")           
                
        def displayData():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("StudentDatabase")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM studdatabase")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", ssis.END, text=row[0], values=row[0:])
            conn.close()
                            
        def editData():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Please Select a record.")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
            
        def Refresh():
            displayData()
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])

#________WINDOWS BUTTON________#
        
        Button1 =ssis.Button(self, text="Course",font=("Palatino roman",25,"bold"),bd=10,width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Course))
        Button1.place(x=265,y=550)
        Button2 = ssis.Button(self, text="Home",font=("Palatino roman",25,"bold"),bd=10,width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Home))
        Button2.place(x=525,y=550)
        Button3 =ssis.Button(self, text="Students",font=("Palatino roman",25,"bold"),bd=10, width = 10,bg="burlywood1",fg="black",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=790,y=550)

#_______LABELS AND ENTRIES_______#

        InfoFrame=Frame(self, bd=4, bg="#B99470", relief = GROOVE)
        InfoFrame.place(x=60,y=165, width=500, height=250)

        self.lblStudentID = Label(InfoFrame, font=("Palatino roman", 16,"bold"), text="ID No:", padx=5, pady=5, bg = "#B99470", fg = "black", width = 10)
        self.lblStudentID.place(x=10,y=20)
        self.txtStudentID = Entry(InfoFrame, font=("Palatino roman", 16), textvariable=Student_ID, width=26, fg = "black")
        self.txtStudentID.place(x=160,y=25)
        self.txtStudentID.insert(0,'YYYY-NNNN')

        self.lblStudentName = Label(InfoFrame, font=("Palatino roman", 16,"bold"), text="Full Name:", padx=5, pady=5, bg = "#B99470", fg = "black",  width = 10)
        self.lblStudentName.place(x=10,y=65)
        self.txtStudentName = Entry(InfoFrame, font=("Palatino roman", 16), textvariable=Student_Name, width=26, fg = "BLACK")
        self.txtStudentName.place(x=160,y=70)

        self.lblStudentCourse = Label(InfoFrame, font=("Palatino roman", 16,"bold"), text="Course:", padx=5, pady=5, bg = "#B99470", fg = "black",  width = 10)
        self.lblStudentCourse.place(x=10,y=115)
        self.txtStudentCourse = Entry(InfoFrame, font=("Palatino roman", 16), textvariable=Course_Code, width=26, fg = "black")
        self.txtStudentCourse.place(x=160,y=120)

        self.lblStudentYearLevel = Label(InfoFrame, font=("Palatino roman", 16,"bold"), text="YearLevel:", padx=5, pady=5, bg = "#B99470", fg = "black",  width = 10)
        self.lblStudentYearLevel.place(x=10,y=155)
        ttk.Style().layout('combostyleO.TCombobox')
        ttk.Style().configure('combostyleO.TCombobox', selectforeground='black', selectbackground='white',  foreground='black')
        self.txtStudentYearLevel = ttk.Combobox(InfoFrame,value=["I", "II", "III", "IV","V"],state="readonly", font=("Palatino roman", 16), textvariable=Student_YearLevel,width=25, style="combostyleO.TCombobox")
        self.txtStudentYearLevel.place(x=160,y=160)
        
        self.lblStudentGender = Label(InfoFrame, font=("Source code", 16,"bold"), text="Gender:", padx=5, pady=5, bg = "#B99470", fg = "black",  width = 10)
        self.lblStudentGender.place(x=10,y=200)
        self.txtStudentGender = ttk.Combobox(InfoFrame, value=["Male", "Female"], font=("Palatino roman", 16),state="readonly", textvariable=Student_Gender, width=25, style="combostyleO.TCombobox")
        self.txtStudentGender.place(x=160,y=205)

        self.SearchBarlbl = Label(self, font=("Palatino roman", 16,"bold"), text="ID Number:", padx=2, pady=2, bg = "#B99470", fg = "black")
        self.SearchBarlbl.place(x=590,y=165)        
        self.SearchBar = Entry(self, font=("Palatino roman", 16), textvariable=SearchBar_Var,width=25, fg = "black")
        self.SearchBar.place(x=725,y=170)

#______TREE VIEW_______#
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1270,y=216,height=304)
        self.studentlist = ttk.Treeview(self,columns=("ID Number", "Name", "Gender", "Year Level", "Course"),height =14,yscrollcommand=scrollbar.set)
        self.studentlist.heading("ID Number", text="ID Number", anchor=CENTER)
        self.studentlist.heading("Name", text="Name",anchor=CENTER)
        self.studentlist.heading("Gender", text="Course",anchor=CENTER)
        self.studentlist.heading("Year Level", text="Year Level",anchor=CENTER)
        self.studentlist.heading("Course", text="Gender",anchor=CENTER)
        self.studentlist['show'] = 'headings'
        self.studentlist.column("ID Number", width=130, anchor=CENTER)
        self.studentlist.column("Name", width=200, anchor=CENTER)
        self.studentlist.column("Course", width=100, anchor=CENTER)
        self.studentlist.column("Year Level", width=145, anchor=CENTER)
        self.studentlist.column("Gender", width=105, anchor=CENTER)
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        self.studentlist.place(x=580,y=215)
        scrollbar.config(command=self.studentlist.yview)
        
#________STUDENT BUTTONS______#

        ButtonFrame=Frame(self, bd=4, bg="#B99470", relief = GROOVE)
        ButtonFrame.place(x=60,y=445, width=500, height=75)

        self.btnAddID = Button(ButtonFrame, text="Add", font=('Palatino roman', 14, "bold" ), height=1, width=7, bd=1,bg="burlywood1", fg="black",command=addData)
        self.btnAddID.place(x=7,y= 10)
        self.btnUpdate = Button(ButtonFrame, text="Update", font=('Palatino roman', 14, "bold"), height=1, width=7, bd=1,bg="burlywood1", fg="black", command=updateData) 
        self.btnUpdate.place(x=264,y=10)
        self.btnClear = Button(ButtonFrame, text="Clear", font=('Palatino roman', 14, "bold"), height=1, width=7, bd=1,bg="burlywood1", fg="black", command=clear)
        self.btnClear.place(x=133,y=10)
        self.btnDelete = Button(ButtonFrame, text="Delete", font=('Palatino roman', 14, "bold"), height=1, width=7, bd=1,bg="burlywood1", fg="black", command=deleteData)
        self.btnDelete.place(x=398,y=10)
        self.btnSearch = Button(self,text= "Search",font=("Palatino roman", 14,"bold"), height=1, width=7, bg = "burlywood1", fg = "black", command=searchData)
        self.btnSearch.place(x=1040,y=165)
        self.btnRefresh = Button(self, text="Refresh", font=('Palatino roman', 14, "bold"), height=1, width=7, bg="burlywood1", fg="black", command=Refresh)
        self.btnRefresh.place(x=1150,y=165)
        
        connect()
        displayData()

app = AppDatabase()
app.geometry("1650x650+0+0")
app.mainloop()

