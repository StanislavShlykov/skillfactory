
from string import digits
from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dot = [self.x, self.y]

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if isinstance(other, Dot):
            return Dot(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f'Dot ({self.x}, {self.y})'

    def __getitem__(self, item):
        return self.dot[item]

    def __hash__(self):
        return hash((self.x, self.y))

class GameExceptions(Exception):
    pass


class BoardOutException(GameExceptions):
    def __str__(self):
        return 'Клетка находится за пределами поля'


class OccupiedDot(GameExceptions):
    def __str__(self):
        return 'Клетка занята другим кораблем'


class DoubleShot(GameExceptions):
    def __str__(self):
        return 'В эту клетку уже стреляли, выберите другую'


class DotValue(GameExceptions):
    def __str__(self):
        return 'значением координаты клетки по оси Х или Y  может быть только целое число от 1 до 6'

class Ship:
    def __init__(self, len_s, start_dot: Dot, position):
        self.len_s = len_s
        self.start_dot = start_dot
        self.position = position
        self.lives = len_s

    def dots(self):
        ship_dots = []
        for i in range(self.len_s):
            coord_x = self.start_dot.x
            coord_y = self.start_dot.y

            if self.position == 0: ##горизонтальное положение
                coord_y += i
            else:
                coord_x += i
            ship_dots.append(Dot(coord_x, coord_y))

        return ship_dots


class Board:
    def __init__(self, hide=False, size=6):
        self.hide = hide
        self.size = size
        self.count = 0
        self.field_condition = {Dot(i, j): '0' for i in range(1, self.size + 1) for j in range(1, self.size + 1)}
        self.ships = []
        self.used_dots = []

    def out_of_board(self, dot):
        if dot in self.field_condition:
            return True
        else:
            return False

    def add_ship(self, boat):
        if isinstance(boat, Ship):
            for i in boat.dots():
                if not self.out_of_board(i):
                    raise BoardOutException
            for i in boat.dots():
                if i in self.used_dots:
                    raise OccupiedDot
            for i in boat.dots():
                self.field_condition[i] = '■'
                self.used_dots.append(i)
            self.ships.append(boat)
            self.ship_perimeter(boat)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |\n"
        for i in range(1, self.size + 1):
            a = ''
            for j in range(1, self.size + 1):
                a += f'{self.field_condition[Dot(i, j)]} | '
            res += f'{i} | {a}\n'
        if self.hide == True:
            res = res.replace("■", "O")
        return res


    def ship_perimeter(self, boat, pr_per=False):
        boat_perimeter = [Dot(-1, -1), Dot(-1, 0), Dot(-1, 1), Dot(0, -1), Dot(0, 0), Dot(0, 1), Dot(1, -1),
                          Dot(1, 0), Dot(1, 1)]
        for i in boat.dots():
            for j in boat_perimeter:
                if i + j in self.field_condition and self.field_condition[i + j] != 'X':
                    if pr_per:
                        self.field_condition[i + j] = '.'
                    self.used_dots.append(i+j)

    def shot(self, dot):
        if not self.out_of_board(dot):
            raise BoardOutException
        elif self.field_condition[dot] == 'x' or self.field_condition[dot] == 'X':
            raise DoubleShot

        self.used_dots.append(dot)

        for i in self.ships:
            if dot in i.dots():
                i.lives -=1
                self.field_condition[dot] = 'X'
                if i.lives == 0:
                    self.count +=1
                    self.ship_perimeter(i, pr_per=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True
        self.field_condition[dot] = '.'
        print("Не попал!")
        return False


    def begin(self):
        self.used_dots = []

    def input_xy(self):
        x = input('Введите координаты первой точки по оси Х: -->')
        y = input('введите координаты первой точки по оси Y: -->')
        if len(x) == 0 or len(y) == 0 or x not in digits or y not in digits or int(x) > 6 or int(y) > 6 or int(x) < 0 or int(y) < 0:
            print('Данные ввода не верны, введите числовые координаты Х/Y в пределах от 1 до 6')
            return self.input_xy()
        else:
            return Dot(int(x), int(y))

    def input_z(self):
        z = input('введите положение корабля (0-горизонтальное 1-вертикальное): -->')
        if len(z) == 0 or z not in digits or int(z) > 1 or int(z) < 0:
            print('Данные ввода не верны, введите 0 или 1')
            return self.input_z()
        else:
            return int(z)
class Player:
    def __init__(self, board:Board):
        self.board = board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                a = self.ask()
                repeat = self.board.shot(a)
                return repeat
            except GameExceptions as e:
                print(e)

class User(Player):

    def ask(self):
        return self.board.input_xy()


class AI(Player):

    def ask(self):
        dot = Dot(randint(1, 6), randint(1, 6))
        print(f"Ход компьютера: {dot.x} {dot.y}")
        return dot

class Game:
    def __init__(self):
        self.greet()
        player = self.player_board()
        comp = self.random_board()
        comp.hide = True

        self.comp = AI(player)
        self.user = User(comp)

    def try_board(self):
        ship_lens = [3, 2, 2, 1, 1, 1]
        count_try = 0
        board = Board()
        for i in ship_lens:
            while True:
                count_try += 1
                if count_try > 1000:
                    return None
                ship = Ship(i, Dot(randint(1, 6), randint(1, 6)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except GameExceptions:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def player_board(self):
        ship_lens = [3, 2, 2, 1, 1, 1]
        board = Board()
        for i in ship_lens:
            while True:
                ship = Ship(i, board.input_xy(), board.input_z())
                try:
                    board.add_ship(ship)
                    print(board)
                    break
                except GameExceptions as e:
                    print(e)
        return board

    def greet(self):
        print('*'*65)
        print('                  Приветствуем Вас в ИГРЕ                        ')
        print('------------------------МОРСКОЙ БОЙ------------------------------')
        print('                      правила просты                             ')
        print("             для начала расставим свои корабли                   ")
        print('   вводим 2 координаты X/Y от 1 до 6 обозначающие нос корабоя    ')
        print('  затем вводим цифру от 0 или 1, обозначающие положение корабля  ')
        print("          0 - горизонтальное, 1 - вертикальное                   ")
        print('               всего расставляем 6 кораблей:\n       '
              '1- трехпалубный, 2 - двухпалубных и 3 - однопалубных')
        print('                    начинаем с больших!                          ')
        print('далее, поочередно с компьютером, вводим 2 координаты X/Y от 1 до 6')
        print('          обозначающие выстрел по доске соперника                ')
        print('   побеждает тот, кто первым потопит все корабли соперника       ')
        print('----------------------------УДАЧИ--------------------------------')
        print('*' * 65)
        print('*' * 65)
        print('*' * 65)
        print()


    def game_proc(self):
        count = 0
        while True:
            print('*'*20)
            print('Ваша доска')
            print(self.comp.board)
            print('*' * 20)
            print()
            print("Доска компьютера:")
            print(self.user.board)

            if count % 2 == 0:
                print("Ваш ход!")

                repeat = self.user.move()
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.comp.move()
            if repeat:
                count -= 1

            if self.user.board.count == 6:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.comp.board.count == 6:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            count += 1



    def start(self):
        self.game_proc()


game = Game()
game.start()