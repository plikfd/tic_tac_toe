import socket
#import select #для работы с несколькими подключениями
#server = socket.create_server(('127.0.0.1',2048))#создали сервер - айпи, хост(быстрый вариант)
#сложный
class TicTacToeServer:
    def __init__(self, host = '192.168.137.1', port = 2048):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#адресные семьи
        self.server.bind((host, port))
        self.server.listen(2) #сколько подключенных пользователей
        self.mtr = [[" " for _ in range(3)] for _ in range(3)]
        self.flag = True
        self.player1, self.addres1 = self.server.accept()#пока никто не подключен дальше код не работает
        self.player2, self.addres2 = self.server.accept()
        self.player1.sendall(f'x'.encode('utf-8'))
        self.player2.sendall(f'o'.encode('utf-8'))
        with self.player1 and self.player2:
            while 1:
                if self.flag:
                    ans = self.player1.recv(1024).decode('utf-8')
                    if ans == "gg":
                        self.player2.sendall('You won'.encode('utf-8'))
                        break
                    data = ans.split()
                    self.mtr[int(data[0])][int(data[1])] = 'x'
                    self.player2.sendall(ans.encode('utf-8'))
                    self.flag = 0
                else:
                    ans = self.player2.recv(1024).decode('utf-8')
                    if ans == "gg":
                        self.player1.sendall('You won'.encode('utf-8'))
                        break
                    data = ans.split()
                    self.mtr[int(data[0])][int(data[1])] = 'o'
                    self.player1.sendall(ans.encode('utf-8'))
                    self.flag = 1
                #логика вычисления победителя
                self.win = self.check_winner(self.mtr)
                if self.win == "x":
                    self.player1.sendall('You won'.encode('utf-8'))
                    self.player2.sendall('You lose'.encode('utf-8'))
                    break
                if self.win == "o":
                    self.player2.sendall('You won'.encode('utf-8'))
                    self.player1.sendall('You lose'.encode('utf-8'))
                    break
                if all(cell != " " for row in self.mtr for cell in row) and self.win is None:
                    self.player2.sendall('Draw'.encode('utf-8'))
                    self.player1.sendall('Draw'.encode('utf-8'))
                    break
        #
    
    def check_winner(self, mtr):
         # Проверка строк
        for row in self.mtr:
            if row[0] == row[1] == row[2] != " ":
                return row[0]  # Возвращает "X" или "O"
        # Проверка столбцов
        for col in range(3):
            if self.mtr[0][col] == self.mtr[1][col] == self.mtr[2][col] != " ":
                return self.mtr[0][col]
        # Проверка диагоналей
        if self.mtr[0][0] == self.mtr[1][1] == self.mtr[2][2] != " ":
            return self.mtr[0][0]
        if self.mtr[0][2] == self.mtr[1][1] == self.mtr[2][0] != " ":
            return self.mtr[0][2]
        return None 

if __name__ == '__main__':
    print('Start')
    server = TicTacToeServer()
    print('End')


