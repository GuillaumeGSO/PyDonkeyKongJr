# pygame_functions

# Documentation at www.github.com/stevepaget/pygame_functions
# Report bugs at https://github.com/StevePaget/Pygame_Functions/issues


import pygame, sys, os

from pathlib import Path
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\','/')
os.chdir(DIR)

def loadImage(fileName, useColorKey=False):
        if os.path.isfile(fileName):
            image = pygame.image.load(fileName)
            image = image.convert_alpha()
            # Return the image
            return image
        else:
            raise Exception(f"Error loading image: {fileName} – Check filename and path?")

def makeSound(filename):
    pygame.mixer.init()
    return pygame.mixer.Sound(filename)

def makeSprite(filename, frames=1, altDims = None):
    return newSprite(filename, frames, altDims)

def parseColour(colour):
        if type(colour) == str:
            # check to see if valid colour
            return pygame.Color(colour)
        else:
            colourRGB = pygame.Color("white")
            colourRGB.r = colour[0]
            colourRGB.g = colour[1]
            colourRGB.b = colour[2]
            return colourRGB

class PyGame:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()
    spriteGroup = pygame.sprite.OrderedUpdates()
    textboxGroup = pygame.sprite.OrderedUpdates()
    gameClock = pygame.time.Clock()
    musicPaused = False
    hiddenSprites = pygame.sprite.OrderedUpdates()
    screenRefresh = True
    background = None
    gameName = "Graphical Window"
    keydict = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
            "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "return": pygame.K_RETURN,
            "a": pygame.K_a,
            "b": pygame.K_b,
            "c": pygame.K_c,
            "d": pygame.K_d,
            "e": pygame.K_e,
            "f": pygame.K_f,
            "g": pygame.K_g,
            "h": pygame.K_h,
            "i": pygame.K_i,
            "j": pygame.K_j,
            "k": pygame.K_k,
            "l": pygame.K_l,
            "m": pygame.K_m,
            "n": pygame.K_n,
            "o": pygame.K_o,
            "p": pygame.K_p,
            "q": pygame.K_q,
            "r": pygame.K_r,
            "s": pygame.K_s,
            "t": pygame.K_t,
            "u": pygame.K_u,
            "v": pygame.K_v,
            "w": pygame.K_w,
            "x": pygame.K_x,
            "y": pygame.K_y,
            "z": pygame.K_z,
            "1": pygame.K_1,
            "2": pygame.K_2,
            "3": pygame.K_3,
            "4": pygame.K_4,
            "5": pygame.K_5,
            "6": pygame.K_6,
            "7": pygame.K_7,
            "8": pygame.K_8,
            "9": pygame.K_9,
            "0": pygame.K_0,
            "num0": pygame.K_KP0,
            "num1": pygame.K_KP1,
            "num2": pygame.K_KP2,
            "num3": pygame.K_KP3,
            "num4": pygame.K_KP4,
            "num5": pygame.K_KP5,
            "num6": pygame.K_KP6,
            "num7": pygame.K_KP7,
            "num8": pygame.K_KP8,
            "num9": pygame.K_KP9}
    screen = ""
    
    def hideSprite(self, sprite):
        self.hiddenSprites.add(sprite)
        self.spriteGroup.remove(sprite)
        if self.screenRefresh:
            self.updateDisplay()


    def hideAll(self):
        self.hiddenSprites.add(self.spriteGroup.sprites())
        self.spriteGroup.empty()
        if self.screenRefresh:
            self.updateDisplay()


    def unhideAll(self):
        self.spriteGroup.add(self.hiddenSprites.sprites())
        self.hiddenSprites.empty()
        if self.screenRefresh:
            self.updateDisplay()


    def showSprite(self, sprite):
        self.spriteGroup.add(sprite)
        if self.screenRefresh:
            self.updateDisplay()


    def moveSprite(self, sprite, x, y, centre=False):
        sprite.move(x, y, centre)
        if self.screenRefresh:
            self.updateDisplay()


    def transformSprite(self,sprite, angle, scale, hflip=False, vflip=False):
        oldmiddle = sprite.rect.center
        if hflip or vflip:
            tempImage = pygame.transform.flip(sprite.images[sprite.currentImage], hflip, vflip)
        else:
            tempImage = sprite.images[sprite.currentImage]
        if angle != 0 or scale != 1:
            sprite.angle = angle
            sprite.scale = scale
            tempImage = pygame.transform.rotozoom(tempImage, -angle, scale)
        sprite.image = tempImage
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = oldmiddle
        sprite.mask = pygame.mask.from_surface(sprite.image)
        if self.screenRefresh:
            self.updateDisplay()


    def killSprite(self,sprite):
        sprite.kill()
        if self.screenRefresh:
            self.updateDisplay()

    
    def textBoxInput(self, textbox, functionToCall=None, args=[]):
        # starts grabbing key inputs, putting into textbox until enter pressed
        textbox.text = ""
        returnVal = None
        while True:
            self.updateDisplay()
            if functionToCall:
                returnVal = functionToCall(*args)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        textbox.clear()
                        if returnVal:
                            return textbox.text, returnVal
                        else:
                            return textbox.text
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        textbox.update(event)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def pause(self, milliseconds, allowEsc=True):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        waittime = current_time + milliseconds
        self.updateDisplay()
        while not (current_time > waittime or (keys[pygame.K_ESCAPE] and allowEsc)):
            pygame.event.clear()
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_ESCAPE] and allowEsc):
                pygame.quit()
                sys.exit()
            current_time = pygame.time.get_ticks()

    def clock():
        return pygame.time.get_ticks()

    def tick(self,fps):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == self.keydict["esc"]) or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.gameClock.tick(fps)
        return self.gameClock.get_fps()


    def showLabel(self, labelName):
        self.textboxGroup.add(labelName)
        if self.screenRefresh:
            self.updateDisplay()


    def hideLabel(self,labelName):
        self.textboxGroup.remove(labelName)
        if self.screenRefresh:
            self.updateDisplay()


    def showTextBox(self,textBoxName):
        self.textboxGroup.add(textBoxName)
        if self.screenRefresh:
            self.updateDisplay()


    def hideTextBox(self, textBoxName):
        self.textboxGroup.remove(textBoxName)
        if self.screenRefresh:
            self.updateDisplay()


    def updateDisplay(self):
        self.spriteRects = self.spriteGroup.draw(self.screen)
        self.textboxRects = self.textboxGroup.draw(self.screen)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE]):
            pygame.quit()
            sys.exit()
        self.spriteGroup.clear(self.screen, self.background.surface)
        self.textboxGroup.clear(self.screen, self.background.surface)


    def mousePressed():
        #pygame.event.clear()
        mouseState = pygame.mouse.get_pressed()
        if mouseState[0]:
            return True
        else:
            return False


    def spriteClicked(sprite):
        mouseState = pygame.mouse.get_pressed()
        if not mouseState[0]:
            return False  # not pressed
        pos = pygame.mouse.get_pos()
        if sprite.rect.collidepoint(pos):
            return True
        else:
            return False


    


    def mouseX(self):
        x = pygame.mouse.get_pos()
        return x[0]


    def mouseY(self):
        y = pygame.mouse.get_pos()
        return y[1]


    def scrollBackground(self, x, y):
        self.background.scroll(x, y)


    def setAutoUpdate(self, val):
        self.screenRefresh = val

    def setIcon(iconfile):
        gameicon = pygame.image.load(iconfile)
        pygame.display.set_icon(gameicon)

    def setWindowTitle(string):
        pygame.display.set_caption(string)

    def screenSize(self, sizex, sizey, xpos=None, ypos=None, fullscreen=False):
        if xpos != None and ypos != None:
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{xpos}, {ypos + 50}"
        else:
            windowInfo = pygame.display.Info()
            monitorWidth = windowInfo.current_w
            monitorHeight = windowInfo.current_h
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(monitorWidth - sizex) // 2}, {(monitorHeight - sizey) // 2}"
        if fullscreen:
            self.screen = pygame.display.set_mode([sizex, sizey], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode([sizex, sizey])
        self.background = Background()
        self.screen.fill(self.background.colour)
        pygame.display.set_caption(self.gameName)
        self.background.surface = self.screen.copy()
        pygame.display.update()
        return self.screen
    
    def setBackgroundColour(self,colour):
        self.background.setColour(colour)
        if self.screenRefresh:
            self.updateDisplay()


    def setBackgroundImage(self, img):
        self.background.setTiles(img)
        if self.screenRefresh:
            self.updateDisplay()
        

    


    def addSpriteImage(sprite, image):
        sprite.addImage(image)


    def changeSpriteImage(sprite, index):
        sprite.changeImage(index)


    def nextSpriteImage(sprite):
        sprite.currentImage += 1
        if sprite.currentImage > len(sprite.images) - 1:
            sprite.currentImage = 0
        sprite.changeImage(sprite.currentImage)


    def prevSpriteImage(sprite):
        sprite.currentImage -= 1
        if sprite.currentImage < 0:
            sprite.currentImage = len(sprite.images) - 1
        sprite.changeImage(sprite.currentImage)


    def makeImage(filename):
        return loadImage(filename)


    def touching(sprite1, sprite2):
        return pygame.sprite.collide_mask(sprite1, sprite2)


    def allTouching(self,spritename):
        if self.spriteGroup.has(spritename):
            collisions = pygame.sprite.spritecollide(spritename, self.spriteGroup, False, collided=pygame.sprite.collide_mask)
            collisions.remove(spritename)
            return collisions
        else:
            return []

    def keyPressed(self, keyCheck=""):
    
        keys = pygame.key.get_pressed()
        if len(keys) > 0:
            if keyCheck == "" or keys[self.keydict[keyCheck.lower()]]:
                return True
        return False


    def makeLabel(self, text, fontSize, xpos, ypos, fontColour='black', font='Arial', background="clear"):
        # make a text sprite
       return  newLabel(text, fontSize, font, fontColour, xpos, ypos, background)


    def moveLabel(self, sprite, x, y):
        sprite.rect.topleft = [x, y]
        if self.screenRefresh:
            self.updateDisplay()


    def changeLabel(textObject, newText, fontColour=None, background=None):
        # textObject.update(newText, fontColour, background)
        # updateDisplay()
        pass


    def waitPress():
        pygame.event.clear()
        keypressed = False
        thisevent = pygame.event.wait()
        while thisevent.type != pygame.KEYDOWN:
            thisevent = pygame.event.wait()
        return thisevent.key


    def makeTextBox(self, xpos, ypos, width, case=0, startingText="Please type here", maxLength=0, fontSize=22):
        thisTextBox = newTextBox(startingText, xpos, ypos, width, case, maxLength, fontSize)
        self.textboxGroup.add(thisTextBox)
        return thisTextBox


    def drawRect(self, xpos, ypos, width, height, colour, linewidth=0):
        colour = parseColour(colour)
        thisrect = pygame.draw.rect(self.screen, colour, [xpos, ypos, width, height], linewidth)
        if self.screenRefresh:
            pygame.display.update(thisrect)


    def drawLine(self, x1, y1, x2, y2, colour, linewidth=1):
        colour = parseColour(colour)
        thisrect = pygame.draw.line(self.screen, colour, (x1, y1), (x2, y2), linewidth)
        if self.screenRefresh:
            pygame.display.update(thisrect)


    def drawPolygon(self, pointlist, colour, linewidth=0):
        colour = parseColour(colour)
        thisrect = pygame.draw.polygon(self.screen, colour, pointlist, linewidth)
        if self.screenRefresh:
            pygame.display.update(thisrect)


    def drawEllipse(self,centreX, centreY, width, height, colour, linewidth=0):
        colour = parseColour(colour)
        thisrect = pygame.Rect(centreX - width / 2, centreY - height / 2, width, height)
        pygame.draw.ellipse(self.screen, colour, thisrect, linewidth)
        if self.screenRefresh:
            pygame.display.update(thisrect)


    def drawTriangle(self,x1, y1, x2, y2, x3, y3, colour, linewidth=0):
        colour = parseColour(colour)
        thisrect = pygame.draw.polygon(self.screen, colour, [(x1, y1), (x2, y2), (x3, y3)], linewidth)
        if self.screenRefresh:
            pygame.display.update(thisrect)


    def clearShapes(self):
        self.screen.blit(self.background.surface, [0, 0])
        if self.screenRefresh:
            self.updateDisplay()


    def updateShapes(self):
        pygame.display.update()


    def end(self):
        pygame.quit()
    
    def playSound(self, sound, loops=0):
        sound.play(loops)


    def stopSound(self, sound):
        sound.stop()


    def playSoundAndWait(self, sound):
        sound.play()
        while pygame.mixer.get_busy():
            # pause
            self.pause(10)


    def makeMusic(filename):
        pygame.mixer.music.load(filename)


    def playMusic(loops=0):
        global musicPaused
        if musicPaused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play(loops)
        musicPaused = False


    def stopMusic():
        pygame.mixer.music.stop()


    def pauseMusic():
        global musicPaused
        pygame.mixer.music.pause()
        musicPaused = True


    def rewindMusic():
        pygame.mixer.music.rewind()


    def endWait(self):
        self.updateDisplay()
        print("Press ESC to quit")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == keydict["esc"]):
                    waiting = False
        pygame.quit()
        exit()



class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, altDims = None):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename)
        if altDims:
            img = pygame.transform.scale(img, (altDims[0]*frames, altDims[1]))
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)
        if self.screenRefresh:
            self.updateDisplay()


class newTextBox(pygame.sprite.Sprite):
    def __init__(self, text, xpos, ypos, width, case, maxLength, fontSize):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.width = width
        self.initialText = text
        self.case = case
        self.maxLength = maxLength
        self.boxSize = int(fontSize * 1.7)
        self.image = pygame.Surface((width, self.boxSize))
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, width - 1, self.boxSize - 1], 2)
        self.rect = self.image.get_rect()
        self.fontFace = pygame.font.match_font("Arial")
        self.fontColour = pygame.Color("black")
        self.initialColour = (180, 180, 180)
        self.font = pygame.font.Font(self.fontFace, fontSize)
        self.rect.topleft = [xpos, ypos]
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])

    def update(self, keyevent):
        key = keyevent.key
        unicode = keyevent.unicode
        if (31 < key < 127 or 255 < key < 266) and (
                self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
            if keyevent.mod in (1, 2) and self.case == 1 and key >= 97 and key <= 122:
                # force lowercase letters
                self.text += chr(key)
            elif keyevent.mod == 0 and self.case == 2 and key >= 97 and key <= 122:
                self.text += chr(key - 32)
            else:
                # use the unicode char
                self.text += unicode

        elif key == 8:
            # backspace. repeat until clear
            keys = pygame.key.get_pressed()
            nexttime = pygame.time.get_ticks() + 200
            deleting = True
            while deleting:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    thistime = pygame.time.get_ticks()
                    if thistime > nexttime:
                        self.text = self.text[0:len(self.text) - 1]
                        self.image.fill((255, 255, 255))
                        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
                        newSurface = self.font.render(self.text, True, self.fontColour)
                        self.image.blit(newSurface, [10, 5])
                        self.updateDisplay()
                        nexttime = thistime + 50
                        pygame.event.clear()
                else:
                    deleting = False

        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.text, True, self.fontColour)
        self.image.blit(newSurface, [10, 5])
        # if self.screenRefresh:
        #     self.updateDisplay()

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.topleft = [xpos, ypos]
        else:
            self.rect.center = [xpos, ypos]

    def clear(self):
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])
        # if screenRefresh:
        #     updateDisplay()


class newLabel(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColour, xpos, ypos, background):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColour = parseColour(fontColour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font(self.fontFace, fontSize)
        self.renderText()
        self.rect.topleft = [xpos, ypos]

    def update(self, newText, fontColour, background):
        self.text = newText
        if fontColour:
            self.fontColour = parseColour(fontColour)
        if background:
            self.background = parseColour(background)

        oldTopLeft = self.rect.topleft
        self.renderText()
        self.rect.topleft = oldTopLeft
        # if screenRefresh:
        #     self.updateDisplay()

    def renderText(self):
        lineSurfaces = []
        textLines = self.text.split("<br>")
        maxWidth = 0
        maxHeight = 0
        for line in textLines:
            lineSurfaces.append(self.font.render(line, True, self.fontColour))
            thisRect = lineSurfaces[-1].get_rect()
            if thisRect.width > maxWidth:
                maxWidth = thisRect.width
            if thisRect.height > maxHeight:
                maxHeight = thisRect.height
        self.image = pygame.Surface((maxWidth, (self.fontSize + 1) * len(textLines) + 5), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        if self.background != "clear":
            self.image.fill(parseColour(self.background))
        linePos = 0
        for lineSurface in lineSurfaces:
            self.image.blit(lineSurface, [0, linePos])
            linePos += self.fontSize + 1
        self.rect = self.image.get_rect()



class Background():
    def __init__(self):
        self.colour = pygame.Color("black")

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        # self.screen.blit(self.tiles[0][0], [0, 0])
        # self.surface = self.screen.copy()

    def scroll(self, x, y):
        self.stagePosX -= x
        self.stagePosY -= y
        col = (self.stagePosX % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        xOff = (0 - self.stagePosX % self.tileWidth)
        row = (self.stagePosY % (self.tileHeight * len(self.tiles))) // self.tileHeight
        yOff = (0 - self.stagePosY % self.tileHeight)

        col2 = ((self.stagePosX + self.tileWidth) % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        row2 = ((self.stagePosY + self.tileHeight) % (self.tileHeight * len(self.tiles))) // self.tileHeight
        # self.screen.blit(self.tiles[row][col], [xOff, yOff])
        # self.screen.blit(self.tiles[row][col2], [xOff + self.tileWidth, yOff])
        # self.screen.blit(self.tiles[row2][col], [xOff, yOff + self.tileHeight])
        # self.screen.blit(self.tiles[row2][col2], [xOff + self.tileWidth, yOff + self.tileHeight])

        # self.surface = self.screen.copy()

    def setColour(self, colour):
        self.colour = parseColour(colour)
        self.screen.fill(self.colour)
        pygame.display.update()
        # self.surface = self.screen.copy()



if __name__ == "__main__":
    print("pygame_functions is not designed to be run directly.\n" \
        "See the wiki at https://github.com/StevePaget/Pygame_Functions/wiki/Getting-Started for more information.")
