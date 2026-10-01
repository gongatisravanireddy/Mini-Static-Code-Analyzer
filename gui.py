import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from analyzer.core import Analyzer
from report_generator import generate_html_report


class StaticCodeAnalyzerGUI:

    def __init__(self, root):

        self.root = root

        # Window settings
        self.root.title("Mini Static Code Analyzer")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)

        self.selected_file = None
        self.result = None

        # ==================================================
        # TITLE
        # ==================================================

        title = tk.Label(
            root,
            text="MINI STATIC CODE ANALYZER",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=(20, 15))

        # ==================================================
        # FILE SELECTION FRAME
        # ==================================================

        file_frame = tk.Frame(root)

        file_frame.pack(
            fill=tk.X,
            padx=40,
            pady=5
        )

        self.file_label = tk.Label(
            file_frame,
            text="No Python file selected",
            font=("Arial", 11),
            anchor="w"
        )

        self.file_label.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(0, 15)
        )

        browse_button = tk.Button(
            file_frame,
            text="Browse",
            font=("Arial", 11, "bold"),
            width=12,
            command=self.browse_file
        )

        browse_button.pack(
            side=tk.RIGHT
        )

        # ==================================================
        # ANALYZE BUTTON
        # ==================================================

        analyze_button = tk.Button(
            root,
            text="ANALYZE CODE",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            command=self.analyze_code
        )

        analyze_button.pack(
            pady=15
        )

        # ==================================================
        # ANALYSIS SUMMARY
        # ==================================================

        summary_title = tk.Label(
            root,
            text="Analysis Summary",
            font=("Arial", 18, "bold")
        )

        summary_title.pack(
            pady=(5, 8)
        )

        self.summary_label = tk.Label(
            root,
            text=(
                "Unused Variables: 0     "
                "Dead Code: 0     "
                "Duplicate Declarations: 0     "
                "Total: 0"
            ),
            font=("Arial", 12)
        )

        self.summary_label.pack(
            pady=(0, 15)
        )

        # ==================================================
        # DETECTED ISSUES TITLE
        # ==================================================

        issue_title = tk.Label(
            root,
            text="Detected Issues",
            font=("Arial", 18, "bold")
        )

        issue_title.pack(
            pady=(0, 8)
        )

        # ==================================================
        # ISSUE TEXT AREA
        # ==================================================

        text_frame = tk.Frame(root)

        text_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30,
            pady=(0, 10)
        )

        scrollbar = tk.Scrollbar(
            text_frame
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            height=15,
            yscrollcommand=scrollbar.set
        )

        self.output_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.config(
            command=self.output_text.yview
        )

        # ==================================================
        # REPORT BUTTON
        # ==================================================

        report_button = tk.Button(
            root,
            text="SAVE HTML REPORT",
            font=("Arial", 11, "bold"),
            width=20,
            height=1,
            command=self.save_report
        )

        report_button.pack(
            pady=(5, 20)
        )

    # ======================================================
    # BROWSE FILE
    # ======================================================

    def browse_file(self):

        filepath = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=[
                ("Python Files", "*.py"),
                ("All Files", "*.*")
            ]
        )

        if filepath:

            self.selected_file = filepath

            self.file_label.config(
                text=filepath
            )

            # Clear previous output
            self.output_text.delete(
                "1.0",
                tk.END
            )

            self.summary_label.config(
                text=(
                    "Unused Variables: 0     "
                    "Dead Code: 0     "
                    "Duplicate Declarations: 0     "
                    "Total: 0"
                )
            )

    # ======================================================
    # ANALYZE CODE
    # ======================================================

    def analyze_code(self):

        if not self.selected_file:

            messagebox.showwarning(
                "No File Selected",
                "Please select a Python file first."
            )

            return

        try:

            analyzer = Analyzer(
                self.selected_file
            )

            self.result = analyzer.run()

            summary = self.result.summary()

            # Update summary
            self.summary_label.config(
                text=(
                    f"Unused Variables: "
                    f"{summary['Unused Variable']}     "
                    f"Dead Code: "
                    f"{summary['Dead Code']}     "
                    f"Duplicate Declarations: "
                    f"{summary['Duplicate Declaration']}     "
                    f"Total: "
                    f"{summary['Total']}"
                )
            )

            # Clear previous issues
            self.output_text.delete(
                "1.0",
                tk.END
            )

            # Display issues
            if not self.result.issues:

                self.output_text.insert(
                    tk.END,
                    "No issues found.\n"
                )

            else:

                for issue in self.result.issues:

                    self.output_text.insert(
                        tk.END,
                        str(issue)
                    )

                    self.output_text.insert(
                        tk.END,
                        "\n\n"
                    )

            messagebox.showinfo(
                "Analysis Complete",
                "Code analysis completed successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Analysis Error",
                str(e)
            )

    # ======================================================
    # SAVE HTML REPORT
    # ======================================================

    def save_report(self):

        if self.result is None:

            messagebox.showwarning(
                "No Analysis",
                "Please analyze a Python file first."
            )

            return

        filepath = filedialog.asksaveasfilename(
            title="Save HTML Report",
            defaultextension=".html",
            filetypes=[
                ("HTML Files", "*.html")
            ]
        )

        if not filepath:

            return

        try:

            html = generate_html_report(
                self.result
            )

            Path(filepath).write_text(
                html,
                encoding="utf-8"
            )

            messagebox.showinfo(
                "Report Saved",
                f"HTML report saved successfully.\n\n{filepath}"
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                str(e)
            )


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = StaticCodeAnalyzerGUI(
        root
    )

    root.mainloop()