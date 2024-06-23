import flet as ft
import numpy as np
import sympy as sp
from solver.newton_raphson import NewtonRaphsonSolver
import speech_recognition as sr

class UIWidgets:
    def __init__(self, page):
        self.page = page
        self.num_eqs_input = ft.TextField(label="Nombre d'équations", keyboard_type="number", hint_text="Ex: 1", width=400)
        self.num_vars_input = ft.TextField(label="Nombre de composants de X0", keyboard_type="number", width=400, hint_text="Ex: 1")
        self.tolerance_input = ft.TextField(label="Tolérance", hint_text="Ex: 0.0001 ou 1e-4", width=200)
        self.equations_container = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        self.initial_guess_container = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        self.solution_output = ft.TextField(label="Solution", multiline=True, read_only=True, width=350)
        self.M = ft.Row(controls=[ft.Text("                                                         ", size=20), self.solution_output])
        self.T = ft.Row(controls=[ft.Text("                                             ", size=20), self.tolerance_input])

    def recognize_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Dites quelque chose :")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="fr-FR")
                print(f"Vous avez dit : {text}")
                return text
            except sr.UnknownValueError:
                print("Désolé, je n'ai pas compris.")
                return ""
            except sr.RequestError:
                print("Erreur de service ; veuillez réessayer.")
                return ""

    math_map = {
    'un': '1',
    'deux': '2',
    'trois': '3',
    'quatre': '4',
    'cinq': '5',
    'six': '6',
    'sept': '7',
    'huit': '8',
    'neuf': '9',
    'zéro': '0',
    'fois': '*',
    'plus': '+',
    'moins': '-',
    'divisé': '/',
    'au carré': '**2',
    'racine carrée': 'sqrt',
    'ln': 'log',
    'log': 'log10',
    'expo': 'exp'
    }

    def process_text(text):
        words = text.split()
        processed_words = []
        for word in words:
            if word in set.math_map:
                processed_words.append(set.math_map[word])
            else:
                processed_words.append(word)
        return ' '.join(processed_words)

    def create_input_fields(self):
        mic_button1 = ft.IconButton(icon=ft.icons.MIC, on_click=self.open_num_eqs_dialog)
        row1 = ft.Row([self.num_eqs_input, mic_button1], alignment=ft.MainAxisAlignment.CENTER)

        mic_button2 = ft.IconButton(icon=ft.icons.MIC, on_click=self.open_num_vars_dialog)
        row2 = ft.Row([self.num_vars_input, mic_button2], alignment=ft.MainAxisAlignment.CENTER)

        generate_inputs_button = ft.ElevatedButton(text="Générer les champs", on_click=self.update_inputs)

        return ft.Column(
            controls=[
                ft.Text("", size=10),
                ft.Stack(
                    [
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    "           Résolution des Systèmes d'Équations Non Linéaires par la methode de Newton :",
                                    ft.TextStyle(
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        foreground=ft.Paint(
                                            color=ft.colors.GREEN_700,
                                            stroke_width=6,
                                            stroke_join=ft.StrokeJoin.ROUND,
                                            style=ft.PaintingStyle.STROKE,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    "           Résolution des Systèmes d'Équations Non Linéaires par la methode de Newton :",
                                    ft.TextStyle(
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.BLUE_GREY_100,
                                    ),
                                ),
                            ],
                        ),
                    ]
                ),
                ft.Text("", size=20),
                row1,
                ft.Text("", size=20),
                row2,
                ft.Text("", size=20),
                generate_inputs_button,
                self.equations_container,
                self.initial_guess_container,
                ft.Text("", size=20),
                self.T,
                ft.Text("", size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def update_inputs(self, e):
        num_eqs = int(self.num_eqs_input.value)
        num_vars = int(self.num_vars_input.value)

        self.equations_container.controls = [
            ft.TextField(label=f"Équation {i + 1}", multiline=True, width=600, hint_text="Ex: x0**2 + x1**2 - 1") for i in range(num_eqs)]
        self.initial_guess_container.controls = [
            ft.Row([ft.TextField(label=f"x0[{i}]", hint_text="Ex: 0.0", width=200),
                    ft.IconButton(icon=ft.icons.MIC, on_click=lambda e, i=i: self.open_modal_dialog(e, i))],
                alignment=ft.MainAxisAlignment.CENTER) for i in range(num_vars)]
        self.page.update()

    def open_num_eqs_dialog(self, e):
        self.num_eqs_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Parler pour le nombre d'équations"),
            content=ft.Text("En cours de développement... Trouver le code dans test/test.py"),
            actions=[
                ft.TextButton("Fermer", on_click=lambda e: self.close_modal_dialog(self.num_eqs_dialog))
            ]
        )
        self.page.dialog = self.num_eqs_dialog
        self.num_eqs_dialog.open = True
        self.page.update()

    def open_num_vars_dialog(self, e):
        self.num_vars_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Parler pour le nombre de composants de X0"),
            content=ft.Text("En cours de développement... Trouver le code dans test/test.py"),
            actions=[
                ft.TextButton("Fermer", on_click=lambda e: self.close_modal_dialog(self.num_vars_dialog))
            ]
        )
        self.page.dialog = self.num_vars_dialog
        self.num_vars_dialog.open = True
        self.page.update()

    def open_modal_dialog(self, e, i):
        spoken_text = self.recognize_speech()
        if spoken_text:
            processed_text = self.process_text(spoken_text)
            self.initial_guess_container.controls[i].controls[0].value = processed_text
        self.page.update()

    def close_modal_dialog(self, modal_dialog):
        modal_dialog.open = False
        self.page.update()

    def on_calculate_click(self, e):
        if self.num_eqs_input.value.strip() == "":
            self.solution_output.color = ft.colors.RED
            self.solution_output.value = "Veuillez entrer le nombre d'équations."
            self.page.auto_scroll = False
            self.page.scroll_to(offset=-1, duration=100)
            self.page.update()
            return

        if self.num_vars_input.value.strip() == "":
            self.solution_output.color = ft.colors.RED
            self.solution_output.value = "Veuillez entrer le nombre de composants de X0."
            self.page.auto_scroll = False
            self.page.scroll_to(offset=-1, duration=100)
            self.page.update()
            return

        if self.tolerance_input.value.strip() == "":
            self.solution_output.color = ft.colors.RED
            self.solution_output.value = "Veuillez entrer une valeur de tolérance."
            self.page.auto_scroll = False
            self.page.scroll_to(offset=-1, duration=100)
            self.page.update()
            return

        try:
            num_eqs = int(self.num_eqs_input.value)
            num_vars = int(self.num_vars_input.value)
            tolerance = float(self.tolerance_input.value)
        except ValueError as ex:
            self.solution_output.value = str(ex)
            self.page.auto_scroll = True
            self.page.update()
            return

        equations = [eq_control.value for eq_control in self.equations_container.controls if eq_control.value.strip() != ""]
        initial_guess = [guess_control.controls[0].value for guess_control in self.initial_guess_container.controls if guess_control.controls[0].value.strip() != ""]

        try:
            initial_guess = [float(value) for value in initial_guess]
        except ValueError as ex:
            self.solution_output.color = ft.colors.RED
            self.solution_output.value = f"Erreur de conversion des valeurs initiales en flottants : {str(ex)}"
            self.page.auto_scroll = False
            self.page.scroll_to(offset=-1, duration=100)
            self.page.update()
            return

        if len(equations) != num_eqs or len(initial_guess) != num_vars:
            self.solution_output.color = ft.colors.RED
            self.solution_output.value = "Veuillez remplir toutes les équations et valeurs initiales."
            self.page.auto_scroll = False
            self.page.scroll_to(offset=-1, duration=100)
            self.page.update()
            return

        symbols_list = sp.symbols(f"x0:{num_vars}")
        equations_sym = [sp.sympify(eq, locals=dict(zip(symbols_list, symbols_list))) for eq in equations]

        def F(x):
            subs = dict(zip(symbols_list, x))
            return np.array([float(eq.evalf(subs=subs)) for eq in equations_sym], dtype=float)

        x0_array = np.array(initial_guess, dtype=float)

        try:
            solver = NewtonRaphsonSolver(F, x0_array, tolerance)
            solution, iter = solver.solve()
            self.solution_output.color = ft.colors.GREEN
            self.solution_output.value = f"Solution: {solution}\nNombre d'itérations: {iter}"
            self.page.auto_scroll = False
            self.page.scroll_to(offset=-1, duration=50)
        except Exception as ex:
            self.solution_output.value = str(ex)

        self.page.update()

    def on_reset_click(self, e):
        self.num_eqs_input.value = ""
        self.num_vars_input.value = ""
        self.tolerance_input.value = ""
        self.equations_container.controls.clear()
        self.initial_guess_container.controls.clear()
        self.solution_output.value = ""
        self.page.auto_scroll = False
        self.page.scroll_to(delta=-200, duration=300)
        self.page.update()

    def create_buttons(self):
        return ft.Row(
            controls=[
                ft.ElevatedButton(text="Calculer", on_click=self.on_calculate_click),
                ft.Text("   ", size=20),
                ft.ElevatedButton(text="Réinitialiser", on_click=self.on_reset_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def create_output_area(self):
        return ft.Column(
            controls=[
                ft.Text("", size=20),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "                      Résultats :",
                            ft.TextStyle(
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    gradient=ft.PaintLinearGradient(
                                        (170, 20), (250, 20), [ft.colors.RED, ft.colors.YELLOW]
                                    )
                                ),
                            ),
                        ),
                    ],
                ),
                self.M,
                ft.Text("", size=20)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

def init_ui(page: ft.Page):
    ui_widgets = UIWidgets(page)
    page.add(ui_widgets.create_input_fields())
    page.add(ui_widgets.create_buttons())
    page.add(ui_widgets.create_output_area())
