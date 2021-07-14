from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3

# function to define database
def Database():
    global conn, cursor
    # creating student database
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    # creating STUD_REGISTRATION table
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS STUD_REGISTRATION (SR_NO INTEGER PRIMARY KEY AUTOINCREMENT, STU_NAME TEXT, '
        'STU_ROLLNO INTEGER UNIQUE, STU_PRACTICALS INTEGER, STU_ASSIGNMENTS INTEGER , STU_ATTENDANCE INTEGER, TOTAL REAL)')


# defining function for creating GUI Layout
def DisplayForm():
    # creating window
    display_screen = Tk()
    # setting width and height for window
    display_screen.geometry("900x400")
    # setting title for window
    display_screen.title("Student Assessment Calculator")
    global tree
    global SEARCH
    global name, po, assignments, rollno, attendance
    SEARCH = StringVar()
    sr = StringVar()
    name = StringVar()
    po = StringVar()
    assignments = StringVar()
    rollno = StringVar()
    attendance = StringVar()
    # creating frames for layout
    # topview frame for heading
    TopViewForm = Frame(display_screen, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    # first left frame for registration from
    LFrom = Frame(display_screen, width="350", bg="#03A5C4")
    LFrom.pack(side=LEFT, fill=Y)
    # seconf left frame for search form
    LeftViewForm = Frame(display_screen, width=500, bg="#B0E2EB")
    LeftViewForm.pack(side=LEFT, fill=Y)
    # mid frame for displaying students record
    MidViewForm = Frame(display_screen, width=600)
    MidViewForm.pack(side=LEFT)
    # label for heading
    lbl_text = Label(TopViewForm, text="Student Assessment Calculator", font=('verdana', 18), width=600, bg="#084D5A",
                     fg="white")
    lbl_text.pack(fill=X)
    # creating registration form in first left frame
    Label(LFrom, text="Name", font=("Arial", 12), bg="#03A5C4").pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"), textvariable=name).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Rollno ", font=("Arial", 12), bg="#03A5C4").pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"), textvariable=rollno).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Practicals", font=("Arial", 12), bg="#03A5C4").pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"), textvariable=po).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Assignments", font=("Arial", 12), bg="#03A5C4").pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"), textvariable=assignments).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Attendance", font=("Arial", 12), bg="#03A5C4").pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"), textvariable=attendance).pack(side=TOP, padx=10, fill=X)
    Button(LFrom, text="Submit", font=("Arial", 10, "bold"), command=register).pack(side=TOP, padx=10, pady=20, fill=X)

    # creating search label and entry in second frame
    lbl_txtsearch = Label(LeftViewForm, text="Enter name to Search", font=('verdana', 10), bg="#B0E2EB")
    lbl_txtsearch.pack()
    # creating search entry
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, pady=7, fill=X)
    # creating search button
    btn_search = Button(LeftViewForm, text="Search", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    # creating view button
    btn_view = Button(LeftViewForm, text="View All", command=DisplayData)
    btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
    # creating reset button
    btn_reset = Button(LeftViewForm, text="Clear", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    # creating delete button
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    # setting scrollbar
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    # tree = ttk.Treeview(MidViewForm, columns=("Student Rollno", "Name", "Practicals", "Assignments", "Attendance"),
    tree = ttk.Treeview(MidViewForm,
                        columns=("Sr", "Name", "Student Rollno", "Practicals", "Assignments", "Attendance", "Cgpa"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)

    # setting headings for the columns
    tree.heading('Sr', text="Sr", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Student Rollno', text="Rollno", anchor=W)
    tree.heading('Practicals', text="Practicals", anchor=W)
    tree.heading('Attendance', text="Attendance", anchor=W)
    tree.heading('Assignments', text="Assignments", anchor=W)
    tree.heading('Cgpa', text="Cgpa", anchor=W)

    # setting width of the columns
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=70)
    tree.column('#5', stretch=NO, minwidth=0, width=80)
    tree.column('#6', stretch=NO, minwidth=0, width=75)
    tree.column('#7', stretch=NO, minwidth=0, width=80)
    tree.pack()
    DisplayData()


# function to insert data into database
def register():
    Database()
    # getting form data
    name1 = name.get()
    rollno1 = rollno.get()
    po1 = po.get()
    assignments1 = assignments.get()
    attendance1 = attendance.get()
    total1 = (int(po1) + int(assignments1) + int(attendance1))/30*10

    # applying empty validation
    if name1 == '' or rollno1 == '' or po1 == '' or assignments1 == '' or attendance1 == '':
        tkMessageBox.showinfo("Warning", "fill the empty field!!!")
    elif int(assignments1)>10 or int(attendance1)>10 or int(po1)>10:
        tkMessageBox.showinfo("Warning", "Values exceeded!!!")
        total1=10
    else:
        # execute query
        conn.execute('INSERT INTO STUD_REGISTRATION (STU_NAME,STU_ROLLNO,STU_PRACTICALS,STU_ASSIGNMENTS,STU_ATTENDANCE,TOTAL) \
              VALUES (?,?,?,?,?,?)', (name1, rollno1, po1, assignments1, attendance1, ("{0:.2f}".format(total1))))

        conn.commit()
        tkMessageBox.showinfo("Message", "Stored successfully")
        # refresh table data
        DisplayData()
        conn.close()


def Reset():
    # clear current data from table
    tree.delete(*tree.get_children())
    # refresh table data
    DisplayData()
    # clear search text
    SEARCH.set("")
    name.set("")
    rollno.set("")
    po.set("")
    assignments.set("")
    attendance.set("")


def Delete():
    # open database
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Warning", "Select data to delete")
    else:
        result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            cursor = conn.execute("DELETE FROM STUD_REGISTRATION WHERE SR_NO = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()


# function to search data
def SearchRecord():
    # open database
    Database()
    # checking search text is empty or not
    if SEARCH.get() != "":
        # clearing current display data
        tree.delete(*tree.get_children())
        # select query with where clause
        cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_NAME LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        # fetch all matching records
        fetch = cursor.fetchall()
        # loop for displaying all records into GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


# defining function to access data from SQLite database
def DisplayData():
    # open database
    Database()
    # clear current data
    tree.delete(*tree.get_children())
    # select query
    cursor = conn.execute("SELECT * FROM STUD_REGISTRATION")
    # fetch all data from database
    fetch = cursor.fetchall()
    # loop for displaying all data in GUI
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


# calling function
DisplayForm()
if __name__ == '__main__':
    mainloop()
