import flet as ft
import Login
import paginaInicial
import paginaFormulario
import paginaAcompanhamento
import database
import paginaEdicao
import os # 👈 Importe o 'os'

def main(page: ft.Page):

    database.init_db()
    
    page.title = "Meu App"
    # Você pode remover as dimensões fixas para que 
    # ele se ajuste melhor ao navegador
    # page.window.height = 800
    # page.window.width = 400
    
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        if page.route == "/":
            page.views.append(Login.view(page))   # Tela de login
        elif page.route == "/home":
            page.views.append(paginaInicial.view(page))  # Tela principal
        elif page.route == "/form":
            page.views.append(paginaFormulario.view(page)) # Tela de formulário
        elif page.route == "/acompanhamento":
            page.views.append(paginaAcompanhamento.view(page)) # Tela de acompanhamento
        
        # CORREÇÃO: Deve ser 'elif' para fazer parte do bloco
        elif page.route.startswith("/edit"): 
            try:
                # Pega o ID da rota
                ocorrencia_id = int(page.route.split("/")[-1]) 
                page.views.append(paginaEdicao.view(page, ocorrencia_id))
            except (ValueError, IndexError):
                # Se o ID for inválido, volta para o acompanhamento
                page.go("/acompanhamento")
        
        # O bloco duplicado de rotas que estava aqui foi removido.
            
        page.update()
        
    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route) # Navega de volta para a rota anterior

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

# --- CONFIGURAÇÃO DE DEPLOY ---

# Pega a porta fornecida pelo Render (ou usa 8080 como padrão local)
port = int(os.getenv("PORT", 8080))

# Roda o app no modo WEB_BROWSER na porta designada
ft.app(
    target=main, 
    port=port, 
    view=ft.AppView.WEB_BROWSER
)