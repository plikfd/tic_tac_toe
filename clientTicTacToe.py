import socket
import os
import threading

from tkinter import *
from tkinter import messagebox

class TicTacToeClient:
    def __init__(self, host = '192.168.137.1', port = 2048):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))#подключились к серваку
        data = self.client.recv(1024).decode('utf-8')#узнали мы x | o
        self.sym = data[0]
        #
        self.win = Tk()#окно
        self.win.title(f'Крестики нолики\t{self.sym.upper()}')#название
        self.win.geometry('600x600')#размер окна
        self.win.resizable(width = False, height = False)#чтобы пользователь не мог изменять размеры окна
        self.label = Label(self.win, text="Ну здравствуй, Чемпион", width = 90, height = 2)#метка сверху
        self.label.place(x=0, y=0)
        self.frame = Frame(self.win)# Создаем фрейм для игрового поля(группа виджетов)
        self.frame.pack(pady=100)
        self.buttons = [] # Создаем кнопки для игрового поля 3x3
        for row in range(3):
            self.button_row = []
            for col in range(3):
                self.button = Button(self.frame, text="", width=10, height=3,
                                command=lambda r=row, c=col, s = self.sym: self.button_click(r, c, s))
                self.button.grid(row=row, column=col, padx=5, pady=5)  # Размещаем кнопки в сетке
                self.button_row.append(self.button)
            self.buttons.append(self.button_row)
        self.close_button = Button(self.win, text="Закрыть", command=self.win.quit)# Создаем кнопку "Закрыть"
        self.close_button.pack(side=BOTTOM, pady=10)
        self.give_up_button = Button(self.win, text = "Капитулируем", command=self.give_up)
        self.give_up_button.pack(side=RIGHT,pady=10)
        self.del_buttons =  [[0,0,0], [0,0,0], [0,0,0]]#кнопки в неактив
        if self.sym == 'o':
            for row in range(3):
                for col in range(3):
                    self.buttons[row][col].config(state=DISABLED)
        #
        self.receive_thread = threading.Thread(target=self.update_server)#новый поток и функция которая будет выполняться в потоке
        self.receive_thread.daemon = True#поток работает на фоне и не блочит программы
        self.receive_thread.start()
        #

    def update_server(self):
        while 1:
            data = self.client.recv(1024).decode('utf-8')
            if data == 'You won':
                messagebox.showinfo('You won')
                self.win.quit()
            elif data == 'You lose':
                messagebox.showinfo('You lose')
                self.win.quit()
            elif data == 'Draw':
                messagebox.showinfo('Draw')
                self.win.quit()
            else:
                ans = data.split()
                self.button_update(int(ans[0]), int(ans[1]), self.sym)
            for row in range(3):
                for col in range(3):
                    if not self.del_buttons[row][col] == 1:
                       self.buttons[row][col].config(state=NORMAL)
    

    def give_up(self):
        messagebox.showinfo('You lose')
        self.win.quit()
        self.client.sendall(('gg').encode('utf-8'))



    def button_click(self, row, col, sym):
        #messagebox.showinfo("Кнопка нажата", f"Вы нажали кнопку на позиции ({row}, {col})")
        self.buttons[row][col].config(text=self.sym) #Обновляем текст в ячейке
        self.client.sendall((str(row) + ' ' + str(col)).encode('utf-8'))#отправляем на обновление таблицы второму игроку
        self.del_buttons[row][col] = 1
        for row in range(3):#кнопки в неактив
            for col in range(3):
                self.buttons[row][col].config(state=DISABLED)
        
    def button_update(self, row, col, sym):
        self.del_buttons[row][col] = 1
        self.buttons[row][col].config(state=DISABLED)
        if sym == 'x':
            self.buttons[row][col].config(text='o') #Обновляем текст в ячейке
        else:
            self.buttons[row][col].config(text='x') #Обновляем текст в ячейке

if __name__ == '__main__':
    client = TicTacToeClient()
    client.win.mainloop()
