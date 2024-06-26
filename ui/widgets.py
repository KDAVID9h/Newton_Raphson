import flet as ft
import numpy as np
from sympy import symbols, sympify, sqrt, log, sin, cos, exp
from solver.newton_raphson import NewtonRaphsonSolver

class UIWidgets:
    def __init__(self, page):
        self.page = page
        self.num_eqs_input = ft.TextField(label="Nombre d'équations", keyboard_type="number", hint_text="Ex: 1", width=400)
        self.num_vars_input = ft.TextField(label="Nombre de composants de X0", keyboard_type="number", width=400, hint_text="Ex: 1")
        self.tolerance_input = ft.TextField(label="Tolérance", hint_text="Ex: 0.0001 ou 1e-4", width=200 ) #bgcolor= 'GREY_900')
        self.equations_container = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        self.initial_guess_container = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        self.solution_output = ft.TextField(label="Solution", multiline=True, read_only=True, width=350)
        self.M = ft.Row(controls=[ft.Text("                                                         ", 
                                        size=20), self.solution_output])
        self.T = ft.Row(controls=[ft.Text("                                             ", 
                                        size=20), self.tolerance_input])

    def create_input_fields(self):
        mic_button1 = ft.IconButton(icon=ft.icons.MIC, on_click=self.open_num_eqs_dialog)
        row1 = ft.Row([self.num_eqs_input, mic_button1],
                    alignment=ft.MainAxisAlignment.CENTER)

        mic_button2 = ft.IconButton(icon=ft.icons.MIC, on_click=self.open_num_vars_dialog)
        row2 = ft.Row([self.num_vars_input, mic_button2],
                    alignment=ft.MainAxisAlignment.CENTER)

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
                #ft.Text("", size=20),
                self.equations_container,
                #ft.Text("", size=20),
                self.initial_guess_container,
                ft.Text("", size=20),
                #self.tolerance_input,
                self.T,
                ft.Text("", size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def update_inputs(self, e):
        num_eqs = int(self.num_eqs_input.value)
        num_vars = int(self.num_vars_input.value)

        self.equations_container.controls = [ft.TextField(label=f"Équation {i+1}", multiline=True, width=600, hint_text="Ex: x0**2 + x1**2 - 1") for i in range(num_eqs)]
        self.initial_guess_container.controls = [ft.Row([ft.TextField(label=f"x0[{i}]", hint_text="Ex: 0.0", width=200),
                                                        ft.IconButton(icon=ft.icons.MIC, on_click=lambda e, i=i: self.open_modal_dialog(e, i))],
                                                    alignment=ft.MainAxisAlignment.CENTER) for i in range(num_vars)]
        self.page.update()

    def open_num_eqs_dialog(self, e):
        self.num_eqs_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Parler pour le nombre d'équations"),
            content=ft.Text("En cours de développement... Trouver le code dans test/test.py"),#ft.TextField(hint_text="Dites le nombre d'équations"),
            actions=[
                #ft.TextButton("Confirmer", on_click=self.confirm_num_eqs),
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
            content= ft.Text("En cours de développement... Trouver le code dans test/test.py"), #ft.TextField(hint_text="Dites le nombre de composants de X0"),
            actions=[
                #ft.TextButton("Confirmer", on_click=self.confirm_num_vars),
                ft.TextButton("Fermer", on_click=lambda e: self.close_modal_dialog(self.num_vars_dialog))
            ]
        )
        self.page.dialog = self.num_vars_dialog
        self.num_vars_dialog.open = True
        self.page.update()

    def open_modal_dialog(self, e, i):
        modal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Parler pour x0[{i}]"),
            content=ft.Text("En cours de développement... Trouver le code dans test/test.py"),
            actions=[ft.TextButton("Fermer", on_click=lambda e: self.close_modal_dialog(modal_dialog))]
        )
        self.page.dialog = modal_dialog
        modal_dialog.open = True
        self.page.update()

    def close_modal_dialog(self, modal_dialog):
        modal_dialog.open = False
        self.page.update()

    def on_calculate_click(self, e):
        # Vérification des entrées et conversion initiale
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
        except ValueError as ex:
            self.solution_output.value = str(ex)
            self.page.auto_scroll = True
            self.page.update()
            return

        # Définir les symboles pour les variables
        symbols_list = symbols(f"x0:{num_vars}")

        # Créer un dictionnaire local contenant les symboles et les fonctions mathématiques
        math_map = {
            'sqrt': sqrt,
            'ln': log,
            'log': log,
            'sin': sin,
            'cos': cos,
            'exp': exp
        }

        local_dict = {str(symbol): symbol for symbol in symbols_list}
        local_dict.update(math_map)

        try:
            tolerance = float(sympify(self.tolerance_input.value, locals=local_dict))
        except ValueError as ex:
            self.solution_output.value = str(ex)
            self.page.auto_scroll = True
            self.page.update()
            return

        # Récupération des équations et des valeurs initiales
        equations = [eq_control.value for eq_control in self.equations_container.controls if eq_control.value.strip() != ""]
        initial_guess = [guess_control.controls[0].value for guess_control in self.initial_guess_container.controls if guess_control.controls[0].value.strip() != ""]

        try:
            initial_guess = [float(sympify(value, locals=local_dict)) for value in initial_guess]
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

        # Transformation des équations en expressions sympy
        try:
            equations_sym = [sympify(eq, locals=local_dict) for eq in equations]
        except Exception as ex:
            self.solution_output.color = ft.colors.RED
            self.solution_output.value = f"Erreur dans l'évaluation des équations : {str(ex)}"
            self.page.auto_scroll = False
            self.page.scroll_to(offset=-1, duration=100)
            self.page.update()
            return

        # Définir la fonction pour évaluer les équations
        def F(x):
            subs = dict(zip(symbols_list, x))
            return np.array([float(eq.evalf(subs=subs)) for eq in equations_sym], dtype=float)

        # Initialiser le tableau des valeurs initiales
        x0_array = np.array(initial_guess, dtype=float)

        # Résoudre les équations avec la méthode de Newton-Raphson
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
        self.page.scroll_to(delta= - 200, duration = 300)
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
    
    #M = ft.Row(controls= [ft.Text("                        ", size=20), solution_output])


    def create_output_area(self):
        return ft.Column(
            controls=[
                ft.Text("", size=20),
                #ft.Text("Résultats:", size=20),
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
                #ft.Row(ft.Text("                        ", size=20),self.solution_output,)
                #self.solution_output,
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

    footer_cont = ft.Container(
        content=ft.Text(
            "© HKDE",
            style=ft.TextStyle(
                size=10,
                weight=ft.FontWeight.BOLD,
                foreground=ft.Paint(
                    gradient=ft.PaintLinearGradient(
                        (0, 0), (50, 0), [ft.colors.ORANGE, ft.colors.BLUE_200]
                    )
                ),
            ),
            italic=True,
        ),
        alignment=ft.Alignment(-1.0, 1.0),
        bgcolor=ft.colors.TRANSPARENT,
        padding=10
    )
    t = ft.Text("", size=5, color=ft.colors.BLUE_GREY_100)
    rowf = ft.Row([footer_cont, t],
                    ft.Alignment(-1.0, 1.0), scroll= None)
    
    page.add(rowf)
