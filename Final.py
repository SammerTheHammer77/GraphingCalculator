#Hey there! This is a Sam program.
import pygame, math, time

#Define colours, constants pi and e, and the start time of the program
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (242, 106, 33)
YELLOW = (247, 213, 42)
SCREENCOLOUR = (211, 227, 227)
LIGHTGREEN = (22, 224, 56)
GREEN = (20, 84, 21)
DARKGREEN = (13, 122, 31)
LIGHTBLUE = (58, 244, 244)
BLUE = (0, 0, 255)
PURPLE = (129, 25, 214)
PINK = (242, 106, 183)
BLACK = (0, 0, 0)
PI = math.pi
EULER = math.e
STARTTIME = time.time()

#The Function class stores information like the function, a table of points, a table of coordinates, a colour,
#the scale of the function, the domain, the range, if there's an x or f(x) that should be evaluated, and if the
#options window is open. It also can draw the graph, change its colour, limit its domain and range, and evaluate
#f(x) at a certain x value.
class Function():
    def __init__(self):
        self.function = ""
        self.tab_vals = []
        self.tab_points = []
        self.colours = [RED, ORANGE, YELLOW, LIGHTGREEN, DARKGREEN, LIGHTBLUE, BLUE, PURPLE, PINK, BLACK]
        self.colour = 9
        self.scale = 10
        self.domain = "ALL"
        self.range = "ALL"
        self.x = "NONE"
        self.f_of_x = "NONE"
        self.options = False

    #Takes in a list of points, and draws the lines for a graph on the grid picture
    def draw_graph(self, calc_screen):
        for i in range(len(self.tab_points)-1):
            try: pygame.draw.line(calc_screen, self.colours[self.colour], (self.tab_points[i][0], self.tab_points[i][1]), (self.tab_points[i+1][0], self.tab_points[i+1][1]), 4)
            except: pass

    #Changes colour of graph if signaled
    def change_colour(self, pointer_rect):
        k = 0
        for i in range(545, 605, 30):
            for j in range(675, 805, 30):
                rect = pygame.Rect(j, i, 20, 20)
                if rect.colliderect(pointer_rect):
                    self.colour = k
                k += 1

    #Limits domain of graph
    def limit_domain(self, calc):
        if "<" in self.domain:
            expr = self.domain
            expr = expr.replace("X<", "")
            num = float(parse(calc, expr))
            for i in range(len(self.tab_vals)):
                if self.tab_vals[i][0] > num:
                    self.tab_vals[i][1] = "UNDEFINED"
                    
        elif ">" in self.domain:
            expr = self.domain
            expr = expr.replace("X>", "")
            num = float(parse(calc, expr))
            for i in range(len(self.tab_vals)):
                if self.tab_vals[i][0] < num:
                    self.tab_vals[i][1] = "UNDEFINED"

    #Limits range of graph 
    def limit_range(self, calc):
        if "<" in self.range:
            expr = self.range
            expr = expr.replace("F(X)<", "")
            num = float(parse(calc, expr))
            for i in range(len(self.tab_vals)):
                try:
                    if self.tab_vals[i][1] > num:
                        self.tab_vals[i][1] = "UNDEFINED"
                except: pass
                    
        elif ">" in self.range:
            expr = self.range
            expr = expr.replace("F(X)>", "")
            num = float(parse(calc, expr))
            for i in range(len(self.tab_vals)):
                if self.tab_vals[i][1] < num:
                    self.tab_vals[i][1] = "UNDEFINED"

    #Evaluates f(x) at a certain x value depending on what function is stored at the time
    def eval_x(self, calc):
        func = self.function
        func = func.replace("F(X)=", "")
        func = func.replace("X", str(self.x))
        if self.x != "NONE":
            try: self.f_of_x = float(parse(calc, func))
            except: self.f_of_x = "UNDEFINED"

#The Calculator class stores calculator's input value, output value, whether it's in degrees, radians, or gradians,
#if second function is currently pressed, if there's a function to graph, if there's a number stored in memory, where
#the index is in the input string, and a function object. It has methods to change between degrees, radians, and
#gradians, to calculate coordinates to be graphed, and to add a value to the input string.
class Calculator():
    def __init__(self):
        self.val = "0"
        self.ans_val = ""
        self.mode = "DEG"
        self.second_f = False
        self.grid = False
        self.mem = ""
        self.index = 0
        self.function = Function()

    #Changes between degrees, gradians, and radians
    def change_mode(self):
        if self.mode == "RAD":
            self.mode = "GRAD"
        elif self.mode == "GRAD":
            self.mode = "DEG"
        elif self.mode == "DEG":
            self.mode = "RAD"
        return self.mode

    #Calculates a list of coordinates that is drawn using another method.
    def calculate_values(self):
        self.function.tab_vals.clear()
        self.function.tab_points.clear()
        x = -(self.function.scale)
        while x <= self.function.scale:
            func = self.function.function
            func = func.replace("F(X)=", "")
            func = func.replace("-X", "-1xX")
            func = func.replace("X", str(x))
            try: y = float(parse(self, func))
            except: y = "UNDEFINED"
            self.function.tab_vals.append([x,y])
            x += (self.function.scale/100)
            x = round(x, 2)
            
        self.function.limit_domain(self)
        self.function.limit_range(self)
            
        for i in range(len(self.function.tab_vals)):
            try:
                x = self.function.tab_vals[i][0] * (500/(self.function.scale*2)) + 575
                y = self.function.tab_vals[i][1] * -(500/(self.function.scale*2)) + 250
                self.function.tab_points.append([x,y])
            except: self.function.tab_points.append([x,"UNDEFINED"])

    #Adds a value to the input string depending on the position of the "|" calculator
    def add_character(self, label):
        if self.index == 0:  self.val = (self.val + str(label))
        else: self.val = (self.val[:-self.index] + str(label) + self.val[-self.index:])
        
#Button class, giving attributes to all buttons on the calculator (Its rectangle, what it says, its picture, and if it's pressed)
class Button():
    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)
        self.label = ""
        self.pic = pygame.image.load("Buttons/Button0.png").convert()
        self.pressed = False
        self.font = pygame.font.SysFont("Times New Roman", 25, False, False)
        
    #This method draws a singular button in its proper position, and adds the label to it
    def draw_button(self, screen):      
        screen.blit(self.pic, self.rect)
        label = self.font.render(self.label, False, BLACK)
        screen.blit(label, (self.rect.x-1, self.rect.centery-10))
        
    #This method determines the course of action depending on the button pressed   
    def logic(self, calc, i, buttons):
        calc.val = calc.val.replace("|", "")
        calc.val = calc.val.replace(" ", "")
        if calc.val == "0" and i != 10 or calc.val == "0.0" and i != 10:
            calc.val = ""

        #If certain buttons are pressed, add said button to the input string
        if i <= 10 or i >= 13 and i <= 14 or i >= 16 and i <= 22 or i == 27: calc.add_character(str(self.label))
        elif i == 11: calc.add_character("-")
        
        #Determines whether to evaluate the input string, draw a graph, limit the domain or range, or evaluate f(x) at x
        elif i == 12:
            if calc.val == "":
                calc.ans_val = "0"
            elif "F(X)=" in calc.val:
                calc.function.function = calc.val
                calc.calculate_values()
                calc.grid = True
                calc.function.domain = "ALL"
                calc.function.range = "ALL"
                calc.function.x = "NONE"
                calc.function.f_of_x = "NONE"
                if not calc.function.options: calc_screen = pygame.display.set_mode((825, 500))
            elif "Domain" in calc.val:
                domain = calc.val.replace("Domain:", "")
                calc.function.domain = domain
                buttons[17].label = "   ("
                buttons[18].label = "   )"
                calc.val = calc.function.function
                calc.calculate_values()
            elif "Range" in calc.val:
                range_y = calc.val.replace("Range:", "")
                calc.function.range = range_y
                buttons[17].label = "   ("
                buttons[18].label = "   )"
                calc.val = calc.function.function
                calc.calculate_values()
            elif "Evaluate" in calc.val:
                calc.function.x = calc.val.replace("Evaluate:F", "")
                calc.val = calc.function.function
                calc.function.eval_x(calc)
            else:
                try: calc.ans_val = str(round(float(parse(calc, calc.val)), 12))
                except: calc.ans_val = "ERROR 2: Logic Error"
        elif i == 15: calc.add_character("•")
        elif i == 23: calc.add_character("^")
        elif i == 24: calc.add_character("^2")
        elif i == 25: calc.add_character("2√")
        elif i == 26: calc.add_character("√")
        elif i == 28:
            if not calc.second_f:
                calc.val = (calc.val + "EE+")
            elif calc.second_f:
                calc.val = (calc.val + self.label)
        #Clears input string, and replaces it with "0"
        elif i == 29:
            calc.val = "0"
            calc.index = 0
        #Deletes one character from the input string depending on the placement of the "|"
        elif i == 30:
            if calc.index == 0: calc.val = calc.val[0:len(calc.val)-1]
            else: calc.val = (calc.val[:-(calc.index)-1] + calc.val[-calc.index:])
        #Saves or recalls a value from or to memory
        elif i == 31:
            if calc.second_f: calc.mem = calc.ans_val
            elif not calc.second_f:
                if calc.mem != "":
                    calc.add_character("MEM")
        #Clears memory or changes degrees, radians, gradians
        elif i == 32:
            if calc.second_f: calc.mem = ""
            elif not calc.second_f: calc.mode = calc.change_mode()
        #Switches if second function is true
        elif i == 33:
            calc.second_f = not calc.second_f
            if calc.second_f:
                buttons[19].label = "  sin`¹"
                buttons[20].label = "  cos`¹"
                buttons[21].label = "  tan`¹"
                buttons[22].label = "    e"
                buttons[28].label = "    !"
                buttons[31].label = " memS"
                buttons[32].label = " memC"
            elif not calc.second_f:
                buttons[19].label = "  sin"
                buttons[20].label = "  cos"
                buttons[21].label = "  tan"
                buttons[22].label = "    π"
                buttons[28].label = "  exp"
                buttons[31].label = " memR"
                buttons[32].label = " MOD"
        #Gets calculator ready for function input or adds an "X" to the input string depending on "|" position
        elif i == 34:
            if "F(X)=" not in calc.val:
                calc.val = "F(X)="
            else:
                multiply = False
                for i in range(10):
                    if calc.val[-1] == str(i):
                        multiply = True
                        
                if not multiply: calc.add_character("X")
                elif multiply: calc.add_character("•X")
        #Toggles the function options menu
        elif i == 35:
            calc.function.options = not calc.function.options
            if calc.function.options: calc_screen = pygame.display.set_mode((825, 600))
            elif not calc.function.options: calc_screen = pygame.display.set_mode((825, 500))
        #Clears the grid
        elif i == 36:
            calc.grid = False
            calc.function.options = False
            calc_screen = pygame.display.set_mode((325, 500))
        #Zooms in the graph
        elif i == 37:
            if calc.function.scale >= 2:
                calc.function.scale -= 1
                calc.calculate_values()
        #Zooms out the graph
        elif i == 38:
            calc.function.scale += 1
            calc.calculate_values()
        #Sets no limit to domain
        elif i == 39:
            calc.function.domain = "ALL"
            calc.function.limit_domain(calc)
            calc.calculate_values()
        #Sets a limit to domain depending on user input
        elif i == 40:
            calc.val = "Domain:X"
            buttons[17].label = "   <"
            buttons[18].label = "   >"
        #Sets no limit to range
        elif i == 41:
            calc.function.range = "ALL"
            calc.function.limit_range(calc)
            calc.calculate_values()
        #Sets a limit to range depending on user input
        elif i == 42:
            calc.val = "Range:F(X)"
            buttons[17].label = "   <"
            buttons[18].label = "   >"
        #Moves position of "|" in input string one to the left
        elif i == 43 and calc.index != len(calc.val): calc.index += 1
        #Moves position of "|" in input string one to the right
        elif i == 44 and calc.index != 0: calc.index -= 1
        #Prepares user to input a value of x to find f(x)
        elif i == 45: calc.val = "Evaluate:F("
        
        calc.val = calc.val.replace(" ", "")
        if calc.val == "": calc.val = "0"
        calc.val = calc.val.replace("|", "")
                
#Parses through a string to break it into pieces that the evaluate() function will understand
def parse(calc, expr):
    
    #Replaces terms in expression to terms that parse() can recognise
    expr = expr.replace("--", "")
    expr = expr.replace("•", "x")
    expr = expr.replace("sin`¹", "1xf")
    expr = expr.replace("cos`¹", "1xg")
    expr = expr.replace("tan`¹", "1xh")
    expr = expr.replace("sin", "1xs")
    expr = expr.replace("cos", "1xc")
    expr = expr.replace("tan", "1xt")
    expr = expr.replace("log", "1xl")
    expr = expr.replace("EE+", "x10^")
    expr = expr.replace("!", "!1")
    expr = expr.replace("MEM", calc.mem)
    expr = expr.replace("π", str(PI))
    expr = expr.replace("e", str(EULER))
    expr = (expr + " ")

    #Checks if there are brackets in the expression, and if so, makes a recursive call to evaluate it 
    while "(" in expr:
        start = 0
        end = 0
        new_expr = ""
        new_val = 0
        i = 0
        done = False
        while not done:
            if expr[i] == "(":
                start = i+1
            if expr[i] == ")":
                end = i
                new_expr = expr[start:end]
                new_val = parse(calc, new_expr)
                expr = expr.replace(("(" + new_expr + ")"), new_val)
                done = True
            i += 1

    #Breaks expression into operators and numerical values. If expression is invalid, return an Error.
    expr = expr.replace("--", "")
    values = []
    oper_list = []
    total = 0
    index = -1
    
    for i in range(len(expr)):
        try:
            if expr[i] == "s":
                oper_list.append("sin")
                index = i
            elif expr[i] == "c":
                oper_list.append("cos")
                index = i
            elif expr[i] == "t":
                oper_list.append("tan")
                index = i
            elif expr[i] == "f":
                oper_list.append("asin")
                index = i
            elif expr[i] == "g":
                oper_list.append("acos")
                index = i
            elif expr[i] == "h":
                oper_list.append("atan")
                index = i
            elif expr[i] == "l":
                oper_list.append("log")
                index = i
            else:
                float(expr[i])
        except ValueError:
            if expr[i] != "." and expr[i] != "-":
                try: num = float(expr[index+1:i])
                except ValueError: return ("ERROR 1: Input Error")
                values.append(num)
                index = i
            if expr[i] == "+": oper_list.append("+")
            elif expr[i] == "–": oper_list.append("-")
            elif expr[i] == "x": oper_list.append("x")
            elif expr[i] == "÷": oper_list.append("÷")
            elif expr[i] == "^": oper_list.append("^")
            elif expr[i] == "√": oper_list.append("√")
            elif expr[i] == "!": oper_list.append("!")
    done = False
    while not done:
        try: values, oper_list = evaluate(values, oper_list, calc) #Calls evaluate() to get answer
        except: return ("ERROR 2: Logic Error") #If answer is not valid, return an Error.
        if len(oper_list) == 0:
            done = True
            return str(values[0]) #If answer is valid, return answer
        
#Evaluates two lists: one of operators, and one of values
def evaluate(num, oper, calc):
    if len(oper) == 0:
        return (num, oper)
    
    num, oper = trig(num, oper, calc)
    num, oper = exponents(num, oper)
    num, oper = mul_div(num, oper)
    if len(oper) == 0:
        return (num, oper)

    #Evaluates the addition and subtraction operations
    i = 0
    total = num[0]
    done = False
    while not done:
        if oper[i] == "+": total = total + num[i+1]
        elif oper[i] == "-": total = total - num[i+1]
        i += 1
        if i >= len(oper): done = True
    num.clear()
    oper.clear()
    num.append(total)
    
    return (num, oper) #Returns answer

#Evaluates the trig operations from the evaluate() function
def trig(num, oper, calc):
    if len(oper) == 0:
        return (num, oper)
    i = 0
    again = True
    while again:
        if oper[i] == "sin":
            num[i] =  eval_trig("sin", num[i], calc)
            del oper[i]
            del oper[i-1]
            del num[i-1]
            i = 0
        elif oper[i] == "cos":
            num[i] =  eval_trig("cos", num[i], calc)
            del oper[i]
            del oper[i-1]
            del num[i-1]
            i = 0
        elif oper[i] == "tan":
            num[i] =  eval_trig("tan", num[i], calc)
            del oper[i]
            del oper[i-1]
            del num[i-1]
            i = 0
        elif oper[i] == "asin":
            num[i] =  eval_trig("asin", num[i], calc)
            del oper[i]
            del oper[i-1]
            del num[i-1]
            i = 0
        elif oper[i] == "acos":
            num[i] =  eval_trig("acos", num[i], calc)
            del oper[i]
            del oper[i-1]
            del num[i-1]
            i = 0
        elif oper[i] == "atan":
            num[i] =  eval_trig("atan", num[i], calc)
            del oper[i]
            del oper[i-1]
            del num[i-1]
        else: i += 1
        if "sin" not in oper and "cos" not in oper and "tan" not in oper and "asin" not in oper and "acos" not in oper and "atan" not in oper:
            again = False
    return (num, oper)

#Evaluates the exponential operations from the evaluate() function
def exponents(num, oper):
    if len(oper) == 0:
        return (num, oper)
    i = 0
    again = True
    while again:
        if oper[i] == "^":
            num[i] = num[i] ** num[i+1]
            del oper[i]
            del num[i+1]
            i = 0
        elif oper[i] == "√":
            num[i] =  num[i+1] ** (1/num[i])
            del oper[i]
            del num[i+1]
            i = 0
        elif oper[i] == "log":
            num[i] = math.log10(num[i])
            del oper[i]
            i = 0
        else:
            i += 1
        if "^" not in oper and "√" not in oper and "log" not in oper:
            again = False
    return (num, oper)

#Evaluates the multiplication and division operations from the evaluate() function
def mul_div(num, oper):
    if len(oper) == 0:
        return (num, oper)
    i = 0
    again = True
    while again:
        if oper[i] == "x":
            num[i] =  num[i] * num[i+1]
            del oper[i]
            del num[i+1]
            i = 0
        elif oper[i] == "÷":
            num[i] =  num[i] / num[i+1]
            del oper[i]
            del num[i+1]
            i = 0
        elif oper[i] == "!":
            num[i] = math.gamma(num[i] + 1)
            del oper[i]
            del num[i+1]
        else:
            i += 1
        
        if "x" not in oper and "÷" not in oper and "!" not in oper:
            again = False
    return (num, oper)

#Evaluates a trig ratio depending on whether it's in degrees, radians, or gradians
def eval_trig(ratio, value, calc):
    if ratio == "sin" or ratio == "cos" or ratio == "tan":
        if calc.mode == "DEG": value = math.radians(value)
        elif calc.mode == "GRAD": value = value * 0.015707963267949
        if ratio == "sin": value = math.sin(value)
        elif ratio == "cos": value = math.cos(value)
        elif ratio == "tan": value = math.tan(value)
        return value
    
    else:
        if ratio == "asin": value = math.asin(value)
        elif ratio == "acos": value = math.acos(value)
        elif ratio == "atan": value = math.atan(value)
        if calc.mode == "DEG": value = math.degrees(value)
        elif calc.mode == "GRAD": value = value * 63.66197723675814
        return value
    
#Renders and blits calculator display to the screen
def display(screen, calc, font, graph_pic):

    pygame.draw.rect(screen, SCREENCOLOUR, [50, 50, 300, 200])
    text = font.render(calc.val, False, GREEN)
    text2 = font.render(calc.ans_val, False, GREEN)
    text3 = font.render(calc.mode, False, GREEN)
    
    width_val = text.get_width()
    if width_val > 225: screen.blit(text, ((275 - width_val), 60))
    else: screen.blit(text, (53, 60))
    
    width_ans = text2.get_width()
    if width_ans > 225: screen.blit(text2, ((275 - width_ans), 85))
    else: screen.blit(text2, (53, 85))
    
    screen.blit(text3, (220, 133))

    if calc.mem != "":
        mem = font.render("MEM", False, GREEN)
        screen.blit(mem, (50, 133))

    #If grid is true, blits the grid picture to the screen, and the function graph to go with it
    if calc.grid:
        screen.blit(graph_pic, (325, 0))
        calc.function.draw_graph(screen)
        
        scale = font.render((str(calc.function.scale/2)), False, BLACK)
        neg_scale = font.render((str(calc.function.scale/2*-1)), False, BLACK)
        screen.blit(scale, (685, 255))
        screen.blit(neg_scale, (435, 255))
        screen.blit(scale, (580, 115))
        screen.blit(neg_scale, (575, 365))

        #If options is true, blits options list to screen
        if calc.function.options:
            text = ["Evaluate F(X):", "Domain:", "Range:", "Colour:"]
            
            pygame.draw.rect(screen, WHITE, [0, 500, 825, 100])
            pygame.draw.line(screen, BLACK, [0, 500], [825, 500], 5)
            
            for i in range(len(text)):
                surface = font.render(text[i], False, BLACK)
                screen.blit(surface, ((180*i + 60), 550))

            if calc.function.x != "NONE":
                surface = font.render(("F" + str(calc.function.x) + "=" + str(float(round(calc.function.f_of_x, 5)))), False, BLACK)
                screen.blit(surface, (65, 575))
                
            domain = font.render(calc.function.domain, False, BLACK)
            range_y = font.render(calc.function.range, False, BLACK)
            screen.blit(domain, (245, 575))
            screen.blit(range_y, (430, 575))

            bold_font = pygame.font.SysFont("Andulus", 35, True, False)
            surface = bold_font.render(("Function: " + calc.function.function), False, RED)
            function_width = surface.get_width()
            screen.blit(surface, ((825/2-function_width/2), 510))
            
            k = 0
            for i in range(545, 605, 30):
                for j in range(675, 805, 30):
                    pygame.draw.rect(screen, calc.function.colours[k], [j, i, 20, 20])
                    rect = pygame.Rect(j, i, 20, 20)
                    k += 1
                    
#Draws all buttons and determines if the mouse is rolled over them
def draw_buttons(buttons, calc_screen, pics, pos):
    pointer_rect = pygame.Rect(pos[0], pos[1], 1, 1)
        
    for i in range(len(buttons)):
        buttons[i].draw_button(calc_screen)
        if buttons[i].rect.colliderect(pointer_rect):
            buttons[i].pressed = True
            if i <= 18 or i == 37 or i == 38: buttons[i].pic = pics[1]
            elif i >= 19 and i <= 28 or i >= 39 and i <= 42 or i == 45: buttons[i].pic = pics[3]
            elif i >= 29 and i <= 33: buttons[i].pic = pics[5]
            elif i == 34: buttons[i].pic = pics[7]
            elif i == 35: buttons[i].pic = pics[9]
            elif i == 36: buttons[i].pic = pics[11]
            elif i >= 43: buttons[i].pic = pics[13]
        else:
            buttons[i].pressed = False
            if i <= 18 or i == 37 or i == 38: buttons[i].pic = pics[0]
            elif i >= 19 and i <= 28 or i >= 39 and i <= 42 or i == 45: buttons[i].pic = pics[2]
            elif i >= 29 and i <= 33: buttons[i].pic = pics[4]
            elif i == 34: buttons[i].pic = pics[6]
            elif i == 35: buttons[i].pic = pics[8]
            elif i == 36: buttons[i].pic = pics[10]
            elif i >= 43: buttons[i].pic = pics[12]
            
#Main function
def main():
    #Initialize python and other important features of pygame
    pygame.init()

    #Gets the window and icon ready
    size = (325, 500)
    calc_screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Graphing Calculator")
    icon = pygame.image.load("Pics/icon.png")
    icon.set_colorkey(WHITE)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    
    #Loads pictures and fonts
    calc_pic = pygame.image.load("Pics/Calculator.png").convert()
    calc_pic = pygame.transform.scale(calc_pic, size)
    calc_pic.set_colorkey(RED)
    graph_pic = pygame.image.load("Pics/grid.png").convert()
    pointer = pygame.image.load("Pics/mouse.png").convert()
    pointer.set_colorkey(BLACK)
    pointer = pygame.transform.scale(pointer, (12, 20))
    pointer_rect = pointer.get_rect()
    calc_font = pygame.font.SysFont("Andulus", 27, False, False)
    
    #Puts pictures of buttons into a list
    button_pics = []
    for i in range(14):
        button = pygame.image.load("Buttons/Button" + str(i) + ".png").convert()
        button.set_colorkey(WHITE)
        if i == 0 or i == 1 or i == 6 or i == 7:
            button = pygame.transform.scale(button, (50, 50))
        elif i == 4 or i == 5:
            button = pygame.transform.scale(button, (50, 30))
        elif i == 2 or i == 3:
            button = pygame.transform.scale(button, (40, 30))
        elif i == 8 or i == 9 or i == 10 or i == 11:
            button = pygame.transform.scale(button, (30, 30))
        elif i == 12 or i == 13:
            button = pygame.transform.scale(button, (20, 40))
        button_pics.append(button)

    #Creates all button (objects of Button class), assigns them a label and picture, and adds them to a list
    buttons = []
    for i in range(46):
        button = Button()
        if i <= 9: button.label = ("   " + str(9 - i))
        elif i == 10: button.label = "   ."
        elif i == 11: button.label = "  (-)"
        elif i == 12: button.label = "   ="
        elif i == 13: button.label = "   +"
        elif i == 14: button.label = "   –"
        elif i == 15: button.label = "   x"
        elif i == 16: button.label = "   ÷"
        elif i == 17: button.label = "   ("
        elif i == 18: button.label = "   )"
        elif i == 19: button.label = "  sin"
        elif i == 20: button.label = "  cos"
        elif i == 21: button.label = "  tan"
        elif i == 22: button.label = "    π"
        elif i == 23: button.label = "  a^b"
        elif i == 24: button.label = "   a²"
        elif i == 25: button.label = "   √"
        elif i == 26: button.label = "   b√"
        elif i == 27: button.label = "  log"
        elif i == 28: button.label = "  exp"
        elif i == 29: button.label = "  CLR"
        elif i == 30: button.label = "   DEL"
        elif i == 31: button.label = " memR"
        elif i == 32: button.label = " MOD"
        elif i == 33: button.label = "  2ndF"
        elif i == 34: button.label = "  f(x)"
        elif i == 37: button.label = "   +"
        elif i == 38: button.label = "   -"
        elif i == 39 or i == 41: button.label = " ALL"
        elif i == 40 or i == 42: button.label = " LIM"
        elif i == 43: button.label = " ◄"
        elif i == 44: button.label = " ►"
        elif i == 45: button.label = "  EVAL"
        
        if i <= 18 or i == 37 or i == 38: button.pic = button_pics[0]
        elif i >= 19 and i <= 28 or i >= 39 and i <= 42 or i == 45: button.pic = button_pics[4]
        elif i >= 29 and i <= 33: button.pic = button_pics[2]
        elif i == 34: button.pic = button_pics[6]
        elif i == 35: button.pic = button_pics[8]
        elif i == 36: button.pic = button_pics[10]
        elif i >= 43: button.pic = button_pics[12]
                    
        buttons.append(button)

    #Sets where each button should appear on the screen, and what font their label will be
    counter = 0
    for i in range(275, 475, 50):
        for j in range(35, 185, 50):
            buttons[counter].rect = pygame.Rect(j, i, 50, 50)
            counter += 1
    buttons[counter].rect = pygame.Rect(185, 425, 50, 50)
    counter += 1
    for i in range(275, 425, 50):
        for j in range(185, 285, 50):
            buttons[counter].rect = pygame.Rect(j, i, 50, 50)
            counter += 1
    for i in range(215, 275, 30):
        for j in range(40, 280, 50):
            buttons[counter].rect = pygame.Rect(j, i, 40, 30)
            buttons[counter].font = pygame.font.SysFont("Times New Roman", 15, False, False)
            counter += 1
    for i in range(35, 285, 50):
        buttons[counter].rect = pygame.Rect(i, 185, 50, 30)
        buttons[counter].font = pygame.font.SysFont("Times New Roman", 15, True, False)
        counter += 1
    
    buttons[34].rect = pygame.Rect(235, 425, 50, 50)
    buttons[35].rect = pygame.Rect(788, 463, 30, 30)
    buttons[36].rect = pygame.Rect(788, 12, 30, 30)
    buttons[37].rect = pygame.Rect(3, 493, 50, 50)
    buttons[38].rect = pygame.Rect(3, 543, 50, 50)
    buttons[39].rect = pygame.Rect(315, 545, 40, 30)
    buttons[40].rect = pygame.Rect(355, 545, 40, 30)
    buttons[41].rect = pygame.Rect(485, 545, 40, 30)
    buttons[42].rect = pygame.Rect(525, 545, 40, 30)
    buttons[43].rect = pygame.Rect(19, 75, 20, 40)
    buttons[44].rect = pygame.Rect(279, 75, 20, 40)
    buttons[45].rect = pygame.Rect(185, 545, 40, 30)

    buttons[34].font = pygame.font.SysFont("Times New Roman", 23, False, True)
    buttons[45].font = pygame.font.SysFont("Times New Roman", 13, True, False)
    for i in range(39, 45):
        buttons[i].font = pygame.font.SysFont("Times New Roman", 15, True, False)

    #Creates calculator object to store a bunch of varibles in an organised way
    calc = Calculator()
    
    done = False
    shift = False

    #Main event loop
    while not done:
        #Event checking for keyboard input, clicks, and mouse scrolling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    shift = True
            elif event.type == pygame.KEYUP:
                calc.ans_val = ""
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    shift = False
                elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    if event.key == pygame.K_0 and shift:
                        buttons[18].logic(calc, 18, buttons)
                    else:
                        buttons[9].logic(calc, 9, buttons)
                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    buttons[8].logic(calc, 8, buttons)
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    buttons[7].logic(calc, 7, buttons)
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    buttons[6].logic(calc, 6, buttons)
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    buttons[5].logic(calc, 5, buttons)
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    buttons[4].logic(calc, 4, buttons)
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    if event.key == pygame.K_6 and shift:
                        buttons[23].logic(calc, 23, buttons)
                    else:
                        buttons[3].logic(calc, 3, buttons)
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    buttons[2].logic(calc, 2, buttons)
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    buttons[1].logic(calc, 1, buttons)
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    if event.key == pygame.K_9 and shift:
                        buttons[17].logic(calc, 17, buttons)
                    else:
                        buttons[0].logic(calc, 0, buttons)
                elif event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                    buttons[10].logic(calc, 10, buttons)
                elif event.key == pygame.K_DELETE:
                    buttons[29].logic(calc, 29, buttons)
                elif event.key == pygame.K_BACKSPACE:
                    buttons[30].logic(calc, 30, buttons)
                elif event.key == pygame.K_MINUS:
                    buttons[14].logic(calc, 14, buttons)
                elif event.key == pygame.K_SPACE:
                    calc.change_mode()
                elif event.key == pygame.K_x:
                    buttons[15].logic(calc, 15, buttons)
                elif event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                    buttons[16].logic(calc, 16, buttons)
                elif event.key == pygame.K_p:
                    buttons[22].logic(calc, 22, buttons)
                elif event.key == pygame.K_r:
                    buttons[26].logic(calc, 26, buttons)
                elif event.key == pygame.K_s:
                    buttons[19].logic(calc, 20, buttons)
                elif event.key == pygame.K_c:
                    buttons[20].logic(calc, 21, buttons)
                elif event.key == pygame.K_t:
                    buttons[21].logic(calc, 22, buttons)
                elif event.key == pygame.K_f:
                    buttons[34].logic(calc, 34, buttons)
                elif event.key == pygame.K_m:
                    buttons[31].logic(calc, 31, buttons)
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    buttons[33].logic(calc, 33, buttons)
                elif event.key == pygame.K_LEFT:
                    buttons[43].logic(calc, 43, buttons)
                elif event.key == pygame.K_RIGHT:
                    buttons[44].logic(calc, 44, buttons)
                elif event.key == pygame.K_n:
                    buttons[11].logic(calc, 11, buttons)
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    if event.key == pygame.K_EQUALS and shift:
                        buttons[13].logic(calc, 13, buttons)
                    else:
                        buttons[12].logic(calc, 12, buttons)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    buttons[37].logic(calc, 37, buttons)
                if event.button == 5:
                    buttons[37].logic(calc, 38, buttons)
            elif event.type == pygame.MOUSEBUTTONUP:
                for i in range(len(buttons)):
                    if buttons[i].pressed:
                        if i >= 31 and i <= 33: pass
                        else: calc.ans_val = ""
                        buttons[i].logic(calc, i, buttons)
                        
                if calc.function.options:
                    pointer_rect = pygame.Rect(pos[0], pos[1], 1, 1)
                    calc.function.change_colour(pointer_rect)

        pygame.mouse.set_visible(False)
        
        pos = pygame.mouse.get_pos()

        elapsed_time = time.time() - STARTTIME

        if int(elapsed_time) % 2:
            if "|" not in calc.val:
                calc.val = calc.val.replace(" ", "")
                calc.add_character("|")
        else:
            if " " not in calc.val:
                calc.val = calc.val.replace("|", "")
                calc.add_character(" ")
                
        if "Domain" in calc.val or "Range" in calc.val:
            buttons[17].label = "   <"
            buttons[18].label = "   >"
        else:
            buttons[17].label = "   ("
            buttons[18].label = "   )"
        
        #DRAW EVERYTHING!
        calc_screen.fill(WHITE)
        
        display(calc_screen, calc, calc_fnt, graph_pic)
        
        calc_screen.blit(calc_pic, (0,0))
        
        draw_buttons(buttons, calc_screen, button_pics, pos)
        
        if pygame.mouse.get_focused() == 1: calc_screen.blit(pointer, pos)
        
        #Flip the screen
        pygame.display.flip()
        
        clock.tick(60)

    #Quits program
    pygame.quit()

#Calls main function
if __name__ == "__main__":
    main()
