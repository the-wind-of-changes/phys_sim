import pygame


def getting_data():
    pygame.init()
    zero_string = pygame.font.Font(None, 24)
    first_string = pygame.font.Font(None, 24)
    second_string = pygame.font.Font(None, 24)
    third_string = pygame.font.Font(None, 36)
    result = []
    screen = pygame.display.set_mode((900, 600))
    font = pygame.font.Font(None, 64)
    clock = pygame.time.Clock()
    input_area = pygame.Rect(150, 300, 600, 120)
    text = ''
    counter = 0

    while counter < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                counter = 10
            elif event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:
                    counter = 10
                  elif event.key == pygame.K_RETURN:
                      result.append(text)
                      text = ''
                      counter += 1
                  elif event.key == pygame.K_BACKSPACE:
                      text = text[:-1]
                  else:
                      text += event.unicode
        
        screen.fill((100, 100, 100))
        zero_message = zero_string.render("Сначала введите длину поля (число от 500 до 1500)", 1, (255, 255, 255))
        screen.blit(zero_message, (10, 50))
        first_message = first_string.render(" Далее поочередно задайте объект 1 и 2 (вводя каждый из объектов вводите Enter) по следующему примеру", 1, (255, 255, 255))
        screen.blit(first_message, (10, 100))
        second_message = second_string.render(
"тип_объекта масса начальная_скорость (рекомендуется ставить от 150) длина_стороны/радиус (до 230)", 1, (255, 255, 255))
        screen.blit(second_message, (10, 180))
        third_message = third_string.render("Например: Cube 10 250 150", 1, (255, 255, 255))
        screen.blit(third_message, (10, 240))
        showing_data = font.render(text, 1, (255, 255, 255))
        screen.blit(showing_data, (180, 330))
        pygame.draw.rect(screen, (255, 255, 255), input_area, 2)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
    return result