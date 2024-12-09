import tkinter as tk
from tkinter import Toplevel

class KittyKlickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Kitty Klicker")
        self.cats = 0
        self.cats_per_click = 1
        self.cats_per_second = 0
        self.upgrade_costs = [10, 50, 100, 200, 300, 500, 700, 1000, 1500, 2000]
        self.upgrade_cats_per_second = [1, 5, 10, 20, 30, 50, 70, 100, 150, 200]
        self.upgrade_counts = [0] * 10
        self.upgrade_total_bought = [0] * 10

        self.upgrade_names = [
            "Catnip", "Toy", "Extra Cat", "Laser Pointer",
            "Feather Wand", "Scratch Post", "Cat Tree",
            "Cat Bed", "Food Dispenser", "Cat Castle"
        ]

        self.upgrade_fonts = [
            ("Arial", 12), ("Courier", 12), ("Comic Sans MS", 12), ("Georgia", 12),
            ("Helvetica", 12), ("Times New Roman", 12), ("Verdana", 12), ("Trebuchet MS", 12),
            ("Palatino", 12), ("Garamond", 12)
        ]

        self.buy_mode = True

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.label = tk.Label(self.main_frame, text="Cats: 0", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.cps_label = tk.Label(self.main_frame, text="0/s", font=("Helvetica", 12))
        self.cps_label.pack(pady=10)

        self.cat_button = tk.Button(self.main_frame, text="", command=self.click_cat, width=25, height=12)  # Bigger button
        self.cat_button.pack(pady=20)

        self.stats_window = None
        self.stats_button = tk.Button(self.main_frame, text="Stats", command=self.toggle_stats, width=4, height=2)
        self.stats_button.place(relx=0.95, rely=0.05, anchor=tk.CENTER)

        self.upgrade_frame = tk.Frame(root)
        self.upgrade_frame.place(relx=0.85, rely=0.6, anchor=tk.CENTER)

        self.toggle_button = tk.Button(self.upgrade_frame, text="Buy Mode", command=self.toggle_mode, width=10, height=2)
        self.toggle_button.pack(pady=10)

        # Create a canvas and scrollbar for the upgrades
        self.canvas = tk.Canvas(self.upgrade_frame, width=300, height=600)  # Extended height
        self.scrollbar = tk.Scrollbar(self.upgrade_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.upgrade_buttons = []
        for i, name in enumerate(self.upgrade_names):
            button = tk.Button(
                self.scrollable_frame, 
                text=f"{name}\n{self.upgrade_costs[i]} Cats (0)", 
                command=lambda i=i: self.buy_or_sell_upgrade(i),
                width=30,  # Make the buttons longer
                height=3, 
                justify=tk.LEFT, 
                anchor='w', 
                font=self.upgrade_fonts[i]
            )
            button.pack(pady=5)
            self.upgrade_buttons.append(button)

        self.update_upgrade_visibility()
        self.update_cats_per_second()

    def click_cat(self):
        self.cats += self.cats_per_click
        self.update_cats()

    def buy_or_sell_upgrade(self, index):
        if self.buy_mode:
            self.buy_upgrade(index)
        else:
            self.sell_upgrade(index)

    def buy_upgrade(self, index):
        cost = self.upgrade_costs[index]
        if self.cats >= cost:
            self.cats -= cost
            self.cats_per_second += self.upgrade_cats_per_second[index]
            self.upgrade_counts[index] += 1
            self.upgrade_total_bought[index] += 1
            self.upgrade_costs[index] = int(cost * 1.5)  # Increase cost by 50% each time
            self.upgrade_buttons[index].config(text=f"{self.upgrade_names[index]}\n{self.upgrade_costs[index]} Cats ({self.upgrade_counts[index]})")
            self.upgrade_buttons[index].pack()  # Ensure the button is visible once purchased
        self.update_cats()

    def sell_upgrade(self, index):
        if self.upgrade_counts[index] > 0:
            self.upgrade_counts[index] -= 1
            self.cats_per_second -= self.upgrade_cats_per_second[index]
            sell_price = int(self.upgrade_costs[index] / 1.5 * 0.75)  # 75% of the original price
            self.cats += sell_price
            self.upgrade_buttons[index].config(text=f"{self.upgrade_names[index]}\n{self.upgrade_costs[index]} Cats ({self.upgrade_counts[index]})")
        self.update_cats()

    def update_cats(self):
        self.label.config(text=f"Cats: {self.cats}")
        self.cps_label.config(text=f"{self.cats_per_second}/s")
        self.update_upgrade_visibility()

    def update_cats_per_second(self):
        self.cats += self.cats_per_second
        self.update_cats()
        self.root.after(1000, self.update_cats_per_second)

    def update_upgrade_visibility(self):
        for i, button in enumerate(self.upgrade_buttons):
            if self.cats >= self.upgrade_costs[i] * 0.9 or self.upgrade_counts[i] > 0:
                button.pack(pady=5)
            else:
                button.pack_forget()

    def toggle_mode(self):
        self.buy_mode = not self.buy_mode
        self.toggle_button.config(text="Buy Mode" if self.buy_mode else "Sell Mode")

    def toggle_stats(self):
        if self.stats_window is None or not tk.Toplevel.winfo_exists(self.stats_window):
            self.show_stats()
        else:
            self.stats_window.destroy()
            self.stats_window = None

    def show_stats(self):
        self.stats_window = Toplevel(self.root)
        self.stats_window.title("Stats")
        self.stats_window.geometry("300x400")

        stats_frame = tk.Frame(self.stats_window)
        stats_frame.pack(expand=True, fill=tk.BOTH)

        canvas = tk.Canvas(stats_frame)
        scrollbar = tk.Scrollbar(stats_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        stats_label = tk.Label(scrollable_frame, text=f"Total Cats: {self.cats}\nCats per Second (CPS): {self.cats_per_second}", font=("Helvetica", 12))
        stats_label.pack(pady=10)

        upgrades_label = tk.Label(scrollable_frame, text="Total Upgrades Bought:", font=("Helvetica", 12))
        upgrades_label.pack(pady=10)

        for i, name in enumerate(self.upgrade_names):
            upgrade_stat = tk.Label(scrollable_frame, text=f"{name}: {self.upgrade_total_bought[i]}", font=("Helvetica", 12))
            upgrade_stat.pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = KittyKlickerGame(root)
    root.mainloop()
