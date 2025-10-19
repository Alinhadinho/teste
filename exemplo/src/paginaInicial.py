import flet as ft
# A lista e função importadas ainda são necessárias se você mantiver 
# qualquer lógica de ocorrências aqui, mas serão removidas da visualização.


def view(page: ft.Page):
    # ------------------- Lista de ocorrências (REMOVIDA DA VIEW) -------------------
    # Mantemos a variável prodList (embora não a usaremos mais na UI desta página)
    # ou simplesmente a removemos, focando apenas no layout.

    # ------------------- Funções de navegação -------------------
    def cliqueMenu(e):
        page.drawer.open = True
        page.update()
        
    def irParaFormulario(e):
        page.go("/form")
    
    def irParaAcompanhamento(e):
        page.go("/acompanhamento")

    # ------------------- AppBar -------------------
    appBar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=cliqueMenu),
        title=ft.Text("Página Inicial"),
        center_title=True,
        actions=[
            ft.IconButton(icon=ft.Icons.SEARCH, on_click=irParaAcompanhamento),
            ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda _: page.go("/")),
        ],
    )

    # ------------------- Botões centralizados -------------------
    botoes = ft.Column(
        [
            # Botão 1: Nova Ocorrência
            ft.ElevatedButton("Nova Ocorrência", icon=ft.Icons.ADD, width=250, on_click=irParaFormulario),
            # Botão 2: Acompanhar Ocorrências (usando o ícone corrigido HISTORY)
            ft.ElevatedButton("Acompanhar Ocorrências", icon=ft.Icons.HISTORY, width=250, on_click=irParaAcompanhamento),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ------------------- Conteúdo principal (Centralizado) -------------------
    # Criamos um Container para centralizar o conteúdo na tela
    conteudo_central = ft.Container(
        content=ft.Column(
            [
                ft.Text("Bem-vindo!", size=40, weight=ft.FontWeight.BOLD),
                ft.Text("O que você gostaria de fazer hoje?", size=18, color=ft.Colors.WHITE70),
                ft.Container(height=30), # Espaçamento
                botoes,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        expand=True,
        alignment=ft.alignment.center
    )
    
    # ------------------- Footer fixo -------------------
    footer = ft.Container(
        content=ft.Text("© 2025 - Meu App | Todos os direitos reservados", size=12, color=ft.Colors.GREY),
        alignment=ft.alignment.center,
        padding=10,
    )

    # ------------------- Layout principal (Simplificado) -------------------
    layout = ft.Column(
        [
            conteudo_central, # Ocupa a maior parte da tela e centraliza o conteúdo
            footer          # Fixo na parte inferior
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Nota: A função 'popular_lista_ocorrencias' foi removida, 
    # e page.on_view_change não é mais necessário aqui.
    
    return ft.View(
        route="/home",
        controls=[
            appBar,
            layout,
        ]
    )