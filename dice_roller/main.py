import tkinter as tk
from tkinter import ttk
import random
import time

class DiceRollerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lanceur de Dés Pro")
        self.configure(background='#F0F0F0')

        # Appliquer un thème moderne
        style = ttk.Style(self)
        style.theme_use('clam')

        # Couleurs personnalisées
        style.configure('.', background='#F0F0F0', foreground='#333333', font=('Arial', 12))
        style.configure('TFrame', background='#F0F0F0')
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 12, 'bold'), borderwidth=0)
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TEntry', font=('Arial', 12))
        self.geometry("800x600")
        self.resizable(True, True)

        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Titre
        title_label = ttk.Label(main_frame, text="Lanceur de Dés Pro", font=('Arial', 24, 'bold'), foreground='#007BFF')
        title_label.pack(pady=(0, 20))

        # Controls frame
        controls_frame = ttk.Frame(main_frame, padding="10")
        controls_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(controls_frame, text="Nombre de dés (1-15):").pack(side="left", padx=5)

        self.num_dice_var = tk.StringVar(value="1")
        self.num_dice_entry = ttk.Entry(controls_frame, textvariable=self.num_dice_var, width=5)
        self.num_dice_entry.pack(side="left", padx=5)

        roll_button = ttk.Button(controls_frame, text="Lancer les dés", command=self.roll_dice)
        roll_button.pack(side="left", padx=5)

        reroll_button = ttk.Button(controls_frame, text="Relancer", command=self.roll_dice) # Same command for now
        reroll_button.pack(side="left", padx=5)

        clear_button = ttk.Button(controls_frame, text="Effacer", command=self.clear_results)
        clear_button.pack(side="left", padx=5)

        # Results frame
        self.results_frame = ttk.Frame(main_frame, padding="10")
        self.results_frame.pack(fill="both", expand=True)

        ttk.Label(self.results_frame, text="Les résultats apparaîtront ici.").pack()

        # History frame
        history_frame = ttk.Frame(main_frame)
        history_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(history_frame, text="Historique des Lancers:", font=('Arial', 14, 'bold')).pack(anchor='w')
        self.history_text = tk.Text(history_frame, height=5, width=80, font=('Arial', 10), relief='solid', borderwidth=1)
        self.history_text.pack(pady=5, fill='x', expand=True)


    def roll_dice(self):
        try:
            num_dice = int(self.num_dice_var.get())
            if not 1 <= num_dice <= 15:
                raise ValueError("Le nombre de dés doit être entre 1 et 15.")
        except ValueError as e:
            self.display_error(e)
            return

        # Animation
        for _ in range(5):
            temp_results = [random.randint(1, 10) for _ in range(num_dice)]
            self.display_dice_results(temp_results)
            self.update()
            time.sleep(0.1)

        results = self._roll_d10_piped(num_dice)
        self.display_dice_results(results)
        print(f"Rolled {num_dice} dice with results: {results}")

        # Add to history
        self.history_text.insert(tk.END, f"Lancer de {num_dice} dé(s): {results}\n")
        self.history_text.see(tk.END)

    def display_error(self, error_message):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.results_frame, text=f"Erreur: {error_message}", foreground="red").pack()

    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.results_frame, text="Les résultats apparaîtront ici.").pack()
        self.history_text.delete('1.0', tk.END)

    def display_dice_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Ajouter un label de résultat
        result_label = ttk.Label(self.results_frame, text=f"Résultats pour {len(results)} dés :", font=('Arial', 14, 'bold'))
        result_label.pack(pady=(0, 10))

        # Frame avec scrollbar pour les dés
        canvas = tk.Canvas(self.results_frame, bg='#F0F0F0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        num_cols = 3
        for i, number in enumerate(results):
            row = i // num_cols
            col = i % num_cols

            die_canvas = tk.Canvas(scrollable_frame, width=120, height=120, bg='#F0F0F0', highlightthickness=0)
            die_canvas.grid(row=row, column=col, padx=10, pady=10)

            # Dessiner un dé plus réaliste (carré avec ombre)
            die_canvas.create_rectangle(12, 12, 112, 112, fill='#F0F0F0', outline='#F0F0F0', width=2) # ombre
            die_canvas.create_rectangle(10, 10, 110, 110, fill='ivory', outline='black', width=2)

            color = 'red' if number % 2 == 0 else 'blue'
            die_canvas.create_text(60, 60, text=str(number), font=('Arial', 40, 'bold'), fill=color, tags="number_text")

            if number <= 6:
                self.draw_dots(die_canvas, number)

    def draw_dots(self, canvas, number):
        canvas.delete("number_text")
        positions = {
            1: [(60, 60)],
            2: [(40, 40), (80, 80)],
            3: [(40, 40), (60, 60), (80, 80)],
            4: [(40, 40), (40, 80), (80, 40), (80, 80)],
            5: [(40, 40), (40, 80), (60, 60), (80, 40), (80, 80)],
            6: [(40, 40), (40, 60), (40, 80), (80, 40), (80, 60), (80, 80)],
        }
        for pos in positions.get(number, []):
            canvas.create_oval(pos[0]-7, pos[1]-7, pos[0]+7, pos[1]+7, fill='black', outline='black')

    def _roll_one_piped_die(self):
        # This function handles the full logic for a single die roll.

        # Step 1: Determine the base result with the primary bias logic.
        # 10% chance of a fair roll, 90% chance of a biased roll.
        if random.randint(1, 100) <= 10:
            result = random.randint(1, 10)
        else:
            # Biased roll logic (P(1) is reduced).
            roll = random.randint(1, 810)
            if roll <= 63:
                result = 1
            else:
                result = 2 + (roll - 64) // 83

        # Step 2: Apply the second layer of bias (25% chance to increment 2, 3, or 4).
        if result in [2, 3, 4] and random.randint(1, 100) <= 25:
            result += 1

        # Step 3: Apply the third layer of bias (20% chance to re-roll a 3).
        # If the result is a 3, we recursively call this function to re-roll.
        if result == 3 and random.randint(1, 100) <= 20:
            return self._roll_one_piped_die()

        return result

    def _roll_d10_piped(self, num_dice):
        # This is now a simple loop that calls the single-die roller.
        results = []
        for _ in range(num_dice):
            results.append(self._roll_one_piped_die())
        return results

if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()
