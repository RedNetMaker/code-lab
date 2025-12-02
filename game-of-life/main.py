import random

# Создание мёртвой доски
def dead_state(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

# Создание доски с случайным расположением живых клеток
def random_state(rows, cols):
    state = dead_state(rows, cols)
    for i in range(rows):
        for j in range(cols):
            # state[i][j] = random.randint(0, 1)
            if random.random() < 0.5:
                state[i][j] = 1
            else:
                state[i][j] = 0

    return state

# Вывод состояния доски в терминал
def render(state):
    for row in state:
        for cell in row:
            print('■' if cell == 1 else '□', end=' ')
        print()

# Подсчёт соседей
def count_neighbors(state, row, cell):
    sum = 0

    left = cell - 1
    right = cell + 1
    top = row - 1
    bottom = row + 1

    # Обработка граничных клеток
    if row == 0:
        top = 0
    if row == len(state) - 1:
        bottom = len(state) - 1
    if cell == 0:
        left = 0
    if cell == len(state[row]) - 1:
        right = len(state[row]) - 1

    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            sum += state[i][j]
    return sum - state[row][cell]

# Рассчёт следующего состояния доски
def next_board_state(state):
    new_state = dead_state(len(state), len(state[0]))
    for row in range(len(state)):
        for cell in range(len(state[row])):
            count = count_neighbors(state, row, cell)
            if state[row][cell] == 1:
                if count < 2 or count > 3:
                    new_state[row][cell] = 0
                else:
                    new_state[row][cell] = 1
            else:
                if count == 3:
                    new_state[row][cell] = 1
                else:
                    new_state[row][cell] = 0
    return new_state

if __name__ == "__main__":
    render(random_state(100, 100))