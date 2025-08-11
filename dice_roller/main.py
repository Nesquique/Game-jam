import tkinter as tk
from tkinter import ttk
import random

class DiceRollerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lanceur de Dés")
        self.geometry("800x600")
        self.resizable(False, False)

        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Controls frame
        controls_frame = ttk.Frame(main_frame, padding="10")
        controls_frame.pack(fill="x")

        ttk.Label(controls_frame, text="Nombre de dés (1-15):").pack(side="left", padx=5)

        self.num_dice_var = tk.StringVar(value="1")
        self.num_dice_entry = ttk.Entry(controls_frame, textvariable=self.num_dice_var, width=5)
        self.num_dice_entry.pack(side="left", padx=5)

        roll_button = ttk.Button(controls_frame, text="Lancer les dés", command=self.roll_dice)
        roll_button.pack(side="left", padx=5)

        # Results frame
        self.results_frame = ttk.Frame(main_frame, padding="10")
        self.results_frame.pack(fill="both", expand=True)

        ttk.Label(self.results_frame, text="Les résultats apparaîtront ici.").pack()

    def roll_dice(self):
        try:
            num_dice = int(self.num_dice_var.get())
            if not 1 <= num_dice <= 15:
                raise ValueError("Le nombre de dés doit être entre 1 et 15.")
        except ValueError as e:
            self.display_error(e)
            return

        results = self._roll_d10_piped(num_dice)
        self.display_dice_results(results)
        print(f"Rolled {num_dice} dice with results: {results}")

    def display_error(self, error_message):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.results_frame, text=f"Erreur: {error_message}", foreground="red").pack()

    def display_dice_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Configure grid to center the dice
        num_cols = 5
        self.results_frame.grid_columnconfigure(list(range(num_cols)), weight=1)

        for i, number in enumerate(results):
            row = i // num_cols
            col = i % num_cols

            die_canvas = tk.Canvas(self.results_frame, width=100, height=100, bg="#F0F0F0", highlightthickness=0)
            die_canvas.grid(row=row, column=col, padx=10, pady=10)

            # Draw a simple circle as the die face
            die_canvas.create_oval(10, 10, 90, 90, fill="ivory", outline="black", width=2)
            die_canvas.create_text(50, 50, text=str(number), font=("Arial", 30, "bold"))

    def _roll_d10_piped(self, num_dice):
        results = []
        for _ in range(num_dice):
            roll = random.randint(1, 20)
            if roll == 1:
                results.append(1)
            elif 2 <= roll <= 3:
                results.append(2)
            elif 4 <= roll <= 5:
                results.append(3)
            elif 6 <= roll <= 7:
                results.append(4)
            elif 8 <= roll <= 9:
                results.append(5)
            elif 10 <= roll <= 11:
                results.append(6)
            elif 12 <= roll <= 13:
                results.append(7)
            elif 14 <= roll <= 15:
                results.append(8)
            elif 16 <= roll <= 17:
                results.append(9)
            elif 18 <= roll <= 20:
                results.append(10)
        return results

if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()
