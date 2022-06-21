import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk

from dtln.run_evaluation import run_process

TITLE_MSG = (
    "Автоматизированная подсистема анализа и обработки речи для систем мультимедийной связи "
    "| Дипломный проект бАП-181 Борисов Максим"
)

HELP_MSG = ""


class UI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.model_path = None

        self.title(TITLE_MSG)
        self.resizable(False, False)

        self.switch_frame(InitPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()


class InitPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.selected_model_path = None
        self.activate_model_button = None
        self.choose_model_button = None
        self.model_path_field = None
        self.input_model_frame = None

        self.show()

    def show(self):
        self.input_model_frame = ttk.Frame(self)

        self.model_path_field = ttk.Entry(self.input_model_frame)
        self.model_path_field.insert(0, "Model path in .h5 format")
        self.model_path_field.bind("<Key>", lambda x: "break")
        self.model_path_field["state"] = tk.DISABLED
        self.choose_model_button = ttk.Button(
            self.input_model_frame,
            text="...",
            command=self.choose_model_button_trigger,
            width=1,
        )
        self.model_path_field.pack(side=tk.LEFT)
        self.choose_model_button.pack(side=tk.RIGHT)
        self.input_model_frame.pack()

        self.activate_model_button = ttk.Button(
            self,
            text="Активировать модель",
            command=self.activate_model_button_trigger,
            state=tk.DISABLED,
        )
        self.activate_model_button.pack()

    def choose_model_button_trigger(self):
        self.selected_model_path = fd.askopenfilename(
            filetypes=[("Trained model", "*.h5")]
        )
        if not self.selected_model_path:
            return
        self.model_path_field["state"] = tk.NORMAL
        self.activate_model_button["state"] = tk.NORMAL
        self.model_path_field.delete(0, tk.END)
        self.model_path_field.insert(0, self.selected_model_path.strip())

    def activate_model_button_trigger(self):
        self.master.model_path = self.selected_model_path
        self.master.switch_frame(MainPage)


class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.choose_out_package_button = None
        self.out_package_path_field = None
        self.out_package_frame = None
        self.out_package_path = None
        self.in_package_path = None
        self.process_button = None
        self.help_button = None
        self.in_package_path_field = None
        self.choose_in_package_button = None
        self.input_package_frame = None

        self.show()

    def show(self):
        self.input_package_frame = ttk.Frame(self)

        # setup input package path choosing elements
        self.choose_in_package_button = ttk.Button(
            self.input_package_frame,
            text="...",
            command=self.choose_in_package_button_trigger,
            width=1,
        )

        self.in_package_path_field = ttk.Entry(self.input_package_frame)
        self.in_package_path_field.insert(
            0, "Catalog path with .wav file(-es) should be here"
        )
        self.in_package_path_field.bind("<Key>", lambda x: "break")
        self.in_package_path_field["state"] = tk.DISABLED

        self.in_package_path_field.pack(side=tk.LEFT)
        self.choose_in_package_button.pack(side=tk.RIGHT)
        self.input_package_frame.pack()

        # setup output package path choosing elements
        self.out_package_frame = ttk.Frame(self)

        self.out_package_path_field = ttk.Entry(self.out_package_frame)
        self.out_package_path_field.insert(0, "Destination catalog path")
        self.out_package_path_field.bind("<Key>", lambda x: "break")
        self.out_package_path_field["state"] = tk.DISABLED

        self.choose_out_package_button = ttk.Button(
            self.out_package_frame,
            text="...",
            command=self.choose_out_package_button_trigger,
            width=1,
        )

        self.out_package_path_field.pack(side=tk.LEFT)
        self.choose_out_package_button.pack(side=tk.RIGHT)
        self.out_package_frame.pack()

        self.process_button = ttk.Button(
            self, text="Обработать", command=self.process_button_trigger
        )
        self.help_button = ttk.Button(
            self, text="Помощь", command=self.help_button_trigger
        )

        self.process_button.pack()
        self.help_button.pack()

    def choose_in_package_button_trigger(self):
        self.in_package_path = fd.askdirectory()

        if not self.in_package_path:
            return

        self.in_package_path_field["state"] = tk.NORMAL

        self.in_package_path_field.delete(0, tk.END)
        self.in_package_path_field.insert(0, self.in_package_path)

        if self.in_package_path and self.out_package_path:
            self.process_button["state"] = tk.NORMAL

    def choose_out_package_button_trigger(self):
        self.out_package_path = fd.askdirectory()

        if not self.out_package_frame:
            return

        self.out_package_path_field["state"] = tk.NORMAL

        self.out_package_path_field.delete(0, tk.END)
        self.out_package_path_field.insert(0, self.out_package_path)

        if self.in_package_path and self.out_package_path:
            self.process_button["state"] = tk.NORMAL

    def process_button_trigger(self):
        try:
            run_process(
                self.in_package_path, self.out_package_path, self.master.model_path
            )
            mb.showinfo(
                "Processing completed",
                f"Processing successfully completed! Results saved in the specified package: {self.out_package_path}",
            )
        except Exception:
            mb.showerror(
                "Processing failed",
                f"Failed to process the specified package: {self.in_package_path}",
            )

    def help_button_trigger(self):
        pass
