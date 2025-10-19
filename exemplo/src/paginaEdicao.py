import flet as ft
import datetime
import database

def view(page: ft.Page, ocorrencia_id: int):
    # Carrega os dados da ocorrência com base no ID
    ocorrencia_data = database.get_ocorrencia_by_id(ocorrencia_id)
    
    if not ocorrencia_data:
        page.go("/acompanhamento")
        return ft.View(route="/editar")
    
    # Extrai os dados para preencher os campos
    id_registro = ocorrencia_data["id"]
    titulo_inicial = ocorrencia_data["titulo"]
    desc_inicial = ocorrencia_data["descricao"]
    status_inicial = ocorrencia_data["status"]
    data_inicial = ocorrencia_data["data"]

    # 1. Date Picker
    data_ocorrencia_display = ft.TextField(
        label="Data da Ocorrência",
        read_only=True,
        filled=True,
        value=data_inicial,
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
        value=titulo_inicial,
        filled=True,
    )
    ocorrencia_desc = ft.TextField(
        label="Descrição Detalhada",
        value=desc_inicial,
        multiline=True,
        max_lines=5,
        filled=True,
    )
    
    status_dropdown = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("Aberta"),
            ft.dropdown.Option("Em Andamento"),
            ft.dropdown.Option("Fechada"),
        ],
        value=status_inicial,
    )

    # 3. Funções de Ação e Modal de Confirmação
    
    # Define o modal antes da função que o utiliza, para evitar NameError
    confirm_dialog = ft.AlertDialog(modal=True) 
    
    def deletar_ocorrencia_confirmada(e):
        page.close(confirm_dialog)
        
        database.delete_ocorrencia(id_registro) 

        page.snack_bar = ft.SnackBar(
            ft.Text("🗑️ Ocorrência excluída com sucesso!"),
            duration=2000,
            bgcolor=ft.Colors.YELLOW_600,
        )
        page.snack_bar.open = True
        page.update()
        page.go("/acompanhamento") 
        
    # Finaliza a definição do Modal
    confirm_dialog.title = ft.Text("Confirmar Exclusão")
    confirm_dialog.content = ft.Text("Tem certeza que deseja apagar esta ocorrência permanentemente?")
    confirm_dialog.actions = [
        ft.TextButton("Cancelar", on_click=lambda e: page.close(confirm_dialog)),
        ft.TextButton("Apagar", 
                      on_click=deletar_ocorrencia_confirmada, 
                      style=ft.ButtonStyle(color=ft.Colors.RED_ACCENT_700)),
    ]
    confirm_dialog.actions_alignment = ft.MainAxisAlignment.END


    def salvar_edicao(e):
        if not (ocorrencia_titulo.value and ocorrencia_desc.value and data_ocorrencia_display.value):
            page.snack_bar = ft.SnackBar(
                ft.Text("⚠️ Por favor, preencha todos os campos."),
                duration=3000,
                bgcolor=ft.Colors.RED_400,
            )
            page.snack_bar.open = True
            page.update()
            return

        database.update_ocorrencia(
            id_registro, 
            ocorrencia_titulo.value,
            ocorrencia_desc.value,
            status_dropdown.value,
            data_ocorrencia_display.value
        )

        page.snack_bar = ft.SnackBar(
            ft.Text("✅ Ocorrência atualizada com sucesso!"),
            duration=2000,
            bgcolor=ft.Colors.BLUE_ACCENT_700,
        )
        page.snack_bar.open = True
        page.update()
        page.go("/acompanhamento")

    def deletar_ocorrencia(e):
        # Abre o modal de confirmação
        page.open(confirm_dialog)
        page.update()
        
    # 4. Layout da Página
    return ft.View(
        route=f"/edit/{id_registro}",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Editar Ocorrência #{id_registro}"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/acompanhamento")),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Detalhes da Ocorrência #{id_registro}:", size=18, weight=ft.FontWeight.BOLD),
                        ocorrencia_titulo,
                        ocorrencia_desc,
                        ft.Row([data_ocorrencia_display], alignment=ft.MainAxisAlignment.CENTER),
                        status_dropdown,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            text="Salvar Edição",
                            icon=ft.Icons.SAVE,
                            on_click=salvar_edicao,
                            width=300,
                            height=50,
                            bgcolor=ft.Colors.BLUE_ACCENT_700,
                            color=ft.Colors.WHITE,
                        ),
                        ft.OutlinedButton(
                            text="Excluir Ocorrência",
                            icon=ft.Icons.DELETE_FOREVER,
                            on_click=deletar_ocorrencia,
                            width=300,
                            height=50,
                            style=ft.ButtonStyle(color=ft.Colors.RED_ACCENT_700),
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