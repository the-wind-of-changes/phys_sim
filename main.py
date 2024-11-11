import pygame
import sys


class Rigid_body:
  def __init__(self, m, v, x0, l):
    self.coordinate = x0 # координата тела
    self.length = l # сторона тела
    self.mass = m # масса тела
    self.velocity = v # скорость тела
    
  
  def get_coordinate(self):
    return self.coordinate

  def get_length(self):
    return self.length

  def get_mass(self):
    return self.mass

  def get_velocity(self):
    return self.velocity


class Cube(Rigid_body):
  def get_type(self):
    return "Cube"


class Circle(Rigid_body):
  def get_type(self):
    return "Circle"


class Board:
  def __init__(self, len):
    self.length = len  # атрибут отвечает за длину поля (расстояние между очень массивными стенками)

  def get_length(self):
    return self.length


fps = 50
clock = pygame.time.Clock()
time = 0 # текущее время (в секундах)
collisions = 0 # количество столкновений
t = 1/fps # время между двумя кадрами


board = Board(int(input("Введите длину поля от 500 до 1500: ")))
print()
print("Задайте объект 1 по следующему шаблону:")
print("тип_объекта масса начальная_скорость (рекомендуется ставить от 150) длина_стороны/радиус (до 230)")
print("")
print("Например: Cube 10 250 150")
data1 = input().split()
print("Задайте объект 2")
data2 = input().split()
if data1[0] == "Cube":
  object1 = Cube(int(data1[1]), int(data1[2]), 0, int(data1[3]))
# elif data1[0] == "Circle":
#   object1 = Circle(int(data1[1]), int(data1[2]), int(data1[3]), int(data1[3]))
else:
  print("Неверно введены начальные данные")
  sys.exit()
if data2[0] == "Cube":
  object2 = Cube(int(data2[1]), (-1) * int(data2[2]), board.get_length() - int(data2[3]), int(data2[3]))
# elif data2[0] == "Circle":
#   object2 = Circle(int(data2[1]), int(data2[2]), board.get_length() - int(data2[3]), int(data2[3]))
else:
  print("Неверно введены начальные данные")
  sys.exit()


pygame.init()
screen = pygame.display.set_mode((board.get_length(), 300), flags=pygame.NOFRAME)
screen.fill((255, 255, 255))
f1 = pygame.font.Font(None, 36)
f2 = pygame.font.Font(None, 36)
f3 = pygame.font.Font(None, 36)
f4 = pygame.font.Font(None, 36)


while True:
  screen.fill((255, 255, 255))

  text1 = f1.render(f"time = {round(time, 2)} c", 1, (0, 0, 0))
  screen.blit(text1, (10, 20))
  text2 = f2.render(f"количество столкновений = {collisions}", 1, (0, 0, 0))
  screen.blit(text2, (10, 40))
  text3 = f3.render(f"m1 = {object1.get_mass()} кг", 1, (0, 0, 0))
  screen.blit(text3, (board.get_length() - 200, 20))
  text4 = f4.render(f"m2 = {object2.get_mass()} кг", 1, (0, 0, 0))
  screen.blit(text4, (board.get_length() - 200, 40))


  if object1.get_type() == "Cube":
    pygame.draw.rect(screen, (0, 0, 255), (object1.get_coordinate(), 300 - object1.get_length(), object1.get_length(), object1.get_length()))
  # else:
  #   pygame.draw.circle(screen, (255, 0, 0), (object1.get_coordinate(), 150))
  
  if object2.get_type() == "Cube":
    pygame.draw.rect(screen, (255, 0, 0), (object2.get_coordinate(), 300 - object2.get_length(), object2.get_length(), object2.get_length()))
  # else:
  #   pygame.draw.circle(screen, (255, 0, 0), (object2.get_coordinate(), 300 - object2.get_length()), object2.get_length())

  pygame.display.update()

  time += t
  clock.tick(fps)

  x1 = object1.get_coordinate() + object1.get_velocity() * t # потенциальные координаты кубов, если столкновения не случится
  x2 = object2.get_coordinate() + object2.get_velocity() * t

  if x1 < 0:
    t_before = abs(object1.get_coordinate() / object1.get_velocity())
    t_after = 0.02 - t_before
    object1.coordinate = -1 * object1.get_velocity() * t_after
    collisions += 1
    object1.velocity *= -1
  if x2 + object2.get_length() > board.get_length():
    t_before = abs((board.get_length() - (object2.get_coordinate() + object2.get_length())) / object2.get_velocity())
    t_after = 0.02 - t_before
    object2.coordinate = board.get_length() - abs(object2.get_velocity() * t_after) - object2.get_length()
    object2.velocity *= -1
    collisions += 1
  if x2 - (x1 + object1.get_length()) >= 0: # проверка, случится ли столкновение
    object1.coordinate += object1.velocity * t
    object2.coordinate += object2.velocity * t
  else: # если столкновение случается, расчитываем новые скорости по ЗСИ и ЗСЭ, также считаем координаты после столкновения
    new_velocity2 = (object2.get_mass() * object2.get_velocity() - object1.get_mass() * object2.get_velocity() + 2 * object1.get_mass() * object1.get_velocity()) / (object2.get_mass() + object1.get_mass())
    new_velocity1 = (object1.get_mass() * object1.get_velocity() - object2.get_mass() * object1.get_velocity() + 2 * object2.get_mass() * object2.get_velocity()) / (object1.get_mass() + object2.get_mass())
    time_before_collision = (object2.get_coordinate() - (object1.get_coordinate() + object1.get_length())) / abs(object1.get_velocity() - object2.get_velocity())
    time_after_collision = 0.02 - time_before_collision
    object1.coordinate += object1.get_velocity() * time_before_collision + new_velocity1 * time_after_collision
    object2.coordinate += object2.get_velocity() * time_before_collision + new_velocity2 * time_after_collision
    object1.velocity = new_velocity1
    object2.velocity = new_velocity2
    collisions += 1



  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      break

sys.exit()
