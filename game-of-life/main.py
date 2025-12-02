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
            # print("#" if cell == 1 else " ", end = ' ')
            print('■' if cell == 1 else '□', end=' ')
        print()


render(random_state(100, 100))