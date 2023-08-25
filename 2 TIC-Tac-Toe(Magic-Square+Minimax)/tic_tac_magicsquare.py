import random


class TicTacToe:
    def __init__(self):
        self.matrix = None
        self.human_move = []
        self.machine_move = []
        self.turn = 1   # 0: Human, 1: Machine
        self.temp = []
        self.ans = None
        self.winner = -1

    def magic_square(self):
        self.matrix = [[8, 3, 4],
                       [1, 5, 9],
                       [6, 7, 2]]

    def check_win(self, arr, turn):
        if len(arr) >= 3:
            for i in range(0, len(arr)):
                for j in range(i+1, len(arr)):
                    for k in range(j+1, len(arr)):
                        if arr[i]+arr[j]+arr[k] == 15:
                            if not turn:
                                print("Machine Wins")
                            else:
                                print("Human Wins")
                            self.winner = turn
                            break

    def check(self, arr):
        if len(arr) >= 2:
            for i in range(0, len(arr)):
                for j in range(i + 1, len(arr)):
                    if arr[i] + arr[j] < 15:
                        x = 15 - arr[i] - arr[j]
                        if x not in self.machine_move and self.human_move:
                            self.temp.append(x)
                            return True
        return False

    def play(self):
        for _ in range(9):
            if self.turn == 1:   # Machine

                self.check_win(self.machine_move, self.turn)  # Check for winner
                if self.winner == self.turn:
                    break

                if self.check(self.machine_move):   # Check for moves by machine
                    if len(self.temp) > 0:
                        for i in self.temp:
                            if i not in self.human_move and self.machine_move:
                                self.machine_move.append(i)
                                break
                        else:
                            continue
                        self.temp = []

                elif self.check(self.human_move):   # Check for human moves
                    if len(self.temp) > 0:
                        for i in self.temp:
                            if i not in self.human_move and self.machine_move:
                                self.machine_move.append(i)
                                break
                        else:
                            continue
                        self.temp = []

                else:    # Generate random move
                    while True:
                        x = random.randint(1, 8)
                        if x not in self.machine_move:
                            self.machine_move.append(x)
                            break
                self.turn = 0
                print(f"Machine: {self.machine_move}")
                print(f"Human: {self.human_move}")

            else:
                self.check_win(self.machine_move, self.turn)
                if self.winner == self.turn:
                    break
                a = int(input("Enter your no. "))
                self.human_move.append(a)
                self.turn = 1
                print(f"Machine: {self.machine_move}")
                print(f"Human: {self.human_move}")

a = TicTacToe()
a.play()
