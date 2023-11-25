"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

# KWABENA APPIAH (KOA24) VAIL CHEN (VAC68)
#DECEMBER 8TH, 2022
"""
from game2d import *
from consts import *
from models import *
import random
import datetime


# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    #
    #Attribute _cool: cooldown for animations
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setLives(self,int):
        """lives setter"""
        assert int >= 0
        self._lives = int
    
    def getLives(self):
        """lives getter"""
        return self._lives
    def setShip(self,json):
        pos = json["ship"]["position"]
        angle =json["ship"]["angle"]
        self._ship = Ship(x=pos[0],y=pos[1],
        width=SHIP_RADIUS*2,height=SHIP_RADIUS*2,
        source=SHIP_IMAGE,angle=angle)
    
    def getShip(self):
        """ship getter"""
        return self._ship
    
    def setFirerate(self):
        """firerate setter"""
        self._firerate = 0
    
    def getFirerate(self):
        """firerate getter"""
        return self._firerate

    def setAsteroids(self,json):
        """asteroid setter"""
        self._asteroids = []
        for a in json["asteroids"]:
            if a["size"] == "large":
                self._asteroids.append(Asteroid(x=a["position"][0],
                y=a["position"][1],
                width=LARGE_RADIUS*2,height=LARGE_RADIUS*2,
                source=LARGE_IMAGE,size=LARGE_ASTEROID,
                direction=a["direction"]))
            if a["size"] == "medium":
                self._asteroids.append(Asteroid(x=a["position"][0],
                y=a["position"][1],
                width=MEDIUM_RADIUS*2,height=MEDIUM_RADIUS*2,
                source=MEDIUM_IMAGE,size=MEDIUM_ASTEROID,
                direction=a["direction"]))
            if a["size"] == "small":
                self._asteroids.append(Asteroid(x=a["position"][0],
                y=a["position"][1],
                width=SMALL_RADIUS*2,height=SMALL_RADIUS*2,
                source=SMALL_IMAGE,size=SMALL_ASTEROID,
                direction=a["direction"]))

    def getAsteroids(self):
        """
        Asteroid getter. Returns a list of asteroids
        """
        return self._asteroids
    
    def setBullets(self):
         self._bullets.append(Bullet(fillcolor=BULLET_COLOR
        ,x=self.bulletPosition()[0],y=self.bulletPosition()[1],
        width=BULLET_RADIUS*2,height=BULLET_RADIUS*2,ship=self._ship))

    def getBullets(self):
        """
        bullet getter. Returns a lsit of bullets
        """
        return self._bullets

    
    def setData(self,json):
        """
        Data Setter. Takes a json as an arg and sets the contents of that
        json to _data attribute
        """
        self._data = json
    
    def getData(self):
        """
        data getter
        """
        return self._data

    def setCool(self):
        """
        cooldown setter
        """
        self._cool = THRUSTER_COOLDOWN

    def getCool(self):
        """
        cooldown getter
        """
        return self._cool
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self,json,int):
        """
        Wave object intializer
        """
        self.setData(json)
        self.setShip(json)
        self.setAsteroids(json)
        self._bullets = []
        self.setFirerate()
        self.setLives(int)
        self.setCool()
        self._pewSound = Sound('pew1.wav')
        self._explosionSound = Sound('explosion.wav')
        self._thrusterSound = Sound('afterburner.wav')
    
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self,dt,input):
        """update method for Wave object"""
        if not self._ship is None:
            self.shipPhysics(input)
        self.asteroidPhysics()
        self.bulletPhysics()
        self.bulletAsteroidCollision()
        self.shipAsteroidCollision()
        self.determineLives()
        self.thrusterSpriteAnimation()
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self,view):
        """
        Draw method for Wave class.
        """
        if not self._ship is None:
            self._ship.draw(view)
            if not self._ship._thrusters is None:
                self._ship._thrusters.draw(view)
        for asteroids in self._asteroids:
            asteroids.draw(view)
        for bullets in self._bullets:
            bullets.draw(view)
    
    # RESET METHOD FOR CREATING A NEW LIFE
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def determineLives(self):
        """lives determiner. based on ship state, reduces lives by one."""
        if self._ship is None:
            self._lives = self._lives - 1


    def shipPhysics(self,input):
        """method for ship physics"""
        self._ship.turn(input)
        self._ship.impulse(input)
        self._ship.move(input)
        self.fireBullet(input)
        self._ship.BorderCollision()
        if input.is_key_down("w"):
            print('is thrust')
            self._ship.setThrusters()
        else:
            print('is none')
            self._ship._thrusters = None



    def bulletPhysics(self):
        """method for bullet physics"""
        for bullets in self._bullets:
            bullets.bulletMove()
        self.bulletBorderCollision()

    def asteroidPhysics(self):
        """metho for asteroid physics"""
        for i in self._asteroids:
            i.move()
            i.BorderCollision()


    def fireBullet(self,input):
        if input.is_key_down("spacebar") and self._firerate >= BULLET_RATE:
            self.setBullets()
            self._firerate = 0
            self._pewSound.play()
        else:
            self._firerate += 1
    
    def bulletBorderCollision(self):
        i = 0
        while i < len(self._bullets):
            if self._bullets[i].x > GAME_WIDTH or \
            self._bullets[i].y > GAME_HEIGHT:
                del self._bullets[i]
            elif self._bullets[i].x < 0 or \
            self._bullets[i].y < 0:
                del self._bullets[i]
            else:
                i += 1
    
    def bulletAsteroidCollision(self):
        """Bullet asteroid collision function. 
        handles bullet asteroid collision physics."""
        for bullet in self._bullets:
            for asteroid in self._asteroids:
                if asteroid._size == LARGE_ASTEROID:
                    ogdist = LARGE_RADIUS+BULLET_RADIUS
                    self.BulletAsteroidCollisionLoop(asteroid,bullet,ogdist)
                if asteroid._size == MEDIUM_ASTEROID:
                    ogdist = MEDIUM_RADIUS+BULLET_RADIUS
                    self.BulletAsteroidCollisionLoop(asteroid,bullet,ogdist)
                if asteroid._size == SMALL_ASTEROID:
                    ogdist = SMALL_RADIUS+BULLET_RADIUS
                    self.BulletAsteroidCollisionLoop(asteroid,bullet,ogdist)


    def shipAsteroidCollision(self):
        """Asteroid ship collision. Handles collisions 
        between the ship and asteroids."""
        for asteroid in self._asteroids:
            if not self._ship is None:
                dist = (((self._ship.x - asteroid.x)**2)+\
                    ((self._ship.y - asteroid.y)**2))**(1/2)
                if dist < (self._ship.width//2 + asteroid.width//2):
                    if asteroid._size is LARGE_ASTEROID:
                        self.AsteroidBreakup(object=self._ship, 
                        asteroid=asteroid, size=MEDIUM_ASTEROID
                        ,source=MEDIUM_IMAGE,
                        radius=MEDIUM_RADIUS)
                    if asteroid._size is MEDIUM_ASTEROID:
                        self.AsteroidBreakup(object=self._ship, 
                        asteroid=asteroid, size=SMALL_ASTEROID,
                        source=SMALL_IMAGE,
                        radius=SMALL_RADIUS)
                    self._ship = None
                    del self._asteroids[self._asteroids.index(asteroid)]
                    self._explosionSound.play()

                
    def BulletAsteroidCollisionLoop(self,asteroid,bullet,ogdist):
        """Asteroid bullet collision loop function to be
            used bulletAsteroidCollision handler."""
        i = 0
        while i < len(self._bullets):
            dist = (((self._bullets[i].x - asteroid.x)**2)+\
                ((self._bullets[i].y - asteroid.y)**2))**(1/2)
            if dist < ogdist:
                if asteroid._size is LARGE_ASTEROID:
                        self.AsteroidBreakup(object=self._bullets[i], 
                        asteroid=asteroid, size=MEDIUM_ASTEROID
                        ,source=MEDIUM_IMAGE,
                        radius=MEDIUM_RADIUS)
                if asteroid._size is MEDIUM_ASTEROID:
                        self.AsteroidBreakup(object=self._bullets[i], 
                        asteroid=asteroid, size=SMALL_ASTEROID,
                        source=SMALL_IMAGE,
                        radius=SMALL_RADIUS)
                del self._bullets[i]
                del self._asteroids[self._asteroids.index(asteroid)]
            else:
                i += 1

    def AsteroidBreakup(self,object,asteroid,size,source,radius):
        """Asteroid breakup method to be used inside collision loops"""
        vectors = self.resultantVectors(object)
        self._asteroids.append(Asteroid(x=asteroid.x,
        y=asteroid.y,
        width=radius*2,height=radius*2,
        source=source,size=size,
        direction=[vectors[0].x,vectors[0].y]))
        self._asteroids.append(Asteroid(x=asteroid.x,
        y=asteroid.y,
        width=radius*2,height=radius*2,
        source=source,size=size,
        direction=[vectors[1].x,vectors[1].y]))
        if object._velocity.x == 0 and object._velocity.y == 0:
            self._asteroids.append(Asteroid(x=asteroid.x,
            y=asteroid.y,
            width=radius*2,height=radius*2,
            source=source,size=size,
            direction=[object._facing.normal().x,object._facing.normal().y]))
        else:
            self._asteroids.append(Asteroid(x=asteroid.x,
            y=asteroid.y,
            width=radius*2,height=radius*2,
            source=source,size=size,
            direction=[object._velocity.normal().x,object._velocity.normal().y]))
    


    def bulletPosition(self):
        """determines bullet position"""
        bulletposx = (self._ship._facing.x*SHIP_RADIUS)+(self._ship.x)
        bulletposy = (self._ship._facing.y*SHIP_RADIUS)+(self._ship.y)
        return (bulletposx,bulletposy)

    def thrusterSpriteAnimation(self):
        """handles sprite cooldown animation for thrusters"""
        if not self._ship is None:
            if not self._ship.getThrusters() is None:
                if self._cool == 0:
                    self._ship._thrusters.frame = (self._ship._thrusters.frame + 1) \
                        % self._ship._thrusters.count
                    self._cool = THRUSTER_COOLDOWN
            if self._cool != 0:
                self._cool -= 1

    
    def resultantVectors(self,object):
        """Computes resultant vectors"""
        if object._velocity.x == 0 and object._velocity.y == 0:
            vector1 = Vector2((((object._facing.x)*math.cos(degToRad(120)))-
            ((object._facing.y)*math.sin(degToRad(120)))), (((object._facing.x)
            *math.sin(degToRad(120)))-
            ((object._facing.y)*math.cos(degToRad(120)))))

            vector1norm = vector1.normal()

            vector2 = Vector2((((object._facing.x)*math.cos(degToRad(-120)))-
            ((object._facing.y)*math.sin(degToRad(-120)))), (((object._facing.x)
            *math.sin(degToRad(-120)))-
            ((object._facing.y)*math.cos(degToRad(-120)))))

            vector2norm = vector2.normal()

            return (vector1norm,vector2norm)

        else:
            vector1 = Vector2((((object._velocity.x)*math.cos(degToRad(120)))-
            ((object._velocity.y)*math.sin(degToRad(120)))),(((object._velocity.x)
            *math.sin(degToRad(120)))-
            ((object._velocity.y)*math.cos(degToRad(120)))))

            vector1norm = vector1.normal()

            vector2 = Vector2((((object._velocity.x)*math.cos(degToRad(-120)))-
            ((object._velocity.y)*math.sin(degToRad(-120)))), (((object._velocity.x)
            *math.sin(degToRad(-120)))-
            ((object._velocity.y)*math.cos(degToRad(-120)))))

            vector2norm = vector2.normal()

            return (vector1norm,vector2norm)

