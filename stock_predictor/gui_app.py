import customtkinter as ctk
import threading
from stock_predictor.main import main as run_stock_predictor

class StockPredictorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Stock Predictor GUI")
        self.geometry("800x600")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Run Analysis Button
        self.run_button = ctk.CTkButton(self, text="Run Stock Analysis", command=self.run_analysis)
        self.run_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Results Frame (for table-like display)
        self.results_frame = ctk.CTkScrollableFrame(self, label_text="Recommendations")
        self.results_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Initial message in results frame
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=1)
        self.results_frame.grid_columnconfigure(2, weight=1)
        self.results_frame.grid_columnconfigure(3, weight=1)
        self.results_frame.grid_columnconfigure(4, weight=1)

        self.status_label = ctk.CTkLabel(self, text="Ready")
        self.status_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.progress_label = ctk.CTkLabel(self, text="")
        self.progress_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.create_table_headers()

    def create_table_headers(self):
        headers = ["Ticker", "Last Price", "Target Price", "Stop-Loss", "Confidence"]
        for i, header_text in enumerate(headers):
            label = ctk.CTkLabel(self.results_frame, text=header_text, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

    def run_analysis(self):
        self.run_button.configure(state="disabled")
        self.status_label.configure(text="Running analysis...")
        self.clear_results()

        # Run the analysis in a separate thread to keep the GUI responsive
        threading.Thread(target=self._run_analysis_thread).start()

    def _update_progress(self, current, total, ticker):
        self.progress_label.configure(text=f"Analyzing stock {current} of {total}: {ticker}")

    def _run_analysis_thread(self):
        try:
            recommendations = run_stock_predictor(progress_callback=self._update_progress)
            self.after(0, self.display_results, recommendations)
        except Exception as e:
            self.after(0, self.status_label.configure, {"text": f"Error: {e}", "text_color": "red"})
        finally:
            self.after(0, self.run_button.configure, {"state": "normal"})
            self.after(0, self.progress_label.configure, {"text": ""}) # Clear progress label

    def display_results(self, recommendations):
        if not recommendations:
            self.status_label.configure(text="No suitable stocks found for recommendation.", text_color="orange")
            return

        self.status_label.configure(text="Analysis complete.", text_color="green")
        
        # Start from row 1 to leave space for headers
        row_num = 1
        for rec in recommendations:
            # Only display if confidence is > 75 (as per main.py logic)
            if rec['confidence'] > 75:
                ctk.CTkLabel(self.results_frame, text=rec['ticker']).grid(row=row_num, column=0, padx=5, pady=2, sticky="ew")
                ctk.CTkLabel(self.results_frame, text=f"{rec['last_price']:.2f}").grid(row=row_num, column=1, padx=5, pady=2, sticky="ew")
                ctk.CTkLabel(self.results_frame, text=f"{rec['target_price']:.2f}").grid(row=row_num, column=2, padx=5, pady=2, sticky="ew")
                ctk.CTkLabel(self.results_frame, text=f"{rec['stop_loss']:.2f}").grid(row=row_num, column=3, padx=5, pady=2, sticky="ew")
                ctk.CTkLabel(self.results_frame, text=f"{rec['confidence']:.2f}%").grid(row=row_num, column=4, padx=5, pady=2, sticky="ew")
                row_num += 1

    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            # Keep headers, remove other labels
            if isinstance(widget, ctk.CTkLabel) and widget.cget("font").cget("weight") != "bold":
                widget.destroy()
        self.create_table_headers() # Recreate headers after clearing

if __name__ == "__main__":
    app = StockPredictorApp()
    app.mainloop()
