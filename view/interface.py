from service.generate import CertifyMaker
import flet as ft

class Interface:
    def main(self, page: ft.Page):
        page.window.alignment = ft.Alignment.CENTER
        page.window.maximizable = False
        page.window.resizable = False
        page.window.shadow = False
        page.window.width = 826
        page.window.height = 544
        page.title = "Certificador de archivos"

        def create_inputField(text_prev: str) -> ft.TextField:
            return ft.TextField(label=text_prev, multiline=False, smart_dashes_type=True)
            
        def create_label(label_text: str, font_size: int) -> ft.Text:
            return ft.Text(value=label_text, size=font_size)

        def certify_task(e: ft.Event[ft.Button]):
            extension_list.controls=[]
            result = CertifyMaker(input_path.value, input_fileName.value).process()
            for item in result:
                ext = str(item.get("extension")).upper()
                inc_item = f"{ext } = {item.get("conteo")}"
                extension_list.controls.append(ft.Text(inc_item))

        def clean_components(e: ft.Event[ft.Button]):
            state_totalStorage.value="-"
            state_usedStorage.value="-"
            state_freeStorage.value="-"
            input_path.value=""
            input_fileName.value=""
            extension_list.controls=[]

        # Global Variables
        font_label = 16

        # Status Column
        label_status = create_label("Estado actual:", font_label)
        status_field = ft.ListView(
            height=72,
            controls=[]
        )

        # Input Column
        label_path = create_label("Direccion raiz:", font_label)
        input_path = create_inputField(text_prev="G:/")
        label_fileName = create_label("Nombre de salida:", font_label)
        input_fileName = create_inputField(text_prev="CERTIFICACION-16_04_25")
        make_button = ft.Button(content="Certificar", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder()), on_click=certify_task)
        clean_button = ft.Button(content="Limpiar", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder()), on_click=clean_components)

        # Output Column
        label_totalStorage = create_label("Espacio Total:", font_label)
        state_totalStorage = create_label("-", font_size=18)
        label_usedStorage = create_label("Espacio Utilizado:", font_label)
        state_usedStorage = create_label("-", font_size=18)
        label_freeStorage = create_label("Espacio Disponible:", font_label)
        state_freeStorage = create_label("-", font_size=18)
        label_extensionList = create_label("Lista de archivos y extensiones:", font_label)
        extension_list = ft.ListView(
            height=200,
            controls=[]
        )

        make_button.on_click
        clean_button.on_click

        page.add(
            ft.Container(
                border= ft.Border.all(1, ft.Colors.RED),
                padding=24,
                expand=True,
                content=
                ft.Column(
                    controls=[
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            spacing=24,
                            tight=True,
                            controls=[
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.START,
                                    intrinsic_width=True,
                                    tight=True,
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
                                        ft.Row(
                                            controls=[
                                                make_button,
                                                clean_button
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            expand=True
                                        )
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            # Space between storage stats and item list component
                                            spacing=24,
                                            controls=[
                                                ft.Column(
                                                    controls=[
                                                        label_totalStorage,
                                                        state_totalStorage
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                                ft.Column(
                                                    controls=[
                                                        label_usedStorage,
                                                        state_usedStorage
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                                ft.Column(
                                                    controls=[
                                                        label_freeStorage,
                                                        state_freeStorage
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                label_extensionList,
                                                ft.Container(
                                                    content=extension_list,
                                                    border=ft.Border.all(1, ft.Colors.BLACK),
                                                    expand=True,
                                                    padding=16
                                                )
                                            ],
                                            expand=True
                                        )
                                    ],
                                    tight=True,
                                    intrinsic_width=True,
                                    alignment=ft.MainAxisAlignment.START
                                )
                            ]
                        )
                    ],
                    intrinsic_width=True,
                    tight=True,
                    alignment=ft.MainAxisAlignment.START
                )
            )
        )