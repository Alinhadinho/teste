import flet as ft
# Importa a lista mock de ocorrências
import database # 👈 Importe o database

# Função utilitária para obter a cor do status
def get_status_color(status):
    if status == "Fechada":
        return ft.Colors.GREEN_600
    elif status == "Em Andamento":
        return ft.Colors.ORANGE_600
    else: # Aberta
        return ft.Colors.RED_600

# ... (imports e get_status_color) ...

def view(page: ft.Page):
    
    # ------------------- Lista de Cards de Acompanhamento -------------------
    cards_ocorrencias = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=15)

    # ------------------- Campo de Pesquisa -------------------
    search_field = ft.TextField(
        label="Pesquisar Ocorrência",
        hint_text="Digite o título ou descrição para filtrar...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: refresh_view(e, filter_text=e.control.value), # Chama o refresh com o texto do filtro
        filled=True,
        color=ft.Colors.WHITE,
    )
    # -----------------------------------------------------------
    
    def get_status_color(status):
        # ... (função get_status_color como está) ...
        if status == "Fechada":
            return ft.Colors.GREEN_600
        elif status == "Em Andamento":
            return ft.Colors.ORANGE_600
        else: # Aberta
            return ft.Colors.RED_600

    # ------------------- Função de Refresh (Modificada) -------------------
    # Adicionamos um argumento opcional 'filter_text'
    def refresh_view(e, filter_text=""):
        # 1. Carrega as ocorrências do banco de dados
        ocorrencias = database.get_all_ocorrencias()

        # Adicionar filtro
        if filter_text:
            filter_text = filter_text.lower()
            # Filtra a lista se o texto de pesquisa estiver no título ou na descrição
            ocorrencias = [
                o for o in ocorrencias 
                if filter_text in o["titulo"].lower() 
                or filter_text in o["descricao"].lower()
            ]

        # Limpa e recria a lista com os dados mais recentes
        cards_ocorrencias.controls.clear()

        # 2. Usa a lista carregada (agora filtrada)
        if not ocorrencias:
            cards_ocorrencias.controls.append(
                ft.Text(
                    "Nenhuma ocorrência encontrada com o filtro aplicado." 
                    if filter_text else "Nenhuma ocorrência registrada ainda.", 
                    size=16, 
                    italic=True
                )
            )
        else:
            for ocorrencia in ocorrencias:
                # ----------------- MODIFICAÇÃO AQUI -----------------
                cards_ocorrencias.controls.append(
                    ft.Card(
                        # Adiciona o evento de clique para ir para a rota /edit/{id}
                        elevation=4,
                        content=ft.Container(
                            on_click=lambda e, id=ocorrencia["id"]: page.go(f"/edit/{id}"),
                            padding=15,
                            content=ft.Column(
                                [
                                    # Usa ocorrencia["titulo"] normalmente
                                    ft.Text(ocorrencia["titulo"], size=18, weight=ft.FontWeight.BOLD),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.ACCESS_TIME, size=16, color=ft.Colors.GREY),
                                            ft.Text(
                                                f'Status: {ocorrencia["status"]}',
                                                color=get_status_color(ocorrencia["status"]),
                                                weight=ft.FontWeight.BOLD
                                            ),
                                        ],
                                        spacing=5
                                    ),
                                    ft.Text(f'Descrição: {ocorrencia["descricao"][:70]}...', color=ft.Colors.BLACK54),
                                    # Opcional: Adicionar a Data
                                    ft.Text(f'Data: {ocorrencia["data"]}', size=12, color=ft.Colors.BLACK38),
                                ],
                                spacing=5
                            )
                        )
                    )
                )
        page.update()

# ... (restante da função view) ...

    # Chama a função de refresh na primeira vez que a view é carregada
    # e certifica-se de que o campo de pesquisa esteja limpo
    search_field.value = "" 
    refresh_view(None) 

    return ft.View(
        route="/acompanhamento",
        controls=[
            ft.AppBar(
                title=ft.Text("Acompanhamento de Ocorrências"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/home")),
                actions=[
                    ft.IconButton(ft.Icons.REFRESH, on_click=refresh_view, tooltip="Recarregar")
                ]
            ),
            ft.Container(
                content=ft.Column( # Adiciona um Column para o campo de pesquisa e a lista
                    [
                        search_field, # Campo de Pesquisa
                        cards_ocorrencias,
                    ],
                    expand=True,
                ),
                padding=ft.padding.all(15),
                expand=True
            )
        ]
    )