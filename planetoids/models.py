"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

# KWABENA APPIAH (KOA24) VAIL CHEN (VAC68)
#DECEMBER 8TH, 2022
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180
# END REMOVE


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute _velocity: A two-dimensional Vector representing the velocity of the bullet.

    def __init__(self, ship, **keywords):
        """Initialize a Bullet object.
        This method initializes a new Bullet object with the specified 
        position and velocity.
        Args:
            ship: The Ship object that fired the bullet.
            **keywords: Additional keyword arguments to be passed to the 
            superclass constructor.
        """
        super().__init__(**keywords)
        shipfacing = ship._facing
        self._velocity = shipfacing * BULLET_SPEED

    def getVelocity(self):
        """Return the velocity of the bullet.
        This method returns the current velocity of the bullet as a
         two-dimensional Vector object.
        Returns:
            The velocity of the bullet as a Vector object.
        """
        return self._velocity

    def bulletMove(self):
        """Move the bullet in its current direction.
        This method updates the position of the bullet by adding its
         velocity to its current position.
        """
        self.x = self.x + self._velocity.x
        self.y = self.y + self._velocity.y


class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vector (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: velocity vector of the ship
    # Attribute _facing: vector of where the ship is facing in space
    # Attribute _thrusters: thrusters animation
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def __init__(self, **keywords):
        """Initialize a Ship object.

        This method initializes a new Ship object with the specified position 
        and initial velocity and facing.

        Args:
            **keywords: Additional keyword arguments to be 
            passed to the superclass constructor.
        """
        super().__init__(**keywords)
        self._velocity = Vector2()
        self._facing = Vector2(math.cos(degToRad(self.angle)), 
        math.sin(degToRad(self.angle)))
        self._thrusters = None

    def setThrusters(self):
        """Set the thrusters of the ship.

        This method sets the thrusters of the ship as a GSprite object 
        with the specified position, source, format,
        width, height, and angle.
        """
        self._thrusters = GSprite(
            x=self.x, y=self.y,
            source='flame-sprites.png', format=(4, 1), width=4 * self.width,
            height=2 * self.width, angle=self.angle
        )

    def getThrusters(self):
        """Return the thrusters of the ship.

        This method returns the thrusters of the ship as a GSprite object.

        Returns:
            The thrusters of the ship as a GSprite object.
        """
        return self._thrusters

    def getVelocity(self):
        """Return the velocity of the ship.

        This method returns the current velocity of the 
        ship as a two-dimensional Vector object.

        Returns:
            The velocity of the ship as a Vector object.
        """
        return self._velocity

    def getFacing(self):
        """Return the direction in which the ship is facing.

        This method returns the direction in which the ship 
        is currently facing as a two-dimensional Vector object.

        Returns:
            The direction in which the ship is facing as a Vector object.
        """
        return self._facing
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self,input):
        """
        This function updates the angle of the ship based on input from the 
        user. 
        If the 'a' key is down, the angle of the ship is increased by 
        SHIP_TURN_RATE.
        If the 'd' key is down, the angle of the ship is decreased by 
        SHIP_TURN_RATE. 
        The ship's facing direction is then updated to match the new angle.
        """
        if input.is_key_down('a'):
            self.angle = self.angle+SHIP_TURN_RATE
        if input.is_key_down('d'):
            self.angle = self.angle-SHIP_TURN_RATE
        self._facing.x = math.cos(degToRad(self.angle))
        self._facing.y = math.sin(degToRad(self.angle))


    def impulse(self,input):
        """
        This function updates the velocity of the ship based on user input. 
        If the 'w' key is down, the velocity of the ship is increased in the 
        direction of the ship's facing. If the magnitude of the ship's velocity
         exceeds SHIP_MAX_SPEED, the velocity is normalized and scaled to
        SHIP_MAX_SPEED.
        """
        imp = self._facing*SHIP_IMPULSE
        if input.is_key_down('w'):
            self._velocity += imp
        smag = (((self._velocity.x)**2)+((self._velocity.y)**2))**(1/2)
        if smag > SHIP_MAX_SPEED:
            self._velocity = (self._velocity.normal())*SHIP_MAX_SPEED


    def move(self,input):
        """
        This function updates the position of the ship based on its current
         velocity. The x and y coordinates of the ship are updated by 
         the corresponding x and y components of the velocity vector.
        """
        self.x = self.x + self._velocity.x
        self.y = self.y + self._velocity.y


    def BorderCollision(self):
        """
        This function checks if the ship has collided with the borders of 
        the game screen. If the ship is outside the game screen, its position 
        is adjusted to the opposite side of the screen. For example, if the ship
         is outside the left border of the screen, its x coordinate
          is increased by the width of the game screen plus twice the value 
          of DEAD_ZONE.
        """
        if self.x < -(DEAD_ZONE):
            self.x += GAME_WIDTH + 2*(DEAD_ZONE)
        elif self.x > DEAD_ZONE+GAME_WIDTH:
            self.x -= (GAME_WIDTH+(2*DEAD_ZONE))
        elif self.y < -(DEAD_ZONE):
            self.y += GAME_HEIGHT + 2*(DEAD_ZONE)
        elif self.y > DEAD_ZONE+GAME_HEIGHT:
            self.y -= (GAME_HEIGHT+(2*DEAD_ZONE))
        elif self.y < 0 and self.x < 0:
            self.y += GAME_HEIGHT
            self.x += GAME_WIDTH
        elif self.y < 0 and self.x > GAME_WIDTH:
            self.y += GAME_HEIGHT
            self.x -= GAME_WIDTH
        elif self.y > GAME_HEIGHT and self.x < 0:
            self.y -= GAME_HEIGHT
            self.x += GAME_WIDTH
        elif self.y > GAME_HEIGHT and self.x > GAME_WIDTH:
            self.y -= GAME_HEIGHT
            self.x -= GAME_WIDTH


class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: velocity vector of the asteroid
    # Attribute _size: size of asteroid
    # 
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """Returns the asteroid's current velocity as a Vector2 object.
        """
        return self._velocity
    def getSize(self):
        """Returns the asteroid's size.
        """
        return self._size
    def getDirection(self):
        """Returns the asteroid's direction as a tuple of x and y values.
        This function returns the value of the `direction` attribute, which is a tuple
        containing the x and y values representing the asteroid's direction.
        """
        return self.direction
    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self,size,direction,**keywords):
        """INitializer for Asteroid class."""
        super().__init__(**keywords)
        self.direction = direction
        self._size = size
        if self.if_Stationary():
            self._velocity = Vector2()
        else:
            vector = Vector2(self.direction[0],self.direction[1])
            self._velocity = vector.normal()*self.speed()

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def speed(self):
        """Returns the asteroid's speed.
        This function returns the asteroid's current speed based on its size.
        """
        if not self.if_Stationary():
            if self._size == LARGE_ASTEROID:
                return LARGE_SPEED
            elif self._size == MEDIUM_ASTEROID:
                return MEDIUM_SPEED
            elif self._size == SMALL_ASTEROID:
                return SMALL_SPEED
    def if_Stationary(self):
        """Returns True if the asteroid is stationary, False otherwise.
        """
        if self.direction[0] == 0 and self.direction[1] == 0:
            return True
        else:
            return False
    def move(self):
        """Moves the asteroid based on its current velocity."""
        self.x = self.x + self._velocity.x
        self.y = self.y + self._velocity.y
        
    def BorderCollision(self):
        """
        This function checks if the asteroid has collided with the borders of 
        the game screen. If the asteroid is outside the game screen, 
        its position is adjusted to the opposite side of the screen. For example, 
        if the asteroid
         is outside the left border of the screen, its x coordinate
          is increased by the width of the game screen plus twice the value 
          of DEAD_ZONE.
        """
        if self.x < -(DEAD_ZONE):
            self.x += GAME_WIDTH + 2*(DEAD_ZONE)
        elif self.x > DEAD_ZONE+GAME_WIDTH:
            self.x -= (GAME_WIDTH+(2*DEAD_ZONE))
        elif self.y < -(DEAD_ZONE):
            self.y += GAME_HEIGHT + 2*(DEAD_ZONE)
        elif self.y > DEAD_ZONE+GAME_HEIGHT:
            self.y -= (GAME_HEIGHT+(2*DEAD_ZONE))
        elif self.y < 0 and self.x < 0:
            self.y += GAME_HEIGHT
            self.x += GAME_WIDTH
        elif self.y < 0 and self.x > GAME_WIDTH:
            self.y += GAME_HEIGHT
            self.x -= GAME_WIDTH
        elif self.y > GAME_HEIGHT and self.x < 0:
            self.y -= GAME_HEIGHT
            self.x += GAME_WIDTH
        elif self.y > GAME_HEIGHT and self.x > GAME_WIDTH:
            self.y -= GAME_HEIGHT
            self.x -= GAME_WIDTH

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
