import tkinter as tk
import tksheet
from minizinc import Instance, Model, Solver
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def setup_gui():
    HEADERS = [
        "Topic",
        "Min nb of pages",
        "Max nb of pages",
        "Potential readers (per page)",
    ]
    DEFAULT_DATA = [
        ["International", 5, 9, 1500],
        ["National", 4, 7, 2000],
        ["Local news", 2, 5, 1000],
        ["Sport", 1, 4, 1500],
        ["Culture", 1, 3, 750],
        ["", "", "", ""],
    ]
    DEFAULT_TOTAL_PAGES = 10

    input_window = tk.Tk()
    input_window.title("Problema del periódico: Solver")
    input_window.grid_columnconfigure(0, weight=1)
    input_window.grid_rowconfigure(0, weight=1)

    input_widgets = tk.Frame(input_window)
    input_widgets.grid_columnconfigure(0, weight=1)
    input_widgets.grid_rowconfigure(0, weight=1)

    table = tksheet.Sheet(
        input_widgets,
        headers=HEADERS,
        total_columns=4,
        width=515,
        height=260,
        header_align="w",
        show_x_scrollbar=False,
    )
    table.enable_bindings(
        [
            "single_select",
            "row_select",
            "arrowkeys",
            "right_click_popup_menu",
            "edit_cell",
            "copy",
            "cut",
            "delete",
            "undo",
            "rc_insert_row",
            "rc_delete_row",
        ]
    )
    table.grid()
    table.set_sheet_data(DEFAULT_DATA)

    def append_empty_col(e):
        if e.row == table.get_total_rows() - 1 and e.text != "":
            table.insert_row(values=["", "", "", ""])

    table.extra_bindings("end_edit_cell", append_empty_col)
    table.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

    total_label = tk.Label(input_widgets, text="Total de páginas")
    total_label.grid(
        row=1,
        column=0,
        sticky="e",
        padx=5,
        pady=5,
    )
    total_input = tk.Entry(input_widgets)
    total_input.insert(0, DEFAULT_TOTAL_PAGES)
    total_input.grid(row=1, column=1)

    def solve():
        apply_model(
            table.get_sheet_data(return_copy=True)[:-1],  # remove empty row
            total=int(total_input.get()),
        )

    button = tk.Button(input_widgets, text="Solve", command=solve)
    button.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="e")

    input_widgets.grid(row=0, column=0, padx=5, pady=5)

    input_window.mainloop()


def apply_model(table, total):
    print("solving ...")
    print(table)
    model = Model("../PeriodicoGenerico.mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)
    topics = [row[0] for row in table]
    instance["Topics"] = topics
    instance["minPages"] = [int(row[1]) for row in table]
    instance["maxPages"] = [int(row[2]) for row in table]
    instance["potentialReaders"] = [int(row[3]) for row in table]
    instance["limitTotalPages"] = total
    result = instance.solve()
    print(result)
    show_bar_graph(topics, total, pages=result.solution.pages, readers=result.objective)


matplotlib.use("TkAgg")


def show_bar_graph(topics, total, pages, readers):
    results_window = tk.Tk()
    results_window.title("Problema del periódico: Solución")
    figure = Figure(figsize=(6, 4), dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure, results_window)
    axes = figure.add_subplot()
    axes.bar(topics, pages)
    axes.set_title(
        "Solución (Total páginas: %d, Número potencial de lectores: %d)"
        % (total, readers)
    )
    axes.set_ylabel("Número de páginas")
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    setup_gui()
