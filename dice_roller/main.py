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
            result = 0
            # Step 1: Determine the base result with the primary bias logic
            # With a 10% chance, perform a perfectly fair roll to add noise
            if random.randint(1, 100) <= 10:
                result = random.randint(1, 10)
            else:
                # Otherwise, perform a biased roll.
                # P(1) is ~8% average, other faces are ~10.2%
                roll = random.randint(1, 810)
                if roll <= 63:  # 63/810 chance for a "1"
                    result = 1
                else:
                    # Map the rest of the range to faces 2-10
                    result = 2 + (roll - 64) // 83

            # Step 2: Apply the second layer of bias
            # 25% chance to increment a result of 2, 3, or 4
            if result in [2, 3, 4] and random.randint(1, 100) <= 25:
                result += 1

            results.append(result)
        return results

if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()
