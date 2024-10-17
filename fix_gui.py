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

        self.must_capture = False
        self.capture_chain = False

        self.canvas = tk.Canvas(self.master, width=640, height=640)
        self.canvas.pack(side=tk.LEFT)

        self.size = 80
        self.selected_piece = None
        self.selected_pos = None
        self.pieces = []

        self.create_board()
        self.place_pieces()
        self.canvas.bind("<Button-1>", self.on_click)

        self.right_frame = tk.Frame(self.master, width=120, height=640, bg='gray')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.captured_canvas = tk.Canvas(self.right_frame, width=120, height=640, bg='gray', highlightthickness=0)
        self.captured_canvas.pack(pady=10, expand=True, fill=tk.BOTH)
        self.captured_canvas.pack_propagate(False)

        self.turn_label = tk.Label(self.right_frame, text=self.get_turn_message(), font=('Arial', 16), bg='gray')
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
        if self.check_winner():
            return
        
        col = event.x // self.size
        row = event.y // self.size
        
        if self.selected_piece is None:
            for piece, r, c in self.pieces:
                if r == row and c == col:
                    if self.canvas.itemcget(piece, 'fill') == self.turn:
                        self.selected_piece = piece
                        self.selected_pos = (row, col)
                        self.must_capture = self.check_capture_available()
                        break
        else:
            if self.is_valid_move(self.selected_pos, (row, col)):
                if self.must_capture or self.capture_chain:
                    if self.is_capture_move(self.selected_pos, (row, col)):
                        self.move_piece(self.selected_piece, (row, col))
                        if self.can_continue_capturing((row, col)):
                            self.selected_pos = (row, col)
                            self.capture_chain = True
                        else:
                            self.capture_chain = False
                            self.end_turn()
                    else:
                        return
                else:
                    self.move_piece(self.selected_piece, (row, col))
                    self.end_turn()
            self.selected_piece = None

    def end_turn(self):
        self.turn = 'red' if self.turn == 'blue' else 'blue'
        self.turn_count += 1
        self.turn_label.config(text=self.get_turn_message())
        self.must_capture = self.check_capture_available()

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

        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            middle_row = (from_row + to_row) // 2
            middle_col = (from_col + to_col) // 2

            if (from_row < to_row and self.canvas.itemcget(self.selected_piece, 'fill') == 'red') or \
               (from_row > to_row and self.canvas.itemcget(self.selected_piece, 'fill') == 'blue'):
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
                        self.add_captured_piece('blue', self.blue_captured)
                    else:
                        self.red_captured += 1
                        self.add_captured_piece('red', self.red_captured)

    def is_capture_move(self, from_pos, to_pos):
        return abs(from_pos[0] - to_pos[0]) == 2 and abs(from_pos[1] - to_pos[1]) == 2

    def can_continue_capturing(self, pos):
        row, col = pos
        current_piece = self.canvas.itemcget(self.selected_piece, 'fill')
        can_capture = False

        for d_row, d_col in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            new_row = row + d_row
            new_col = col + d_col
            middle_row = (row + new_row) // 2
            middle_col = (col + new_col) // 2

            if current_piece == 'red' and new_row < row:
                continue
            if current_piece == 'blue' and new_row > row:
                continue

            if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                not self.is_space_occupied(new_row, new_col)):
                for piece, r, c in self.pieces:
                    if r == middle_row and c == middle_col and \
                       self.canvas.itemcget(piece, 'fill') != current_piece:
                        can_capture = True
                        break
        return can_capture

    def check_capture_available(self):
        for piece, row, col in self.pieces:
            if self.canvas.itemcget(piece, 'fill') == self.turn:
                if self.can_continue_capturing((row, col)):
                    return True
        return False

    def add_captured_piece(self, color, count):
        radius = 40
        x_start = (self.captured_canvas.winfo_width() - 4 * radius) // 2
        y_start = 0 if color == 'blue' else 160

        row_offset = count // 4
        col_offset = count % 4
        x_position = x_start + col_offset * (radius + 5)
        y_position = y_start + row_offset * (radius + 5)

        self.captured_canvas.create_oval(x_position, y_position, 
                                          x_position + radius, y_position + radius, 
                                          fill=color)

    def check_winner(self):
        if self.red_captured == 8:
            self.turn_label.config(text="ฝ่ายแดงชนะ!")
            return True
        elif self.blue_captured == 8:
            self.turn_label.config(text="ฝ่ายน้ำเงินชนะ!")
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = Checkergame(root)
    root.mainloop()
