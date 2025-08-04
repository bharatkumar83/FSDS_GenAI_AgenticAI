import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        
        # Game constants
        self.WIDTH = 600
        self.HEIGHT = 600
        self.GRID_SIZE = 20
        self.GAME_SPEED = 150
        
        # Colors
        self.BG_COLOR = "#2C3E50"
        self.SNAKE_COLOR = "#27AE60"
        self.FOOD_COLOR = "#E74C3C"
        self.GRID_COLOR = "#34495E"
        
        # Game variables
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_running = True
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg=self.BG_COLOR)
        self.canvas.pack()
        
        # Create score label
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16), bg=self.BG_COLOR, fg="white")
        self.score_label.pack()
        
        # Bind keys
        self.root.bind("<KeyPress>", self.change_direction)
        self.root.focus_set()
        
        # Start game
        self.update()
    
    def create_food(self):
        while True:
            x = random.randint(0, self.GRID_SIZE - 1)
            y = random.randint(0, self.GRID_SIZE - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def change_direction(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif key == "r" or key == "R":
            self.restart_game()
    
    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 1)
        elif self.direction == "Left":
            new_head = (head[0] - 1, head[1])
        else:  # Right
            new_head = (head[0] + 1, head[1])
        
        # Check collision with walls
        if (new_head[0] < 0 or new_head[0] >= self.GRID_SIZE or 
            new_head[1] < 0 or new_head[1] >= self.GRID_SIZE):
            self.game_over()
            return
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over()
            return
        
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
        else:
            self.snake.pop()
    
    def draw(self):
        self.canvas.delete("all")
        
        # Draw grid
        for i in range(self.GRID_SIZE + 1):
            x = i * (self.WIDTH // self.GRID_SIZE)
            y = i * (self.HEIGHT // self.GRID_SIZE)
            self.canvas.create_line(x, 0, x, self.HEIGHT, fill=self.GRID_COLOR, width=1)
            self.canvas.create_line(0, y, self.WIDTH, y, fill=self.GRID_COLOR, width=1)
        
        # Draw snake
        for segment in self.snake:
            x, y = segment
            x1 = x * (self.WIDTH // self.GRID_SIZE)
            y1 = y * (self.HEIGHT // self.GRID_SIZE)
            x2 = x1 + (self.WIDTH // self.GRID_SIZE)
            y2 = y1 + (self.HEIGHT // self.GRID_SIZE)
            
            # Make head slightly different
            if segment == self.snake[0]:
                self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill=self.SNAKE_COLOR, outline="white", width=2)
                # Add eyes
                eye_size = 3
                self.canvas.create_oval(x1+5, y1+5, x1+5+eye_size, y1+5+eye_size, fill="black")
                self.canvas.create_oval(x2-8, y1+5, x2-8+eye_size, y1+5+eye_size, fill="black")
            else:
                self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, fill=self.SNAKE_COLOR, outline="")
        
        # Draw food
        x, y = self.food
        x1 = x * (self.WIDTH // self.GRID_SIZE)
        y1 = y * (self.HEIGHT // self.GRID_SIZE)
        x2 = x1 + (self.WIDTH // self.GRID_SIZE)
        y2 = y1 + (self.HEIGHT // self.GRID_SIZE)
        
        # Draw apple with shine
        self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill=self.FOOD_COLOR, outline="")
        self.canvas.create_oval(x1+4, y1+4, x1+8, y1+8, fill="#FF6B6B", outline="")
    
    def game_over(self):
        self.game_running = False
        self.canvas.create_text(
            self.WIDTH // 2, 
            self.HEIGHT // 2 - 30, 
            text="GAME OVER!", 
            fill="white", 
            font=("Arial", 24, "bold")
        )
        self.canvas.create_text(
            self.WIDTH // 2, 
            self.HEIGHT // 2 + 10, 
            text=f"Final Score: {self.score}", 
            fill="white", 
            font=("Arial", 16)
        )
        self.canvas.create_text(
            self.WIDTH // 2, 
            self.HEIGHT // 2 + 50, 
            text="Press 'R' to restart", 
            fill="white", 
            font=("Arial", 12)
        )
    
    def restart_game(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.game_running = True
        self.update()
    
    def update(self):
        if self.game_running:
            self.move_snake()
            self.draw()
            self.root.after(self.GAME_SPEED, self.update)

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    
    # Add instructions
    instructions = tk.Label(
        root, 
        text="Use Arrow Keys to move | Press 'R' to restart", 
        font=("Arial", 10), 
        bg=game.BG_COLOR, 
        fg="white"
    )
    instructions.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main() 