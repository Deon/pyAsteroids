'''
By: Deon Hua
Date: 16 May 2013
Description: This module contains the Spaceship, Asteroid, ScoreKeeper, Rocket, 
UFO, Powerup, and Shield sprites for Asteroids.
'''
import pygame, random

class Spaceship(pygame.sprite.Sprite):
    '''Creates the spaceship that will be controlled by the user.
    
    Instance Variables:
    self.__screen - screen, used when the player goes off the screen
    self.__speed - speed of the spaceship, varies based on acceleration
    self.__angle - angle of the spaceship (direction it's facing)
    '''
    def __init__(self, screen):
        '''Initializer method for the Spaceship sprite.'''
        pygame.sprite.Sprite.__init__(self)        
        
        #Image attribute
        self.image = pygame.image.load("spaceships.png")
        
        #Set other attributes
        self.__screen = screen
        self.__speed = 0
        self.__angle = 90
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.centerx = 320
        self.rect.centery = 240     
        
        
    def rotate_left(self):
        '''Rotates the spaceship counter-clockwise.'''        
        self.image = pygame.transform.rotate(self.image, 90)
        self.__angle += 90
        
    def rotate_right(self):
        '''Rotates the spaceship clockwise.'''
        self.image = pygame.transform.rotate(self.image, -90)
        self.__angle -= 90

    def move_forwards(self):
        '''Moves the spaceship in the direction it is facing. The max speed is 5
        but it accelerates by 1 per update cycle.'''
        if self.__speed < 5:
            self.__speed += 1        
    
    def get_angle(self):
        '''Returns the direction the spaceship is facing.'''        
        return self.__angle
           
    def reset(self):
        '''Resets the spaceship.'''
        #Ensures that the spaceship is always facing upwards when it resets.
        while self.__angle != 90:
            if self.__angle == -90:
                self.__angle = 270 
            self.rotate_right()            
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.centerx = 320
        self.rect.centery = 240

        self.__speed = 0
        
    def update(self):
        '''Updates location of the spaceship if it leaves the screen.'''
        #Ensures that angles stay between 0 & 360
        if self.__angle == -90:
            self.__angle = 270
        elif self.__angle == 450:
            self.__angle = 90
        
        #Flies in a certain direction given the shooter's angle.
        if self.__angle == 90:
            self.rect.centery -= self.__speed
        elif self.__angle == 180:
            self.rect.centerx -= self.__speed
        elif self.__angle == 270:
            self.rect.centery += self.__speed
        elif (self.__angle == 0) or (self.__angle == 360):
            self.rect.centerx += self.__speed
        
        #If the spaceship goes off one side of the screen, it comes back in the other.
        if (self.rect.centerx < 0):
            self.rect.centerx = self.__screen.get_width()
        if (self.rect.centerx > self.__screen.get_width()):
            self.rect.centerx = 0
        if (self.rect.centery < 0):
            self.rect.centery = self.__screen.get_height()
        if self.rect.centery > self.__screen.get_height():
            self.rect.centery = 0
            
        self.__location = self.rect.centerx, self.rect.centery
        
        #Physics - decelerates the ship's speed by 0.25 every update cycle.
        if self.__speed > 0:
            self.__speed -= 0.25
          
    
class Asteroid(pygame.sprite.Sprite):
    '''Creates the asteroids that the player will have to destroy before it hits
    them or the Earth.
    
    Instance Variables:
    self.__screen - screen, used for going off the screen.
    self.__moving - bool, used to check if the asteroid is moving or not.
    self.__size - size, a larger number is a smaller asteroid.'''
    def __init__(self, screen, image):
        '''Initializer method for the Asteroid sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        #Set other attributes
        self.__screen = screen
        self.__moving = False
        self.__size = 1
        
        #Image Attributes
        self.image = image        
        self.reset()
        
    def collided(self):
        '''Makes the asteroid smaller if it was hit with a rocket.'''
        if self.__size == 3:
            self.kill()
                 
        self.__size += 1
        #Set image attribute
        self.image = pygame.transform.scale(self.image, (69-10*self.__size, 65 - 10* self.__size))
        
        #Set rect attribute
        self.rect = self.image.get_rect()
        
        #Ensures the smaller asteroid is spawned at the point of the larger one
        self.rect.centerx = self.__old_centerx
        self.rect.centery = self.__old_centery
        
        self.check_movement()
        
    def reset(self):
        '''Resets the asteroid off the screen at a random x coordinate.'''
        #Set the rect attribute
        self.rect = self.image.get_rect()        
        self.rect.left = random.randint(0,640)
        self.rect.top = 500
        
        self.check_movement()
        
    def get_size(self):
        '''Gets/Returns the size of the asteroid.'''
        return self.__size
    
    def check_movement(self):
        '''Ensures that the asteroid has movement both vertically and horizontally.'''
        self.__moving = False
        
        while not self.__moving:
            self.__dx = random.randint(-self.__size*2, self.__size*2)
            self.__dy = random.randint(-self.__size*2, self.__size*2)
            if self.__dx and self.__dy:
                self.__moving = True
        
        
    def update(self):
        '''Updates the position of the asteroid on the screen.'''
        self.rect.centerx += self.__dx
        self.rect.centery += self.__dy
        
        #If Asteroid is outside of the screen, enter in the opposite side.
        if (self.rect.centerx < 0):
            self.rect.centerx = self.__screen.get_width()
        if (self.rect.centerx > self.__screen.get_width()):
            self.rect.centerx = 0
        if (self.rect.centery < 0):
            self.rect.centery = self.__screen.get_height()
        if self.rect.centery > self.__screen.get_height():
            self.rect.centery = 0
            
        self.__old_centerx = self.rect.centerx
        self.__old_centery = self.rect.centery
        
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''Keeps track of the score, lives, and shields.
    
    Instance Variables:
    
    self.__life - lives of the player left
    self.__score - player's score
    self.__shields - current shield level
    self.__max_capacity - max shield level
    '''
    def __init__(self):
        '''Initializer method for the ScoreKeeper sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        #Image Attributes
        self.image = pygame.Surface((34,10))
        self.image = self.image.convert()
        self.image.fill((255,255,0))
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0,640)
        self.rect.top = random.randint(0,480)
        
        # Load font
        self.__font = pygame.font.Font("good times rg.ttf", 25)
        
        #Initialize other attributes
        self.__life = 3
        self.__score = 0
        self.__shields = 100
        self.__max_capacity = 100
        
    def add_life(self):
        '''If the player hits a +life powerup, this method adds a life to the 
        player's total life count.'''        
        self.__life += 1
        
    def lose_life(self):
        '''If the player crashes into an asteroid or UFO, or is hit by a rocket,
        a life is lost.'''        
        self.__life -= 1
        
    def add_score(self, value):
        '''Adds a value to the player's total score, depending on the value
        that is passed to it.'''        
        self.__score += value
        
    def enable_shield(self):
        '''Drains the capacity of the shield when the shield is in use.'''                
        self.__shields -= 1
    
    def recharge_shield(self):
        '''Recharges the shield by a small amount when the shield is not in use.'''        
        if self.__shields < self.__max_capacity:
            self.__shields += 0.25
            
    def add_capacity(self):
        '''Adds 10 to the maximum capacity of the shields when the appropriate
        powerup is activated.'''
        self.__max_capacity += 10
        
    def get_shield(self):
        '''Gets/Returns the strength of the shield.'''        
        return self.__shields
    
    def get_lives(self):
        '''Gets/Returns the lives of the player's spaceship.'''
        return self.__life
    
    def get_score(self):
        '''Gets/Returns the score of the player.'''
        return self.__score
    
    def update(self):
        '''Updates all the status indicators on screen.'''
        
        message = "Score: %d   Lives: %d   Shields: %d" %\
                (self.__score, self.__life, self.__shields)
        self.image = self.__font.render(message, 1, (255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.center = (310, 15)
     
                
    
class Rocket(pygame.sprite.Sprite):
    '''Creates a rocket flying from a location (UFO/Spaceship), heading in a 
    certain direction.
    
    Instance variables:        
    self.__angle - direction of travel
    self.__distance - distance the rocket has travelled
    self.__speed - speed of the rocket
    self.__screen - screen, used for going off the screen.'''
    def __init__(self, direction, centerx, centery, screen, friendly):
        '''Initializer method for the Rocket sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.__angle = direction
        self.__distance = 0
        self.__speed = 8
        self.__screen = screen
        
        #Image Attributes

        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        #The Rocket(Beam) will be green if friendly, red if enemy.
        if friendly:
            pygame.draw.circle(self.image, (0, 255, 0), (5, 5), 5, 0)
        else:
            pygame.draw.circle(self.image, (255, 0, 0), (5, 5), 5, 0)
            
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        
    def reset(self):
        '''If told to reset, this sprite will kill itself, so that there are no
        rockets remaining on screen when the player resets.'''
        self.kill()
    
    
    def update(self):
        '''Updates the position of the rocket on the screen.'''
        #Kills itself after travelling a certain distance.
        if self.__distance > 50:
            self.kill()
        self.__distance += 1
        
        #If the rocket goes off one side of the screen, it comes back in the other.
        if (self.rect.centerx < 0):
            self.rect.centerx = self.__screen.get_width()
        if (self.rect.centerx > self.__screen.get_width()):
            self.rect.centerx = 0
        if (self.rect.centery < 0):
            self.rect.centery = self.__screen.get_height()
        if self.rect.centery > self.__screen.get_height():
            self.rect.centery = 0          
            
        #Ensures all angles are between 0 and 360.
        if self.__angle == -90:
            self.__angle = 270
        elif self.__angle == 450:
            self.__angle = 90
            
        
        #Direction of travel depends on the angle.    
        if self.__angle == 90:
            self.rect.centery -= self.__speed
        elif self.__angle == 180:
            self.rect.centerx -= self.__speed
        elif self.__angle == 270:
            self.rect.centery += self.__speed
        elif (self.__angle == 0) or (self.__angle == 360):
            self.rect.centerx += self.__speed
        


            
        
class Powerup(pygame.sprite.Sprite):
    '''Creates a powerup of a random type.  Powerups that will randomly appear 
    on the playing field, giving the player a boost. This class does not
    activate the powerup. It creates a sprite which the player can touch to 
    activate.
    
    Instance Variable:
    self.__type = the type of powerup
    '''
    
    def __init__(self, num, centerx, centery, images):
        '''Initializer method for the Powerup sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        #Image Attributes        
        if num == 1:
            self.image = images[0]            
        elif num == 2:
            self.image = images[1]
        else:
            self.image = images[2]
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        
        self.__type = num        
      
    def get_type(self):
        '''Returns the type of powerup.'''        
        return self.__type
    

class UFO(pygame.sprite.Sprite):
    '''Creates the UFOs which will attempt to attack the user.
    
    Instance Variables:
    self.__screen - screen, used when the UFO goes off screen
    self.__moving - bool variable to track if the UFO is moving
    self.__player_centerx - rect.centerx of the player
    self.__player_centery - rect.centery of the player
    self.__dx - change in x direction per update cycle
    self.__dy - change in y direction per update cycle
    ''' 
    
    def __init__(self, screen, image):
        '''Initializer method for the UFO sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        #Image Attributes
        self.image = image
        
        self.__screen = screen
        self.__moving = False
        self.reset()                 
        
    def shoot(self, centerx, centery):
        '''Checks to see if the player is within a certain x or y coordinate of 
        the UFO. If it is, then it returns either 1 (for within range vertically)
        or 2 (for within range horizontally). '''
        #Updates the player's location for comparison.
        self.__player_centerx = centerx
        self.__player_centery = centery
        
        if abs(self.rect.centerx - self.__player_centerx) < 75:
            return 1
        if abs(self.rect.centery - self.__player_centery) < 75:
            return 2
      
    def reset(self):
        '''Resets the UFO off the screen at a random x coordinate.'''
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,640)
        self.rect.centery = 20
        
        self.check_movement()
        
    def check_movement(self):
        '''Ensures that the UFO has movement. If it doesn't, then it will continue
        to generate values until it does.'''
        self.__moving = False
        while not self.__moving:
            self.__dx = random.randint(-5,5)
            self.__dy = random.randint(-5,5)
            if self.__dx and self.__dy:
                self.__moving = True
    
    def update(self):
        '''Updates the position of the UFO.'''
        self.rect.centerx += self.__dx
        self.rect.centery += self.__dy
        
        if (self.rect.centerx < 0):
            self.rect.centerx = self.__screen.get_width()
        if (self.rect.centerx > self.__screen.get_width()):
            self.rect.centerx = 0
        if (self.rect.centery < 0):
            self.rect.centery = self.__screen.get_height()
        if self.rect.centery > self.__screen.get_height():
            self.rect.centery = 0
            
        
            
class Shield(pygame.sprite.Sprite):
    '''The Shield sprite, which forms a protective "bubble" around the player.
    
    Instance Variable:
    self.__capacity - remaining capacity of the shields'''
    
    def __init__(self, centerx, centery, capacity):
        '''Initializer method for the Shield sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        #Image Attributes
        self.image = pygame.Surface((60, 60))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (0, 191, 225), (30, 30), 30, 2)
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.update_location(centerx, centery)
        self.update_capacity(capacity)
        
    def update_location(self, centerx, centery):
        '''Updates the location of the shields using the spaceship's rects.'''
        self.rect.centerx = centerx
        self.rect.centery = centery
        
    def update_capacity(self, capacity):
        '''Updates the remaining capacity of the shields.'''
        self.__capacity = capacity       
        
    def update(self):
        '''Kills itself if the capacity of the shields is less than or equal to 0.'''
        if self.__capacity <= 0:
            self.kill()
            
class Space(pygame.sprite.Sprite):    
    '''The background sprite, an image of space.'''
    def __init__(self):
        '''Initializes the Space sprite.'''
        pygame.sprite.Sprite.__init__(self)
        #Set image attributes
        self.image = pygame.image.load("background.png")
        self.image = self.image.convert()
        
        #Set rect attribute
        self.rect = self.image.get_rect()
    
class Cursor(pygame.sprite.Sprite):
    '''The cursor sprite, used by the player in the menus.'''
    def __init__(self):
        '''Initializes the Cursor sprite.'''
        pygame.sprite.Sprite.__init__(self)
        #Set image attribute
        self.image = pygame.image.load("cursor.png")
        
        #Set rect attributes
        self.rect = self.image.get_rect()
        self.rect.centerx = 360
        self.rect.centery = 240
        
    def update_position(self, location):
        '''Updates the position of the player's mouse/cursor.'''
        pygame.sprite.Sprite.__init__(self)
        self.rect.centerx, self.rect.centery = location
       
class Button(pygame.sprite.Sprite):
    '''The Button sprite, which can be pressed by the player.'''
    def __init__(self, centerx, centery, variant):
        '''Initializes the Button sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        #Set image attributes
        if variant == "quit":
            self.image = pygame.image.load("./Buttons/quit.png")
        elif variant == "play":
            self.image = pygame.image.load("./Buttons/play.png")
        elif variant == "help":
            self.image = pygame.image.load("./Buttons/help.png")
        elif variant == "back":
            self.image = pygame.image.load("./Buttons/back.png")
        
        #Set rect attributes
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        
        