import flet as ft

def main(page: ft.Page):
    page.title = "Calculadora de Leyes de Física"
    page.window_width = 500
    page.window_height = 700
    page.theme_mode = "dark"

    formulas = {
        "Ley de Coulomb": {
            "Fuerza (F)": "F = (k * q1 * q2) / r²",
            "Carga 1 (q1)": "q1 = (F * r²) / (k * q2)",
            "Carga 2 (q2)": "q2 = (F * r²) / (k * q1)",
            "Distancia (r)": "r = √((k * q1 * q2) / F)"
        },
        "Ley de Gauss": {
            "Flujo eléctrico (Φ)": "Φ = E * A",
            "Campo eléctrico (E)": "E = Φ / A",
            "Área (A)": "A = Φ / E"
        },
        "Energía Potencial": {
            "Energía (U)": "U = q * V",
            "Carga (q)": "q = U / V",
            "Voltaje (V)": "V = U / q"
        }
    }

    unidades = {
        "Ley de Coulomb": {
            "Fuerza (F)": "N (Newton)",
            "Carga 1 (q1)": "C (Coulombs)",
            "Carga 2 (q2)": "C (Coulombs)",
            "Distancia (r)": "m (metros)"
        },
        "Ley de Gauss": {
            "Flujo eléctrico (Φ)": "Nm²/C (Newton metro cuadrado por Coulomb)",
            "Campo eléctrico (E)": "N/C (Newton por Coulomb)",
            "Área (A)": "m² (metros cuadrados)"
        },
        "Energía Potencial": {
            "Energía (U)": "J (Joules)",
            "Carga (q)": "C (Coulombs)",
            "Voltaje (V)": "V (Volts)"
        }
    }

    ley_seleccionada = ""
    variable_seleccionada = ""
    inputs = []

    def calcular_resultado(e, ley, variable_calculada):
        global inputs
        try:
            valores = [input.value.strip() for input in inputs]
            valores_float = [float(value) for value in valores]

            # Comprobar si hay algún valor inválido
            if len(valores_float) < len(inputs):
                resultado_text.value = "Por favor, completa todos los campos."
                page.update()
                return
            
            k = 8.99e9  # Constante de Coulomb

            if ley == "Ley de Coulomb":
                if variable_calculada == "Fuerza (F)":
                    q1, q2, r = valores_float
                    resultado = (k * q1 * q2) / (r ** 2)
                elif variable_calculada == "Carga 1 (q1)":
                    F, q2, r = valores_float
                    resultado = (F * (r ** 2)) / (k * q2)
                elif variable_calculada == "Carga 2 (q2)":
                    F, q1, r = valores_float
                    resultado = (F * (r ** 2)) / (k * q1)
                elif variable_calculada == "Distancia (r)":
                    F, q1, q2 = valores_float
                    resultado = ((k * q1 * q2) / F) ** 0.5

            elif ley == "Ley de Gauss":
                if variable_calculada == "Flujo eléctrico (Φ)":
                    E, A = valores_float
                    resultado = E * A
                elif variable_calculada == "Campo eléctrico (E)":
                    Φ, A = valores_float
                    resultado = Φ / A
                elif variable_calculada == "Área (A)":
                    Φ, E = valores_float
                    resultado = Φ / E

            elif ley == "Energía Potencial":
                if variable_calculada == "Energía (U)":
                    q, V = valores_float
                    resultado = q * V
                elif variable_calculada == "Carga (q)":
                    U, V = valores_float
                    resultado = U / V
                elif variable_calculada == "Voltaje (V)":
                    U, q = valores_float
                    resultado = U / q

            resultado_text.value = f"Resultado: {resultado:.2e} [{unidades[ley][variable_calculada]}]"
        except ValueError:
            resultado_text.value = "Por favor, ingresa valores válidos en todos los campos."
        except ZeroDivisionError:
            resultado_text.value = "Error: División por cero. Revisa los valores ingresados."
        
        page.update()



    def mostrar_menu_principal(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Calculadora de Leyes de Física", size=30, color="white", weight="bold", text_align=ft.TextAlign.CENTER),
                    ft.Dropdown(
                        label="Selecciona una ley",
                        options=[ft.dropdown.Option("Ley de Coulomb"), ft.dropdown.Option("Ley de Gauss"), ft.dropdown.Option("Energía Potencial")],
                        on_change=lambda e: mostrar_menu_variables(e.control.value)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()

    def mostrar_menu_variables(ley):
        global ley_seleccionada
        ley_seleccionada = ley
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text(f"{ley_seleccionada}", size=30, color="white", weight="bold", text_align=ft.TextAlign.CENTER),
                    ft.Dropdown(
                        label="Selecciona la variable a calcular",
                        options=[ft.dropdown.Option(var) for var in formulas[ley_seleccionada].keys()],
                        on_change=lambda evt: mostrar_formulario(ley_seleccionada, evt.control.value)
                    ),
                    ft.Row(
                        [ft.ElevatedButton("Volver al Menú de Leyes", on_click=mostrar_menu_principal)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()

    def mostrar_formulario(ley, variable_calculada):
        global variable_seleccionada, inputs
        variable_seleccionada = variable_calculada
        formula_text.value = f"Usando la fórmula: {formulas[ley][variable_calculada]}"
        titulo_text.value = f"{ley} - {variable_calculada}"

        if ley == "Ley de Coulomb":
            if variable_calculada == "Fuerza (F)":
                inputs = [ft.TextField(label="Carga 1 (q1) [Coulombs]"), ft.TextField(label="Carga 2 (q2) [Coulombs]"), ft.TextField(label="Distancia (r) [Metros]")]
            elif variable_calculada == "Carga 1 (q1)":
                inputs = [ft.TextField(label="Fuerza (F) [Newtons]"), ft.TextField(label="Carga 2 (q2) [Coulombs]"), ft.TextField(label="Distancia (r) [Metros]")]
            elif variable_calculada == "Carga 2 (q2)":
                inputs = [ft.TextField(label="Fuerza (F) [Newtons]"), ft.TextField(label="Carga 1 (q1) [Coulombs]"), ft.TextField(label="Distancia (r) [Metros]")]
            elif variable_calculada == "Distancia (r)":
                inputs = [ft.TextField(label="Fuerza (F) [Newtons]"), ft.TextField(label="Carga 1 (q1) [Coulombs]"), ft.TextField(label="Carga 2 (q2) [Coulombs]")]
        elif ley == "Ley de Gauss":
            if variable_calculada == "Flujo eléctrico (Φ)":
                inputs = [ft.TextField(label="Campo eléctrico (E) [N/C]"), ft.TextField(label="Área (A) [m²]")]
            elif variable_calculada == "Campo eléctrico (E)":
                inputs = [ft.TextField(label="Flujo eléctrico (Φ) [Nm²/C]"), ft.TextField(label="Área (A) [m²]")]
            elif variable_calculada == "Área (A)":
                inputs = [ft.TextField(label="Flujo eléctrico (Φ) [Nm²/C]"), ft.TextField(label="Campo eléctrico (E) [N/C]")]
        elif ley == "Energía Potencial":
            if variable_calculada == "Energía (U)":
                inputs = [ft.TextField(label="Carga (q) [Coulombs]"), ft.TextField(label="Voltaje (V) [Volts]")]
            elif variable_calculada == "Carga (q)":
                inputs = [ft.TextField(label="Energía (U) [Joules]"), ft.TextField(label="Voltaje (V) [Volts]")]
            elif variable_calculada == "Voltaje (V)":
                inputs = [ft.TextField(label="Energía (U) [Joules]"), ft.TextField(label="Carga (q) [Coulombs]")]

        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text(f"{ley} - {variable_calculada}", size=24, color="white", weight="bold"),
                    formula_text,
                    *inputs,
                    resultado_text,
                    ft.Row(
                        [
                            ft.ElevatedButton("Calcular", on_click=lambda e: calcular_resultado(e, ley, variable_calculada)),
                            ft.ElevatedButton("Limpiar Campos", on_click=lambda e: limpiar_campos(inputs))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    ft.Row(
                        [ft.ElevatedButton("Volver al Menú de Leyes", on_click=mostrar_menu_principal)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()

    def limpiar_campos(inputs):
        for input in inputs:
            input.value = ""
        resultado_text.value = "Resultado: "
        page.update()

    titulo_text = ft.Text("", size=24, color="white", weight="bold")
    formula_text = ft.Text("", size=18, color="lightgray")
    resultado_text = ft.Text("Resultado: ", size=20, color="green")

    mostrar_menu_principal()

ft.app(target=main)
