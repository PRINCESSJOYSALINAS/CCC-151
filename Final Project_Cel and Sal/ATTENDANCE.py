import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import time
import datetime
from PIL import Image, ImageTk, ImageSequence
from tkinter import Label, RIDGE
from tkinter import messagebox


conn = sqlite3.connect("ydatabase.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS courses (course_code TEXT PRIMARY KEY, course_name TEXT NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS students (student_id TEXT PRIMARY KEY, year_level TEXT, first_name TEXT, middle_name TEXT, surname TEXT, gender TEXT, course_code TEXT, FOREIGN KEY (course_code) REFERENCES courses(course_code))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS activities (activity_name TEXT PRIMARY KEY, academic_year TEXT, duration TEXT, semester TEXT, location TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS attends (student_id TEXT, activity_name TEXT, sign_in_time DATETIME, sign_out_time DATETIME, FOREIGN KEY (student_id) REFERENCES students(student_id), FOREIGN KEY (activity_name) REFERENCES activities(activity_name))''')



class Attendance(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Attendance")
        self.geometry("1537x790")
        self.current_time = tk.StringVar()
        self.current_date = tk.StringVar()
        
        all_frame = tk.Frame(self)
        all_frame.pack(side="top", fill="both", expand = True)
        all_frame.rowconfigure(0, weight=1)
        all_frame.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Home, Course, Student, Activities, Attends):
            frame = F(all_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show(Home)
    def show(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        img1 = Image.open(r"C:\Users\Cristine Joy Ebcay\Documents\Final Project_Cel and Sal\welcome.png")
        img1 = img1.resize((1080, 790), Image.BICUBIC)

        self.photoimg1 = ImageTk.PhotoImage(img1)
        lblimg = Label(self, image=self.photoimg1, bd=0, relief=RIDGE)
        lblimg.place(x=0, y=5, width=1080, height=790)

      
        label = tk.Label(self, borderwidth=8, relief="raised", font=("Algerian", 29), bg=("#4D0B0B"), fg=("lightslategray"))
        label.place(x=1080,y=0,width=457,height=790)
        
        button_courses = tk.Button(self, text="COURSE", font=("Courier", 16), bd=9, width=20, height=1,
                                   fg="white", bg="#930606", relief='ridge',
                                   command=lambda: controller.show(Course))
        button_courses.place(x=1170, y=175)
        button_courses.config(cursor="hand2")
        
        button_student = tk.Button(self, text="STUDENT INFORMATION", font=("Courier", 16), bd=9, width=20, height=1,
                        fg="white", bg="#930606", relief='ridge',
                        command=lambda: controller.show(Student))
        button_student.place(x=1170, y=250)
        button_student.config(cursor="hand2")
        
        button_activities = tk.Button(self, text="ACTIVITIES", font=("Courier", 16), bd=9, width=20, height=1,
                        fg="white", bg="#930606", relief='ridge',
                        command=lambda: controller.show(Activities))
        button_activities.place(x=1170, y=325)
        button_activities.config(cursor="hand2")

        button_attends = tk.Button(self, text="ATTENDS", font=("Courier", 16), bd=9, width=20, height=1,
                                   fg="white", bg="#930606", relief='ridge',
                                   command=lambda: controller.show(Attends))
        button_attends.place(x=1170, y=400)
        button_attends.config(cursor="hand2")

        button_exit = tk.Button(self, text="EXIT", font=("Courier", 16), bd=9, width=20,
                                height=1, fg="white", bg="#930606", relief='ridge',
                                command=iExit)
        button_exit.place(x=1170, y=475)
        button_exit.config(cursor="hand2") 
        
        def time1():
            time_string = time.strftime("%H:%M:%S")
            date_string = time.strftime("%d:%m:%y")
            clock.config(text="Time: "+time_string+"\n""Date: "+date_string, font =('Arial', 15, 'bold'))
            clock.after(200, time1)

        clock = Label(self, font = ('Times', 14, 'bold'), width = 15, relief = RIDGE, background = "#000000", foreground = 'white')
        clock.place(x = 1170, y = 50, width = 280)
        time1()



class Course(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, font=("Times New Roman", 40), bg="#4D0B0B", fg="#930606")
        label.place(x=0, y=0, width=1537, height=800)

        self.lblccode = tk.Label(self, font=("Times New Roman", 30, "bold"), bd=5, bg="#930606", fg="white", text="COURSE", padx=2, pady=4)
        self.lblccode.place(x=360, y=20, width=800)
        
        home_icon = Image.open(r"C:\Users\Cristine Joy Ebcay\Documents\Final Project_Cel and Sal\Bahay.jpg")
        home_icon = home_icon.resize((65, 65), Image.BICUBIC)
        self.photoimg_search1 = ImageTk.PhotoImage(home_icon)
        
        home = tk.Button(self, text="HOME", font=("Lucida Console", 13, "bold"), bd=5, width=60, image=self.photoimg_search1, bg="#930606", fg="white", command=lambda: controller.show(Home))
        home.place(x=1470, y=50, height=65, anchor="center")
        home.config(cursor="hand2")

        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("CourseCode", "CourseName")
        self.tree.column("#0", width=0, stretch="NO")
        self.tree.column("CourseCode", anchor="w")
        self.tree.column("CourseName", anchor="w")
        self.tree.heading("CourseCode", text="Course Code")
        self.tree.heading("CourseName", text="Course Name")
        self.tree.place(x=30, y=100, width=640, height=550)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=660, y=100, height=550)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.populate_treeview()

        self.course_code_entry = tk.Entry(self)
        self.course_code_entry.place(x=1000, y=150, width=350, height=40)
        self.course_code_label = tk.Label(self, text="Course Code:", font=("Sans-serif", 16, "bold"), bg="#930606", fg="white")
        self.course_code_label.place(x=850, y=155)

        self.course_name_entry = tk.Entry(self)
        self.course_name_entry.place(x=1000, y=220, width=350, height=40)
        self.course_name_label = tk.Label(self, text="Course Name:", font=("Sans-serif", 16, "bold"), bg="#930606", fg="white")
        self.course_name_label.place(x=848, y=225)

        self.add_course_button = tk.Button(self, text="Add Course", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.add_course)
        self.add_course_button.place(x=800, y=450, width=300, height=70)

        self.delete_course_button = tk.Button(self, text="Delete Course", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.delete_course)
        self.delete_course_button.place(x=1125, y=450, width=300, height=70)

        self.edit_course_button = tk.Button(self, text="Edit Course", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.edit_course)
        self.edit_course_button.place(x=800, y=540, width=300, height=70)

        self.update_course_button = tk.Button(self, text="Update Course", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.update_course)
        self.update_course_button.place(x=1125, y=540, width=300, height=70)

        self.display_all_button = tk.Button(self, text="Display All", font=("Lucida Console", 11, "bold"), bd=4, width=16, bg="#930606", fg="white", command=self.populate_treeview)
        self.display_all_button.place(x=1190, y=350, width=120, height=40)

        self.clear_button = tk.Button(self, text="Clear", font=("Lucida Console", 11, "bold"), bd=4, width=16, bg="#930606", fg="white", command=self.clear_entries)
        self.clear_button.place(x=1320, y=350, width=100, height=40)

        self.search_entry = tk.Entry(self)
        self.search_entry.place(x=910, y=350, width=270, height=40)
        
        search_icon = Image.open(r"C:\Users\Cristine Joy Ebcay\Documents\Final Project_Cel and Sal\search bar.png")
        search_icon = search_icon.resize((35, 35), Image.BICUBIC)
        self.photoimg_search2 = ImageTk.PhotoImage(search_icon)

        self.search_button = tk.Button(self, text="Search", font=("Lucida Console", 11, "bold"), bd=4, width=16, image=self.photoimg_search2, bg="#930606", fg="white", command=self.search_course)
        self.search_button.place(x=800, y=350, width=100, height=40)

        self.selected_course = None

        self.tree.bind("<ButtonRelease-1>", self.select_course)
        

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        for course in courses:
            self.tree.insert("", "end", values=course)

    def add_course(self):
        course_code = self.course_code_entry.get()
        course_name = self.course_name_entry.get()

        if not course_code or not course_name:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            conn = sqlite3.connect("ydatabase.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM courses WHERE course_code=?", (course_code,))
            existing_course = cursor.fetchone()
            
            if existing_course:
                messagebox.showerror("Error", "The course already exists.")
            else:
                cursor.execute("INSERT INTO courses (course_code, course_name) VALUES (?, ?)", (course_code, course_name))
                conn.commit()
                self.populate_treeview()
                self.clear_entries()
                messagebox.showinfo("Success", "Course Added Successfully!")

        conn.close()

    def delete_course(self):
        try:
            if self.selected_course:
                course_code = self.selected_course[0]
                confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this course?")
                if confirmation:
                    conn = sqlite3.connect("ydatabase.db")
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT student_id FROM students WHERE course_code=?", (course_code,))
                    enrolled_students = cursor.fetchall()
                    
                    if enrolled_students:
                        messagebox.showerror("Error", "Cannot delete the course. Students are still enrolled in this course.")
                    else:
                        cursor.execute("PRAGMA foreign_keys = ON")
                        cursor.execute("DELETE FROM courses WHERE course_code=?", (course_code,))
                        conn.commit()
                        self.populate_treeview()
                        self.clear_entries()
                        messagebox.showinfo("Success", "Course deleted successfully!")
                    
                    conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))
   
                
    def edit_course(self):
        if self.selected_course:
            self.edit_mode = True
            self.course_code_entry.delete(0, tk.END)
            self.course_name_entry.delete(0, tk.END)
            self.course_code_entry.insert(0, self.selected_course[0])
            self.course_name_entry.insert(0, self.selected_course[1])
        else:
            messagebox.showerror("Error", "Please select a course to edit.")

    def update_course(self):
        if hasattr(self, 'edit_mode') and self.edit_mode:
            if self.selected_course:
                course_code = self.selected_course[0]
                new_course_name = self.course_name_entry.get()

                cursor.execute("UPDATE courses SET course_name=? WHERE course_code=?",
                            (new_course_name, course_code))
                conn.commit()
                self.populate_treeview()
                self.clear_entries()
                self.edit_mode = False
                messagebox.showinfo("Success", "Course updated successfully!")
            else:
                messagebox.showerror("Error", "Please select a course to update.")
        else:
            messagebox.showerror("Error", "Please click the Edit button first.")

    def search_course(self):
        search_term = self.search_entry.get()
        cursor.execute("SELECT * FROM courses WHERE course_code LIKE ? OR course_name LIKE ?",
                    (f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_entries(self):
        self.course_code_entry.delete(0, tk.END)
        self.course_name_entry.delete(0, tk.END)
        self.selected_course = None

    def select_course(self, event):
        selected_item = self.tree.focus()
        course_values = self.tree.item(selected_item)['values']
        if course_values:
            self.selected_course = course_values
        else:
            self.selected_course = None
            
            
class Student(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, font=("Times New Roman", 40), bg="#4D0B0B", fg="#930606")
        label.place(x=0, y=0, width=1537, height=790)

        self.lblccode = tk.Label(self, font=("Times New Roman", 30, "bold"), bd=5, bg="#930606", fg="white", text="STUDENT INFORMATION", padx=2, pady=4)
        self.lblccode.place(x=360, y=26, width=800)

        home_icon = Image.open(r"C:\Users\Cristine Joy Ebcay\Documents\Final Project_Cel and Sal\Bahay.jpg")
        home_icon = home_icon.resize((65, 65), Image.BICUBIC)
        self.photoimg_search1 = ImageTk.PhotoImage(home_icon)
        
        home = tk.Button(self, text="HOME", font=("Lucida Console", 13, "bold"), bd=5, width=60, image=self.photoimg_search1, bg="#930606", fg="white", command=lambda: controller.show(Home))
        home.place(x=1470, y=50, height=65, anchor="center")
        home.config(cursor="hand2")



        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("StudentID", "YearLevel", "FirstName", "MiddleName", "Surname", "Gender", "CourseCode")
        self.tree.column("#0", width=0, stretch="NO")
        self.tree.column("StudentID", anchor="w")
        self.tree.column("YearLevel", anchor="w")
        self.tree.column("FirstName", anchor="w")
        self.tree.column("MiddleName", anchor="w")
        self.tree.column("Surname", anchor="w")
        self.tree.column("Gender", anchor="w")
        self.tree.column("CourseCode", anchor="w")
        self.tree.heading("StudentID", text="Student ID")
        self.tree.heading("YearLevel", text="Year Level")
        self.tree.heading("FirstName", text="First Name")
        self.tree.heading("MiddleName", text="Middle Name")
        self.tree.heading("Surname", text="Surname")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("CourseCode", text="Course Code")
        self.tree.place(x=30, y=100, width=1300, height=225)

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=1330, y=100, height=225)

        # Configure the treeview to use the scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.populate_treeview()

        self.student_id_entry = tk.Entry(self)
        self.student_id_entry.place(x=300, y=350, width=350, height=30)
        self.student_id_label = tk.Label(self, text="Student ID:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.student_id_label.place(x=35, y=350)

        self.year_level_entry = tk.Entry(self)
        self.year_level_entry.place(x=300, y=400, width=350, height=30)
        self.year_level_label = tk.Label(self, text="Year Level:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.year_level_label.place(x=35, y=400)

        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.place(x=300, y=450, width=350, height=30)
        self.first_name_label = tk.Label(self, text="First Name:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.first_name_label.place(x=35, y=450)

        self.middle_name_entry = tk.Entry(self)
        self.middle_name_entry.place(x=300, y=500, width=350, height=30)
        self.middle_name_label = tk.Label(self, text="Middle Name:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.middle_name_label.place(x=35, y=500)

        self.surname_entry = tk.Entry(self)
        self.surname_entry.place(x=300, y=550, width=350, height=30)
        self.surname_label = tk.Label(self, text="Surname:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.surname_label.place(x=35, y=550)

        self.gender_entry = tk.Entry(self)
        self.gender_entry.place(x=300, y=600, width=350, height=30)
        self.gender_label = tk.Label(self, text="Gender:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.gender_label.place(x=35, y=600)

        self.course_code_entry = tk.Entry(self)
        self.course_code_entry.place(x=300, y=650, width=350, height=30)
        self.course_code_label = tk.Label(self, text="Course Code:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.course_code_label.place(x=35, y=650)

        self.add_student_button = tk.Button(self, text="Add Student", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.add_student)
        self.add_student_button.place(x=700, y=450, width=300, height=70)

        self.delete_student_button = tk.Button(self, text="Delete Student", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.delete_student)
        self.delete_student_button.place(x=1025, y=450, width=300, height=70)

        self.edit_student_button = tk.Button(self, text="Edit Student", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.edit_student)
        self.edit_student_button.place(x=700, y=540, width=300, height=70)

        self.update_student_button = tk.Button(self, text="Update Student", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.update_student)
        self.update_student_button.place(x=1025, y=540, width=300, height=70)

        self.display_all_button = tk.Button(self, text="Display All", font=("Lucida Console", 11, "bold"), bd=4, width=16, bg="#930606", fg="white", command=self.populate_treeview)
        self.display_all_button.place(x=1090, y=350, width=120, height=40)

        self.clear_button = tk.Button(self, text="Clear", font=("Lucida Console", 11, "bold"), bd=4, width=16, bg="#930606", fg="white", command=self.clear_entries)
        self.clear_button.place(x=1220, y=350, width=100, height=40)

        self.search_entry = tk.Entry(self)
        self.search_entry.place(x=810, y=350, width=270, height=40)

        self.search_button = tk.Button(self, text="Search", font=("Lucida Console", 11, "bold"), bd=4, width=16, bg="#930606", fg="white", command=self.search_student)
        self.search_button.place(x=700, y=350, width=100, height=40)

        self.selected_student = None

        self.tree.bind("<ButtonRelease-1>", self.select_student)

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        for student in students:
            self.tree.insert("", "end", values=student)

    def add_student(self):
        student_id = self.student_id_entry.get()
        year_level = self.year_level_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        surname = self.surname_entry.get()
        gender = self.gender_entry.get()
        course_code = self.course_code_entry.get()

        # Check if any of the fields are empty
        if not student_id or not year_level or not first_name or not middle_name or not surname or not gender or not course_code:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            # Check if the student ID already exists
            cursor.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
            result = cursor.fetchone()

            if result is not None:
                messagebox.showerror("Error", "Student ID already exists. Please choose a different ID.")
            else:
                # Check if the course code exists in the courses table
                cursor.execute("SELECT course_code FROM courses WHERE course_code = ?", (course_code,))
                course_result = cursor.fetchone()

                if course_result is None:
                    messagebox.showerror("Error", "Course Code does not exist. Please enter a valid Course Code.")
                else:
                    cursor.execute("INSERT INTO students (student_id, year_level, first_name, middle_name, surname, gender, course_code) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                   (student_id, year_level, first_name, middle_name, surname, gender, course_code))
                    conn.commit()
                    self.populate_treeview()
                    self.clear_entries()
                    messagebox.showinfo("Success", "Student added successfully!")

    def delete_student(self):
        if self.selected_student:
            student_id = self.selected_student[0]
            
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this attendance record?")
            if confirmation:
                conn = sqlite3.connect("ydatabase.db")
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM attends WHERE student_id=?", (student_id,))
                conn.commit()
                
                cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
                conn.commit()

                conn.close()
                self.populate_treeview()
                self.clear_entries()
                messagebox.showinfo("Success", "Student and attendance record deleted successfully!")
        else:
            messagebox.showerror("Error", "Please select an attendance record to delete.")


    def edit_student(self):
        if self.selected_student:
            self.edit_mode = True
            self.student_id_entry.delete(0, tk.END)
            self.year_level_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.middle_name_entry.delete(0, tk.END)
            self.surname_entry.delete(0, tk.END)
            self.gender_entry.delete(0, tk.END)
            self.course_code_entry.delete(0, tk.END)

            self.student_id_entry.insert(0, self.selected_student[0])
            self.year_level_entry.insert(0, self.selected_student[1])
            self.first_name_entry.insert(0, self.selected_student[2])
            self.middle_name_entry.insert(0, self.selected_student[3])
            self.surname_entry.insert(0, self.selected_student[4])
            self.gender_entry.insert(0, self.selected_student[5])
            self.course_code_entry.insert(0, self.selected_student[6])
        else:
            messagebox.showerror("Error", "Please select a student to edit.")

    def update_student(self):
        if hasattr(self, 'edit_mode') and self.edit_mode:
            if self.selected_student:
                student_id = self.selected_student[0]
                new_year_level = self.year_level_entry.get()
                new_first_name = self.first_name_entry.get()
                new_middle_name = self.middle_name_entry.get()
                new_surname = self.surname_entry.get()
                new_gender = self.gender_entry.get()
                new_course_code = self.course_code_entry.get()

                cursor.execute("UPDATE students SET year_level=?, first_name=?, middle_name=?, surname=?, gender=?, course_code=? WHERE student_id=?",
                            (new_year_level, new_first_name, new_middle_name, new_surname, new_gender, new_course_code, student_id))
                conn.commit()
                self.populate_treeview()
                self.clear_entries()
                self.edit_mode = False
                messagebox.showinfo("Success", "Student updated successfully!")
            else:
                messagebox.showerror("Error", "Please select a student to update.")
        else:
            messagebox.showerror("Error", "Please click the Edit button first.")

    def search_student(self):
        search_term = self.search_entry.get()
        cursor.execute("SELECT * FROM students WHERE student_id LIKE ? OR first_name LIKE ? OR middle_name LIKE ? OR surname LIKE ? OR course_code LIKE ?",
                    (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.year_level_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.middle_name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.course_code_entry.delete(0, tk.END)
        self.selected_student = None

    def select_student(self, event):
        selected_item = self.tree.focus()
        student_values = self.tree.item(selected_item)['values']
        if student_values:
            self.selected_student = student_values
        else:
            self.selected_student = None
            
class Activities(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Main Color for the Home Page
        label = tk.Label(self, font=("Times New Roman", 40), bg=("#4D0B0B"), fg=("#930606"))
        label.place(x=0, y=0, width=1537, height=790)
        
        # Top Title Frame
        self.lblccode = tk.Label(self, font=("Times New Roman", 30, "bold"), bd=5, bg=("#930606"), fg=("white"), text="ACTIVITIES INFORMATION", padx=2, pady=4)
        self.lblccode.place(x=360, y=26, width=800)
        
        # Home Button
        home_icon = Image.open(r"C:\Users\Cristine Joy Ebcay\Documents\Final Project_Cel and Sal\Bahay.jpg")
        home_icon = home_icon.resize((65, 65), Image.BICUBIC)
        self.photoimg_search1 = ImageTk.PhotoImage(home_icon)
        
        home = tk.Button(self, text="HOME", font=("Lucida Console", 13, "bold"), bd=5, width=60, image=self.photoimg_search1, bg="#930606", fg="white", command=lambda: controller.show(Home))
        home.place(x=1470, y=50, height=65, anchor="center")
        home.config(cursor="hand2")


        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("ActivityName", "ActivityYear", "Duration", "Semester", "Location")
        self.tree.column("#0", width=0, stretch="NO")
        self.tree.column("ActivityName", anchor="w")
        self.tree.column("ActivityYear", anchor="w")
        self.tree.column("Duration", anchor="w")
        self.tree.column("Semester", anchor="w")
        self.tree.column("Location", anchor="w")
        self.tree.heading("ActivityName", text="Activity Name")
        self.tree.heading("ActivityYear", text="Activity Year")
        self.tree.heading("Duration", text="Duration")
        self.tree.heading("Semester", text="Semester")
        self.tree.heading("Location", text="Location")
        self.tree.place(x=30, y=100, width=1300, height=225)     

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=1330, y=100, height=225)

        # Configure the treeview to use the scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.populate_treeview()

        self.activity_name_entry = tk.Entry(self)
        self.activity_name_entry.place(x=300, y=350, width=350, height=30)
        self.activity_name_label = tk.Label(self, text="Activity Name:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.activity_name_label.place(x=35, y=350)

        self.academic_year_entry = tk.Entry(self)
        self.academic_year_entry.place(x=300, y=400, width=350, height=30)
        self.academic_year_label = tk.Label(self, text="Activity Year:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.academic_year_label.place(x=35, y=400)

        self.duration_entry = tk.Entry(self)
        self.duration_entry.place(x=300, y=450, width=350, height=30)
        self.duration_label = tk.Label(self, text="Duration:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.duration_label.place(x=35, y=450)

        self.semester_entry = tk.Entry(self)
        self.semester_entry.place(x=300, y=500, width=350, height=30)
        self.semester_label = tk.Label(self, text="Semester:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.semester_label.place(x=35, y=500)

        self.location_entry = tk.Entry(self)
        self.location_entry.place(x=300, y=550, width=350, height=30)
        self.location_label = tk.Label(self, text="Location:", font=("Sans-serif", 15, "bold"), bg="#930606", fg="white")
        self.location_label.place(x=35, y=550)

        self.add_activity_button = tk.Button(self, text="Add Activity", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.add_activity)
        self.add_activity_button.place(x=700, y=450, width=300, height=70)
        
        self.delete_activity_button = tk.Button(self, text="Delete Activity", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.delete_activity)
        self.delete_activity_button.place(x=1025, y=450, width=300, height=70)

        self.edit_activity_button = tk.Button(self, text="Edit Activity", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.edit_activity)
        self.edit_activity_button.place(x=700, y=540, width=300, height=70)

        self.update_activity_button = tk.Button(self, text="Update Activity", font=("Lucida Console", 12, "bold"), bd=6, width=16, bg="#930606", fg="white", command=self.update_activity)
        self.update_activity_button.place(x=1025, y=540, width=300, height=70)

        self.display_all_button = tk.Button(self, text="Display All", font=("Lucida Console", 11, "bold"), bd=4, width=16, bg="#930606", fg="white", command=self.populate_treeview)
        self.display_all_button.place(x=1090, y=350, width=120, height=40)

        self.search_entry = tk.Entry(self)
        self.search_entry.place(x=810, y=350, width=270, height=40)

        self.search_button = tk.Button(self, text="Search", font=("Lucida Console", 11, "bold"), bd=4, width=16, bg="#930606", fg="white", command=self.search_activity)
        self.search_button.place(x=700, y=350, width=100, height=40)

        self.selected_activity = None

        self.tree.bind("<ButtonRelease-1>", self.select_activity)

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM activities")
        activities = cursor.fetchall()

        for activity in activities:
            self.tree.insert("", "end", values=activity)

    def add_activity(self):
        activity_name = self.activity_name_entry.get()
        academic_year = self.academic_year_entry.get()
        duration = self.duration_entry.get()
        semester = self.semester_entry.get()
        location = self.location_entry.get()

        # Check if any of the fields are empty
        if not activity_name or not academic_year or not duration or not semester or not location:
            messagebox.showerror("Error", "Please fill in all required fields.")
        else:
            # Check if the activity name already exists
            cursor.execute("SELECT activity_name FROM activities WHERE activity_name = ?", (activity_name,))
            result = cursor.fetchone()

            if result is not None:
                messagebox.showerror("Error", "Activity name already exists. Please choose a different name.")
            else:
                cursor.execute("INSERT INTO activities (activity_name, academic_year, duration, semester, location) VALUES (?, ?, ?, ?, ?)",
                               (activity_name, academic_year, duration, semester, location))
                conn.commit()
                self.populate_treeview()
                self.clear_entries()
                messagebox.showinfo("Success", "Activity added successfully!")

    def delete_activity(self):
        if self.selected_activity:
            activity_name = self.selected_activity[0]

            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this activity?")
            if confirmation:
                cursor.execute("DELETE FROM activities WHERE activity_name=?", (activity_name,))
                conn.commit()
                self.populate_treeview()
                self.clear_entries()
                messagebox.showinfo("Success", "Activity deleted successfully!")
        else:
            messagebox.showerror("Error", "Please select an activity to delete.")

    def edit_activity(self):
        if self.selected_activity:
            self.edit_mode = True
            self.activity_name_entry.delete(0, tk.END)
            self.academic_year_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.semester_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)
            self.activity_name_entry.insert(0, self.selected_activity[0])
            self.academic_year_entry.insert(0, self.selected_activity[1])
            self.duration_entry.insert(0, self.selected_activity[2])
            self.semester_entry.insert(0, self.selected_activity[3])
            self.location_entry.insert(0, self.selected_activity[4])
        else:
            messagebox.showerror("Error", "Please select an activity to edit.")

    def update_activity(self):
        if hasattr(self, 'edit_mode') and self.edit_mode:
            if self.selected_activity:
                activity_name = self.selected_activity[0]
                new_academic_year = self.academic_year_entry.get()
                new_duration = self.duration_entry.get()
                new_semester = self.semester_entry.get()
                new_location = self.location_entry.get()

                cursor.execute("UPDATE activities SET academic_year=?, duration=?, semester=?, location=? WHERE activity_name=?",
                               (new_academic_year, new_duration, new_semester, new_location, activity_name))
                conn.commit()
                self.populate_treeview()
                self.clear_entries()
                self.edit_mode = False
                messagebox.showinfo("Success", "Activity updated successfully!")
            else:
                messagebox.showerror("Error", "Please select an activity to update.")
        else:
            messagebox.showerror("Error", "Please click the Edit button first.")

    def search_activity(self):
        search_term = self.search_entry.get()
        cursor.execute("SELECT * FROM activities WHERE activity_name LIKE ? OR academic_year LIKE ? OR duration LIKE ? OR semester LIKE ? OR location LIKE ?",
                       (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_entries(self):
        self.activity_name_entry.delete(0, tk.END)
        self.academic_year_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.semester_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.selected_activity = None

    def select_activity(self, event):
        selected_item = self.tree.focus()
        activity_values = self.tree.item(selected_item)['values']
        if activity_values:
            self.selected_activity = activity_values
        else:
            self.selected_activity = None
          
class Attends(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, font=("Times New Roman", 40), bg="#4D0B0B", fg="#930606")
        label.place(x=0, y=0, width=1537, height=800)

        self.lblccode = tk.Label(self, font=("Times New Roman", 30, "bold"), bd=5, bg="#930606", fg="white", text="ATTENDANCE", padx=2, pady=4)
        self.lblccode.place(x=360, y=26, width=800)

        home_icon = Image.open(r"C:\Users\Cristine Joy Ebcay\Documents\Final Project_Cel and Sal\Bahay.jpg")
        home_icon = home_icon.resize((65, 65), Image.BICUBIC)
        self.photoimg_search1 = ImageTk.PhotoImage(home_icon)
        
        home = tk.Button(self, text="HOME", font=("Lucida Console", 13, "bold"), bd=5, width=60, image=self.photoimg_search1, bg="#930606", fg="white", command=lambda: controller.show(Home))
        home.place(x=1470, y=50, height=65, anchor="center")
        home.config(cursor="hand2")


        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("StudentID", "ActivityName", "SignInTime", "SignOutTime")
        self.tree.column("#0", width=0, stretch="NO")
        self.tree.column("StudentID", anchor="w")
        self.tree.column("ActivityName", anchor="w")
        self.tree.column("SignInTime", anchor="w")
        self.tree.column("SignOutTime", anchor="w")
        self.tree.heading("StudentID", text="Student ID")
        self.tree.heading("ActivityName", text="Activity Name")
        self.tree.heading("SignInTime", text="Sign In Time")
        self.tree.heading("SignOutTime", text="Sign Out Time")
        self.tree.place(x=30, y=100, width=1300, height=225)     

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=1330, y=100, height=225)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.populate_treeview()

        self.student_id_entry = tk.Entry(self)
        self.student_id_entry.place(x=300, y=350, width=350, height=30)
        self.student_id_label = tk.Label(self, text="Student ID:", font=("Sans-serif",15,"bold"), bg="#930606", fg="white")
        self.student_id_label.place(x=35, y=350)

        self.activity_name_entry = tk.Entry(self)
        self.activity_name_entry.place(x=300, y=400, width=350, height=30)
        self.activity_name_label = tk.Label(self, text="Activity Name:", font=("Sans-serif",15,"bold"), bg="#930606", fg="white")
        self.activity_name_label.place(x=35, y=400)

        self.sign_in_time_entry = tk.Entry(self)
        self.sign_in_time_entry.place(x=300, y=450, width=350, height=30)
        self.sign_in_time_label = tk.Label(self, text="Sign In Time:", font=("Sans-serif",15,"bold"), bg="#930606", fg="white")
        self.sign_in_time_label.place(x=35, y=450)

        self.sign_out_time_entry = tk.Entry(self)
        self.sign_out_time_entry.place(x=300, y=500, width=350, height=30)
        self.sign_out_time_label = tk.Label(self, text="Sign Out Time:", font=("Sans-serif",15,"bold"), bg="#930606", fg="white")
        self.sign_out_time_label.place(x=35, y=500)

        self.add_attendance_button = tk.Button(self, text="Add Attendance", font=("Lucida Console",12,"bold"),bd=6, width = 16, bg="#930606", fg="white", command=self.add_attendance)
        self.add_attendance_button.place(x=700, y=450, width=300, height=70)
        
        self.delete_attendance_button = tk.Button(self, text="Delete Attendance", font=("Lucida Console",12,"bold"),bd=6, width = 16, bg="#930606", fg="white", command=self.delete_attendance)
        self.delete_attendance_button.place(x=1025, y=450, width=300, height=70)

        self.edit_attendance_button = tk.Button(self, text="Edit Attendance", font=("Lucida Console",12,"bold"),bd=6, width = 16, bg="#930606", fg="white", command=self.edit_attendance)
        self.edit_attendance_button.place(x=700, y=540, width=300, height=70)

        self.update_attendance_button = tk.Button(self, text="Update Attendance", font=("Lucida Console",12,"bold"),bd=6, width = 16, bg="#930606", fg="white", command=self.update_attendance)
        self.update_attendance_button.place(x=1025, y=540, width=300, height=70)

        self.display_all_button = tk.Button(self, text="Display All", font=("Lucida Console",11,"bold"),bd=4, width = 16, bg="#930606", fg="white", command=self.populate_treeview)
        self.display_all_button.place(x=1090, y=350, width=120, height=40)

        self.clear_button = tk.Button(self, text="Clear", font=("Lucida Console",11,"bold"),bd=4, width = 16, bg="#930606", fg="white", command=self.clear_entries)
        self.clear_button.place(x=1220, y=350, width=100, height=40)
        
        self.search_entry = tk.Entry(self)
        self.search_entry.place(x=810, y=350, width=270, height=40)

        self.search_button = tk.Button(self, text="Search", font=("Lucida Console",11,"bold"),bd=4, width = 16, bg="#930606", fg="white", command=self.search_attendance)
        self.search_button.place(x=700, y=350, width=100, height=40)

        self.selected_attendance = None

        self.tree.bind("<ButtonRelease-1>", self.select_attendance)
        
        def time1():
            time_string = time.strftime("%H:%M:%S")
            date_string = time.strftime("%d:%m:%y")
            clock.config(text="Time: "+time_string+"\n""Date: "+date_string, font =('Arial', 15, 'bold'))
            clock.after(200, time1)

        clock = Label(self, font = ('Times', 14, 'bold'), width = 15, relief = RIDGE, background = "#000000", foreground = 'white')
        clock.place(x = 30, y = 30, width = 280)
        time1()

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM attends")
        attendance_records = cursor.fetchall()

        for record in attendance_records:
            self.tree.insert("", "end", values=record)

    def add_attendance(self):
        student_id = self.student_id_entry.get()
        activity_name = self.activity_name_entry.get()
        sign_in_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sign_out_time = self.sign_out_time_entry.get()


        if not student_id or not activity_name:
            messagebox.showerror("Error", "Please fill in the Student ID and Activity Name.")
        else:
            conn = sqlite3.connect("ydatabase.db")
            cursor = conn.cursor()
            
            
            cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
            student = cursor.fetchone()

        if not student:
            messagebox.showerror("Error", "Student with the given ID does not exist.")
        else:
            cursor.execute("INSERT INTO attends (student_id, activity_name, sign_in_time, sign_out_time) VALUES (?, ?, ?, ?)", 
                           (student_id, activity_name, sign_in_time, sign_out_time))
            conn.commit()
            self.populate_treeview()
            self.clear_entries()
            messagebox.showinfo("Success", "Attendance record added successfully!")

        conn.close()


    def delete_attendance(self):
        if self.selected_attendance:
            student_id = self.selected_attendance[0]

            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this attendance record?")
            if confirmation:
                conn = sqlite3.connect("ydatabase.db")
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM attends WHERE student_id=?", (student_id,))
            conn.commit()
            self.populate_treeview()
            self.clear_entries()
            messagebox.showinfo("Success", "Attendance record deleted successfully!")

            conn.close()
        else:
            messagebox.showerror("Error", "Please select an attendance record to delete.")

    def edit_attendance(self):
        if self.selected_attendance:
            self.edit_mode = True
            self.student_id_entry.delete(0, tk.END)
            self.activity_name_entry.delete(0, tk.END)
            self.sign_in_time_entry.delete(0, tk.END)
            self.sign_out_time_entry.delete(0, tk.END)

            # Fetch the selected attendance record
            student_id, activity_name, sign_in_time, sign_out_time = self.selected_attendance

            # Display the information in each entry
            self.student_id_entry.insert(0, student_id)
            self.activity_name_entry.insert(0, activity_name)
            self.sign_in_time_entry.insert(0, sign_in_time)
            self.sign_out_time_entry.insert(0, sign_out_time)

            # Disable the sign-in time entry
            self.sign_in_time_entry.config(state="disabled")

            # Enable the sign-out time entry for editing
            self.sign_out_time_entry.config(state="normal")
        else:
            messagebox.showerror("Error", "Please select an attendance record to edit.")

    def update_attendance(self):
        if hasattr(self, 'edit_mode') and self.edit_mode:
            if self.selected_attendance:
                student_id = self.selected_attendance[0]
                activity_name = self.selected_attendance[1]
                new_sign_out_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                conn = sqlite3.connect("ydatabase.db")
                cursor = conn.cursor()

                cursor.execute("UPDATE attends SET sign_out_time=? WHERE student_id=? AND activity_name=?", 
                            (new_sign_out_time, student_id, activity_name))
                conn.commit()
                self.populate_treeview()
                self.clear_entries()
                self.edit_mode = False
                messagebox.showinfo("Success", "Attendance record updated successfully!")
                
                conn.close()
            else:
                messagebox.showerror("Error", "Please select an attendance record to update.")
        else:
            messagebox.showerror("Error", "Please click the Edit button first.")

    def search_attendance(self):
        search_term = self.search_entry.get()
        search_term = f"%{search_term}%"
        
        conn = sqlite3.connect("ydatabase.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM attends WHERE student_id LIKE ? OR activity_name LIKE ? OR sign_in_time LIKE ? OR sign_out_time LIKE ?",
                   (search_term, search_term, search_term, search_term))
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()
        
    def clear_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.activity_name_entry.delete(0, tk.END)
        self.sign_in_time_entry.delete(0, tk.END)
        self.sign_out_time_entry.delete(0, tk.END)
        self.selected_attendance = None

    def select_attendance(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            attendance_data = self.tree.item(selected_item, 'values')
            self.selected_attendance = attendance_data
        else:
            self.selected_attendance = None


def iExit():
    iExit = messagebox.askyesno("CSM ATTENDANCE", "Confirm if you want to exit")
    if iExit > 0:
        app.destroy()

if __name__ == "__main__":
    app = Attendance()
    app.mainloop()

conn.close()