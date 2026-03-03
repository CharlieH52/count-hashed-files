import flet as ft

class Interface:
    def main(self, page: ft.Page):
        page.window.alignment = ft.Alignment.CENTER
        page.window.maximizable = False
        page.window.resizable = False
        page.window.shadow = False
        page.window.width = 300
        page.window.height = 300
        page.title = "Certificador de archivos"

        def create_inputField() -> ft.TextField:
            return ft.TextField(multiline=False)
            
        def create_label(label_text: str) -> ft.Text:
            return ft.Text(value=label_text)

        input_path = create_inputField()
        input_fileName = create_inputField()
        make_button = ft.Button(content="Certificar")
        label_path = create_label("Direccion raiz:")
        label_fileName = create_label("Nombre del archivo:")
        
        page.add(
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[
                            label_path,
                            input_path
                        ]
                    ),
                    ft.Column(
                        controls=[
                            label_fileName,
                            input_fileName
                        ]
                    ),
                    make_button
                ]
            )
        )