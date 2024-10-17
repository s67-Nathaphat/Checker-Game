import tkinter as tk

class Checkergame:
    def __init__(self, master):
        self.master = master
        self.master.title("เกมหมากฮอส")
        
        self.canvas = tk.Canvas(self.master, width=640, height=640)
        self.canvas.pack()
        
        self.size = 80
        self.create_board()

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

if __name__ == "__main__":
    root = tk.Tk()
    game = Checkergame(root)
    root.mainloop()
