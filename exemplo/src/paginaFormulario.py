import flet as ft
import datetime
import database

def view(page: ft.Page):
    
    # 1. Date Picker
    data_ocorrencia_display = ft.TextField(
        label="Data da Ocorrência",
        read_only=True,  # só leitura para evitar digitação
        filled=True,
        hint_text="Selecione a data...",
        width=300,
        on_click=lambda _: page.open(date_picker)
    )

    def handle_date_selection(e):
        if e.control.value:
            data_formatada = e.control.value.strftime("%d/%m/%Y")
            data_ocorrencia_display.value = data_formatada
            page.update()

    date_picker = ft.DatePicker(
        on_change=handle_date_selection,
        first_date=datetime.datetime(2024, 1, 1),
        last_date=datetime.datetime.now(),
    )

    # 2. Campos do formulário
    ocorrencia_titulo = ft.TextField(
        label="Título da Ocorrência",
        hint_text="Ex: Lentidão no Sistema X",
        filled=True,
    )
    ocorrencia_desc = ft.TextField(
        label="Descrição Detalhada",
        hint_text="Descreva o problema em detalhes.",
        multiline=True,
        max_lines=5,
        filled=True,
    )
    
    status_dropdown = ft.Dropdown(
        label="Status",
        hint_text="Selecione o status da ocorrência",
        options=[
            ft.dropdown.Option("Aberta"),
            ft.dropdown.Option("Em Andamento"),
            ft.dropdown.Option("Fechada"),
        ],
        value="Aberta",
    )

    def adicionar_e_voltar(e):
        # Validação
        if not (ocorrencia_titulo.value and ocorrencia_desc.value and data_ocorrencia_display.value):
            page.snack_bar = ft.SnackBar(
                ft.Text("⚠️ Por favor, preencha todos os campos e selecione a data."),
                duration=3000,
                bgcolor=ft.Colors.RED_400,
            )
            page.snack_bar.open = True
            page.update()
            return
            
        # 1. Inserção no banco de dados
        database.insert_ocorrencia(
            ocorrencia_titulo.value,
            ocorrencia_desc.value,
            status_dropdown.value,
            data_ocorrencia_display.value
        )

        # 2. Feedback de sucesso
        page.snack_bar = ft.SnackBar(
            ft.Text("✅ Ocorrência adicionada com sucesso!"),
            duration=2000,
            bgcolor=ft.Colors.GREEN,
        )
        page.snack_bar.open = True
        page.update() # Garante que o snackbar apareça

        # 3. Limpar os campos APÓS a submissão
        ocorrencia_titulo.value = ""
        ocorrencia_desc.value = ""
        status_dropdown.value = "Aberta"
        data_ocorrencia_display.value = ""
        date_picker.value = None # Reseta o valor do DatePicker
        
        # 4. Voltar para home APÓS a submissão
        page.go("/home")


    # ESTE BLOCO ABAIXO FOI REMOVIDO DA VIEW PARA NÃO EXECUTAR ANTES DA HORA
    # ocorrencia_titulo.value = ""
    # ocorrencia_desc.value = ""
    # status_dropdown.value = "Aberta"
    # data_ocorrencia_display.value = ""
    # date_picker.value = None
    # page.go("/home") 👈 ISSO CAUSAVA O BUG

    # 3. Layout da Página
    return ft.View(
        route="/form",
        controls=[
            ft.AppBar(
                title=ft.Text("Nova Ocorrência"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/home")),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Preencha os detalhes da sua nova ocorrência:", size=18, weight=ft.FontWeight.BOLD),
                        ocorrencia_titulo,
                        ocorrencia_desc,
                        ft.Row(
                            [
                                data_ocorrencia_display,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        status_dropdown,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            text="Adicionar Ocorrência",
                            on_click=adicionar_e_voltar,
                            width=300,
                            height=50,
                            bgcolor=ft.Colors.BLUE_ACCENT_700,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
                padding=ft.padding.all(30),
                expand=True,
                alignment=ft.alignment.top_center,
            ),
        ],
    )