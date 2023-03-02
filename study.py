from string import digits

def greet():
    print('''     
     Добро пожаловать в игру крестики-нолики
          |__X__||__O__||__-__|
          |__O__||__X__||__-__|
          |__-__||__O__||__X__|      
          Давайте напомним вам правила:
    1) Первым ходит "Х", за ним "О" и далее по очереди!
    2) Каждый игрок вводит с клавиатуры два цифровых 
       значения, в пределах от 0 до 2, обозначающие
       координаты ячейки, в которую вы хотите поставить
       крестик или нолик.
    3) Выигрывает игрок, первым заполнивший своими значениями
       любую горизонталь, вертикаль или диагональ.
       
    координата Х - означает строку (от 0  до 2)
    координата Y - означает столбец (от 0  до 2)
    
    Для вашего удобства, ниже представлены координаты каждой ячейки
              |_0_0_||_0_1_||_0_2_|
              |_1_0_||_1_1_||_1_2_|
              |_2_0_||_2_1_||_2_2_|''')
    print()

def print_field():
    for i in range(3):
        for j in range(3):
            print(f"""|__{field[i, j]}__|""", end='')
        print()


def in_xy(x, y):
    global check
    if x not in digits or y not in digits or int(x) > 2 or int(y) > 2 or int(x) < 0 or int(y) < 0:
        print('Данные ввода не верны, введите числовые координаты Х/Y в пределах от 0 до 2')
        check = False
    else:
        check = True


def double(x, y):
    global check
    if field[x, y] != '-':
        print('Поле занято, введите другие координаты Х/Y в пределах от 0 до 2')
        check = False
    else:
        check = True


def win():
    global win_ch
    if (field[0, 0] == 'X' and field[0, 1] == 'X' and field[0, 2] == 'X') or (
            field[1, 0] == 'X' and field[1, 1] == 'X' and field[1, 2] == 'X') or (
            field[2, 0] == 'X' and field[2, 1] == 'X' and field[2, 2] == 'X') or (
            field[0, 0] == 'X' and field[1, 0] == 'X' and field[2, 0] == 'X') or (
            field[0, 1] == 'X' and field[1, 1] == 'X' and field[2, 1] == 'X') or (
            field[0, 2] == 'X' and field[1, 2] == 'X' and field[2, 2] == 'X') or (
            field[0, 0] == 'X' and field[1, 1] == 'X' and field[2, 2] == 'X') or (
            field[0, 2] == 'X' and field[1, 1] == 'X' and field[2, 0] == 'X'):
        print('Поздравляем, выиграл "Х" - крестик, попробуйте сыграть еще раз')
        win_ch = True
    elif (field[0, 0] == 'O' and field[0, 1] == 'O' and field[0, 2] == 'O') or (
            field[1, 0] == 'O' and field[1, 1] == 'O' and field[1, 2] == 'O') or (
            field[2, 0] == 'O' and field[2, 1] == 'O' and field[2, 2] == 'O') or (
            field[0, 0] == 'O' and field[1, 0] == 'O' and field[2, 0] == 'O') or (
            field[0, 1] == 'O' and field[1, 1] == 'O' and field[2, 1] == 'O') or (
            field[0, 2] == 'O' and field[1, 2] == 'O' and field[2, 2] == 'O') or (
            field[0, 0] == 'O' and field[1, 1] == 'O' and field[2, 2] == 'O') or (
            field[0, 2] == 'O' and field[1, 1] == 'O' and field[2, 0] == 'O'):
        print('Поздравляем, выиграл "0" - нолик, попробуйте сыграть еще раз')
        win_ch = True


field = {}
check = True
win_ch = False
count = 0

for i in range(3):
    for j in range(3):
        field[i, j] = '-'

greet()
while count < 8:
    if count % 2 == 0:
        print('Ходит крестик')
        z = 'X'
    else:
        print('Ходит нолик')
        z = 'O'
    x = input('Введите значение координаты Х = ')
    y = input('Введите значение координаты Y = ')
    in_xy(x, y)
    if check:
        double(int(x), int(y))
    else:
        continue
    if check:
        field[int(x), int(y)] = z
        print_field()
        count += 1
    else:
        continue
    win()
    if win_ch:
        break
