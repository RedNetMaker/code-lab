from main import next_board_state, count_neighbors

def test_count_neighbors():
    state = [
        [0, 0, 1],
        [0, 1, 1],
        [0, 1, 0],
    ]
    expected_count = 3
    actual_count = count_neighbors(state, 0, 1)
    if actual_count == expected_count:
        print("\033[32mTest count neighbors passed\033[0m")
    else:
        print("\033[31mTest count neighbors failed\033[0m")
        print(f"Expected: {expected_count}")
        print(f"Actual: {actual_count}")

# Тест что мёртвая клетка остаётся мёртвой
def test_next_board_state_dead_cell():
    init_state = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 0, 1],
    ]
    expected_state = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    actual_state = next_board_state(init_state)

    if actual_state == expected_state:
        print("\033[32mTest dead cell passed\033[0m")
    else:
        print("\033[31mTest dead cell failed\033[0m")
        print(f"Expected: {expected_state}")
        print(f"Actual: {actual_state}")

# Тест что живая клетка остаётся живой и рождается новая клетка
def test_next_board_state_live_cell():
    init_state = [
        [0, 0, 1],
        [0, 1, 1],
        [0, 0, 0],
    ]
    expected_state = [
        [0, 1, 1],
        [0, 1, 1],
        [0, 0, 0],
    ]
    actual_state = next_board_state(init_state)
    if actual_state == expected_state:
        print("\033[32mTest live cell passed\033[0m")
    else:
        print("\033[31mTest live cell failed\033[0m")
        print(f"Expected: {expected_state}")
        print(f"Actual: {actual_state}")

# Тест что живая клетка умирает если у неё больше 3 соседей
def test_next_board_state_excess_cell():
    init_state = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
    expected_state = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    actual_state = next_board_state(init_state)
    if actual_state == expected_state:
        print("\033[32mTest excess cell passed\033[0m")
    else:
        print("\033[31mTest excess cell failed\033[0m")
        print(f"Expected: {expected_state}")
        print(f"Actual: {actual_state}")

if __name__ == "__main__":
    test_count_neighbors()
    test_next_board_state_dead_cell()
    test_next_board_state_live_cell()
    test_next_board_state_excess_cell()