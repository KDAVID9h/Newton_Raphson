import flet as ft
import numpy as np
from sympy import symbols, sympify, diff
from ui.widgets import initial_guess_values, equations_id, num_eqs_input_id, num_vars_input_id, tolerance_id
from solver.newton_raphson import NewtonRaphsonSolver

def on_calculate_click(e):
    page = e.page
    num_eqs_input = num_eqs_input_id
    num_vars_input = num_vars_input_id
    tolerance_input = tolerance_id
    
    equations = equations_id
    initial_guess = initial_guess_values
    tolerance = float(tolerance_input.value)

    num_eqs = int(num_eqs_input.value)
    num_vars = int(num_vars_input.value)

    eqs = [eq.value for eq in equations[:num_eqs]]
    x0 = [float(guess.value) for guess in initial_guess[:num_vars]]
    
    symbols_list = symbols(f"x0:{num_vars}")
    equations_sym = [sympify(eq, locals=dict(zip(symbols_list, symbols_list))) for eq in eqs]

    def F(x):
        subs = dict(zip(symbols_list, x))
        return np.array([eq.evalf(subs=subs) for eq in equations_sym])

    def jacobian(x):
        J = []
        for eq in equations_sym:
            row = [diff(eq, var).evalf(subs=dict(zip(symbols_list, x))) for var in symbols_list]
            J.append(row)
        return np.array(J)

    x0_array = np.array(x0)

    try:
        solution = NewtonRaphsonSolver(F, jacobian, x0_array, tol=tolerance)
        page.controls[2].controls[1].value = f"Solution: {solution}"
    except Exception as ex:
        page.controls[2].controls[1].value = str(ex)

    page.update()

def on_reset_click(e):
    print('je fonctionne')
    page = e.page
    page.controls[0].controls[1].value = ""
    page.controls[0].controls[2].value = ""
    page.controls[0].controls[4].controls.clear()
    page.controls[0].controls[5].controls.clear()
    page.controls[0].controls[6].value = ""
    page.controls[2].controls[1].value = ""
    page.update()

'''import flet as ft
import numpy as np
from sympy import symbols, sympify, diff
from solver.newton_raphson import NewtonRaphsonSolver
#from ui.handlers import on_calculate_click, on_reset_click

def create_input_fields(page: ft.Page):
	num_eqs_input = ft.TextField(label="Nombre d'équations", keyboard_type="number", width= 300)
	mic_button1 = ft.IconButton(icon=ft.icons.MIC, on_click=lambda e: print("Microphone cliqué"))
	row1 = ft.Row([num_eqs_input, mic_button1])

	num_vars_input = ft.TextField(label="Nombre de composant de X0", keyboard_type="number", width= 300)
	mic_button2 = ft.IconButton(icon=ft.icons.MIC, on_click=lambda e: print("Microphone cliqué"))
	row2 = ft.Row([num_vars_input, mic_button2])

	equations_container = ft.Column()

	initial_guess_container = ft.Column()

	# Créez une fonction pour ouvrir la boîte de dialogue modale
	def open_modal_dialog(e, i):
		# Créez la boîte de dialogue modale
		modal_dialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(f"Parler pour x0[{i}]"),
			content=ft.Text("En cours de développement..."),
			actions=[
				ft.TextButton("Fermer", on_click=lambda e: close_modal_dialog(modal_dialog))
			]
		)
		# Ouvrez la boîte de dialogue modale
		page.dialog = modal_dialog
		modal_dialog.open = True
		page.update()

	# Fonction pour fermer la boîte de dialogue modale
	def close_modal_dialog(modal_dialog):
		modal_dialog.open = False
		#page.dialog = None
		page.update()

	def update_inputs(e):
		nonlocal equations_container, initial_guess_container
		num_eqs = int(num_eqs_input.value)
		num_vars = int(num_vars_input.value)

		equations_container.controls = [ft.TextField(label=f"Équation {i+1}",
													multiline=True,
													width= 600,
													hint_text="Ex: x0**2 + x1**2 - 1")
													for i in range(num_eqs)]
		initial_guess_container.controls = [
			ft.Row([
				ft.TextField(label=f"x0[{i}]", hint_text="EX: 0.0", width=200),
				ft.IconButton(icon=ft.icons.MIC, on_click=lambda e, i=i: open_modal_dialog(e, i))
			]) for i in range(num_vars)
		]
		e.page.update()

	generate_inputs_button = ft.ElevatedButton(text="Générer les champs", on_click=update_inputs)

	tolerance_input = ft.TextField(label="Tolérance", hint_text="Ex: 0.0001", width= 200)

	global num_eqs_input_id; global num_vars_input_id; global tolerance_id
	global equations_id; global initial_guess_values
	num_eqs_input_id = num_eqs_input.value; num_vars_input_id = num_vars_input.value
	tolerance_id = tolerance_input.value; equations_id = [eq_control.value for eq_control in equations_container.controls]
	initial_guess_values = [guess_control.controls[0].value for guess_control in initial_guess_container.controls]

	return ft.Column(
		controls=[
			ft.Text("Entrez vos équations non linéaires:", size=20),
			row1,
			row2,
			generate_inputs_button,
			equations_container,
			initial_guess_container,
			tolerance_input,
		]
	)

sol = ft.TextField(label="Solution", multiline=True, read_only=True, width=300)

def on_calculate_click(e):
    page = e.page
    num_eqs_input = num_eqs_input_id
    num_vars_input = num_vars_input_id
    tolerance_input = tolerance_id
    
    equations = equations_id
    initial_guess = initial_guess_values
    
	# Vérifiez si le champ de tolérance est vide
    if tolerance_input.strip() == "" and num_eqs_input.strip() == "" and num_vars_input.strip() == "":
        # ou en définissant une valeur par défaut
        tolerance_id = 'veillez remplire'
    else:
        try:
            # Si le champ n'est pas vide, convertissez la valeur en float
            tolerance = float(tolerance_input)
            num_eqs = int(num_eqs_input)
            num_vars = int(num_vars_input)
            print('cool')
            # ... le reste de votre code ...
        except ValueError:
            # Gérez le cas où la conversion échoue
            tolerance = 1


    eqs = [eq for eq in equations[:num_eqs]]
    x0 = [float(guess) for guess in initial_guess[:num_vars]]
    
    symbols_list = symbols(f"x0:{num_vars}")
    equations_sym = [sympify(eq, locals=dict(zip(symbols_list, symbols_list))) for eq in eqs]

    def F(x):
        subs = dict(zip(symbols_list, x))
        return np.array([eq.evalf(subs=subs) for eq in equations_sym])

    def jacobian(x):
        J = []
        for eq in equations_sym:
            row = [diff(eq, var).evalf(subs=dict(zip(symbols_list, x))) for var in symbols_list]
            J.append(row)
        return np.array(J)

    x0_array = np.array(x0)

    try:
        solution = NewtonRaphsonSolver(F, jacobian, x0_array, tol=tolerance)
        sol.value = f"Solution: {solution}"
    except Exception as ex:
        sol.value = str(ex)

    page.update()

def on_reset_click(e):
    print('je fonctionne')
    page = e.page
    page.controls[0].controls[1].value = ""
    page.controls[0].controls[2].value = ""
    page.controls[0].controls[4].controls.clear()
    page.controls[0].controls[5].controls.clear()
    page.controls[0].controls[6].value = ""
    page.controls[2].controls[1].value = ""
    page.update()

def create_buttons():
	return ft.Row(
		controls=[
			ft.ElevatedButton(text="Calculer", on_click=on_calculate_click),
			ft.ElevatedButton(text="Réinitialiser", on_click=on_reset_click),
		],
		alignment=ft.MainAxisAlignment.SPACE_AROUND
	)

def create_output_area():
	return ft.Column(
		controls=[
			ft.Text("Résultats:", size=20),
			sol,
			ft.Lottie(
				src="assets/lottie_animation.json",
				width=200,
				height=200,
				repeat=True,
				reverse=False
			),
		]
	)
'''