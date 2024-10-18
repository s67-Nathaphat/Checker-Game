import tkinter as tk
import tkinter.messagebox as messagebox
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
        self.highlighted_piece = None
        self.highlighted_moves = []

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
                        self.highlight_piece(piece)
                        self.highlight_available_moves((row, col))
                        self.highlight_capture_moves((row, col))
                        break
        else:
            if self.is_valid_move(self.selected_pos, (row, col)):
                if self.must_capture or self.capture_chain:
                    if self.is_capture_move(self.selected_pos, (row, col)):
                        self.move_piece(self.selected_piece, (row, col))
                        if self.can_continue_capturing((row, col)):
                            self.selected_pos = (row, col)
                            self.capture_chain = True
                            self.clear_highlight()
                            self.highlight_capture_moves((row, col))
                        else:
                            self.capture_chain = False
                            self.end_turn()
                    else:
                        return
                else:
                    self.move_piece(self.selected_piece, (row, col))
                    self.end_turn()
            self.selected_piece = None
            self.clear_highlight()
            self.clear_available_moves()

    def highlight_piece(self, piece):
        if self.highlighted_piece:
            self.clear_highlight()
        self.highlighted_piece = self.canvas.create_oval(
            *self.canvas.coords(piece), outline='yellow', width=4
        )

    def clear_highlight(self):
        if self.highlighted_piece:
            self.canvas.delete(self.highlighted_piece)
            self.highlighted_piece = None

    def highlight_available_moves(self, pos):
        row, col = pos
        move_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d_row, d_col in move_offsets:
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < 8 and 0 <= new_col < 8 and not self.is_space_occupied(new_row, new_col):
                if self.turn == 'red' and d_row > 0:
                    highlight = self.canvas.create_rectangle(
                        new_col * self.size, new_row * self.size,
                        (new_col + 1) * self.size, (new_row + 1) * self.size,
                        outline='red', width=2
                    )
                    self.highlighted_moves.append(highlight)
                elif self.turn == 'blue' and d_row < 0:
                    highlight = self.canvas.create_rectangle(
                        new_col * self.size, new_row * self.size,
                        (new_col + 1) * self.size, (new_row + 1) * self.size,
                        outline='blue', width=2
                    )
                    self.highlighted_moves.append(highlight)

    def highlight_capture_moves(self, pos):
        row, col = pos
        capture_offsets = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for d_row, d_col in capture_offsets:
            new_row = row + d_row
            new_col = col + d_col
            middle_row = (row + new_row) // 2
            middle_col = (col + new_col) // 2
            if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                self.is_space_occupied(middle_row, middle_col) and 
                self.canvas.itemcget(self.get_piece_by_position(middle_row, middle_col), 'fill') != self.turn and
                not self.is_space_occupied(new_row, new_col)):
                highlight = self.canvas.create_rectangle(
                    new_col * self.size, new_row * self.size,
                    (new_col + 1) * self.size, (new_row + 1) * self.size,
                    outline='yellow', width=2
                )
                self.highlighted_moves.append(highlight)

    def clear_available_moves(self):
        for highlight in self.highlighted_moves:
            self.canvas.delete(highlight)
        self.highlighted_moves.clear()

    def end_turn(self):
        self.turn = 'red' if self.turn == 'blue' else 'blue'
        self.turn_count += 1
        self.turn_label.config(text=self.get_turn_message())
        self.must_capture = self.check_capture_available()
        self.clear_available_moves()

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

    def is_capture_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            middle_row = (from_row + to_row) // 2
            middle_col = (from_col + to_col) // 2
            return self.is_space_occupied(middle_row, middle_col) and \
                   self.canvas.itemcget(self.get_piece_by_position(middle_row, middle_col), 'fill') != self.canvas.itemcget(self.selected_piece, 'fill')
        return False

    def is_space_occupied(self, row, col):
        for piece, r, c in self.pieces:
            if r == row and c == col:
                return True
        return False

    def get_piece_by_position(self, row, col):
        for piece, r, c in self.pieces:
            if r == row and c == col:
                return piece
        return None

    def move_piece(self, piece, to_pos):
        from_row, from_col = self.selected_pos
        to_row, to_col = to_pos
        self.canvas.coords(piece, to_col * self.size + 10, to_row * self.size + 10,
                           to_col * self.size + self.size - 10, to_row * self.size + self.size - 10)
        self.update_piece_position(piece, to_row, to_col)
        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            middle_row = (from_row + to_row) // 2
            middle_col = (from_col + to_col) // 2
            captured_piece = self.get_piece_by_position(middle_row, middle_col)
            if captured_piece:
                self.canvas.delete(captured_piece)
                self.pieces.remove((captured_piece, middle_row, middle_col))
                if self.turn == 'red':
                    self.red_captured += 1
                else:
                    self.blue_captured += 1

    def update_piece_position(self, piece, row, col):
        for i, (p, r, c) in enumerate(self.pieces):
            if p == piece:
                self.pieces[i] = (piece, row, col)
                break

    def check_capture_available(self):
        for piece, row, col in self.pieces:
            if self.canvas.itemcget(piece, 'fill') == self.turn:
                if self.can_continue_capturing((row, col)):
                    return True
        return False

    def can_continue_capturing(self, pos):
        row, col = pos
        capture_offsets = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for d_row, d_col in capture_offsets:
            new_row = row + d_row
            new_col = col + d_col
            middle_row = (row + new_row) // 2
            middle_col = (col + new_col) // 2
            if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                self.is_space_occupied(middle_row, middle_col) and 
                self.canvas.itemcget(self.get_piece_by_position(middle_row, middle_col), 'fill') != self.turn and
                not self.is_space_occupied(new_row, new_col)):
                return True
        return False

    def check_winner(self):
        if self.red_captured == 8:
            messagebox.showinfo("ผลการแข่งขัน", "ฝ่ายแดงชนะ!")
            return True
        elif self.blue_captured == 8:
            messagebox.showinfo("ผลการแข่งขัน", "ฝ่ายน้ำเงินชนะ!")
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = Checkergame(root)
    root.mainloop()
