'''
By: Deon Hua
Date: 16 May 2013
Description: pyAsteroids - a remake of the original game in python! The game contains
a few functions to control the game's menus and overall gameplay. The main()
function is used to call all of this.
'''

#Import and Initialize
import pygame, pygame.mixer, asteroidsSprites, random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))



def main():
    '''This function defines the 'mainline logic' for Asteroids. It takes no
    parameters and returns no values. However, it does process returned values
    from the main_menu() function and goes through the proper functions from that.'''
    #Display
    pygame.display.set_caption("Asteroids!")
    
    option = main_menu()
    
    keepGoing = True
    
    while keepGoing:
        if option == "quit":
            keepGoing = False
        elif option == "help":
            help_menu()
            option = main_menu()
        elif option == "play":
            play()
            option = main_menu()
            
      
    # Unhide mouse pointer
    pygame.mouse.set_visible(True)        
    
    pygame.quit()
    

def main_menu():
    '''This function is the main menu for asteroids. It displays the title and
    three buttons for the user to choose from. It takes no parameters, but returns
    quit, play, or help depending on what button is pressed.'''
    #Entities
    background = pygame.Surface(screen.get_size())
    background = pygame.image.load("menu.png")
    screen.blit(background, (0,0))
    

    #Create Sprites
    cursor = asteroidsSprites.Cursor()
    play_button = asteroidsSprites.Button(500, 150, "play")
    help_button = asteroidsSprites.Button(500, 250, "help")
    quit_button = asteroidsSprites.Button(500, 350, "quit")
    
    allSprites = pygame.sprite.OrderedUpdates(quit_button, play_button, help_button, cursor)
    
    #ACTION
    
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    #Loop
    while keepGoing:
        
        #Timer
        clock.tick(30)
        
        #Event Handling
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                #Quit if escape is pressed.
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            elif event.type == pygame.MOUSEMOTION:
                cursor.update_position (pygame.mouse.get_pos())
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.rect.colliderect(play_button.rect):
                    return "play"
                if cursor.rect.colliderect(help_button.rect):
                    return "help"
                if cursor.rect.colliderect(quit_button.rect):
                    return "quit"
                
   
                
        #Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
                
        
    
def help_menu():
    '''The help menu displays the instructions (a small backstory and controls)
    for the user. It takes no parameters and returns nothing.'''
    #Entities
    background = pygame.Surface(screen.get_size())
    background = pygame.image.load("help.png")
    screen.blit(background, (0,0))

    #SPAWN BUTTONS
    
    cursor = asteroidsSprites.Cursor()
    back_button = asteroidsSprites.Button(50,20,"back")
    allSprites = pygame.sprite.Group(back_button, cursor)
    
    #ACTION
    
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    #Loop
    while keepGoing:
        
        #Timer
        clock.tick(30)
        
        #Event Handling
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                #Quit if escape is pressed.
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    
            elif event.type == pygame.MOUSEMOTION:
                cursor.update_position (pygame.mouse.get_pos())
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.rect.colliderect(back_button.rect):
                    keepGoing = False
            
                
        #Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

def play(): 
    '''This function runs the in-game animation loop and is where most of the
    action occurs. Music and images are initialized in this loop in order for
    usage during the game. The function takes no parameters and returns nothing.'''
    
    #Entities
    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    screen.blit(background, (0,0))
    
    #Load Fonts
    myCustomFont = pygame.font.Font("good times rg.ttf", 63)
    game_over = myCustomFont.render("Game Over!", 1, (255,255,255))
        
    #Load Music
    music = pygame.mixer.music.load("./Audio/vigil.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    explosion = pygame.mixer.Sound("./Audio/explosion.ogg")
    powerup_sound = pygame.mixer.Sound("./Audio/powerup.ogg")
    engine = pygame.mixer.Sound("./Audio/engine.ogg")
    laser = pygame.mixer.Sound("./Audio/laser.ogg")
    engine.set_volume(0.2)
    explosion.set_volume(0.4)
    laser.set_volume(0.4)
    powerup_sound.set_volume(0.5)
    
    #Load images to prevent load from disk everytime the sprite is initialized
    asteroid_image = pygame.image.load("asteroid.png")
    ufo_image = pygame.image.load("UFO.png")
    powerup_images = []
    for number in range (1, 4):
        image = pygame.image.load("./Powerups/%d.png" %number)
        powerup_images.append(image)
            
    #Create sprites
    scorekeeper = asteroidsSprites.ScoreKeeper()
    space = asteroidsSprites.Space()
    spaceship = asteroidsSprites.Spaceship(screen)
    
    #Create Sprite Groups
    spaceshipSprite = pygame.sprite.Group(spaceship)
    asteroidSprites = pygame.sprite.Group()        
    rocketSprites = pygame.sprite.Group()
    enemyRocketSprites = pygame.sprite.Group()
    shieldSprites = pygame.sprite.GroupSingle()    
    powerupSprites = pygame.sprite.Group()
    ufoSprites = pygame.sprite.Group()
     
    #Larger Groups
    dangerSprites = pygame.sprite.Group(enemyRocketSprites, asteroidSprites, ufoSprites)

    allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                              , enemyRocketSprites, scorekeeper)    
    
    #ACTION
    
    #Assign         
    clock = pygame.time.Clock()
    keepGoing = True
    pause = False
     
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    #Loop
    while keepGoing:
        
        #Time
        clock.tick(30)

        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                #Quit if escape is pressed.
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                #Pauses/Unpauses game if "p" is pressed
                if event.key == pygame.K_p:
                    pause = not pause
                    while pause:
                        pygame.time.delay(100)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause = not pause
                        pygame.event.clear()
                        
                if event.key == pygame.K_RIGHT:
                    spaceship.rotate_right()
                if event.key == pygame.K_LEFT:
                    spaceship.rotate_left()
                    
                #Activates the shields if "s" is pressed and the capacity is over 50
                if event.key == pygame.K_s and (scorekeeper.get_shield() > 50):
                    shield = asteroidsSprites.Shield(spaceship.rect.centerx, \
                                                     spaceship.rect.centery, \
                                                     scorekeeper.get_shield())
                    shieldSprites.add(shield)
                    allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                              , enemyRocketSprites, scorekeeper)
                #Allows player to shoot if spacebar is pressed.
                if event.key == pygame.K_SPACE:
                    rocket = asteroidsSprites.Rocket(spaceship.get_angle(), \
                                                     spaceship.rect.centerx, \
                                                     spaceship.rect.centery, \
                                                     screen, True)
                    engine.stop()
                    laser.play()
                    rocketSprites.add(rocket)
                    
                    allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                                , enemyRocketSprites, scorekeeper)  
                    
        #Allows for the user to move "forwards" by using the up arrow key.       
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            spaceship.move_forwards()
            engine.play(-1)
        else:
            engine.stop()
        
        #Ensures that there are 5 asteroids at all times.
        while len(asteroidSprites.sprites()) < 5:
            new_asteroid = asteroidsSprites.Asteroid(screen, asteroid_image)
            asteroidSprites.add(new_asteroid)
            
            dangerSprites = pygame.sprite.Group(enemyRocketSprites, asteroidSprites, ufoSprites)
            allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                              , enemyRocketSprites, scorekeeper)   
        
        #Spawns a UFO if none exist, every 10 sec. when the score is larger than 250
        if not ufoSprites and ((pygame.time.get_ticks()/1000 % 10) == 0) and \
           (scorekeeper.get_score() >= 250):
            ufo = asteroidsSprites.UFO(screen, ufo_image)
            ufoSprites.add(ufo)
            
            dangerSprites = pygame.sprite.Group(enemyRocketSprites, asteroidSprites, ufoSprites)
            allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                              , enemyRocketSprites, scorekeeper)  
        
        #UFO AI shooting
        if ufoSprites and ((pygame.time.get_ticks()/25 %20) == 0):
            if ufo.shoot(spaceship.rect.centerx, spaceship.rect.centery) == 1:
                if spaceship.rect.centery < ufo.rect.centery:
                    rocket = asteroidsSprites.Rocket(90, ufo.rect.centerx, ufo.rect.centery, \
                                                     screen, False)
                else:
                    rocket = asteroidsSprites.Rocket(270, ufo.rect.centerx, ufo.rect.centery, \
                                                     screen, False)
                engine.stop()
                laser.play()
                
                enemyRocketSprites.add(rocket)
                
                dangerSprites = pygame.sprite.Group(enemyRocketSprites, asteroidSprites,\
                                                    ufoSprites)    
                allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                              , enemyRocketSprites, scorekeeper)  
                
            elif ufo.shoot(spaceship.rect.centerx, spaceship.rect.centery) == 2:
                if spaceship.rect.centerx < ufo.rect.centerx:
                    rocket = asteroidsSprites.Rocket(180, ufo.rect.centerx, ufo.rect.centery, \
                                                     screen, False)
                else:
                    rocket = asteroidsSprites.Rocket(0, ufo.rect.centerx, ufo.rect.centery, \
                                                     screen, False)
                enemyRocketSprites.add(rocket)
                
                dangerSprites = pygame.sprite.Group(enemyRocketSprites, asteroidSprites,\
                                                    ufoSprites)
                engine.stop()
                laser.play()
                allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                              , enemyRocketSprites, scorekeeper)  
                  
                
        #Charging / Draining the shield.    
        if shieldSprites:    
            shield.update_location(spaceship.rect.centerx, spaceship.rect.centery)
            shield.update_capacity(scorekeeper.get_shield())
            #If shield is drained, empty the shieldSprites group.
            if not scorekeeper.get_shield():
                shieldSprites.empty()
            scorekeeper.enable_shield()
        else:
            scorekeeper.recharge_shield()
            
                        
                    
        #--------------------Collision Detection--------------------------------
        #Between the shield and anything dangerous to the player.
        if pygame.sprite.groupcollide(shieldSprites, dangerSprites, True, True):
            engine.stop()
            explosion.play()
        
        #Between the asteroids and the rockets
        for asteroid in pygame.sprite.groupcollide(asteroidSprites, rocketSprites, False, True):
            scorekeeper.add_score(10*asteroid.get_size())
            asteroid.collided()
            engine.stop()
            explosion.play()
        
        #Rocket collision with the UFO, may spawn a powerup
        if pygame.sprite.groupcollide(rocketSprites, ufoSprites, False, False):
            engine.stop()
            explosion.play()
            scorekeeper.add_score(50)
            random_number = random.randint(1,5)
            if (random_number <= 3):
                powerup = asteroidsSprites.Powerup(random_number, ufo.rect.centerx, \
                                                   ufo.rect.centery, powerup_images)
                powerupSprites.add(powerup)
                allSprites = pygame.sprite.OrderedUpdates(space, powerupSprites, \
                                                          asteroidSprites, shieldSprites\
                                                          ,spaceship, ufoSprites, rocketSprites\
                                              , enemyRocketSprites, scorekeeper)
            pygame.sprite.groupcollide(rocketSprites, ufoSprites, True, True)
                

        if pygame.sprite.spritecollide(spaceship, dangerSprites, True):            
            scorekeeper.lose_life()
            engine.stop()
            explosion.play()
            
            #Resets the spaceship in its "start position" if there are lives left.
            if scorekeeper.get_lives():
                spaceship.reset()
                
                for sprite in dangerSprites:
                    sprite.reset()
                rocketSprites.empty()
                enemyRocketSprites.empty()
            else:
                spaceship.kill()
                
        #Give powerup buff to player
        for powerup in pygame.sprite.spritecollide(spaceship,powerupSprites,False):
            if powerup.get_type() == 1:
                scorekeeper.add_capacity()
            elif powerup.get_type() == 2:
                scorekeeper.add_life()
            else:
                scorekeeper.add_score(100)
            engine.stop()
            explosion.stop()
            powerup_sound.play()
        #Destroys the sprite once collided with and activated.    
        pygame.sprite.spritecollide(spaceship, powerupSprites, True)
         
        
        #Game over when lives = 0.
        if not scorekeeper.get_lives():
            keepGoing = False
            
        #Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    
    #Display "Game Over!" message
    screen.blit(game_over, (80,100))
    pygame.display.flip()
    
    #Fade music
    pygame.mixer.music.fadeout(2000)    
    pygame.time.delay(2000)
   
# Call the main function
main()
