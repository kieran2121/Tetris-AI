import pygame
import random
import time
from copy import deepcopy

# game stats
width = 1000
height = 650
blocksize = 30
gameWidth = 10
gameHeight = 20
windowWidth = gameWidth*blocksize
windowHeight = gameHeight*blocksize
topScore = 0

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
        self.x = 3
        self.y = -4
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
        self.nextBlock = None
        self.playing = True
        self.blockNums = 0
        self.level = 1
        self.line_clears = 0
        self.numOfBlocks = 0
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

    # a function that creates a new random tetronimo
    def current_block(self):
        self.block = self.nextBlock
        self.next_block()
        self.numOfBlocks += 1

    def next_block(self):
        self.nextBlock = Tetronimo()

    def intersection(self):
        intersect = False
        for i in range(4):
            for j in range(4):
                if i*4 + j in self.block.image():
                    # block at right side of screen, block at left side of screen
                    if (j + self.block.x > self.width - 1) or (j + self.block.x < 0):
                        intersect = True
                    # checks if on board
                    if i + self.block.y >= 0:
                        # checks if on board
                        if (j + self.block.x > self.width - 1) or (j + self.block.x < 0):
                            intersect = True
                        # block hits bottom
                        elif i + self.block.y  > self.height -1:
                            intersect = True
                        # intersects with another block
                        elif self.field[i + self.block.y][j + self.block.x] != 0:
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
                        # makes block permanent
                        self.field[i + self.block.y][j + self.block.x] = self.block.colour
                    
            self.row_clear()
            self.current_block()

    # movement controlls        
    def falling(self):
        self.block.y += 1
        if self.intersection() == True:
            self.block.y -= 1
            self.freeze()

    def down(self):
        self.block.y += 1
        if self.intersection() == True:
            self.block.y -= 1
    
    def left(self):
        self.block.x -= 1
        if self.intersection() == True:
            self.block.x += 1
    
    def right(self):
        self.block.x += 1
        if self.intersection() == True:
            self.block.x -= 1

    def drop(self):
        while self.intersection() != True:
            self.block.y +=1
        self.block.y -= 1
        self.freeze()

    def rotate_clockwise(self):
        self.block.rotate_clockwise()
        if self.intersection() == True:
            self.block.rotate_anticlockwise()
    
    def rotate_anticlockwise(self):
        self.block.rotate_anticlockwise()
        if self.intersection() == True:
            self.block.rotate_clockwise()

class TetrisAI:

    # setting up board, scores and creating an array that represents the board 
    def __init__(self):
        self.width = gameWidth
        self.height = gameHeight
        self.field = []
        self.score = 0
        self.blocksize = blocksize
        self.block = None
        self.nextBlock = None
        self.playing = True
        self.blockNums = 0
        self.level = 1
        self.line_clears = 0
        self.numOfBlocks = 0
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

    def new_block(self):
        self.block = Tetronimo()

    def intersection(self):
        intersect = False
        for i in range(4):
            for j in range(4):
                if i*4 + j in self.block.image():
                    # block at right side of screen, block at left side of screen
                    if (j + self.block.x > self.width - 1) or (j + self.block.x < 0):
                        intersect = True
                    # checks if on board
                    if i + self.block.y >= 0:
                        # checks if on board
                        if (j + self.block.x > self.width - 1) or (j + self.block.x < 0):
                            intersect = True
                        # block hits bottom
                        elif i + self.block.y  > self.height -1:
                            intersect = True
                        # intersects with another block
                        elif self.field[i + self.block.y][j + self.block.x] != 0:
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
                        # makes block permanent
                        self.field[i + self.block.y][j + self.block.x] = self.block.colour
                       
    def left(self):
        while self.intersection() != True:
            self.block.x -= 1
        self.block.x += 1
    
    def right(self):
        self.block.x += 1

    def drop(self):
        while self.intersection() != True:
            self.block.y +=1
        self.block.y -= 1
        self.freeze()

    def rotate_clockwise(self):
        self.block.rotate_clockwise()
        if self.intersection() == True:
            self.block.rotate_anticlockwise()
    
    def rotate_anticlockwise(self):
        self.block.rotate_anticlockwise()
        if self.intersection() == True:
            self.block.rotate_clockwise()

class AI:

    def __init__(self):
        self.weights = []
        self.gameScores = []
        self.gen = 1
        self.learning = True
        self.num = 0
        self.topWeights = []
        self.topScores = []
        self.meanHeight = 0
        self.holes = 0
        self.standardDeviation = 0
        self.heightRange = 0
        self.maxAdjacent = 0 
        self.maxHeight = 0
        self.zeros = 0
        self.generations = 100

    def new_gen(self):
        # if gen is first then creates ten completely new random sets, if not uses genetic algorithm to create new gen
        if self.gen == self.generations+1:
            self.learning = False
        elif self.gen == 1 or self.zeros == 10:
            self.weights = []
            self.gameScores = []
            for i in range(10):
                tempList = []
                for i in range(6):
                    tempList.append(random.randint(1,100)/100)
                self.weights.append(tempList)
        else:
            # creates 6 new 'offspring' of two top fittest
            for i in range(6):
                newWeight = []
                for j in range(6):
                    x = random.randint(0,1)
                    newWeight.append(self.weights[x][j])
                self.weights.append(newWeight)
            # mutates 6 new with 1 in 40 chance of a mutation
            for i in range(2,8):
                for i in range(6):
                    mutate = random.randint(1,40)
                    if mutate == 5:
                        self.weights[i][j] = random.randint(1,100)/100
            # creates last two completely random sets
            for i in range(2):
                tempList = []
                for i in range(6):
                    tempList.append(random.randint(1,100)/100)
                self.weights.append(tempList)
            self.gameScores = []

    def fitness(self):
        # gets top scores and corresponding weights and removes others
        self.topWeights = []
        self.topScores = []
        self.topWeights.append(self.weights[0])
        self.topWeights.append(self.weights[1])
        self.topScores.append(self.gameScores[0])
        self.topScores.append(self.gameScores[1])
        self.weights.pop(0)
        self.gameScores.pop(0)
        self.weights.pop(0)
        self.gameScores.pop(0) 

        for i in range(len(self.gameScores)):
            if self.gameScores[i] > self.topScores[0]:
                if self.topScores[0] > self.topScores[1]:
                    self.topScores[1] = self.gameScores[i]
                    self.topWeights[1] = self.weights[i]
                else:
                    self.topScores[0] = self.gameScores[i]
                    self.topWeights[0] = self.weights[i]
            elif self.gameScores[i] > self.topScores[1]:
                self.topScores[1] = self.gameScores[i]
                self.topWeights[1] = self.weights[i]

        self.weights = self.topWeights

    def fieldStats(self, bot):
        self.meanHeight = 0
        self.holes = 0
        self.standardDeviation = 0
        self.heightRange = 0
        self.maxAdjacent = 0
        self.maxHeight = 0
        # gets all required data from board
        heights = []
        total = 0
        for i in range(10):
            filled = 0
            for j in range(20):
                if bot.field[j][i] != 0:
                    heights.append((20-j))
                    filled += 1
                    break
            if filled == 0:
                heights.append(0)
        total = 0
        for i in heights:
            total += i
        self.meanHeight = total/10
        self.maxHeight = max(heights)
        self.heightRange = max(heights) - min(heights)
        diffSquared = 0
        for i in heights:
            diffSquared += (i-self.meanHeight)**2
        self.standardDeviation = (diffSquared/10)**0.5
        self.standardDeviation = round(self.standardDeviation,2)
        for i in range(9):
            diff = abs(heights[i] - heights[i+1])
            if diff > self.maxAdjacent:
                self.maxAdjacent = diff
        for i in range(10):
            checkHoles = False
            for j in range(20):
                if bot.field[j][i] != 0:
                    checkHoles = True
                if checkHoles:
                    if bot.field[j][i] == 0:
                        self.holes += 1

        
        

    def play(self, type, colour, rotation, grid):
        bot = TetrisAI()
        bot.new_block()
        bot.block.type = deepcopy(type)
        bot.block.colour = deepcopy(colour)
        bot.block.rotation = deepcopy(rotation)
        bot.field = deepcopy(grid)
        # 2D array contating sets of x co-ordinate, block rotation, weighted outcome
        outcomes = []
        for i in range(len(blocks[bot.block.type])):
            bot.field = deepcopy(grid)
            bot.left()
            bot.drop()
            bot.row_clear()
            self.fieldStats(bot)
            weightedOutcome = (self.weights[self.num][0])*self.meanHeight + (self.weights[self.num][1])*self.holes + (self.weights[self.num][2])*self.standardDeviation + (self.weights[self.num][3])*self.heightRange + (self.weights[self.num][4])*self.maxAdjacent + (self.weights[self.num][5])*self.maxHeight
            outcomes.append([bot.block.x, bot.block.rotation, weightedOutcome])
            bot.field = deepcopy(grid)
            bot.block.y = -4
            bot.right()
            while bot.intersection() != True:
                bot.drop()
                bot.row_clear()
                self.fieldStats(bot)
                weightedOutcome = (self.weights[self.num][0])*self.meanHeight + (self.weights[self.num][1])*self.holes + (self.weights[self.num][2])*self.standardDeviation + (self.weights[self.num][3])*self.heightRange + (self.weights[self.num][4])*self.maxAdjacent + (self.weights[self.num][5])*self.maxHeight
                outcomes.append([bot.block.x, bot.block.rotation, weightedOutcome])
                bot.field = deepcopy(grid)
                bot.block.y = -4
                bot.right()
            bot.block.x = 3
            bot.block.y = -4
            bot.block.rotate_clockwise()
        vals = []
        for i in outcomes:
            vals.append((i[2]))
        bestVal = min(vals)
        valIndex = vals.index(bestVal)
        bestMove = outcomes[valIndex]   
        return bestMove    
        

# actual game code
def Main(topScore):
    bot = AI()
    while bot.learning:

        clock = pygame.time.Clock()
        game = Tetris()
        counter = 0
        speed = 100 - 5*game.level
        if speed < 5:
            speed = 5
        
        if bot.weights == []:
            bot.new_gen()

        if len(bot.gameScores) == 10:
            bot.gen += 1
            bot.fitness()
            bot.new_gen()
            bot.num = 0
            print(topScore)

        if bot.gen != bot.generations+1:
            while game.playing:

                if game.block == None:
                    if game.nextBlock == None:
                        game.next_block()
                        game.current_block()

                if counter == speed:
                    game.falling()
                    counter -= speed

                bestMove = AI.play(bot, game.block.type, game.block.colour, game.block.rotation, game.field)

                while bestMove[1] > game.block.rotation:
                    game.rotate_clockwise()
                    print("hello1")
                while bestMove[1] < game.block.rotation:
                    game.rotate_anticlockwise()
                    print("hello2")
                while bestMove[0] > game.block.x:
                    game.right()
                    print("hello3")
                while bestMove[0] < game.block.x:
                    game.left()
                    print("hello4")
                game.drop()


                # creates surface appearance
                screen.fill((55,198,255))
                pygame.draw.rect(screen, (11,102,35), pygame.Rect(0, height-(height-windowHeight)//2, width, (height-windowHeight)//2))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect((width-windowWidth)//2, (height-windowHeight)//2, windowWidth, windowHeight))
                for i in range(game.width):
                    for j in range(game.height):
                        pygame.draw.rect(screen, (230,230,230), pygame.Rect(i*blocksize + ((width-windowWidth)//2), j*blocksize + ((height-windowHeight)//2) , blocksize, blocksize), 1)

                # fills in falling blocks
                if game.block is not None:
                    for i in range(4):
                        for j in range(4):
                            if i*4 + j in game.block.image():
                                pygame.draw.rect(screen, game.block.colour, pygame.Rect(j*blocksize + game.block.x*blocksize + ((width-windowWidth)//2), i*blocksize + game.block.y*blocksize + ((height-windowHeight)//2), blocksize, blocksize))

                # fills in frozen blocks
                for i in range(game.height):
                    for j in range(game.width):
                        if game.field[i][j] != 0:
                            pygame.draw.rect(screen, game.field[i][j], pygame.Rect(j*blocksize + ((width-windowWidth)//2), i*blocksize + ((height-windowHeight)//2), blocksize, blocksize))

                # creates surface appearance
                pygame.draw.rect(screen, (0,0,0), pygame.Rect((width-windowWidth)//2, (height-windowHeight)//2, windowWidth, windowHeight),2)
                
                # covers top of screen
                pygame.draw.rect(screen, (55,198,255), pygame.Rect( ((width-windowWidth)//2), 0, windowWidth, ((height-windowHeight)//2)) )

                # displays next block
                if game.nextBlock is not None:
                    for i in range(4):
                        for j in range(4):
                            if i*4 + j in game.nextBlock.image():
                                pygame.draw.rect(screen, game.nextBlock.colour, pygame.Rect(770 + j*blocksize, 130 + i*blocksize, blocksize, blocksize))
                                

                # Tetris title and score
                font = pygame.font.SysFont('Calibri', 30, True)
                text = font.render("LEVEL: " + str(game.level), True, (0,0,0))
                screen.blit(text, (100, 160))
                text = font.render("SCORE: " + str(game.score), True, (0,0,0))
                screen.blit(text, (100, 200))
                text = font.render("Generation: " + str(bot.gen), True, (0,0,0))
                screen.blit(text, (95, 240))
                text = font.render("Bot number: " + str(bot.num+1), True, (0,0,0))
                screen.blit(text, (95, 280))
                text = font.render("NEXT BLOCK: ", True, (0,0,0))
                screen.blit(text, (750, 100))
                font = pygame.font.SysFont('Calibri', 58, True)
                text = font.render("TETRIS", True, (0,0,0))
                screen.blit(text, (90, 100))
                pygame.display.update()

                counter += 1
                clock.tick(100)
        
            bot.gameScores.append(game.numOfBlocks)
            bot.num += 1
            if game.score > topScore:
                topScore = deepcopy(game.score)



    # game ending
    time.sleep(2)
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Calibri", 25)
    ending = font.render("Learning Finished!", True, (0,0,0))
    screen.blit(ending, (420, 300))
    font = pygame.font.SysFont("Calibri", 25)
    again = font.render("Top score was: " + str(topScore), True, (0,0,0))
    screen.blit(again, (420, 340))
    end = True
    while end:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
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
            Main(topScore)

    

