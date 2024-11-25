import pygame
import sys
from constants import FPS, T
import recieve


class RigidBody:
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


class Cube(RigidBody):
  def get_type(self):
    return "Cube"


class Circle(RigidBody):
  def get_type(self):
    return "Circle"


class Board:
  def __init__(self, len):
    self.length = len  # атрибут отвечает за длину поля (расстояние между очень массивными стенками)

  def get_length(self):
    return self.length


class Initializator:
  def initialize_first_object(self, data):
    if data[0] == "Cube":
      return Cube(int(data[1]), int(data[2]), 0, int(data[3]))
  
  def initialize_second_object(self, data):
    if data[0] == "Cube":
      return Cube(int(data[1]), (-1) * int(data[2]), board.get_length() - int(data[3]), int(data[3]))



def funny_physics(object1, object2, board):
  potential_coordinate_of_first_object = object1.get_coordinate() + object1.get_velocity() * T # потенциальные координаты кубов, если столкновения не случится
  potential_coordinate_of_second_object = object2.get_coordinate() + object2.get_velocity() * T

  global collisions

  if potential_coordinate_of_first_object < 0:
    t_before = abs(object1.get_coordinate() / object1.get_velocity())
    t_after = 0.02 - t_before
    object1.coordinate = -1 * object1.get_velocity() * t_after
    collisions += 1
    object1.velocity *= -1
  if potential_coordinate_of_second_object + object2.get_length() > board.get_length():
    t_before = abs((board.get_length() - (object2.get_coordinate() + object2.get_length())) / object2.get_velocity())
    t_after = 0.02 - t_before
    object2.coordinate = board.get_length() - abs(object2.get_velocity() * t_after) - object2.get_length()
    object2.velocity *= -1
    collisions += 1
  if potential_coordinate_of_second_object - (potential_coordinate_of_first_object + object1.get_length()) >= 0: # проверка, случится ли столкновение
    object1.coordinate += object1.velocity * T
    object2.coordinate += object2.velocity * T
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



if __name__ == "__main__":
  clock = pygame.time.Clock()
  time = 0 # текущее время (в секундах)
  collisions = 0 # количество столкновений


  mans_input = recieve.getting_data()
  board = Board(int(mans_input[0]))

  data_of_first_object = mans_input[1].split() # здесь хранится информация о первом объекте
  data_of_second_object = mans_input[2].split() # здесь хранится информация о втором объекте
  inter = Initializator()
  object1 = inter.initialize_first_object(data_of_first_object)
  object2 = inter.initialize_second_object(data_of_second_object)

  pygame.init()
  screen = pygame.display.set_mode((board.get_length(), 300))
  pygame.display.set_caption("physics vizualization")
  screen.fill((255, 255, 255))
  first_frame = pygame.font.Font(None, 36)
  second_frame = pygame.font.Font(None, 36)
  third_frame = pygame.font.Font(None, 36)
  fourth_frame = pygame.font.Font(None, 36)



  while True:
    screen.fill((255, 255, 255))

    current_time = first_frame.render(f"time = {round(time, 2)} c", 1, (0, 0, 0))
    screen.blit(current_time, (10, 20))
    number_of_collisions = second_frame.render(f"количество столкновений = {collisions}", 1, (0, 0, 0))
    screen.blit(number_of_collisions, (10, 40))
    mass_of_first_object = third_frame.render(f"m1 = {object1.get_mass()} кг", 1, (0, 0, 0))
    screen.blit(mass_of_first_object, (board.get_length() - 200, 20))
    mass_of_second_object = fourth_frame.render(f"m2 = {object2.get_mass()} кг", 1, (0, 0, 0))
    screen.blit(mass_of_second_object, (board.get_length() - 200, 40))


    if object1.get_type() == "Cube":
      pygame.draw.rect(screen, (0, 0, 255), (object1.get_coordinate(), 300 - object1.get_length(), object1.get_length(), object1.get_length()))
    
    if object2.get_type() == "Cube":
      pygame.draw.rect(screen, (255, 0, 0), (object2.get_coordinate(), 300 - object2.get_length(), object2.get_length(), object2.get_length()))


    pygame.display.update()

    time += T
    clock.tick(FPS)

    funny_physics(object1, object2, board)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        break
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          break