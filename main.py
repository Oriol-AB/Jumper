def Game(DificultyAmount=0) -> int:
    import pygame
    import sys
    import time
    import pygame
    from Blur_Image import BlurImage

    pygame.init()

    pygame.font.init()


    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 60)

    smaller_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 45)



    WIDTH = 900 #Temp
    HEIGHT = 600 #Temp

    MAX_FPS = 120

    Main_Clock = pygame.time.Clock()

    display = pygame.display.set_mode((WIDTH, HEIGHT))

    logo = pygame.image.load("Logo.png")


    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    backgroud_img = pygame.image.load("background.png").convert()

    sandpit_img = pygame.transform.scale(pygame.image.load("Sandpit.png").convert(), (529, 140))

    sandpit_img.set_colorkey((255, 255, 255))

    ended = False

    class PowerBar:
        def __init__(self) -> int:
            self.SCALE = [525, 25]

            self.filling_scale = [0, 25]

            self.position = [200, 500]

            self.filling_color = (0, 255, 0)

            self.ended = False

            if DificultyAmount == 0:
                self.minimum = 150

                with open("last_difficulty.txt", "w") as f:
                    f.write(str(self.minimum))
                    f.close()

            
            else:

                with open("last_difficulty.txt", "r") as f:
                    self.minimum = int(f.read())

                    f.close()



                if self.minimum + DificultyAmount >= self.SCALE[0]:

                    with open("last_difficulty.txt", "w") as f:
                        f.write("150")
                        f.close()

                    self.ended = True
                
                else:
                    self.minimum += DificultyAmount
                    with open("last_difficulty.txt", "w") as f:
                        f.write(str(self.minimum))


            self.increasing = False

            self.Rect = pygame.Rect(self.position[0], self.position[1], self.SCALE[0], self.SCALE[1])

            self.outline_rect = pygame.Rect(self.position[0]-3, self.position[1]-3, self.SCALE[0]+6, self.SCALE[1]+6)

            self.rendering = True


        
        def Render(self, display) -> None:
            if self.rendering:
                pygame.draw.rect(display, (0, 0, 0), (self.position[0]-3, self.position[1]-3, self.SCALE[0]+6, self.SCALE[1]+6))

                pygame.draw.rect(display, (255, 255, 255), self.Rect)

                pygame.draw.rect(display, self.filling_color, (self.position[0], self.position[1], self.filling_scale[0], self.filling_scale[1]))

                pygame.draw.rect(display, (0, 0, 0), (self.position[0] + self.minimum, self.position[1] - 3, 3, self.SCALE[1]+6))
        
        def IncreasePower(self, deltatime) -> None:
            if self.increasing:
                self.filling_scale[0] += round(100 * deltatime)

        def TooMuchPower(self) -> bool:

            if self.filling_scale[0] >= self.SCALE[0]:
                return True
            
            return False

        def CheckPower(self) -> bool:
            if self.filling_scale[0] > self.minimum:
                return True
            
            return False
        
        def Update(self):

            if self.filling_scale[0] >= 50 and self.increasing == True:
                self.rendering = False

            if self.filling_scale[0] >= 375:
                self.filling_color = (255, 0, 0)
            
            elif self.filling_scale[0] >= 200:
                self.filling_color = (255, 100, 0)
            
            elif self.filling_scale[0] >= 150:
                self.filling_color = (0, 255, 0)

    



    MainPowerBar = PowerBar()

    if MainPowerBar.ended == True:
        return 3



    MainPowerBar.increasing = False

    prev = time.time()


    class Player:
        def __init__(self) -> None:
            self.position = [95, 150]
        
            self.scale = [60, 150]

            self.index = 0

            self.animation_state = 0


            #self.image = pygame.transform.scale(pygame.image.load("Player/Player.png").convert(), (200, 250))

            self.idle_image = [
                                    pygame.transform.scale(pygame.image.load("Player/Player.png").convert(), (200, 250))
            ]
            
            self.jump_images = [
                                    pygame.transform.scale(pygame.image.load("Player/Player.png").convert(), (200, 250)),
                                    pygame.image.load("Player/1.png").convert(),
                                    pygame.image.load("Player/2.png").convert(),
                                    pygame.image.load("Player/3.png").convert(),
                                    pygame.image.load("Player/4.png").convert(),
                                    pygame.image.load("Player/5.png").convert(),
                                    pygame.image.load("Player/6.png").convert()
            ]

            self.to_render = self.idle_image[self.index]



            for i in self.jump_images:
                i.set_colorkey((0, 0, 0))

            self.idle_image[0].set_colorkey((0, 0, 0))

            self.hitbox = pygame.Rect(self.position[0], self.position[1], self.scale[0], self.scale[1])
    
        def Animate(self):
            if self.animation_state == 0:
                return self.idle_image[0]

            elif self.animation_state == 1:
                return self.jump_images[round(self.index)]

        
        def Update(self) -> bool:
            if self.animation_state == 0:
                self.index = 0
            
            elif self.animation_state == 1:
                if self.index < len(self.jump_images) - 1:
                    self.index += 0.03

                    self.to_render = self.Animate()
                
                else:
                    return True
            
            return False



        def Render(self, display) -> None:
            #pygame.draw.rect(display, (255, 255, 255), self.hitbox)



            if self.to_render in self.jump_images and self.to_render != self.jump_images[0]:

                self.position[0] += 1
                display.blit(self.to_render, (self.position[0]+70, self.position[1]-75))
            
            else: 
                display.blit(self.to_render, self.hitbox)    


    
    MainPlayer = Player()

    update_rect = pygame.Rect(20, 150, 579, 310)

    
    count = 0

    while True:

        #display.fill((165, 42, 42))

        display.blit(backgroud_img, (0, 0))

        now = time.time()

        deltatime = now - prev

        prev = now

        display.blit(sandpit_img, (250, 320))

        pygame.draw.line(display, (255, 0, 0), (300, 320), (245, 460), 5)
        pygame.draw.line(display, (255, 255, 255), (295, 320), (240, 460), 5)
        
        

        #Player---------------------------------

        

        MainPlayer.Animate()

        ended = MainPlayer.Update()

        MainPlayer.Render(display)


        #Power bar-----------------------------
        MainPowerBar.IncreasePower(deltatime)

        MainPowerBar.Update()

        MainPowerBar.Render(display)

        #pygame.draw.polygon(display, (255, 220, 140), ((250, 320), (680, 320), 
        # (730, 460), (200, 460)))



        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    MainPowerBar.increasing = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:

                    

                    MainPowerBar.increasing = False

                    MainPowerBar.rendering = True

                    MainPlayer.animation_state = 1

                    MainPlayer.index = 0
                    

                    if MainPowerBar.TooMuchPower():
                        MainPowerBar.rendering = True

                        MainPowerBar.Render(display)

                        pygame.display.update(MainPowerBar.outline_rect)

                        time.sleep(1)
                        
                        if ended:
                            return 1 
                            pygame.quit()

                    else:
                        if MainPowerBar.CheckPower():
                            pygame.display.flip()

                            pygame.image.save(display, "temp.png")

                            BlurImage("temp.png", 9)

                            

                            MainPowerBar.rendering = True

                            MainPowerBar.Render(display)

                            pygame.display.update(MainPowerBar.outline_rect)

                            time.sleep(1)

                            if ended:
                                return 2
                                pygame.quit()
                        
                        else:
                            
                            MainPowerBar.rendering = True

                            MainPowerBar.Render(display)

                            pygame.display.update(MainPowerBar.outline_rect)

                            time.sleep(1)

                            if ended:

                                return 4
                                pygame.quit()

        

        """if MainPlayer.index == len(MainPlayer.jump_images) - 1:
            ended = True"""
        

        if MainPlayer.index >= len(MainPlayer.jump_images) - 1:
            
            if MainPowerBar.TooMuchPower():
                return 1 
                pygame.quit()

            if MainPowerBar.CheckPower():
                return 2
                pygame.quit()

            else:
                return 4
                pygame.quit()

        
        Main_Clock.tick(MAX_FPS)

        print(round(Main_Clock.get_fps()))

        if count == 0:
            pygame.display.flip()
            count = 1

        else:
            pygame.display.update(update_rect)
            pygame.display.update(MainPowerBar.outline_rect)


#---------------------------------------------------------------------------------------------------------


def WellDone()-> int:
    import pygame
    import sys


    WIDTH, HEIGHT = 900, 600

    pygame.init()

    pygame.font.init()

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 30)

    Next = font.render("Continuar", False, (0, 0, 0))

    display = pygame.display.set_mode((WIDTH, HEIGHT))

    logo = pygame.image.load("Logo.png")


    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    background = pygame.image.load("temp.png").convert()

    button = pygame.transform.scale(pygame.image.load("GUI_BUTTON.png").convert(), (300, 75))
    white_button = pygame.transform.scale(pygame.image.load("GUI_BUTTON_WHITE.png").convert(), (300, 75))

    text = pygame.image.load("Marked_Font.png").convert()

    text.set_colorkey((0, 0, 0))
    button.set_colorkey((0, 0, 0))

    white_button.set_colorkey((0, 0, 0))

    to_render = button


    Next_Rect = pygame.Rect(305, 375, 300, 75)


    MainClock = pygame.time.Clock()

    while True:

        mx, my = pygame.mouse.get_pos()

        display.blit(background, (0, 0))
        
        display.blit(text, (150, 250))
    
        
        display.blit(to_render, (305, 375))


        display.blit(Next, (325, 400))

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if Next_Rect.collidepoint(mx, my):
                        return 50
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 50

        
        if Next_Rect.collidepoint(mx, my):
            to_render = white_button
        
        else:
            to_render = button

        MainClock.tick(120)

        pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------------

"""
TODO:  make tutorial, player animations,sound+ music.
"""


def TryAgain() -> int:
    import pygame
    import sys

    pygame.init()

    pygame.font.init()

    WIDTH, HEIGHT = 900, 600

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 60)
    small_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 45)

    #TooMuch = font.render("Demasiado!", False, "orange")

    #TryAgain = small_font.render("¿Volver a empezar?", False, "orange")

    Yes = small_font.render("Sí", False, (0, 0, 0))

    No = small_font.render("No", False, (0, 0, 0))

    Yes_Rect = pygame.Rect(230, 420, 200, 75)

    No_Rect = pygame.Rect(480, 420, 200, 75)


    display = pygame.display.set_mode((WIDTH, HEIGHT))

    logo = pygame.image.load("Logo.png")


    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    MainClock = pygame.time.Clock()

    button = pygame.image.load("GUI_BUTTON.png").convert()

    white_button = pygame.image.load("GUI_BUTTON_WHITE.png").convert()

    TryAgain = pygame.image.load("TryAgain.png").convert()

    TooMuch = pygame.image.load("Too-Much.png").convert()

    yes_to_render = button

    no_to_render = button

    button.set_colorkey((255, 255, 255))

    white_button.set_colorkey((0, 0, 0))

    while True:

        mx, my = pygame.mouse.get_pos()

        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    if Yes_Rect.collidepoint(mx, my):
                        return 1
                        pygame.quit()

                    elif No_Rect.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()


        if Yes_Rect.collidepoint(mx, my):
            yes_to_render = white_button

        else:
            yes_to_render = button

        
        if No_Rect.collidepoint(mx, my):
            no_to_render = white_button

        else:
            no_to_render = button
        
        
        display.blit(TooMuch, (WIDTH/2-280, HEIGHT/2 -100))

        display.blit(TryAgain, (-20, HEIGHT/2 - 20))



        display.blit(yes_to_render, Yes_Rect)

        display.blit(Yes, (291, 434))

        display.blit(no_to_render, No_Rect)

        display.blit(No, (540, 434))

        pygame.display.flip()

        MainClock.tick(120)



#------------------------------------------------------------------------

def Congratulations() -> None:
    import pygame
    import sys

    pygame.init()

    pygame.font.init()

    WIDTH, HEIGHT = 900, 600

    display = pygame.display.set_mode((WIDTH, HEIGHT))

    logo = pygame.image.load("Logo.png")


    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")
    
    Clock = pygame.time.Clock()

    background = pygame.image.load("temp.png").convert()

    Congrats = pygame.image.load("Congrats.png").convert()

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 15)

    big_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 35)

    credit = font.render("Creado por: Oriol AB", False, "orange")

    quit_text = big_font.render("Salir", False, (0, 0, 0))

    

    button = pygame.image.load("GUI_BUTTON.png").convert()

    white_button = pygame.image.load("GUI_BUTTON_WHITE.png").convert()

    to_render = button

    button_rect = pygame.Rect(360, 375, 200, 75)

    Congrats.set_colorkey((0, 0, 0))

    Thanks = pygame.transform.scale(pygame.image.load("thanks.png").convert(), (600, 40))

    Thanks.set_colorkey((0, 0, 0))


    while True:

        mx, my = pygame.mouse.get_pos()

        display.fill((0, 0, 0))

        display.blit(Congrats, (125, 200))

        display.blit(Thanks, (175, 285))

        display.blit(credit, (540, 550))

        display.blit(to_render, button_rect)

        display.blit(quit_text, (375, 395))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if button_rect.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()
        
        
        if button_rect.collidepoint(mx, my):
            to_render = white_button
        
        else:
            to_render = button

    
        Clock.tick(120)

        pygame.display.flip()
    

def MainMenu() -> int:
    import pygame
    import sys

    pygame.init()

    pygame.font.init()

    WIDTH, HEIGHT = 900, 600

    display = pygame.display.set_mode((WIDTH, HEIGHT))

    logo = pygame.image.load("Logo.png")

    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    Clock = pygame.time.Clock()

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 35)

    small_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 15)

    play = font.render("Jugar", False, (0, 0, 0))
    Quit = font.render("Salir", False, (0, 0, 0))

    credits = small_font.render("Creado por: Oriol AB", False, "orange")

    button = pygame.transform.scale(pygame.image.load("GUI_BUTTON.png").convert(), (200, 75))

    white_button = pygame.transform.scale(pygame.image.load("GUI_BUTTON_WHITE.png").convert(), (200, 75))

    button_rect = pygame.Rect(355, 310, 200, 75)

    quit_button_rect = pygame.Rect(355, 410, 200, 75)

    button_to_render = button

    quit_button_to_render = button



    images = [
        pygame.transform.scale(pygame.image.load("Title/1.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/2.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/3.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/4.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/5.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/6.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/7.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/8.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/9.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/10.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/11.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/12.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/13.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/14.png").convert(), (500, 160)),
        pygame.transform.scale(pygame.image.load("Title/15.png").convert(), (500, 160)),
    ]

    to_render = 0

    while True:

        mx, my = pygame.mouse.get_pos()

        display.fill((0, 0, 0))

        display.blit(button_to_render, button_rect)

        display.blit(quit_button_to_render, quit_button_rect)

        display.blit(play, (369, 328))

        display.blit(Quit, (369, 428))

        display.blit(credits, (570, 560))

        to_render += 0.05

        if to_render > 14:
            to_render = 0

        display.blit(images[round(to_render)], (210, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if button_rect.collidepoint(mx, my):
                        return 1
                    
                    elif quit_button_rect.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()
        
        if button_rect.collidepoint(mx, my):
            button_to_render = white_button

        else:
            button_to_render = button
        

        if quit_button_rect.collidepoint(mx, my):
            quit_button_to_render = white_button

        else:
            quit_button_to_render = button
        

        pygame.display.flip()

        Clock.tick(120)
    

def TooShort() -> int:
    import pygame
    import sys

    pygame.init()

    pygame.font.init()

    WIDTH, HEIGHT = 900, 600

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 60)
    small_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 45)

    #TooMuch = font.render("Demasiado!", False, "orange")

    

    

    #TryAgain = small_font.render("¿Volver a empezar?", False, "orange")

    Yes = small_font.render("Sí", False, (0, 0, 0))

    No = small_font.render("No", False, (0, 0, 0))

    Yes_Rect = pygame.Rect(230, 420, 200, 75)

    No_Rect = pygame.Rect(480, 420, 200, 75)


    display = pygame.display.set_mode((WIDTH, HEIGHT))

    logo = pygame.image.load("Logo.png")

    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    TooShort = pygame.image.load("Too-Short.png").convert()

    TryAgain = pygame.image.load("TryAgain.png").convert()

    MainClock = pygame.time.Clock()

    button = pygame.image.load("GUI_BUTTON.png").convert()

    white_button = pygame.image.load("GUI_BUTTON_WHITE.png").convert()

    yes_to_render = button

    no_to_render = button

    button.set_colorkey((255, 255, 255))

    white_button.set_colorkey((0, 0, 0))

    while True:

        mx, my = pygame.mouse.get_pos()

        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    if Yes_Rect.collidepoint(mx, my):
                        return 1
                        pygame.quit()

                    elif No_Rect.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()


        if Yes_Rect.collidepoint(mx, my):
            yes_to_render = white_button

        else:
            yes_to_render = button

        
        if No_Rect.collidepoint(mx, my):
            no_to_render = white_button

        else:
            no_to_render = button
        
        
        display.blit(TooShort, (265, 165))

        display.blit(TryAgain, (-20, HEIGHT/2 - 20))



        display.blit(yes_to_render, Yes_Rect)

        display.blit(Yes, (291, 434))

        display.blit(no_to_render, No_Rect)

        display.blit(No, (540, 434))

        pygame.display.flip()

        MainClock.tick(120)

        

if __name__ == "__main__":
    count = 0
    MainMenu()
    while True:
        if count == 0:
            ReturnValue = Game()
        else:
            ReturnValue = Game(100)

        if ReturnValue == 1:
            TryAgain()
            count = -1

        elif ReturnValue == 2:
            WellDone()

        elif ReturnValue == 3:
            Congratulations()
            break
    
        elif ReturnValue == 4:
            TooShort()
            count = -1

        count += 1
