import tkinter as tk
import random
import math

class AimTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Aim Trainer Fullscreen Moving Ball")

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.ball_radius = 30
        self.ball_color = "#FF0000"
        self.score = 0

        self.hover_count = 0
        self.click_count = 0

        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.ui_frame = tk.Frame(root, bg="black")
        self.ui_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

        self.score_label = tk.Label(self.ui_frame, text="Treffer: 0", font=("Arial", 14), fg="white", bg="black")
        self.score_label.pack(anchor="e")

        self.accuracy_label = tk.Label(self.ui_frame, text="Akkuratheit: 0.0%", font=("Arial", 14), fg="white", bg="black")
        self.accuracy_label.pack(anchor="e")

        self.color_entry = tk.Entry(self.ui_frame, width=10)
        self.color_entry.insert(0, self.ball_color)
        self.color_entry.pack(anchor="e", pady=2)

        self.set_color_button = tk.Button(self.ui_frame, text="Farbe setzen", command=self.set_color)
        self.set_color_button.pack(anchor="e", pady=2)

        self.exit_button = tk.Button(self.ui_frame, text="Beenden", command=self.root.quit)
        self.exit_button.pack(anchor="e", pady=2)

        # Startposition
        self.ball_x = random.randint(self.ball_radius, self.screen_width - self.ball_radius)
        self.ball_y = random.randint(self.ball_radius, self.screen_height - self.ball_radius)

        # Start mit zufälliger Geschwindigkeit und Richtung
        self.set_random_velocity()

        self.draw_ball()
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.move_ball()
        self.randomly_change_direction()

    def set_color(self):
        color = self.color_entry.get()
        if color.startswith("#") and len(color) == 7:
            self.ball_color = color
            self.canvas.itemconfig(self.ball, fill=self.ball_color)
        else:
            print("Ungültiger Hex-Code")

    def set_random_velocity(self):
        speed = random.uniform(3, 7)  # Geschwindigkeit zwischen 3 und 7
        angle_deg = random.uniform(0, 360)  # Richtung in Grad
        angle_rad = math.radians(angle_deg)
        self.ball_vx = speed * math.cos(angle_rad)
        self.ball_vy = speed * math.sin(angle_rad)

    def draw_ball(self):
        self.canvas.delete("all")
        self.ball = self.canvas.create_oval(
            self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
            self.ball_x + self.ball_radius, self.ball_y + self.ball_radius,
            fill=self.ball_color, outline=""
        )
        self.canvas.tag_bind(self.ball, "<Button-1>", self.hit)

    def move_ball(self):
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # Rand-Kollision & Richtung umdrehen, wenn Ball rauskommt
        if self.ball_x - self.ball_radius <= 0:
            self.ball_x = self.ball_radius
            self.ball_vx = -self.ball_vx
        elif self.ball_x + self.ball_radius >= self.screen_width:
            self.ball_x = self.screen_width - self.ball_radius
            self.ball_vx = -self.ball_vx

        if self.ball_y - self.ball_radius <= 0:
            self.ball_y = self.ball_radius
            self.ball_vy = -self.ball_vy
        elif self.ball_y + self.ball_radius >= self.screen_height:
            self.ball_y = self.screen_height - self.ball_radius
            self.ball_vy = -self.ball_vy

        self.draw_ball()
        self.root.after(30, self.move_ball)

    def randomly_change_direction(self):
        # Mit 10% Chance neue zufällige Geschwindigkeit & Richtung
        if random.random() < 0.1:
            self.set_random_velocity()
        # Nächster Check in 1 Sekunde
        self.root.after(1000, self.randomly_change_direction)

    def on_mouse_move(self, event):
        mx, my = event.x, event.y
        dist = ((mx - self.ball_x)**2 + (my - self.ball_y)**2)**0.5
        if dist <= self.ball_radius:
            self.hover_count += 1
        self.update_accuracy()

    def hit(self, event):
        self.score += 1
        self.click_count += 1
        self.score_label.config(text=f"Treffer: {self.score}")

        # Ball sofort neu an zufälliger Position mit neuer Geschwindigkeit
        self.ball_x = random.randint(self.ball_radius, self.screen_width - self.ball_radius)
        self.ball_y = random.randint(self.ball_radius, self.screen_height - self.ball_radius)
        self.set_random_velocity()
        self.update_accuracy()

    def update_accuracy(self):
        if self.hover_count == 0:
            accuracy = 0.0
        else:
            accuracy = (self.click_count / self.hover_count) * 100
        self.accuracy_label.config(text=f"Akkuratheit: {accuracy:.1f}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = AimTrainer(root)
    root.mainloop()
