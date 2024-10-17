import tkinter as tk

class Checkergame:
    def __init__(self, master):
        self.master = master
        self.master.title("Checkers Game")
        
        self.canvas = tk.Canvas(self.master, width=640, height=640)
        self.canvas.pack()
        
        self.size = 80
        self.selected_piece = None
        self.selected_pos = None
        self.pieces = []

        self.create_board()
        self.place_pieces()
        self.canvas.bind("<Button-1>", self.on_click)

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
                    self.selected_piece = piece
                    self.selected_pos = (row, col)
                    break
        else:
            if self.is_valid_move(self.selected_pos, (row, col)):
                self.move_piece(self.selected_piece, (row, col))
            self.selected_piece = None

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1:
            if (from_row < to_row and self.canvas.itemcget(self.selected_piece, 'fill') == 'red') or \
               (from_row > to_row and self.canvas.itemcget(self.selected_piece, 'fill') == 'blue'):
                return True

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

if __name__ == "__main__":
    root = tk.Tk()
    game = Checkergame(root)
    root.mainloop()
