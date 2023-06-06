import tkinter as tk
from tkcalendar import Calendar
import pyodbc
import customtkinter as ct
from tkinter.messagebox import NO
from tkinter import messagebox
from tkinter import CENTER, LEFT, Frame, ttk

# Установление соединения с базой данной HI HI HA HA
conn = pyodbc.connect(driver='{SQL Server}', server='MSI',
                      database='dbCHOP', user='sa', password='sa')
cur = conn.cursor()

ct.set_appearance_mode('dark')
ct.set_default_color_theme('blue')

app = ct.CTk()
app.title('ЧОП')
app.geometry('1000x600')

style = ttk.Style()
style.configure('Treeview', rowheight=50)


def register_client():
    def new_client(fio, passport, address, phone):
        if (fio == '' or passport == '' or address == '' or phone == ''):
            return
        else:
            try:
                cur.execute('INSERT INTO tblClient VALUES (?,?,?,?)',
                            fio, passport, address, phone)
                conn.commit()
                reg.destroy()
            except:
                print('error')

    reg = ct.CTkToplevel()
    reg.grab_set()
    reg.title('Регистрация клиента')
    reg.geometry('800x400')
    ct.CTkLabel(reg, text='ФИО:').grid(column=0, row=0)
    fio = ct.CTkEntry(reg, width=250)
    fio.grid(column=0, row=1)
    ct.CTkLabel(reg, text='Паспортные данные:').grid(column=0, row=2)
    passport = ct.CTkEntry(reg)
    passport.grid(column=0, row=3)
    ct.CTkLabel(reg, text='Адрес проживания:').grid(column=0, row=4)
    address = ct.CTkEntry(reg, width=250)
    address.grid(column=0, row=5)
    ct.CTkLabel(reg, text='Номер телефона:').grid(column=0, row=6)
    phone = ct.CTkEntry(reg)
    phone.grid(column=0, row=7)
    ct.CTkButton(reg, text='Создать клиента', command=lambda: new_client(fio.get(
    ), passport.get(), address.get(), phone.get())).grid(column=0, row=8, pady=15)

    # reg.grid_rowconfigure(0, weight=1)
    # reg.grid_rowconfigure(1, weight=1)
    reg.grid_columnconfigure(0, weight=1)
    # reg.grid_columnconfigure(1, weight=1)

    print('reg')


def register_employee():
    def new_employee(fio, passport, phone):
        if fio == '' or passport == '' or phone == '':
            messagebox.showerror(
                'Пустые поля', 'Заполните все пустые поля!')
            return
        try:
            cur.execute('INSERT INTO tblEmployee (txtEmployeeFio, txtEmployeePassport, txtEmployeePhone, intEmployeeExperience) VALUES (?,?,?,?)',
                        fio, passport, phone, 0)
            conn.commit()
            reg.destroy()
            messagebox.showinfo(
                'Успешно!', 'Сотрудник успешно добавлен!')
        except:
            messagebox.showerror(
                'Ошибка', 'Произошла ошибка при добавлении сотрудника.')

    reg = ct.CTkToplevel()
    reg.grab_set()
    reg.title('Добавление сотрудника')
    reg.geometry('800x400')
    ct.CTkLabel(reg, text='ФИО:').grid(column=0, row=0)
    fio = ct.CTkEntry(reg, width=250)
    fio.grid(column=0, row=1)
    ct.CTkLabel(reg, text='Паспортные данные:').grid(column=0, row=2)
    passport = ct.CTkEntry(reg)
    passport.grid(column=0, row=3)
    ct.CTkLabel(reg, text='Номер телефона:').grid(column=0, row=4)
    phone = ct.CTkEntry(reg)
    phone.grid(column=0, row=5)
    ct.CTkButton(reg, text='Создать сотрудника', command=lambda: new_employee(
        fio.get(), passport.get(), phone.get())).grid(column=0, row=6, pady=15)

    reg.grid_columnconfigure(0, weight=1)


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

        cur.execute(
            'select intClientId, txtClientFIO, txtClientPhone from tblClient')
        client = ct.CTkToplevel()
        client.grab_set()
        client.title('Список клиентов')
        client.geometry('500x500')
        frame = Frame(client)
        frame.pack(pady=20)
        table = ttk.Treeview(frame, height=7, columns=('', 'Name', 'Phone'))
        table.pack(side='left')

        sb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill='y')

        table.column('#0', width=0, stretch=NO)
        table.column('#1', width=0, stretch=NO)
        table.column('Name', width=230, stretch=NO)
        table.column('Phone', width=230, stretch=NO)
        table.heading('Name', text='ФИО', anchor=CENTER)
        table.heading('Phone', text='Номер телефона', anchor=CENTER)
        table.bind('<Double-Button-1>', log_in)

        i = 1
        while (1):
            result = str(cur.fetchone())
            if (result == "None"):
                break
            j = 0
            while (j != len(result)):
                if (result[j] == ' ' and result[j-1] != ','):
                    result = result[:j] + '_' + result[j + 1:]
                j += 1
            replaced = result.replace(')', '').replace(
                '(', '').replace('\'', '').replace(',', '')
            table.insert(parent='', index='end', iid=i, values=replaced)
            i += 1
        table.pack()

        search_var = tk.StringVar()
        search_var.trace('w', lambda *args: search())
        ct.CTkLabel(client, text='Поиск по ФИО').pack()
        ct.CTkEntry(client, textvariable=search_var).pack()

    login = ct.CTkFrame(app, fg_color='transparent')
    login.pack(expand=True)
    ct.CTkButton(login, text='Выбрать клиента',
                 command=choose_client).grid(column=1, row=1, pady=15)
    ct.CTkButton(login, text='Регистрация клиента',
                 command=register_client).grid(column=1, row=2)
    ct.CTkButton(login, text='Регистрация сотрудника',
                 command=register_employee).grid(column=1, row=3, pady=15)


def main_frame(client_id, client_name):

    def contract():  # основная ф-я с договорами

        def form_add_contract():  # добавление договора

            def add_contract1(date_start, date_end, servece, emplo, equip, quantity):
                if (date_start == '' or date_end == '' or servece == '' or emplo == '' or equip == '' or quantity.isdigit() == False):
                    return
                else:
                    try:

                        date_mas1 = date_start.split('/')
                        date_mas1[0], date_mas1[1] = date_mas1[1], date_mas1[0]
                        date_start = "/".join(date_mas1)

                        date_mas1 = date_end.split('/')
                        date_mas1[0], date_mas1[1] = date_mas1[1], date_mas1[0]
                        date_end = "/".join(date_mas1)

                        cur.execute('INSERT INTO tblContract VALUES (?,?,?,?,?,?,?,?)',
                                    date_start, date_end, 0, client_id, servece, emplo, equip, quantity)
                        conn.commit()
                        add_contract.destroy()

                        table.delete(*table.get_children())
                        cur.execute(
                            'select intContractId, dateContractStart, dateContractEnd, isContractCompleted, intServiceId, intEmployeeId, intEquipmentId, intEquipmentAmount from tblContract where intClientId =?', client_id)
                        i = 1
                        while (1):
                            result = str(cur.fetchone())
                            if (result == "None"):
                                break
                            j = 0
                            while (j != len(result)):
                                if (result[j] == ' ' and result[j-1] != ','):
                                    result = result[:j] + '_' + result[j + 1:]
                                j += 1
                            replaced = result.replace(')', '').replace(
                                '(', '').replace('\'', '').replace(',', '')
                            table.insert(parent='', index='end',
                                         iid=i, values=replaced)
                            i += 1
                    except:
                        print('error_contract')

            add_contract = ct.CTkToplevel()
            add_contract.grab_set()
            add_contract.title('Заключить договор')
            add_contract.geometry('800x500')

            ct.CTkLabel(add_contract, text='Дата начала').grid(column=2, row=0)
            date_start = Calendar(add_contract, selectmode='day')
            date_start.grid(column=2, row=1)

            ct.CTkLabel(add_contract, text='Дата конца').grid(column=2, row=2)
            date_end = Calendar(add_contract, selectmode='day')
            date_end.grid(column=2, row=3)

            ct.CTkLabel(add_contract, text='Сервис').place(x=280, y=0)
            cur.execute('select intServiceId, txtServiceName from tblService')
            serveces = {}
            while (1):
                res = str(cur.fetchone())
                if (res == "None"):
                    break
                res = res.replace(')', '').replace('(', '').replace('\'', '')
                res1 = res.split(',')
                serveces[res1[1]] = res1[0]
            servecesBox = ct.CTkComboBox(
                add_contract, width=225, state='readonly', values=list(serveces.keys()))
            servecesBox.place(x=420, y=0)

            ct.CTkLabel(add_contract, text='Сотрудник').place(x=280, y=50)
            cur.execute('select intEmployeeId,txtEmployeeFIO from tblEmployee')
            emplo = {}
            while (1):
                res = str(cur.fetchone())
                if (res == "None"):
                    break
                res = res.replace(')', '').replace('(', '').replace('\'', '')
                res1 = res.split(',')
                emplo[res1[1]] = res1[0]
            emploBox = ct.CTkComboBox(
                add_contract, width=225, state='readonly', values=list(emplo.keys()))
            emploBox.place(x=420, y=50)

            ct.CTkLabel(add_contract, text='Оборудование').place(x=280, y=100)
            cur.execute(
                'select intEquipmentId,txtEquipmentName from tblEquipment')
            equip = {}
            while (1):
                res = str(cur.fetchone())
                if (res == "None"):
                    break
                res = res.replace(')', '').replace('(', '').replace('\'', '')
                res1 = res.split(',')
                equip[res1[1]] = res1[0]
            equipBox = ct.CTkComboBox(
                add_contract, width=225, state='readonly', values=list(equip.keys()))
            equipBox.place(x=420, y=100)

            ct.CTkLabel(
                add_contract, text='Кол-во оборудования').place(x=280, y=150)
            quantity = ct.CTkEntry(add_contract, width=45, validate="key")
            quantity.place(x=420, y=150)

            ct.CTkButton(add_contract, text='Заключить', command=lambda: add_contract1(date_start.get_date(), date_end.get_date(), str(serveces[servecesBox.get()]), str(emplo[emploBox.get()]),
                                                                                       str(equip[equipBox.get()]), quantity.get())).place(x=320, y=200)

        def print_contract(*args):  # печать договора

            def update_contract(id):
                try:
                    cur.execute(
                        'update tblContract set isContractCompleted = 1 where intContractId = ?', id)
                    conn.commit()
                    print_contract.destroy()

                    table.delete(*table.get_children())
                    cur.execute('select intContractId, dateContractStart, dateContractEnd, isContractCompleted, intServiceId, intEmployeeId, intEquipmentId, intEquipmentAmount from tblContract where intClientId =?', client_id)
                    i = 1
                    while (1):
                        result = str(cur.fetchone())
                        if (result == "None"):
                            break
                        j = 0
                        while (j != len(result)):
                            if (result[j] == ' ' and result[j-1] != ','):
                                result = result[:j] + '_' + result[j + 1:]
                            j += 1
                        replaced = result.replace(')', '').replace(
                            '(', '').replace('\'', '').replace(',', '')
                        table.insert(parent='', index='end',
                                     iid=i, values=replaced)
                        i += 1
                except:
                    print('error_claim')

            def close():
                print_contract.destroy()

            curRow = table.focus()
            contract_id = table.item(curRow, 'values')[0]
            flag = table.item(curRow, 'values')[3]
            if flag == "True":
                return
            print_contract = ct.CTkToplevel()
            print_contract.grab_set()
            print_contract.title('Подтверждение печати')
            print_contract.geometry('450x100')
            ct.CTkLabel(print_contract, text='Завершить договор?').grid(
                column=2, row=0)

            ct.CTkButton(print_contract, text='Да',
                         command=lambda: update_contract(contract_id)).grid(column=0, row=3)

            ct.CTkButton(print_contract, text='Нет',
                         command=close).grid(column=3, row=3)

        cur.execute('select intContractId, dateContractStart, dateContractEnd, isContractCompleted, intServiceId, intEmployeeId, intEquipmentId, intEquipmentAmount from tblContract where intClientId =?', client_id)
        contracts = ct.CTkToplevel()
        contracts.grab_set()
        contracts.title('Контракт клиента: ' + client_name)
        contracts.geometry('1000x500')
        frame = Frame(contracts)
        frame.pack(pady=20)
        table = ttk.Treeview(frame, height=12)
        table.pack(side='left')

        sb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Vertical.TScrollbar', troughcolor='gray',
                    bordercolor='gray', background='gray')
        s.configure('Horizontal.TScrollbar', troughcolor='gray',
                    bordercolor='gray', background='gray')
        table["columns"] = ('', 'Start', 'End', 'Flag', '', '', '', 'Amount')

        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill='y')

        table.column('#0', width=0, stretch=NO)
        table.column('#1', width=0, stretch=NO)
        table.column('#5', width=0, stretch=NO)
        table.column('#6', width=0, stretch=NO)
        table.column('#7', width=0, stretch=NO)
        table.heading('Start', text='Дата заключения договора', anchor=CENTER)
        table.heading('End', text='Дата окончания договора', anchor=CENTER)
        table.heading('Flag', text='Контракт завершен?', anchor=CENTER)
        table.heading('Amount', text='Кол-во оборудования', anchor=CENTER)
        table.bind('<Double-Button-1>', print_contract)
        ct.CTkButton(contracts, text='Заключить договор',
                     command=form_add_contract).pack()

        i = 1
        while (1):
            result = str(cur.fetchone())
            if (result == "None"):
                break
            j = 0
            while (j != len(result)):
                if (result[j] == ' ' and result[j-1] != ','):
                    result = result[:j] + '_' + result[j + 1:]
                j += 1
            replaced = result.replace(')', '').replace(
                '(', '').replace('\'', '').replace(',', '')
            table.insert(parent='', index='end', iid=i, values=replaced)
            i += 1
        table.pack()

    def claim():  # Тут начинаются претензии
        def change_flag(*args):

            def update_flag(id):
                try:
                    cur.execute(
                        'update tblClaim set isClaimClosed = 1 where intClaimId = ?', id)
                    conn.commit()
                    change_flag.destroy()

                    table.delete(*table.get_children())
                    cur.execute(
                        'select intClaimId, txtClaimDescprition, isClaimClosed, dateClaimStart from tblClaim where (intClientId=?)', client_id)
                    i = 1
                    while (1):
                        result = str(cur.fetchone())
                        if (result == "None"):
                            break
                        j = 0
                        while (j != len(result)):
                            if (result[j] == ' ' and result[j-1] != ','):
                                result = result[:j] + '_' + result[j + 1:]
                            j += 1
                        replaced = result.replace(')', '').replace(
                            '(', '').replace('\'', '').replace(',', '')
                        table.insert(parent='', index='end',
                                     iid=i, values=replaced)
                        i += 1
                except:
                    print('error_claim')

            def close():
                change_flag.destroy()
            curRow = table.focus()
            claim_id = table.item(curRow, 'values')[0]
            flag = table.item(curRow, 'values')[2]
            if flag == "True":
                return
            change_flag = ct.CTkToplevel()
            change_flag.grab_set()
            change_flag.title('Подтверждение изменения')
            change_flag.geometry('420x100')
            ct.CTkLabel(change_flag, text='Закрыть претензию?').grid(
                column=2, row=0)
            ct.CTkButton(change_flag, text='Да',
                         command=lambda: update_flag(claim_id)).grid(column=0, row=3)
            ct.CTkButton(change_flag, text='Нет',
                         command=close).grid(column=3, row=3)
            print(claim_id, flag)

        def form_add_claim():

            def add_claim1(name, date):

                if (name == '' or date == ''):
                    return
                else:
                    try:
                        print(date)
                        date_mas = date.split('/')
                        date_mas[0], date_mas[1] = date_mas[1], date_mas[0]
                        print(date_mas)
                        date = "/".join(date_mas)
                        cur.execute(
                            'INSERT INTO tblClaim VALUES (?,?,?,?)', name, 0, date, client_id)
                        conn.commit()
                        add_claim.destroy()

                        table.delete(*table.get_children())
                        cur.execute(
                            'select intClaimId, txtClaimDescprition, isClaimClosed, dateClaimStart from tblClaim where (intClientId=?)', client_id)
                        i = 1
                        while (1):
                            result = str(cur.fetchone())
                            if (result == "None"):
                                break
                            j = 0
                            while (j != len(result)):
                                if (result[j] == ' ' and result[j-1] != ','):
                                    result = result[:j] + '_' + result[j + 1:]
                                j += 1
                            replaced = result.replace(')', '').replace(
                                '(', '').replace('\'', '').replace(',', '')
                            table.insert(parent='', index='end',
                                         iid=i, values=replaced)
                            i += 1
                    except:
                        print('error_claim')

            add_claim = ct.CTkToplevel()
            add_claim.grab_set()
            add_claim.title('Добавить претензию')
            add_claim.geometry('500x500')

            ct.CTkLabel(add_claim, text='Наименование претензии:').grid(
                column=0, row=0)
            name_claim = ct.CTkEntry(add_claim)
            name_claim.grid(column=0, row=1)
            ct.CTkLabel(add_claim, text='Дата претензии:').grid(
                column=0, row=2)
            date_claim = Calendar(add_claim, selectmode='day')
            date_claim.grid(column=0, row=3)

            ct.CTkButton(add_claim, text='Добавить', command=lambda: add_claim1(
                name_claim.get(), date_claim.get_date())).grid(column=0, row=8)

        cur.execute(
            'select intClaimId, txtClaimDescprition, isClaimClosed, dateClaimStart from tblClaim where (intClientId=?)', client_id)
        claim = ct.CTkToplevel()
        claim.grab_set()
        claim.title('Претензии клиента: ' + client_name)
        claim.geometry('900x300')
        frame = Frame(claim)
        frame.pack(pady=20)
        table = ttk.Treeview(frame, height=7)
        table.pack(side='left')

        sb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Vertical.TScrollbar', troughcolor='gray',
                    bordercolor='gray', background='gray')
        s.configure('Horizontal.TScrollbar', troughcolor='gray',
                    bordercolor='gray', background='gray')
        table["columns"] = ('', 'Desceiption', 'Flag', 'Date')

        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill='y')

        table.column('#0', width=0, stretch=NO)
        table.column('#1', width=0, stretch=NO)
        table.column('#2', width=400)
        table.heading(
            'Desceiption', text='Наименование претензии', anchor=CENTER)
        table.heading('Flag', text='Флаг закрытия', anchor=CENTER)
        table.heading('Date', text='Дата', anchor=CENTER)
        table.bind('<Double-Button-1>', change_flag)
        i = 1
        while (1):
            result = str(cur.fetchone())
            if (result == "None"):
                break
            j = 0
            while (j != len(result)):
                if (result[j] == ' ' and result[j-1] != ','):
                    result = result[:j] + '_' + result[j + 1:]
                j += 1
            replaced = result.replace(')', '').replace(
                '(', '').replace('\'', '').replace(',', '')
            table.insert(parent='', index='end', iid=i, values=replaced)
            i += 1
        table.pack()
        ct.CTkButton(claim, text='Добавить претензию',
                     command=form_add_claim).pack()

    def log_off():
        main.pack_forget()
        login_frame()

    main = ct.CTkFrame(app, fg_color='transparent')
    main.pack()
    ct.CTkLabel(main, text='Текущий клиент: ' +
                client_name).grid(column=10, row=0)
    ct.CTkButton(main, text='Сменить клиента', command=log_off).grid(
        column=11, row=0, padx=20)
    ct.CTkButton(main, text='Список договоров',
                 command=contract).grid(column=0, row=0, pady=5)
    ct.CTkButton(main, text='Список претензий',
                 command=claim).grid(column=0, row=1, pady=5)
    ct.CTkButton(main, text='Привязать сотрудника к договору',
                 command=log_off).grid(column=0, row=2, pady=5)
    ct.CTkButton(main, text='Распечатать договор',
                 command=log_off).grid(column=0, row=3, pady=5)


login_frame()

app.mainloop()

conn.close()
