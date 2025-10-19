import flet as ft

def view(page: ft.Page):
    usuario = ft.TextField(
        label="Usuário",
        width=300,
        border_radius=10,
        filled=True,
        bgcolor=ft.Colors.WHITE
    )
    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=10,
        filled=True,
        bgcolor=ft.Colors.WHITE
    )
    mensagemLogin = ft.Text(value="", size=16, weight=ft.FontWeight.BOLD)

    def loginClick(e):
        if usuario.value == "usuario" and senha.value == "senha":
            mensagemLogin.value = "Logado"
            mensagemLogin.color = ft.Colors.GREEN_ACCENT
            page.go("/home")
        else:
            mensagemLogin.value = "Usuário ou senha incorretos"
            mensagemLogin.color = ft.Colors.RED
        page.update()

    return ft.View(
        route="/",
        controls=[
            ft.AppBar(title=ft.Text("Sprint")),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Login!", size=36, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Digite seu Usuário e Senha", size=18, color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER),
                        usuario,
                        senha,
                        ft.ElevatedButton(
                            text="Login",
                            on_click=loginClick,
                            width=300,
                            height=50,
                            bgcolor=ft.Colors.BLUE_ACCENT_700,
                            color=ft.Colors.WHITE,
                        ),
                        mensagemLogin,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(30),
                border_radius=20,
                width=360,
                height=450,
                alignment=ft.alignment.center,
            ),
        ],
    )
