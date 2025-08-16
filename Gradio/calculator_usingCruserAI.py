import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")
        
        # Calculator variables
        self.current_number = ""
        self.first_number = 0
        self.operation = ""
        self.should_reset = False
        
        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Bind keyboard events
        self.bind_keyboard_events()
        
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#2C3E50", height=150)
        display_frame.pack(fill="x", padx=10, pady=10)
        display_frame.pack_propagate(False)
        
        # Display label
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 32, "bold"),
            bg="#34495E",
            fg="white",
            anchor="e",
            padx=20,
            pady=20
        )
        self.display.pack(fill="both", expand=True)
        
    def create_buttons(self):
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2C3E50")
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Button configuration
        button_config = {
            'font': ('Arial', 16, 'bold'),
            'width': 8,
            'height': 3,
            'bd': 0,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        
        # Button definitions
        buttons = [
            ('C', '#E74C3C', self.clear),
            ('±', '#95A5A6', self.negate),
            ('%', '#95A5A6', self.percentage),
            ('÷', '#F39C12', lambda: self.set_operation('÷')),
            
            ('7', '#34495E', lambda: self.add_number('7')),
            ('8', '#34495E', lambda: self.add_number('8')),
            ('9', '#34495E', lambda: self.add_number('9')),
            ('×', '#F39C12', lambda: self.set_operation('×')),
            
            ('4', '#34495E', lambda: self.add_number('4')),
            ('5', '#34495E', lambda: self.add_number('5')),
            ('6', '#34495E', lambda: self.add_number('6')),
            ('-', '#F39C12', lambda: self.set_operation('-')),
            
            ('1', '#34495E', lambda: self.add_number('1')),
            ('2', '#34495E', lambda: self.add_number('2')),
            ('3', '#34495E', lambda: self.add_number('3')),
            ('+', '#F39C12', lambda: self.set_operation('+')),
            
            ('0', '#34495E', lambda: self.add_number('0'), 16),
            ('.', '#34495E', lambda: self.add_decimal()),
            ('=', '#27AE60', self.calculate, 8)
        ]
        
        # Create buttons
        row = 0
        col = 0
        for button_info in buttons:
            if len(button_info) == 4:  # Button with custom width
                text, color, command, width = button_info
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    bg=color,
                    fg="white",
                    command=command,
                    width=width,
                    height=3,
                    font=('Arial', 16, 'bold'),
                    bd=0,
                    relief='flat',
                    cursor='hand2'
                )
            else:
                text, color, command = button_info
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    bg=color,
                    fg="white",
                    command=command,
                    **button_config
                )
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def add_number(self, number):
        if self.should_reset:
            self.current_number = ""
            self.should_reset = False
        
        if number == '0' and self.current_number == "":
            return
        
        self.current_number += number
        self.update_display()
    
    def add_decimal(self):
        if self.should_reset:
            self.current_number = "0"
            self.should_reset = False
        
        if '.' not in self.current_number:
            if self.current_number == "":
                self.current_number = "0"
            self.current_number += "."
            self.update_display()
    
    def clear(self):
        self.current_number = ""
        self.first_number = 0
        self.operation = ""
        self.should_reset = False
        self.display_var.set("0")
    
    def negate(self):
        if self.current_number:
            if self.current_number.startswith('-'):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.update_display()
    
    def percentage(self):
        if self.current_number:
            try:
                value = float(self.current_number)
                value = value / 100
                self.current_number = str(value)
                self.update_display()
            except ValueError:
                pass
    
    def set_operation(self, op):
        if self.current_number:
            try:
                self.first_number = float(self.current_number)
                self.operation = op
                self.should_reset = True
            except ValueError:
                pass
        elif self.operation and not self.should_reset:
            # Change operation
            self.operation = op
    
    def calculate(self):
        if self.current_number and self.operation:
            try:
                second_number = float(self.current_number)
                result = 0
                
                if self.operation == '+':
                    result = self.first_number + second_number
                elif self.operation == '-':
                    result = self.first_number - second_number
                elif self.operation == '×':
                    result = self.first_number * second_number
                elif self.operation == '÷':
                    if second_number == 0:
                        self.display_var.set("Error")
                        return
                    result = self.first_number / second_number
                
                # Format result
                if result.is_integer():
                    result = int(result)
                
                self.current_number = str(result)
                self.operation = ""
                self.should_reset = True
                self.update_display()
                
            except ValueError:
                self.display_var.set("Error")
    
    def update_display(self):
        if self.current_number == "":
            self.display_var.set("0")
        else:
            # Limit display length
            display_text = self.current_number
            if len(display_text) > 12:
                try:
                    # Try to format as scientific notation for large numbers
                    value = float(display_text)
                    if abs(value) >= 1e12 or (abs(value) < 1e-12 and value != 0):
                        display_text = f"{value:.2e}"
                    else:
                        display_text = f"{value:.10g}"
                except ValueError:
                    display_text = display_text[:12]
            
            self.display_var.set(display_text)
    
    def bind_keyboard_events(self):
        """Bind keyboard events to calculator functions"""
        self.root.bind('<Key>', self.handle_keyboard)
        self.root.focus_set()  # Set focus to the window
    
    def handle_keyboard(self, event):
        """Handle keyboard input"""
        key = event.char.lower()
        keysym = event.keysym
        
        # Number keys (0-9)
        if key in '0123456789':
            self.add_number(key)
        
        # Decimal point
        elif key == '.':
            self.add_decimal()
        
        # Operators
        elif key == '+':
            self.set_operation('+')
        elif key == '-':
            self.set_operation('-')
        elif key == '*':
            self.set_operation('×')
        elif key == '/':
            self.set_operation('÷')
        
        # Enter key for calculation
        elif keysym in ['Return', 'KP_Enter']:
            self.calculate()
        
        # Escape key for clear
        elif keysym == 'Escape':
            self.clear()
        
        # Backspace for deleting last character
        elif keysym == 'BackSpace':
            self.backspace()
        
        # Percentage
        elif key == '%':
            self.percentage()
        
        # Negate with N key
        elif key == 'n':
            self.negate()
        
        # Prevent default behavior for these keys
        if key in '0123456789.+-*/%n' or keysym in ['Return', 'KP_Enter', 'Escape', 'BackSpace']:
            return 'break'
    
    def backspace(self):
        """Delete the last character from current number"""
        if self.current_number:
            self.current_number = self.current_number[:-1]
            self.update_display()

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()