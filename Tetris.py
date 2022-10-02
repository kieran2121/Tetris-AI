import pygame
import random
import time

# game stats
width = 1000
height = 650

blocksize = 21
gameWidth = blocksize*10
gameHeight = blocksize*20

# shapes created by following 4x4 matrix:
# 0  1  2  3
# 4  5  6  7
# 8  9  10 11
# 12 13 14 15
# and their possible rotations
# idea from source (DataFlair, n.d.)
blocks = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6]],
    [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
    [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
    [[1, 2, 5, 6]]
]

# the colours the blocks can be
colours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
        

class Tetronimo:
    # settting up all information about the tetronimo
    def __init__(self):
        num = random.randint(0,len(blocks) - 1)
        self.x = 3*blocksize
        self.y = -(4*blocksize)
        self.type = num
        self.colour = colours[num]
        self.rotation = 0
    
    # a function to reuturn the shape type and its rotation
    def image(self):
        return blocks[self.type][self.rotation]

    # functions to rotate the tetrinomo
    def rotate_clockwise(self):
        self.rotation = (self.rotation + 1) % len(blocks[self.type])
    
    def rotate_anticlockwise(self):
        self.rotation = (self.rotation - 1) % len(blocks[self.type])

class Tetris:

    # setting up board, scores and creating an array that represents the board 
    def __init__(self):
        self.width = gameWidth
        self.height = gameHeight
        self.field = []
        self.score = 0
        self.blocksize = blocksize
        self.block = None
        self.playing = True
        self.blockNums = 0
        self.level = 1
        self.line_clears = 0
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

    # a function that creates a new random tetronimo
    def new_block(self):
        self.block = Tetronimo()

    def intersection(self):
        intersect = False
        for i in range(4):
            for j in range(4):
                if i*4 + j in self.block.image():
                    # block at right side of screen, block at left side of screen
                    if (j*blocksize + self.block.x > self.width - 1) or (j*blocksize + self.block.x < 0):
                        intersect = True
                    if i*blocksize + self.block.y + (blocksize-1) > 0:
                        if (j*blocksize + self.block.x > self.width - 1) or (j*blocksize + self.block.x < 0):
                            intersect = True
                        # block hits bottom
                        elif i*blocksize + self.block.y + (blocksize-1) > self.height-1:
                            intersect = True
                        # intersects at bottom or right of moving block
                        elif (self.field[i*blocksize + self.block.y + (blocksize-1)][j*blocksize + self.block.x + (blocksize-1)] != 0):
                            intersect = True
                        elif i*blocksize + self.block.y > 0:
                            #intersects at top or left of moving block (bit of allowance for fitting in gaps under blocks)
                            if (self.field[i*blocksize + self.block.y + 3][j*blocksize + self.block.x] != 0):
                                intersect = True
        return intersect

    def row_clear(self):
        lines = 0
        for i in range(0, self.height):
            zeros = 0
            newLines = []
            for x in range (self.width):
                newLines.append(0)
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                self.field.pop(i)
                self.field = [newLines] + self.field
        
        # adjusts score and level
        lines = lines // blocksize
        self.line_clears += lines
        if lines == 1:
            self.score += 40*self.level
        if lines == 2:
            self.score += 100*self.level
        if lines == 3:
            self.score += 300*self.level
        if lines == 4:
            self.score += 1200*self.level
        if self.line_clears >= 10:
            self.level += 1
            self.line_clears -= 10

    # freezes a block when it hits the bottom or another block
    def freeze(self):
        if self.block.y < 0:
            self.playing  = False
        else:
            for i in range(4):
                for j in range(4):
                    if i *4 + j in self.block.image():
                        for y in range(i*blocksize + self.block.y, i*blocksize + self.block.y + blocksize):
                            for x in range(j*blocksize + self.block.x, j*blocksize + self.block.x + blocksize):
                                self.field[y][x] = self.block.colour
            self.row_clear()
            self.new_block()

    # movement controlls        
    def falling(self):
        self.block.y += blocksize
        if self.intersection() == True:
            self.block.y -= blocksize
            self.freeze()

    def down(self):
        self.block.y += self.blocksize
        if self.intersection() == True:
            self.block.y -= self.blocksize
    
    def left(self):
        self.block.x -= self.blocksize
        if self.intersection() == True:
            self.block.x += self.blocksize
    
    def right(self):
        self.block.x += self.blocksize
        if self.intersection() == True:
            self.block.x -= self.blocksize

    def drop(self):
        while self.intersection() != True:
            self.block.y +=1
        self.block.y -= 1
        self.freeze()

    def rotate_clockwise(self):
        self.block.rotate_clockwise()
        if self.intersection() == True:
            self.block.rotate_anticlockwise()
    
    def roatate_anticlockwise(self):
        self.block.rotate_anticlockwise()
        if self.intersection() == True:
            self.block.rotate_clockwise()

# actual game code
def Main():
    
    clock = pygame.time.Clock()
    game = Tetris()
    counter = 0
    speed = speed = 100 - 5*game.level
    if speed < 5:
        speed = 5

    while game.playing:

        if game.block == None:
            game.new_block()

        if counter == speed:
            game.falling()
            counter -= speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate_clockwise()
                if event.key == pygame.K_x:
                    game.roatate_anticlockwise()
                if event.key == pygame.K_LEFT:
                    game.left()
                if event.key == pygame.K_RIGHT:
                    game.right()
                if event.key == pygame.K_DOWN:
                    game.down()
                if event.key == pygame.K_SPACE:
                    game.drop()

        screen.fill((55,198,255))
        pygame.draw.rect(screen, (11,102,35), pygame.Rect(0, height-(height-game.height)//2, width, (height-game.height)//2))
        pygame.draw.rect(screen, (255,255,255), pygame.Rect((width-game.width)//2, (height-game.height)//2, game.width, game.height))
        for i in range(0, game.width, blocksize):
            for j in range(0, game.height, blocksize):
                pygame.draw.rect(screen, (230,230,230), pygame.Rect(i+((width-game.width)//2), j+((height-game.height)//2) , blocksize, blocksize), 1)

        # fills in falling blocks
        if game.block is not None:
            for i in range(4):
                for j in range(4):
                    if i*4 + j in game.block.image():
                        pygame.draw.rect(screen, game.block.colour, pygame.Rect(j*blocksize + game.block.x + ((width-game.width)//2), i*blocksize + game.block.y + ((height-game.height)//2), blocksize, blocksize))

        # fills in frozen blocks
        for i in range(game.height):
            for j in range(game.width):
                if game.field[i][j] != 0:
                    pygame.draw.rect(screen, game.field[i][j], pygame.Rect(j + ((width-game.width)//2), i + ((height-game.height)//2), 1, 1))

        # creates surface appearance
        for i in range(0, game.width, blocksize):
            for j in range(0, game.height, blocksize):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect((width-game.width)//2, (height-game.height)//2, game.width, game.height),2)
        
        # covers top of screen
        pygame.draw.rect(screen, (55,198,255), pygame.Rect( ((width-game.width)//2), 0, game.width, ((height-game.height)//2)) )

        # Tetris title and score
        font = pygame.font.SysFont('Calibri', 30, True)
        text = font.render("LEVEL: " + str(game.level), True, (0,0,0))
        screen.blit(text, (750, 260))
        text = font.render("SCORE: " + str(game.score), True, (0,0,0))
        screen.blit(text, (750, 300))
        font = pygame.font.SysFont('Calibri', 58, True)
        text = font.render("TETRIS", True, (0,0,0))
        screen.blit(text, (420, 30))
        pygame.display.update()

        counter += 1
        clock.tick(100)



    # game ending
    time.sleep(2)
    if game.playing == False:
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont("Calibri", 25)
        ending = font.render("Game over!", True, (0,0,0))
        screen.blit(ending, (435, 300))
        pygame.display.update()
        time.sleep(1.5)
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont("Calibri", 25)
        again = font.render("Press enter to play again!", True, (0,0,0))
        screen.blit(again, (377, 300))
        end = True
        while end:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        del game 
                        Main()

        pygame.quit()

# creates intro screen and starts game    
pygame.font.init()
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
font = pygame.font.SysFont("Calibri", 25)
intro = font.render("Press any key to start!", True, (0,0,0))
screen.blit(intro, (387, 300))
run = True
while run:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            Main()