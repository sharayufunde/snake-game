from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
FONT_COLOR = "#FFFFFF"

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.canvas = canvas

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        max_x = (GAME_WIDTH // SPACE_SIZE) - 1
        max_y = (GAME_HEIGHT // SPACE_SIZE) - 1
        
        x = random.randint(0, max_x) * SPACE_SIZE
        y = random.randint(0, max_y) * SPACE_SIZE

        self.coordinates = [x, y]
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

class SnakeGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Snake Game")
        self.window.resizable(False, False)
        
        # Score label
        self.score = 0
        self.label = Label(self.window, text=f"Score: {self.score}", font=('consolas', 20), fg=FONT_COLOR, bg=BACKGROUND_COLOR)
        self.label.pack()
        
        # Canvas for game
        self.canvas = Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()
        
        # Position window in center of screen
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Game state variables
        self.direction = 'down'
        self.game_active = False
        self.after_id = None
        
        # Show start screen
        self.show_start_screen()
        
        # Bind keys
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))
        
    def show_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 - 50, 
                              text="SNAKE GAME", font=('consolas', 50), fill=FONT_COLOR, tag="start")
        self.canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 + 20, 
                              text="Use Arrow Keys to Move", font=('consolas', 20), fill=FONT_COLOR, tag="start")
        self.canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 + 60, 
                              text="Press SPACE to Start", font=('consolas', 20), fill=FONT_COLOR, tag="start")
        
        # Bind space to start game
        self.window.bind('<space>', self.start_game)
        
    def start_game(self, event=None):
        # Unbind space key to prevent multiple starts
        self.window.unbind('<space>')
        
        # Reset game state
        self.canvas.delete("all")
        self.score = 0
        self.label.config(text=f"Score: {self.score}")
        self.direction = 'down'
        self.game_active = True
        
        # Create snake and food
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        
        # Start game loop
        self.next_turn()
        
    def next_turn(self):
        if not self.game_active:
            return
            
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.after_id = self.window.after(SPEED, self.next_turn)
        
    def change_direction(self, new_direction):
        if not self.game_active:
            return
            
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake.coordinates[0]

        # Check wall collisions
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        # Check self collisions
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        self.game_active = False
        if self.after_id:
            self.window.after_cancel(self.after_id)
            self.after_id = None
            
        self.canvas.delete("all")
        self.canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 - 50, 
                              font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
        self.canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 + 50, 
                              font=('consolas', 20), text=f"Final Score: {self.score}", fill=FONT_COLOR, tag="gameover")
        self.canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 + 100, 
                              font=('consolas', 20), text="Press SPACE to Play Again", fill=FONT_COLOR, tag="gameover")
        
        # Bind space to restart game
        self.window.bind('<space>', self.start_game)
        
    def run(self):
        self.window.mainloop()

# Create and run the game
if __name__ == "__main__":
    window = Tk()
    game = SnakeGame(window)
    game.run()