from tkinter import Button, Label
import random
import settings, utils
import sys, os



class Cell:

    all = []

    cell_count_label_object = None 

    cell_message_label_object = None 

    cell_count = settings.CELL_COUNT

    flag_count = settings.MINES_COUNT

    reset_button = None

    exit_button = None

    trigger = 0

    def __init__(self, x, y, is_mine =False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_flagged = False
        self.cell_button_object = None
        self.x = x
        self.y = y
        Cell.all.append(self)

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location, 
            text = f'Flags Left: \n {Cell.flag_count}', 
            width = 12, 
            height = 4, 
            bg = 'black', 
            fg = 'white', 
            font = ("", 25)
        )
        Cell.cell_count_label_object = lbl

    @staticmethod
    def create_message_label(location):
        lbl = Label(
            location, 
            text = 'Left Click: Dig\nRight Click: Place Flag', 
            # width = 12, 
            # height = 4, 
            bg = 'black', 
            fg = 'white', 
            font = ("", 25)
        )
        Cell.cell_message_label_object = lbl


    @staticmethod
    def create_exit_button(location):
        btn = Button(
            location, 
            width = 12,
            height = 4,
            text = "Exit Game"
        )

        Cell.exit_button = btn
    

    @staticmethod
    def create_reset_button(location):
        btn = Button(
            location, 
            width = 12,
            height = 4,
            text = "Reset Game"
        )

        Cell.reset_button = btn


    def create_button_object(self, location):
        btn = Button(
            location, 
            width = 12,
            height = 4,
            text = ""
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)

        self.cell_button_object = btn 
        

    def left_click_actions(self, event):
        if not self.is_flagged:
            if self.is_mine:
                self.show_mine()
            else:
                if not self.is_opened:
                    self.show_cell()
                    if self.count_neighbor_mines == 0:
                        for c in self.cell_neighbors:
                            if not c.is_opened:
                                c.left_click_actions(event)
            
                                

    def get_cell_by_axis(self, x, y):
        for c in Cell.all:
            if c.x == x and c.y == y:
                return c
            
    @property        
    def cell_neighbors(self):
        neighbors = [
            self.get_cell_by_axis(self.x -1, self.y -1),
            self.get_cell_by_axis(self.x -1, self.y ),
            self.get_cell_by_axis(self.x -1, self.y +1),
            self.get_cell_by_axis(self.x , self.y -1),
            self.get_cell_by_axis(self.x , self.y +1),
            self.get_cell_by_axis(self.x +1, self.y -1),
            self.get_cell_by_axis(self.x +1, self.y ),
            self.get_cell_by_axis(self.x +1, self.y +1),
        ] 

        neighbors = [cell for cell in neighbors if cell is not None]
        return neighbors

    @property
    def count_neighbor_mines(self):
        count = 0
        for cell in self.cell_neighbors:
            if cell.is_mine == True:
                count += 1
        return count


    def show_cell(self):
        self.cell_button_object.configure(text =f'{self.count_neighbor_mines}')
        self.is_opened = True
        Cell.cell_count -= 1
        if Cell.cell_count == settings.MINES_COUNT:
            for c in Cell.all:
                c.cell_button_object.configure(bg = 'green', text = '')
            if Cell.cell_message_label_object:
                Cell.cell_message_label_object.configure(text = 'YOU WIN!!!')
            Cell.game_over()
        
        


    def show_mine(self):
        #you lose 
        for c in Cell.all:
            c.cell_button_object.configure(bg = 'red', text = '')
        if Cell.cell_message_label_object:
            Cell.cell_message_label_object.configure(text = 'YOU LOSE')
        Cell.game_over()
        

    def right_click_actions(self, event):
        if not self.is_opened:
            if not self.is_flagged:
                self.cell_button_object.configure(bg = 'blue')
                self.is_flagged = True
                Cell.flag_count -= 1
                if Cell.cell_count_label_object:
                    Cell.cell_count_label_object.configure(
                    text = f'Flags Left:\n {Cell.flag_count}'
                )
                
            else:
                self.cell_button_object.configure(bg = '#d9d9d9')
                self.is_flagged = False
                Cell.flag_count += 1
                if Cell.cell_count_label_object:
                    Cell.cell_count_label_object.configure(
                    text = f'Flags Left:\n {Cell.flag_count}'
                    )

        

    @staticmethod
    def reset(event):
        for c in Cell.all:
            c.cell_button_object.configure(bg = '#d9d9d9', text = '')
            c.is_mine = False
            c.is_opened = False
            c.is_flagged = False
        Cell.randomize_mines() 
        Cell.cell_count = settings.CELL_COUNT
        Cell.flag_count = settings.MINES_COUNT
        Cell.trigger = 2


    @staticmethod
    def randomize_mines():
        mines = random.sample(Cell.all, settings.MINES_COUNT)
        for m in mines:
            m.is_mine = True 
        



    @staticmethod
    def game_over():
        Cell.cell_count_label_object.place_forget()
        for c in Cell.all:
            c.is_flagged = True
        Cell.trigger = 1
         






        #