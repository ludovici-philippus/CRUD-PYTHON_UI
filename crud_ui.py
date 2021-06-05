import sqlite3, os, winsound, time
from tkinter import *
from tkinter import messagebox
from functools import partial

class Manager():

    def __init__(self):
        self.SCREEN = "250x250"
        self.root = Tk()
        self.root.geometry(self.SCREEN)
        self.root.title("Grud")
        self.root.resizable(False, False)
        self.name = StringVar()
        self.temp_name = StringVar()
        self.phone = StringVar()
        self.address = StringVar()
    
    def execute_add(self, add_contact):
        db = sqlite3.connect("connection")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM contacts")
        names = cursor.fetchall()
        for name in names:
            if self.temp_name.get() == name[0]:
                messagebox.showerror(message="Person is already registered!", title="Error!")
                db.close()
                add_contact.destroy()
        try:
            self.name.set(self.temp_name.get())
            self.temp_name.set("")
            cursor.execute("""INSERT INTO contacts VALUES (?, ?, ?)""", (self.name.get(), self.phone.get(), self.address.get()))
            db.commit()
            messagebox.showinfo(message=f"{self.name.get()} has been successfully added!", title="Success")
            db.close()
        except:
            pass
    
    def add(self):
        add_contact = Toplevel()
        
        lb_name = Label(add_contact, text="Enter the name: ")
        lb_name.place(x=25, y=30)

        entry_name = Entry(add_contact, textvariable=self.temp_name)
        entry_name.place(x=125, y=30)

        lb_phone = Label(add_contact, text="Enter the phone: ")
        lb_phone.place(x=25, y=60)

        entry_phone = Entry(add_contact, textvariable=self.phone)
        entry_phone.place(x=125, y=60)

        lb_address = Label(add_contact, text="Enter the address: ")
        lb_address.place(x=25, y=90)

        entry_address = Entry(add_contact, textvariable=self.address)
        entry_address.place(x=125, y=90)

        bt_execute = Button(add_contact, width=20, text="To add")
        bt_execute["command"] = partial(self.execute_add, add_contact)
        bt_execute.place(x=75, y=130)

        add_contact.title("Add contact")
        add_contact.geometry("300x200")
        add_contact.resizable(False, False)
        add_contact.mainloop()
        
    
    def update_contact(self, update_contact):
        db = sqlite3.connect("connection")
        cursor = db.cursor()
        try:
            if self.name.get() != "":
                cursor.execute("SELECT name FROM contacts")
                results = cursor.fetchall()
                for name in results:
                    if name[0] == self.name.get():
                        messagebox.showerror(message="Name is already registered!")
                        db.close()
                        update_contact.destroy()
                        break
                cursor.execute("UPDATE contacts SET name = ? WHERE name = ?", (self.name.get(), self.temp_name.get()))
                db.commit()
            
            if self.phone.get() != "":
                cursor.execute("UPDATE contacts SET phone = ? WHERE name = ?", (self.phone.get(), self.temp_name.get()))
                db.commit()
            
            if self.address.get() != "":
                cursor.execute("UPDATE contacts SET address = ? WHERE name = ?", (self.address.get(), self.temp_name.get()))
                db.commit()
            db.close()
            messagebox.showinfo(message=f"{self.temp_name.get()} has been successfully updated!", title="Updated")
            self.temp_name.set("")
            update_contact.destroy()
        except:
            db.close()
            print("Update has been cancelled")
            self.temp_name.set("")
        



    def update_command(self, update_contact):
        for widget in update_contact.winfo_children():
            widget.destroy()

        db = sqlite3.connect("connection")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM contacts")
        results = cursor.fetchall()
        db.close()

        for name in results:
            if self.temp_name.get() == name[0]:
                exists = True
                break
            else:
                exists = False

                
        if exists:
            update_contact.geometry("300x200")

            lb_name = Label(update_contact, text="New name: ")
            lb_name.place(x=25, y=30)

            entry_name = Entry(update_contact, textvariable=self.name)
            entry_name.place(x=125, y=30)

            lb_phone = Label(update_contact, text="New phone: ")
            lb_phone.place(x=25, y=60)

            entry_phone = Entry(update_contact, textvariable=self.phone)
            entry_phone.place(x=125, y=60)

            lb_address = Label(update_contact, text="New address")
            lb_address.place(x=25, y=90)

            entry_address = Entry(update_contact, textvariable=self.address)
            entry_address.place(x=125, y=90)

            bt_update = Button(update_contact, width=20, text="Update")
            bt_update["command"] = partial(self.update_contact, update_contact)
            bt_update.place(x=75, y=130)
            
        else:
            messagebox.showerror(message="Person isn't registered")
            update_contact.destroy()

        

    def update(self):
        update_contact = Toplevel()

        lb_name = Label(update_contact, text="Name to update: ")
        lb_name.place(x=40, y=10)

        entry_name = Entry(update_contact, textvariable=self.temp_name, width=18)
        entry_name.place(x=40, y=40)

        bt_update = Button(update_contact, width=15, text="Update!")
        bt_update["command"] = partial(self.update_command, update_contact)
        bt_update.place(x=40, y=70)

        update_contact.geometry("200x100")
        update_contact.resizable(False, False)
        update_contact.title("Update")
        update_contact.mainloop()
        
    def remove_command(self, remove_contact):
        db = sqlite3.connect("connection")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM contacts")
        names = cursor.fetchall()
        db.close()

        for name in names:
            if name[0] == self.temp_name.get():
                self.name.set(self.temp_name.get())
                self.temp_name.set("")
                exist = True
                break
            else:
                exist = False
        if exist:
            are_you_sure = messagebox.askyesno(title="Delete", message=f"Are you sure you want to remove {self.name.get()}?")
            if are_you_sure:
                db = sqlite3.connect("connection")
                cursor = db.cursor()
                cursor.execute("DELETE FROM contacts WHERE name = ?", (self.name.get(), ))
                db.commit()
                messagebox.showinfo(message=f"{self.name.get()} has been successfully removed")
                db.close()
                remove_contact.destroy()
        else:
            messagebox.showinfo(message="Deletion has been cancelled. User not found")
            db.close()
            remove_contact.destroy()


    def remove(self):
        remove_contact = Toplevel()

        lb_name = Label(remove_contact, text="Name to delete: ")
        lb_name.place(x=40, y=10)

        entry_name = Entry(remove_contact, textvariable=self.temp_name, width=18)
        entry_name.place(x=40, y=40)

        bt_remove = Button(remove_contact, text="Delete", width=15)
        bt_remove["command"] = partial(self.remove_command, remove_contact)
        bt_remove.place(x=40, y=70)

        remove_contact.geometry("200x100")
        remove_contact.resizable(False, False)
        remove_contact.title("Remove")
        remove_contact.mainloop()

    def go_forward(self, get_list):
        global count_1

        for widget in Toplevel.winfo_children(get_list):
            if isinstance(widget, Label):
                widget.destroy()

        for row in range (0, 5):
            try:
                Label(get_list, text=f"{count_1 + 1} - {results[count_1]}").pack()
                count_1 += 1
            except:
                break
        if len(Label.winfo_children(get_list)) == 1:
            messagebox.showinfo(message="End of list!", title="End")
            get_list.destroy()

        

    def get_list(self):
        global count_1
        count_1 = 0
        get_list = Toplevel()
        Label(get_list, text="Click the button to start").pack()

        db = sqlite3.connect("connection")
        cursor = db.cursor()
        cursor.execute("SELECT name, phone, address FROM contacts")
        global results
        results = cursor.fetchall()

        bt_go_forward = Button(get_list, width=20, text=">")
        bt_go_forward["command"] = partial(self.go_forward, get_list)
        bt_go_forward.place(x=130, y=160)

        get_list.title("List")
        get_list.geometry("400x200")
        get_list.resizable(False, False)
        get_list.mainloop()
        db.close()

        

    def terminator(self):
        exit_question = messagebox.askyesno(title="Exit", message="Are you sure you want to exit?")
        if exit_question:
            messagebox.showinfo("Bye!", message="See you later!")
            for i in range(5, 0, -1):
                time.sleep(0.5)
                winsound.Beep(1000*i, 100)
            self.root.destroy()

    def menu(self):
        try:
            bt_add = Button(self.root, text="Add", width=20, command=self.add)
            bt_add.place(x=50, y=50)

            bt_remove = Button(self.root, text="Remove", width=20, command=self.remove)
            bt_remove.place(x=50, y=80)

            bt_update = Button(self.root, text="Update", width=20, command=self.update)
            bt_update.place(x=50, y=110)

            bt_get_list = Button(self.root, text="Get contacts", width=20, command=self.get_list)
            bt_get_list.place(x=50, y=140)

            bt_exit = Button(self.root, text="Exit", width=20, command=self.terminator)
            bt_exit.place(x=50, y=170)

            self.root.mainloop()
        except:
            print("Programa fechado")

    def main(self):
        
        if os.path.isfile("connection"):
            db = sqlite3.connect("connection")
            messagebox.showinfo(message="Successfully connected!", title="Success!")
            db.close()
            self.menu()

        else:
            winsound.Beep(2000, 50)
            messagebox.showinfo(message="Database doesn't exist! Creating one...", title="Database doesn't exist")
            time.sleep(2)
            db = sqlite3.connect("connection")

            cursor = db.cursor()
            cursor.execute("""CREATE TABLE contacts 
                            (name VARCHAR(20), phone VARCHAR(15), address VARCHAR(50))""")
            winsound.Beep(2000, 50)
            messagebox.showinfo(message="Database and table have been successfully created", title="Database created")
            db.close()
            self.menu()

        self.menu()
        
crud = Manager()
crud.main()