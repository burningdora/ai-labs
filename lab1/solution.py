class DFA:

  def __init__(self):
    self.state = "q0"

  def reset(self):
    self.state = "q0"

  def transition(self, char):
    if self.state == "q0":
      if char == "a":
        self.state = "q1"
      else:
        self.state = "q_trap"

    elif self.state == "q1":
      if char == "a":
        self.state = "q2"
      elif char == "c":
        self.state = "q_accept"
      else:
        self.state = "q_trap"

    elif self.state == "q2":
      if char == "b":
        self.state = "q3"
      else:
        self.state = "q_trap"

    elif self.state == "q3":
      if char == "c":
        self.state = "q1"
      else:
        self.state = "q_trap"

    else:
      self.state = "q_trap"

  def process(self, word):
    self.reset()
    for char in word:
      self.transition(char)
      if self.state == "q_trap":
        return False
    return self.state == "q_accept"


# --- Верификация (тестирование на выборке) ---
dfa = DFA()

test_cases = {
    "ac": True,  # n = 0 -> a + c
    "aabcc": True,  # n = 1 -> a + abc + c
    "aabcabcc": True,  # n = 2 -> a + abc + abc + c
    "abc": False,  # нет начальной 'a' и конечной 'c'
    "aab": False,  # не хватает 'c' на конце
    "aaabc": False,  # нарушение структуры блока abc
    "aabccc": False,  # лишняя 'c'
}

print("Результаты проверки автомата для варианта a(abc)ⁿc:")
print("-" * 40)
for word, expected in test_cases.items():
  result = dfa.process(word)
  status = "УСПЕХ" if result == expected else "ОШИБКА ТЕСТА"
  print(
      f"Слово: '{word:<10}' | Ожидалось: {str(expected):<5} | Ответ:"
      f" {str(result):<5} | [{status}]"
  )
