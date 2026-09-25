import random
import time


class Node:
  """Узел игрового дерева."""

  def __init__(self, value=None):
    self.value = value  # Значение для листьев
    self.children = []  # Потомки узла


def generate_tree(depth, width, current_depth=0):
  """Рекурсивно генерирует игровое дерево заданной глубины и ширины."""
  if current_depth == depth:
    # Листовое значение (случайное от -50 до 50)
    return Node(value=random.randint(-50, 50))

  node = Node()
  for _ in range(width):
    node.children.append(generate_tree(depth, width, current_depth + 1))
  return node


# 1. Классический алгоритм Мини-макс
def minimax(node, depth, maximizing_player, counter):
  counter["nodes"] += 1

  if not node.children or depth == 0:
    return node.value

  if maximizing_player:
    max_eval = float("-inf")
    for child in node.children:
      eval = minimax(child, depth - 1, False, counter)
      max_eval = max(max_eval, eval)
    return max_eval
  else:
    min_eval = float("inf")
    for child in node.children:
      eval = minimax(child, depth - 1, True, counter)
      min_eval = min(min_eval, eval)
    return min_eval


# 2. Оптимизированный Мини-макс с альфа-бета отсечением
def minimax_alpha_beta(node, depth, alpha, beta, maximizing_player, counter):
  counter["nodes"] += 1

  if not node.children or depth == 0:
    return node.value

  if maximizing_player:
    max_eval = float("-inf")
    for child in node.children:
      eval = minimax_alpha_beta(
          child, depth - 1, alpha, beta, False, counter
      )
      max_eval = max(max_eval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break  # Бета-отсечение
    return max_eval
  else:
    min_eval = float("inf")
    for child in node.children:
      eval = minimax_alpha_beta(child, depth - 1, alpha, beta, True, counter)
      min_eval = min(min_eval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break  # Альфа-отсечение
    return min_eval


# --- Тестирование и сравнение эффективности ---
if __name__ == "__main__":
  # Параметры дерева (например, глубина 5, ширина 3 — соответствуют вариантам 2/4)
  DEPTH = 5
  WIDTH = 3

  print(
      f"Генерация игрового дерева (глубина: {DEPTH}, ширина: {WIDTH})..."
  )
  root_node = generate_tree(DEPTH, WIDTH)

  # Тест классического Мини-макса
  counter_mm = {"nodes": 0}
  start_time = time.time()
  result_mm = minimax(root_node, DEPTH, True, counter_mm)
  time_mm = time.time() - start_time

  # Тест Мини-макса с альфа-бета отсечением
  counter_ab = {"nodes": 0}
  start_time = time.time()
  result_ab = minimax_alpha_beta(
      root_node, DEPTH, float("-inf"), float("inf"), True, counter_ab
  )
  time_ab = time.time() - start_time

  # Вывод результатов сравнения
  print("\n" + "=" * 45)
  print(f"{'СРАВНЕНИЕ АЛГОРИТМОВ':^45}")
  print("=" * 45)
  print(f"Результат классического Minimax:       {result_mm}")
  print(
      f"  - Проверено узлов: {counter_mm['nodes']}"
      f" | Время: {time_mm:.6f} сек."
  )
  print("-" * 45)
  print(f"Результат Minimax с Alpha-Beta:        {result_ab}")
  print(
      f"  - Проверено узлов: {counter_ab['nodes']}"
      f" | Время: {time_ab:.6f} сек."
  )
  print("=" * 45)

  if counter_mm["nodes"] > 0:
    saved_nodes = (
        (counter_mm["nodes"] - counter_ab["nodes"])
        / counter_mm["nodes"]
        * 100
    )
    print(
        f"Эффективность: альфа-бета отсечение проверило на {saved_nodes:.1f}%"
        " меньше узлов!"
    )
