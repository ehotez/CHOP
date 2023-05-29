import pyodbc
import customtkinter as ct

# Установление соединения с базой данной
conn = pyodbc.connect(driver = '{SQL Server}',server = 'EHOTEZPC' , database = 'dbCHOP', user = 'sa', password = 'sa')
cur = conn.cursor()

ct.set_appearance_mode('dark')
ct.set_default_color_theme('blue')

cur.execute('select intClientId, txtClientFIO from tblClient')
clients = {}
while(1):
    res = str(cur.fetchone())
    if(res == "None"):
        break
    res = res.replace(')','').replace('(','').replace('\'','')
    res1 = res.split(',')
    clients[res1[1]] = res1[0]

app = ct.CTk()
app.title('ЧОП')
app.geometry('1000x600')

def main_frame(clientId):
    login.pack_forget()
    main = ct.CTkFrame(app, fg_color='transparent')
    main.pack(expand=True)
    ct.CTkLabel(main, text='Вы зашли как шнырь номер: '+clientId).grid(row=0,column=0)

#login frame
login = ct.CTkFrame(app,fg_color='transparent')
login.pack(expand=True)
ct.CTkLabel(login, text='Войти как: ').grid(column=0, row=0)
clientBox = ct.CTkComboBox(login, state='readonly', values=list(clients.keys()))
clientBox.grid(column=1,row=0,pady=15)
button = ct.CTkButton(login, text='Войти', 
                      command=lambda: main_frame(str(clients[clientBox.get()])))
button.grid(column=1,row=1,pady=15)

app.mainloop()

conn.close()
