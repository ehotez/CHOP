import tkinter as tk
import pyodbc
import customtkinter as ct
from tkinter.messagebox import NO
from tkinter import CENTER, ttk

# Установление соединения с базой данной HI HI HA HA
conn = pyodbc.connect(driver = '{SQL Server}',server = 'EHOTEZPC' , database = 'dbCHOP', user = 'sa', password = 'sa')
cur = conn.cursor()

ct.set_appearance_mode('dark')
ct.set_default_color_theme('blue')

app = ct.CTk()
app.title('ЧОП')
app.geometry('1000x600')

def register():
    def new_client(fio, passport, address, phone):
        if(fio == ''or passport == '' or address == '' or phone == ''):
            return
        else:
            try:
                cur.execute('INSERT INTO tblClient VALUES (?,?,?,?)', fio, passport, address, phone)
                conn.commit()
                reg.destroy()
            except:
                print('error')
        
    reg = ct.CTkToplevel()
    reg.grab_set()
    reg.title('Регистрация клиента')
    reg.geometry('800x400')
    ct.CTkLabel(reg, text='ФИО:').grid(column=0,row=0)
    fio = ct.CTkEntry(reg)
    fio.grid(column=0,row=1)
    ct.CTkLabel(reg, text='Паспортные данные:').grid(column=0,row=2)
    passport = ct.CTkEntry(reg)
    passport.grid(column=0,row=3)
    ct.CTkLabel(reg, text='Адрес проживания:').grid(column=0,row=4)
    address = ct.CTkEntry(reg)
    address.grid(column=0,row=5)
    ct.CTkLabel(reg, text='Номер телефона:').grid(column=0,row=6)
    phone = ct.CTkEntry(reg)
    phone.grid(column=0,row=7)
    ct.CTkButton(reg, text='Новый клиент', command=
                              lambda: new_client(fio.get(), passport.get(), address.get(), phone.get())).grid(column=0,row=8)
    
    # reg.grid_rowconfigure(0, weight=1)
    # reg.grid_rowconfigure(1, weight=1)
    # reg.grid_columnconfigure(0, weight=1)
    # reg.grid_columnconfigure(1, weight=1)
    
    print('reg')
    
def login_frame():
    
    def choose_client():
        def log_in(*args):
            curRow = table.focus()
            client_id = table.item(curRow, 'values')[0]
            client_fio = table.item(curRow, 'values')[1]
            login.pack_forget()
            main_frame(client_id, client_fio)
            client.destroy()
        
        def search():
            query = search_var.get()
            items = table.get_children()
            for item in items:
                if query.lower() in table.item(item)['values'][1].lower():
                    table.selection_set(item)
                else:
                    table.selection_remove(item)
            
        cur.execute('select intClientId, txtClientFIO, txtClientPhone from tblClient')
        client = ct.CTkToplevel()
        client.grab_set()
        client.title('Список клиентов')
        client.geometry('500x500')
        table = ttk.Treeview(client,columns=('','Name', 'Phone'))
        table.column('#0', width=0, stretch=NO)
        table.column('#1', width=0, stretch=NO)
        table.heading('Name', text='ФИО', anchor=CENTER)
        table.heading('Phone', text='Номер телефона', anchor=CENTER)
        table.bind('<Double-Button-1>', log_in)
        
        i=1
        while(1):
            result = str(cur.fetchone())
            if(result == "None"):
                break
            j = 0
            while(j != len(result)):
                if(result[j] == ' ' and result[j-1] != ','):
                    result = result[:j] + '_' + result[j + 1:]
                j+=1
            replaced = result.replace(')','').replace('(','').replace('\'','').replace(',','')
            table.insert(parent='',index='end',iid=i, values=replaced)
            i+=1
        table.pack()
        
        search_var = tk.StringVar()
        search_var.trace('w', lambda *args: search())
        ct.CTkLabel(client, text='Поиск по ФИО').pack()
        ct.CTkEntry(client, textvariable=search_var).pack()
        
    
    login = ct.CTkFrame(app,fg_color='transparent')
    login.pack(expand=True)
    ct.CTkButton(login, text='Выбрать клиента', 
                    command=choose_client).grid(column=1,row=1,pady=15)
    ct.CTkButton(login, text='Регистрация', command=register).grid(column=1,row=2)

def main_frame(client_id, client_name):
    
    def log_off():
        main.pack_forget()
        login_frame()
    
    main = ct.CTkFrame(app, fg_color='transparent')
    main.pack()
    ct.CTkLabel(main, text='Текущий клиент: '+client_name).grid(column=10,row=0)
    ct.CTkButton(main, text='Сменить клиента', command=log_off).grid(column=11,row=0)
    ct.CTkButton(main, text='Список договоров', command=log_off).grid(column=0,row=0)
    ct.CTkButton(main, text='Новый договор', command=log_off).grid(column=0,row=1)
    ct.CTkButton(main, text='Распечатать договор', command=log_off).grid(column=0,row=2)
    ct.CTkButton(main, text='Список претензий', command=log_off).grid(column=1,row=0)
    ct.CTkButton(main, text='Новая претензия', command=log_off).grid(column=1,row=1)
    ct.CTkButton(main, text='Привязать сотрудника к договору', command=log_off).grid(columnspan=2,row=3)
    
    
login_frame()

app.mainloop()

conn.close()
