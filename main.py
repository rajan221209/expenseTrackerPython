import tkinter as tk
from tkinter import messagebox, filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Manager")
        self.root.geometry("600x600")
        self.root.configure(bg='#f0f0f0')

        # Initialize expense data
        self.expenses = {}

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Create frames
        self.input_frame = tk.Frame(self.root, bg='#e0e0e0', padx=20, pady=20)
        self.input_frame.pack(pady=10)

        self.button_frame = tk.Frame(self.root, bg='#e0e0e0', padx=20, pady=10)
        self.button_frame.pack(pady=10)

        self.result_frame = tk.Frame(self.root, bg='#e0e0e0', padx=20, pady=10)
        self.result_frame.pack(pady=10)

        self.plot_frame = tk.Frame(self.root, bg='#e0e0e0', padx=20, pady=10)
        self.plot_frame.pack(pady=10)

        # Input widgets
        self.month_label = tk.Label(self.input_frame, text="Enter Month:", bg='#e0e0e0', font=('Arial', 12))
        self.month_label.grid(row=0, column=0, padx=5, pady=5)

        self.month_entry = tk.Entry(self.input_frame, font=('Arial', 12))
        self.month_entry.grid(row=0, column=1, padx=5, pady=5)

        self.expense_label = tk.Label(self.input_frame, text="Enter Expense Amount:", bg='#e0e0e0', font=('Arial', 12))
        self.expense_label.grid(row=1, column=0, padx=5, pady=5)

        self.expense_entry = tk.Entry(self.input_frame, font=('Arial', 12))
        self.expense_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit_expense, bg='#4CAF50', fg='white', font=('Arial', 12))
        self.submit_button.grid(row=0, column=0, padx=5, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.show_clear_menu, bg='#f44336', fg='white', font=('Arial', 12))
        self.clear_button.grid(row=0, column=1, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_expenses, bg='#2196F3', fg='white', font=('Arial', 12))
        self.save_button.grid(row=0, column=2, padx=5, pady=5)

        self.load_button = tk.Button(self.button_frame, text="Load", command=self.load_expenses, bg='#FFC107', fg='white', font=('Arial', 12))
        self.load_button.grid(row=0, column=3, padx=5, pady=5)

        self.plot_button = tk.Button(self.button_frame, text="Plot Expenses", command=self.plot_expenses, bg='#673AB7', fg='white', font=('Arial', 12))
        self.plot_button.grid(row=0, column=4, padx=5, pady=5)

        # Dropdown Menu for Month Selection
        self.clear_menu_label = tk.Label(self.button_frame, text="Select Month to Clear:", bg='#e0e0e0', font=('Arial', 12))
        self.clear_menu_label.grid(row=1, column=0, padx=5, pady=5)

        self.month_var = tk.StringVar(self.root)
        self.month_var.set("Select a month")  # Set a default value

        # Initialize OptionMenu with a placeholder option
        self.month_menu = tk.OptionMenu(self.button_frame, self.month_var, "Select a month")
        self.month_menu.grid(row=1, column=1, padx=5, pady=5)
        self.month_menu.config(state='disabled')  # Initially disabled

        self.confirm_clear_button = tk.Button(self.button_frame, text="Confirm Clear", command=self.confirm_clear, bg='#FFC107', fg='white', font=('Arial', 12))
        self.confirm_clear_button.grid(row=1, column=2, padx=5, pady=5)
        self.confirm_clear_button.config(state='disabled')  # Initially disabled

        # Labels for result and summary
        self.comparison_label = tk.Label(self.result_frame, text="", bg='#e0e0e0', font=('Arial', 12))
        self.comparison_label.pack()

        self.summary_label = tk.Label(self.result_frame, text="", bg='#e0e0e0', font=('Arial', 12))
        self.summary_label.pack()

    def submit_expense(self):
        month = self.month_entry.get().strip()
        try:
            expense = float(self.expense_entry.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the expense.")
            return

        if month in self.expenses:
            # Add to existing expense
            previous_expense = self.expenses[month]
            new_expense = previous_expense + expense
            comparison = f"Expense for {month} updated: ${new_expense:.2f}. Previous record: ${previous_expense:.2f}."
            self.expenses[month] = new_expense
        else:
            # Add new entry
            comparison = f"This is the first record for {month}."
            self.expenses[month] = expense

        # Update the comparison label and summary
        self.comparison_label.config(text=comparison)
        self.update_summary()

        # Clear the entries
        self.clear_entries()

    def show_clear_menu(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses data available to clear.")
            return

        # Update the dropdown menu with current months
        self.update_month_menu()
        self.month_menu.config(state='normal')
        self.confirm_clear_button.config(state='normal')

    def update_month_menu(self):
        # Update the dropdown menu with current months
        menu = self.month_menu['menu']
        menu.delete(0, 'end')  # Clear current menu items
        for month in self.expenses:
            menu.add_command(label=month, command=tk._setit(self.month_var, month))

    def confirm_clear(self):
        month = self.month_var.get()
        if not month or month == "Select a month":
            messagebox.showwarning("Selection Error", "Please select a month to clear.")
            return
        
        response = messagebox.askyesno("Confirm Clear", f"Are you sure you want to clear all expenses for {month}?")
        if response:
            if month in self.expenses:
                del self.expenses[month]
                self.comparison_label.config(text=f"Expenses for {month} cleared.")
                self.update_summary()
                self.update_month_menu()  # Update dropdown menu
            else:
                messagebox.showwarning("No Record", f"No expenses found for {month}.")
        
        # Disable the menu and button after clearing
        self.month_menu.config(state='disabled')
        self.confirm_clear_button.config(state='disabled')

        # Clear the entries
        self.clear_entries()

    def clear_entries(self):
        self.month_entry.delete(0, tk.END)
        self.expense_entry.delete(0, tk.END)

    def save_expenses(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.expenses, file)
            messagebox.showinfo("Saved", "Expenses saved successfully.")

    def load_expenses(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.expenses = json.load(file)
            messagebox.showinfo("Loaded", "Expenses loaded successfully.")
            self.update_summary()

    def update_summary(self):
        if not self.expenses:
            self.summary_label.config(text="No expense data available.")
            return

        total_expense = sum(self.expenses.values())
        num_months = len(self.expenses)
        average_expense = total_expense / num_months if num_months > 0 else 0

        last_month = list(self.expenses.keys())[-1]
        last_expense = self.expenses[last_month]

        summary_text = (
            f"Total Expenses: ${total_expense:.2f}\n"
            f"Average Monthly Expense: ${average_expense:.2f}\n"
            f"Last Month's Expense ({last_month}): ${last_expense:.2f}\n"
        )

        self.summary_label.config(text=summary_text)

    def plot_expenses(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses data to plot.")
            return

        months = list(self.expenses.keys())
        amounts = [self.expenses[month] for month in months]

        fig, ax = plt.subplots()
        colors = plt.cm.viridis(range(len(months)))  # Use Viridis colormap for distinct colors
        ax.bar(months, amounts, color=colors)
        ax.set_xlabel('Month')
        ax.set_ylabel('Expense Amount')
        ax.set_title('Monthly Expenses')

        # Embed the plot into the Tkinter window
        for widget in self.plot_frame.winfo_children():
            widget.destroy()  # Clear previous plots

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Initialize and run the application
root = tk.Tk()
app = ExpenseManagerApp(root)
root.mainloop()
