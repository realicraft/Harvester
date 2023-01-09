import sys, os, random, math, pygame
pygame.init()

SIZE = WIDTH, HEIGHT = 640, 480
SIZER = WIDTHR, HEIGHTR = 320, 240

# define colors
BLACK =   pygame.Color(0x00, 0x00, 0x00)
RED =     pygame.Color(0xff, 0x00, 0x00)
ORANGE =  pygame.Color(0xff, 0x7f, 0x00)
YELLOW =  pygame.Color(0xff, 0xff, 0x00)
GREEN =   pygame.Color(0x00, 0xff, 0x00)
CYAN =    pygame.Color(0x00, 0xff, 0xff)
BLUE =    pygame.Color(0x00, 0x00, 0xff)
PURPLE =  pygame.Color(0x7f, 0x00, 0xff)
MAGENTA = pygame.Color(0xff, 0x00, 0xff)
WHITE =   pygame.Color(0xff, 0xff, 0xff)
GRAY =    pygame.Color(0x7f, 0x7f, 0x7f)
BGCOLOR = pygame.Color(0xff, 0xff, 0xe6)
BGSEL   = pygame.Color(0xe6, 0xe6, 0xcf)
PLOTBR  = pygame.Color(0x66, 0x33, 0x00)
PLOTWW  = pygame.Color(0x7f, 0x3f, 0x00)
PLOTNW  = pygame.Color(0xcc, 0x99, 0x66)

# define the framerate and values based on it
FRAMERATE = 60
FRAMERATE8 = int(FRAMERATE*0.8)
FRAMERATE15 = FRAMERATE*15
FRAMERATE30 = FRAMERATE*30

def getImageList(folder):
    return [
        pygame.image.load(os.path.join("assets/"+folder, "item.png")),
        pygame.image.load(os.path.join("assets/"+folder, "grow1.png")),
        pygame.image.load(os.path.join("assets/"+folder, "grow2.png")),
        pygame.image.load(os.path.join("assets/"+folder, "grow3.png"))
    ]

CROPLIST = [ #[name, seed price, sell price, growth time, water multi, [images (item/growth1/growth2/growth3)]]
    ["Wheat", 2, 3, [5,8], 1.2, getImageList("wheat")],
    #["Corn", 4, 7, [7,7], 1.2, getImageList("corn")],
    ["Carrots", 3, 5, [6,7], 1.2, getImageList("carrots")],
    ["Potatoes", 4, 6, [6,8], 1.1, getImageList("potatoes")],
    #["Cabbage", 3, 5, [7,7], 1.4, getImageList("cabbage")],
    ["Mushrooms", 2, 3, [10,11], 1.7, getImageList("mushrooms")],
    ["Grapes", 5, 7, [8,4], 1.1, getImageList("grapes")],
    #["Lettuce", 3, 5, [6,8], 1.3, getImageList("lettuce")],
    ["Tomatoes", 3, 5, [8,5], 1.1, getImageList("tomatoes")],
    ["Beans", 5, 6, [4,4], 1.2, getImageList("beans")],
    #["Green Beans", 5, 7, [6,7], 1.3, getImageList("green_beans")],
    ["Strawberries", 6, 9, [9,3], 1.3, getImageList("strawberries")]
]

MAINFONT16 = pygame.font.SysFont("Arial", 32)
MAINFONT10 = pygame.font.SysFont("Arial", 20)

# the plots that you plant crops in
slots = [ #[id, timer, goal, state, water timer] (default [-1, 0, 1, 0, 0])
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
    [[-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
]
#for i in range(len(slots)):
#    for j in range(len(slots[i])):
#        slots[i][j][0] = random.randint(0, 1)
#        slots[i][j][2] = CROPLIST[slots[i][j][0]][3][0]*FRAMERATE8

SCREEN = pygame.display.set_mode(SIZE)
screenr = pygame.surface.Surface(SIZER)

pygame.display.set_caption("Harvester")
pygame.display.set_icon(CROPLIST[1][5][0])

clock = pygame.time.Clock()

plotsbg = pygame.Rect(87, 47, 146, 146)
selectbg = pygame.Rect(78, 219, 18, 18)
coinimg = pygame.image.load(os.path.join("assets/", "coin.png"))
canimg = pygame.image.load(os.path.join("assets/", "watercan.png"))
fertimg = pygame.image.load(os.path.join("assets/", "fert.png"))
shovelimg = pygame.image.load(os.path.join("assets/", "shovel.png"))
KEYLIST = "SWF12345678"

money = 2
selected = 3 # 0 is harvest, 1 is watering can, 2 is fertilizer, 3+ is a crop seed

# function to determine which plot was clicked on
def getPlotClicked(x, y):
    x = math.floor(x/2)
    y = math.floor(y/2)
    if (x < 88) or (x > 231) or (y < 48) or (y > 191): return (-1, -1)
    else:
        return (math.floor((x-88)/18), math.floor((y-48)/18))

# function to draw the plots
def drawPlots():
    pygame.draw.rect(screenr, PLOTBR, plotsbg)
    for i in range(len(slots)):
        for j in range(len(slots[i])):
            plot = pygame.Rect(88+(j*18), 48+(i*18), 18, 18)
            pygame.draw.rect(screenr, PLOTNW.lerp(PLOTWW, (slots[i][j][4]/FRAMERATE30)), plot)
            pygame.draw.rect(screenr, PLOTBR, plot, 1)

# function to draw planted crops over the plots
def drawCrops():
    for i in range(len(slots)):
        for j in range(len(slots[i])):
            if slots[i][j][0] != -1:
                screenr.blit(CROPLIST[slots[i][j][0]][5][1+slots[i][j][3]], (89+(j*18), 49+(i*18)))

# function to draw the box behind the selected crops
def drawSelection():
    selectbg.x = 60+(selected*18)
    pygame.draw.rect(screenr, BGSEL, selectbg)

# function to draw the available items
def drawItems():
    screenr.blit(shovelimg, (61, 220))
    screenr.blit(canimg, (79, 220))
    screenr.blit(fertimg, (97, 220))
    for i in range(len(CROPLIST)):
        screenr.blit(CROPLIST[i][5][0], (115+(i*18), 220))

# function to draw the keybinds and prices of the items
def drawItemsText():
    SCREEN.blit(MAINFONT10.render("10¢", True, BLACK), (196+((32-(MAINFONT10.size("10¢")[0]))/2), 396))
    for i in range(len(CROPLIST)):
        SCREEN.blit(MAINFONT10.render(str(CROPLIST[i][1])+"¢", True, BLACK), (230+((32-(MAINFONT10.size(str(CROPLIST[i][1])+"¢")[0]))/2)+(i*36), 396))
    for j in range(len(KEYLIST)):
        SCREEN.blit(MAINFONT10.render(KEYLIST[j], True, BLACK), (122+((32-(MAINFONT10.size(KEYLIST[j])[0]))/2)+(j*36), 418))

# functions to draw the money counter
def drawMoney():
    screenr.blit(coinimg, (4,4))
def drawMoneyText():
    SCREEN.blit(MAINFONT16.render(str(money), True, BLACK, BGCOLOR), (48, 8))

# function to draw the framerate
def drawFR():
    SCREEN.blit(MAINFONT10.render(str(int(clock.get_fps())), True, BLACK, BGCOLOR), (4, 456))

def plantCrop(x, y, crop):
    global money
    if ((slots[y][x][0] == -1) and (money >= CROPLIST[crop][1])):
        slots[y][x][0] = crop
        slots[y][x][1] = 0
        slots[y][x][2] = CROPLIST[crop][3][0]*FRAMERATE8
        slots[y][x][3] = 0
        money -= CROPLIST[crop][1]

def harvestCrop(x, y):
    global money
    if (slots[y][x][3] == 2):
        money += CROPLIST[slots[y][x][0]][2]
        slots[y][x][0] = -1
        slots[y][x][1] = 0
        slots[y][x][2] = 1
        slots[y][x][3] = 0

def waterCrop(x, y):
    if (slots[y][x][4] <= FRAMERATE15): slots[y][x][4] = FRAMERATE30

def fertilizeCrop(x, y):
    global money
    if ((slots[y][x][1] <= slots[y][x][2]) and (money >= 10)):
        slots[y][x][1] += 5*FRAMERATE8
        money -= 10

def growCrops():
    for i in range(len(slots)):
        for j in range(len(slots[i])):
            if (slots[i][j][4] > 0): slots[i][j][4] -= 1
            if (slots[i][j][0] == -1) or (slots[i][j][3] == 2): continue
            else:
                if (random.randint(1, 10) <= 8):
                    if (slots[i][j][4] > 0): slots[i][j][1] += CROPLIST[slots[i][j][0]][4]
                    else: slots[i][j][1] += 1
                if (slots[i][j][1] >= slots[i][j][2]):
                    slots[i][j][1] = slots[i][j][2]-slots[i][j][1]
                    slots[i][j][2] = CROPLIST[slots[i][j][0]][3][1]*FRAMERATE8
                    slots[i][j][3] += 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cropPos = getPlotClicked(event.pos[0], event.pos[1])
            if cropPos == (-1, -1): pass
            else:
                if (selected == 0): harvestCrop(cropPos[0], cropPos[1])
                elif (selected == 1): waterCrop(cropPos[0], cropPos[1])
                elif (selected == 2): fertilizeCrop(cropPos[0], cropPos[1])
                elif (selected >= 3): plantCrop(cropPos[0], cropPos[1], selected-3)
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_s): selected = 0
            elif (event.key == pygame.K_w): selected = 1
            elif (event.key == pygame.K_f): selected = 2
            elif (event.key == pygame.K_1): selected = 3
            elif (event.key == pygame.K_2): selected = 4
            elif (event.key == pygame.K_3): selected = 5
            elif (event.key == pygame.K_4): selected = 6
            elif (event.key == pygame.K_5): selected = 7
            elif (event.key == pygame.K_6): selected = 8
            elif (event.key == pygame.K_7): selected = 9
            elif (event.key == pygame.K_8): selected = 10
            elif (event.key == pygame.K_9): selected = 11
            elif (event.key == pygame.K_0): selected = 12
            elif (event.key == pygame.K_MINUS): selected = 13
            elif (event.key == pygame.K_EQUALS): selected = 14

    clock.tick(FRAMERATE)
    screenr.fill(BGCOLOR)
    growCrops()
    drawMoney()
    drawPlots()
    drawCrops()
    drawSelection()
    drawItems()
    SCREEN.blit(pygame.transform.scale(screenr, SCREEN.get_rect().size), (0, 0))
    drawFR()
    drawItemsText()
    drawMoneyText()
    pygame.display.flip()