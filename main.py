def Game(DificultyAmount=0) -> int:
    import pygame
    import sys
    import time
    import pygame
    from Data.Blur_Image import BlurImage

    pygame.init()

    pygame.font.init()

    pygame.mixer.init()


    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 60)

    smaller_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 45)



    WIDTH = 900 #Temp
    HEIGHT = 600 #Temp

    MAX_FPS = 120

    Main_Clock = pygame.time.Clock()

    display = pygame.display.set_mode((WIDTH, HEIGHT))

    logo = pygame.image.load("Data/Logo.png")

    

    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    backgroud_img = pygame.image.load("Data/background.png").convert()

    sandpit_img = pygame.transform.scale(pygame.image.load("Data/Sandpit.png").convert(), (529, 140))

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

                with open("Data/last_difficulty.txt", "w") as f:
                    f.write(str(self.minimum))
                    f.close()

            
            else:

                with open("Data/last_difficulty.txt", "r") as f:
                    self.minimum = int(f.read())

                    f.close()



                if self.minimum + DificultyAmount >= self.SCALE[0]:

                    with open("Data/last_difficulty.txt", "w") as f:
                        f.write("150")
                        f.close()

                    self.ended = True
                
                else:
                    self.minimum += DificultyAmount
                    with open("Data/last_difficulty.txt", "w") as f:
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

    if MainPowerBar.minimum == 150:
        song = pygame.mixer.music.load("Music/2.wav")
        pygame.mixer.music.play(loops=100, fade_ms = 1000)

    elif MainPowerBar.minimum == 250:
        pass


    elif MainPowerBar.minimum == 350:
        song = pygame.mixer.music.load("Music/3.wav")

        pygame.mixer.music.play(loops=100, fade_ms = 1000)

    elif MainPowerBar.minimum == 450:
        song = pygame.mixer.music.load("Music/4.wav")

        pygame.mixer.music.play(loops=100,fade_ms = 1000)
    
    else:
        print(MainPowerBar.minimum)

    
    

    if MainPowerBar.ended == True:
        return 3



    MainPowerBar.increasing = False

    prev = time.time()


    class Player:
        def __init__(self) -> None:

            if MainPowerBar.minimum == 150 or MainPowerBar.minimum == 250:
                self.position = [95, 150]
            
            elif MainPowerBar.minimum == 350:
                self.position = [75, 150]
            
            elif MainPowerBar.minimum == 450:
                self.position = [40, 150]
        
            self.scale = [60, 150]

            self.index = 0

            self.animation_state = 0


            #self.image = pygame.transform.scale(pygame.image.load("Player/Player.png").convert(), (200, 250))

            self.idle_image = [
                                    pygame.transform.scale(pygame.image.load("Player/Player.png").convert(), (200, 250))
            ]
            
            self.jump_Data = [
                                    pygame.transform.scale(pygame.image.load("Player/Player.png").convert(), (200, 250)),
                                    pygame.image.load("Player/1.png").convert(),
                                    pygame.image.load("Player/2.png").convert(),
                                    pygame.image.load("Player/3.png").convert(),
                                    pygame.image.load("Player/4.png").convert(),
                                    pygame.image.load("Player/5.png").convert(),
                                    pygame.image.load("Player/6.png").convert()
            ]

            self.to_render = self.idle_image[self.index]



            for i in self.jump_Data:
                i.set_colorkey((0, 0, 0))

            self.idle_image[0].set_colorkey((0, 0, 0))

            self.hitbox = pygame.Rect(self.position[0], self.position[1], self.scale[0], self.scale[1])
    
        def Animate(self):
            if self.animation_state == 0:
                return self.idle_image[0]

            elif self.animation_state == 1:
                return self.jump_Data[round(self.index)]

        
        def Update(self) -> bool:
            if self.animation_state == 0:
                self.index = 0
            
            elif self.animation_state == 1:
                if self.index < len(self.jump_Data) - 1:
                    self.index += 0.03

                    self.to_render = self.Animate()
                
                else:
                    return True
            
            return False



        def Render(self, display) -> None:
            #pygame.draw.rect(display, (255, 255, 255), self.hitbox)



            if self.to_render in self.jump_Data and self.to_render != self.jump_Data[0]:
                if MainPowerBar.minimum == 150:
                    self.position[0] += 0.5

                if MainPowerBar.minimum == 250:
                    self.position[0] += 1

                if MainPowerBar.minimum == 350:
                    self.position[0] += 1.5

                if MainPowerBar.minimum == 450:
                    self.position[0] += 2

                display.blit(self.to_render, (self.position[0]+70, self.position[1]-75))
            
            else: 
                display.blit(self.to_render, self.hitbox)    


    
    MainPlayer = Player()

    update_rect = pygame.Rect(20, 100, 760, 360)

    
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
                    if MainPlayer.animation_state != 1:
                        MainPowerBar.increasing = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and MainPlayer.animation_state != 1:

                    

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

                            pygame.image.save(display, "Data/temp.png")

                            BlurImage("Data/temp.png", 9)

                            

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
        
        
        

        """if MainPlayer.index == len(MainPlayer.jump_Data) - 1:
            ended = True"""
        

        if MainPlayer.index >= len(MainPlayer.jump_Data) - 1:
            
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

        #print(round(Main_Clock.get_fps()))

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

    logo = pygame.image.load("Data/Logo.png")


    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    background = pygame.image.load("Data/temp.png").convert()

    button = pygame.transform.scale(pygame.image.load("Data/GUI_BUTTON.png").convert(), (300, 75))
    white_button = pygame.transform.scale(pygame.image.load("Data/GUI_BUTTON_WHITE.png").convert(), (300, 75))

    text = pygame.image.load("Data/Marked_Font.png").convert()

    text.set_colorkey((0, 0, 0))
    button.set_colorkey((0, 0, 0))

    white_button.set_colorkey((0, 0, 0))

    to_render = button


    Next_Rect = pygame.Rect(305, 375, 300, 75)


    MainClock = pygame.time.Clock()

    while True:

        mx, my = pygame.mouse.get_pos()

        display.blit(background, (0, 0))
        
        display.blit(text, (130, 250))
    
        
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

    logo = pygame.image.load("Data/Logo.png")


    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    MainClock = pygame.time.Clock()

    button = pygame.image.load("Data/GUI_BUTTON.png").convert()

    white_button = pygame.image.load("Data/GUI_BUTTON_WHITE.png").convert()

    TryAgain = pygame.image.load("Data/TryAgain.png").convert()

    TooMuch = pygame.image.load("Data/Too-Much.png").convert()

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
        
        
        display.blit(TooMuch, (WIDTH/2-305, HEIGHT/2 -100))

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

    logo = pygame.image.load("Data/Logo.png")


    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")
    
    Clock = pygame.time.Clock()

    background = pygame.image.load("Data/temp.png").convert()

    Congrats = pygame.image.load("Data/Congrats.png").convert()

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 15)

    big_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 35)

    credit = font.render("Creado por: Oriol AB", False, "orange")

    quit_text = big_font.render("Salir", False, (0, 0, 0))

    

    button = pygame.image.load("Data/GUI_BUTTON.png").convert()

    white_button = pygame.image.load("Data/GUI_BUTTON_WHITE.png").convert()

    to_render = button

    button_rect = pygame.Rect(360, 375, 200, 75)

    Congrats.set_colorkey((0, 0, 0))

    Thanks = pygame.transform.scale(pygame.image.load("Data/thanks.png").convert(), (600, 40))

    Thanks.set_colorkey((0, 0, 0))


    while True:

        mx, my = pygame.mouse.get_pos()

        display.fill((0, 0, 0))

        display.blit(Congrats, (80, 200))

        display.blit(Thanks, (165, 285))

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

    pygame.mixer.init()

    WIDTH, HEIGHT = 900, 600

    display = pygame.display.set_mode((WIDTH, HEIGHT))

    

    if not pygame.mixer.music.get_busy():
        song = pygame.mixer.music.load("Music/5.wav")
        pygame.mixer.music.play(loops=100, fade_ms=1500)

    logo = pygame.image.load("Data/Logo.png")

    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")


    Clock = pygame.time.Clock()

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 35)

    small_font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 15)

    play = font.render("Jugar", False, (0, 0, 0))
    Quit = font.render("Tutorial", False, (0, 0, 0))

    credits = small_font.render("Creado por: Oriol AB", False, "orange")

    button = pygame.transform.scale(pygame.image.load("Data/GUI_BUTTON.png").convert(), (300, 75))

    white_button = pygame.transform.scale(pygame.image.load("Data/GUI_BUTTON_WHITE.png").convert(), (300, 75))

    button_rect = pygame.Rect(300, 310, 300, 75)

    quit_button_rect = pygame.Rect(300, 410, 300, 75)

    button_to_render = button

    quit_button_to_render = button



    Data = [
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

        display.blit(Quit, (309, 428))

        display.blit(credits, (570, 560))

        to_render += 0.05

        if to_render > 14:
            to_render = 0

        display.blit(Data[round(to_render)], (210, 125))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if button_rect.collidepoint(mx, my):
                        return 1
                    
                    elif quit_button_rect.collidepoint(mx, my):
                        return 2
        
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

    logo = pygame.image.load("Data/Logo.png")

    pygame.display.set_icon(logo)

    pygame.display.set_caption("Jumper")

    TooShort = pygame.image.load("Data/Too-Short.png").convert()

    TryAgain = pygame.image.load("Data/TryAgain.png").convert()

    MainClock = pygame.time.Clock()

    button = pygame.image.load("Data/GUI_BUTTON.png").convert()

    white_button = pygame.image.load("Data/GUI_BUTTON_WHITE.png").convert()

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



def Tutorial():
    import pygame
    import sys


    pygame.init()

    pygame.font.init()

    font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 25)



    
    WIDTH, HEIGHT = 900, 600

    display = pygame.display.set_mode((900, 600))


    logo = pygame.image.load("Data/Logo.png").convert()

    logo.set_colorkey((0, 0, 0))

    pygame.display.set_caption("Jumper")

    pygame.display.set_icon(logo)


    Clock = pygame.time.Clock()

    button = pygame.image.load("Data/GUI_BUTTON_50x50.png").convert()

    next_button = pygame.image.load("Data/GUI_BUTTON.png").convert()

    next_button.set_colorkey((0, 0, 0))


    white_next_button = pygame.image.load("Data/GUI_BUTTON_WHITE.png").convert()

    white_next_button.set_colorkey((0, 0, 0))

    button.set_colorkey((0, 255, 0))

    white_button = pygame.image.load("Data/GUI_BUTTON_50x50_WHITE.png").convert()

    white_button.set_colorkey((0, 255, 0))

    button_rect = pygame.Rect(840, 10, 50, 50)

    next_button_rect = pygame.Rect(525, 400, 200, 75)

    prev_button_rect = pygame.Rect(260, 400, 200, 75)


    tutorial_screens = [
                pygame.image.load("Data/tut2.png").convert(), 
                pygame.image.load("Data/tutorial.png").convert(), 
                pygame.image.load("Data/tutorial3.png").convert(),
                pygame.image.load("Data/tutorial4.png").convert()
                
    ] 

    index = 0

    to_render = tutorial_screens[index]

    next_button_to_render = next_button

    prev_button_to_render = next_button

    button_to_render = button

    right_arrow = pygame.image.load("Data/Right_Arrow.png").convert()

    left_arrow = pygame.image.load("Data/Left_arrow.png").convert()

    right_arrow.set_colorkey((255, 255, 255))

    left_arrow.set_colorkey((255, 255, 255))

    txt1 = font.render("¡Ayúdala a ganar", False, (0, 0, 0))

    txt2 = font.render("los juegos olímpicos!", False, (0, 0, 0))

    space = font.render("espacio", False, (0, 0, 0))

    tutorial3_text1 = font.render("Mantén la barra", False, (0, 0, 0))

    tutorial3_text2 = font.render("por encima del mínimo...", False, (0, 0, 0))

    tutorial4_text1 = font.render("¡Pero por debajo", False, (0, 0, 0))

    tutorial4_text2 = font.render("del máximo!", False, (0, 0, 0))

    while True:

        to_render = tutorial_screens[index]

        mx, my = pygame.mouse.get_pos()

        display.fill((0, 0, 0))


        display.blit(to_render, (0, 0))

        display.blit(button_to_render, button_rect)

        display.blit(next_button_to_render, next_button_rect)

        display.blit(prev_button_to_render, prev_button_rect)

        #pygame.draw.rect(display, (255, 0, 0), (225, 415, 150, 50))


        #525, 400


        display.blit(right_arrow, (555, 412))

        display.blit(left_arrow, (290, 412))


        if index == 1:
            display.blit(space, (379, 215))

        if index == 0:
            display.blit(txt1, (270, 190))

            display.blit(txt2, (230, 240))
        
        if index == 2:
            display.blit(tutorial3_text1, (300, 200))

            display.blit(tutorial3_text2, (200, 250))

            pygame.draw.rect(display, (255, 255, 255), (348, 500, 7, 25), 3)
        
        if index == 3:
            display.blit(tutorial4_text1, (285, 220))
            display.blit(tutorial4_text2, (350, 270))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(mx, my):
                   return 1

                if next_button_rect.collidepoint(mx, my):
                    index += 1
                    if index > len(tutorial_screens) - 1:
                        index -= 1

                if prev_button_rect.collidepoint(mx, my):
                    index -= 1

                    if index < 0:
                        index = 0

        if button_rect.collidepoint(mx, my):
            button_to_render = white_button

        else:
            button_to_render = button


        if next_button_rect.collidepoint(mx, my):
            next_button_to_render = white_next_button

        else:
            next_button_to_render = next_button

        
        if prev_button_rect.collidepoint(mx, my):
            prev_button_to_render = white_next_button
        
        else:
            prev_button_to_render = next_button
        
        Clock.tick(120)

        pygame.display.flip()


        

if __name__ == "__main__":
    count = 0

    
    while True:
        if MainMenu() == 1:
    
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

        else:
            Tutorial()