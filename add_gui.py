import tkinter as tk
import random

class Checkergame:
    def __init__(self, master):
        self.master = master
        self.master.title("เกมหมากฮอส")

        self.turn = random.choice(['red', 'blue'])
        self.turn_count = 1
        self.red_captured = 0
        self.blue_captured = 0

        self.canvas = tk.Canvas(self.master, width=640, height=640)
        self.canvas.pack(side=tk.LEFT)

        self.size = 80
        self.selected_piece = None
        self.selected_pos = None
        self.pieces = []

        self.create_board()
        self.place_pieces()
        self.canvas.bind("<Button-1>", self.on_click)

        self.captured_canvas = tk.Canvas(self.master, width=120, height=320)
        self.captured_canvas.pack(side=tk.LEFT, padx=(0, 5))
        self.captured_canvas.pack_propagate(False)

        self.turn_label = tk.Label(self.master, text=self.get_turn_message(), font=('Arial', 16))
        self.turn_label.pack(side=tk.BOTTOM)

    def create_board(self):
        colors = ['#ffffff', '#000000']

        for row in range(8):
            for col in range(8):
                x0 = col * self.size
                y0 = row * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def place_pieces(self):
        count_red = 0
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 0 and count_red < 8:
                    piece = self.canvas.create_oval(col * self.size + 10, row * self.size + 10,
                                                     col * self.size + self.size - 10, row * self.size + self.size - 10,
                                                     fill='red')
                    self.pieces.append((piece, row, col))
                    count_red += 1

        count_blue = 0
        for row in range(6, 8):
            for col in range(8):
                if (row + col) % 2 == 0 and count_blue < 8:
                    piece = self.canvas.create_oval(col * self.size + 10, row * self.size + 10,
                                                     col * self.size + self.size - 10, row * self.size + self.size - 10,
                                                     fill='blue')
                    self.pieces.append((piece, row, col))
                    count_blue += 1

    def on_click(self, event):
        col = event.x // self.size
        row = event.y // self.size
        
        if self.selected_piece is None:
            for piece, r, c in self.pieces:
                if r == row and c == col:
                    if self.canvas.itemcget(piece, 'fill') == self.turn:
                        self.selected_piece = piece
                        self.selected_pos = (row, col)
                        break
        else:
            if self.is_valid_move(self.selected_pos, (row, col)):
                self.move_piece(self.selected_piece, (row, col))
                self.turn = 'red' if self.turn == 'blue' else 'blue'
                self.turn_count += 1
                self.turn_label.config(text=self.get_turn_message())
            self.selected_piece = None

    def get_turn_message(self):
        return f"ฝ่ายที่เล่น: {self.turn.capitalize()} (เทิร์นที่ {self.turn_count})"

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1:
            if (from_row < to_row and self.canvas.itemcget(self.selected_piece, 'fill') == 'red') or \
               (from_row > to_row and self.canvas.itemcget(self.selected_piece, 'fill') == 'blue'):
                if not self.is_space_occupied(to_row, to_col):
                    return True
                else:
                    return False

        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            middle_row = (from_row + to_row) // 2
            middle_col = (from_col + to_col) // 2

            for piece, r, c in self.pieces:
                if r == middle_row and c == middle_col:
                    if self.canvas.itemcget(piece, 'fill') != self.canvas.itemcget(self.selected_piece, 'fill'):
                        if not self.is_space_occupied(to_row, to_col):
                            return True
        return False

    def is_space_occupied(self, row, col):
        for piece, r, c in self.pieces:
            if r == row and c == col:
                return True
        return False

    def move_piece(self, piece, to_pos):
        from_row, from_col = self.selected_pos
        to_row, to_col = to_pos

        self.canvas.coords(piece, 
                           to_col * self.size + 10, to_row * self.size + 10, 
                           to_col * self.size + self.size - 10, to_row * self.size + self.size - 10)
        
        self.pieces = [(piece, to_row, to_col) if p == (piece, from_row, from_col) else p for p in self.pieces]

        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            middle_row = (from_row + to_row) // 2
            middle_col = (from_col + to_col) // 2
            for i, (p, r, c) in enumerate(self.pieces):
                if r == middle_row and c == middle_col:
                    self.canvas.delete(p)
                    del self.pieces[i]
                    if self.canvas.itemcget(piece, 'fill') == 'red':
                        self.blue_captured += 1
                        self.add_captured_piece('blue')
                    else:
                        self.red_captured += 1
                        self.add_captured_piece('red')

    def add_captured_piece(self, color):
        radius = 40
        x_offset = 10
        if color == 'blue':
            y_position = 10 + (self.blue_captured // 2) * (radius + 5)
            x_position = x_offset + (self.blue_captured % 2) * (radius + 5)
        else:
            y_position = 110 + (self.red_captured // 2) * (radius + 5)
            x_position = x_offset + (self.red_captured % 2) * (radius + 5)

        self.captured_canvas.create_oval(x_position, y_position, x_position + radius, y_position + radius, fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    game = Checkergame(root)
    root.mainloop()
