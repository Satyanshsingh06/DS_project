try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:
    tk = None
    ttk = None


def get_curriculum():
    return {
        "1. Introduction to Data Science": {
            "What is Data Science?": {
                "definition": "Data Science combines statistics, programming, and domain knowledge to extract insights from data.",
                "summary": "It turns raw data into decisions through analysis, visualization, and modeling.",
                "comparison": {"Data": 6, "Insight": 9, "Decision": 8},
            },
            "Data Science Lifecycle": {
                "definition": "A sequence of steps from collecting data to deploying and monitoring solutions.",
                "summary": "Typical stages are collect, clean, explore, model, evaluate, and communicate.",
                "comparison": {"Collect": 7, "Clean": 8, "Model": 9},
            },
        },
        "2. Statistics and Probability": {
            "Mean vs Median": {
                "definition": "Mean is average value; median is the middle value after sorting.",
                "summary": "Median is often better for skewed data because it is less affected by outliers.",
                "comparison": {"Mean": 5, "Median": 8, "Robustness": 9},
            },
            "Probability Basics": {
                "definition": "Probability measures how likely an event is, from 0 to 1.",
                "summary": "It helps quantify uncertainty for predictions and experiments.",
                "comparison": {"Impossible": 0, "Likely": 7, "Certain": 10},
            },
        },
        "3. Data Visualization": {
            "Chart Selection": {
                "definition": "Choose charts based on the question and data type.",
                "summary": "Bar for comparison, line for trend, scatter for relationship.",
                "comparison": {"Bar": 8, "Line": 8, "Scatter": 7},
            },
            "Storytelling with Data": {
                "definition": "Using visuals and context to communicate insights clearly.",
                "summary": "Focus attention on key findings, remove clutter, and explain impact.",
                "comparison": {"Clarity": 9, "Context": 8, "Impact": 9},
            },
        },
    }


if tk is not None:
    class DataScienceLearningApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Interactive Data Science Learning")
            self.geometry("980x560")

            self.curriculum = get_curriculum()

            root_frame = ttk.Frame(self, padding=12)
            root_frame.pack(fill=tk.BOTH, expand=True)

            chapter_frame = ttk.LabelFrame(root_frame, text="Chapters", padding=8)
            chapter_frame.pack(side=tk.LEFT, fill=tk.Y)

            subtopic_frame = ttk.LabelFrame(root_frame, text="Subtopics", padding=8)
            subtopic_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

            details_frame = ttk.LabelFrame(root_frame, text="Learning Panel", padding=8)
            details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

            self.chapter_list = tk.Listbox(chapter_frame, height=20, width=34)
            self.chapter_list.pack(fill=tk.Y)
            self.chapter_list.bind("<<ListboxSelect>>", self.on_chapter_select)

            self.subtopic_list = tk.Listbox(subtopic_frame, height=20, width=30)
            self.subtopic_list.pack(fill=tk.Y)
            self.subtopic_list.bind("<<ListboxSelect>>", self.on_subtopic_select)

            self.details_text = tk.Text(details_frame, height=12, wrap=tk.WORD)
            self.details_text.pack(fill=tk.X)

            self.graph_canvas = tk.Canvas(details_frame, bg="white", height=260)
            self.graph_canvas.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

            for chapter in self.curriculum:
                self.chapter_list.insert(tk.END, chapter)

            self.show_welcome_message()

        def show_welcome_message(self):
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(
                tk.END,
                "Welcome!\n\n"
                "1) Select a chapter\n"
                "2) Select a subtopic\n"
                "3) Read definition and summary\n"
                "4) View comparison graph for quick understanding",
            )
            self.details_text.config(state=tk.DISABLED)

        def on_chapter_select(self, _event):
            selected = self.chapter_list.curselection()
            if not selected:
                return

            chapter = self.chapter_list.get(selected[0])
            subtopics = self.curriculum[chapter]

            self.subtopic_list.delete(0, tk.END)
            for subtopic in subtopics:
                self.subtopic_list.insert(tk.END, subtopic)

            self.graph_canvas.delete("all")
            self.show_welcome_message()

        def on_subtopic_select(self, _event):
            chapter_selected = self.chapter_list.curselection()
            subtopic_selected = self.subtopic_list.curselection()
            if not chapter_selected or not subtopic_selected:
                return

            chapter = self.chapter_list.get(chapter_selected[0])
            subtopic = self.subtopic_list.get(subtopic_selected[0])
            content = self.curriculum[chapter][subtopic]

            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, f"Subtopic: {subtopic}\n\n")
            self.details_text.insert(tk.END, f"Definition:\n{content['definition']}\n\n")
            self.details_text.insert(tk.END, f"Summary:\n{content['summary']}")
            self.details_text.config(state=tk.DISABLED)

            self.draw_comparison_graph(content.get("comparison", {}))

        def draw_comparison_graph(self, comparison):
            self.graph_canvas.delete("all")
            if not comparison:
                return

            canvas_width = self.graph_canvas.winfo_width() or 520
            canvas_height = self.graph_canvas.winfo_height() or 260
            margin = 30

            labels = list(comparison.keys())
            values = list(comparison.values())
            max_value = max(values) if values else 1

            bar_area_width = max(canvas_width - (2 * margin), 1)
            bar_width = max(int(bar_area_width / max(len(values), 1) * 0.6), 18)
            spacing = max(int((bar_area_width - (bar_width * len(values))) / max(len(values) + 1, 1)), 10)

            x = margin + spacing
            for label, value in zip(labels, values):
                bar_height = int((value / max_value) * (canvas_height - 2 * margin))
                y1 = canvas_height - margin - bar_height
                y2 = canvas_height - margin

                self.graph_canvas.create_rectangle(x, y1, x + bar_width, y2, fill="#4f8ef7", outline="")
                self.graph_canvas.create_text(x + bar_width / 2, y1 - 10, text=str(value), font=("Arial", 10))
                self.graph_canvas.create_text(x + bar_width / 2, y2 + 12, text=label, font=("Arial", 9), width=bar_width + 25)

                x += bar_width + spacing


def main():
    if tk is None:
        print("tkinter is required to run this app. Please install python3-tk.")
        return
    app = DataScienceLearningApp()
    app.mainloop()


if __name__ == "__main__":
    main()
