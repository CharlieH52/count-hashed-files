from service.generate import CertifyMaker
from service.file_validator import Validator
from typing import Any
import flet as ft

class Interface:
    def main(self, page: ft.Page):
        page.window.alignment = ft.Alignment.CENTER
        page.window.maximizable = False
        page.window.resizable = False
        page.window.shadow = False
        page.window.width = 808
        page.window.height = 584
        page.title = "Certificador de archivos"

        # COMPONENT FUNCTIONS
        def __add_new_status(message: str):
            text_obj = ft.Text(value=message)
            status_field.controls.append(text_obj)
            status_field.update()

        def __create_inputField(text_prev: str) -> ft.TextField:
            return ft.TextField(label=text_prev, multiline=False, smart_dashes_type=True)
            
        def __create_label(label_text: str, font_size: int) -> ft.Text:
            return ft.Text(value=label_text, size=font_size)

        def __create_modal(modal_title: str, modal_content: str) -> ft.AlertDialog:
            return ft.AlertDialog(
                modal=True,
                title=__create_label(modal_title, 16),
                content=__create_label(modal_content, 16),
                actions=[
                    ft.TextButton("Aceptar", on_click=lambda e: page.pop_dialog())
                    ],
                actions_alignment=ft.MainAxisAlignment.CENTER
                )

        # LOGIC FUNCTIONS
        def __get_total_files(file_list_obj: list[dict[str,int]]) -> int:
            files = 0
            for item in file_list_obj:
                value = item.get("conteo")
                assert value is not None
                files = files + int(value)
            return files

        def __get_file_list(file_list_obj: list[dict[str,Any]]):
            for item in file_list_obj:
                ext = str(item.get("extension")).upper()
                inc_item = f"{ext} = {item.get("conteo")}"
                extension_list.controls.append(ft.Text(inc_item))

        def __validations() -> str | None:
            path = input_path.value
            file = input_fileName.value
            val = Validator(path, file)
            if len(path) < 2:
                return "Escribe una ruta valida."
            
            if not val.valid_dir_path():
                return "No se encontro el directorio especificado. Verifica que exista o que cuente con permisos de lectura."

            if len(file) < 5:
                return "El nombre del archivo es demasiado corto."
            
            if not val.valid_file_name():
                return "El nombre del archivo ya existe. Intenta agregar un sufijo."
            
            return None

        def __certify_process():
            extension_list.controls=[]
            __disable_components(True)
            state_modal = __create_modal("Mensaje de estado", "Certificacion completada con exito.")

            __add_new_status("Iniciando certificacion")

            __add_new_status("Proceso de lectura, esto puede tardar algunos minutos...")
            cm = CertifyMaker(input_path.value, input_fileName.value)
            counted_files = cm.get_file_extension_list()

            __add_new_status("Generando conteos")
            __get_file_list(counted_files)
            label_files.value = str(__get_total_files(counted_files))

            __add_new_status("Calculando tamaños de informacion")
            state_usedStorage.value = cm.get_used_space()
            state_totalStorage.value = cm.get_logical_drive_size()
            state_freeStorage.value = cm.get_logical_drive_free_space()

            __add_new_status("Certificacion completada")
            page.show_dialog(state_modal)
            __disable_components(False)
            page.update()

        def __validation_task(e: ft.Event[ft.Button]):
            error = __validations()

            if error:
                __add_new_status(error)
                return
            
            __certify_process()

        def __clean_components(e: ft.Event[ft.Button]):
            state_totalStorage.value="-"
            state_usedStorage.value="-"
            state_freeStorage.value="-"
            label_files.value = "-"
            input_path.value=""
            input_fileName.value=""
            extension_list.controls.clear()
            status_field.controls.clear()

        def __disable_components(component_state: bool):
            controls = [
                input_fileName,
                input_path,
                make_button,
                clean_button,
            ]
            for control in controls:
                control.disabled = component_state
            page.update()

        # Global Variables
        font_label = 16
        font_big_label = 18
        font_count_label = 24
        inner_padding = 16
        block_spacing = 24

        # Status Column
        label_status = __create_label("Estado actual:", font_label)
        status_field = ft.ListView(
            height=96,
            padding=inner_padding,
            reverse=True,
            controls=[]
        )

        # Input Column
        label_path = __create_label("Direccion raiz:", font_label)
        input_path = __create_inputField(text_prev="G:\\")
        label_fileName = __create_label("Nombre de salida:", font_label)
        input_fileName = __create_inputField(text_prev="CERTIFICACION-16_04_25")
        make_button = ft.Button(content="Certificar", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder()), on_click=__validation_task)
        clean_button = ft.Button(content="Limpiar", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder()), on_click=__clean_components)
        label_quantity = __create_label("Archivos contados:", font_label)
        label_files = __create_label("-", font_count_label)

        # Output Column
        label_totalStorage = __create_label("Espacio Total:", font_label)
        state_totalStorage = __create_label("-", font_big_label)
        label_usedStorage = __create_label("Espacio Utilizado:", font_label)
        state_usedStorage = __create_label("-", font_big_label)
        label_freeStorage = __create_label("Espacio Disponible:", font_label)
        state_freeStorage = __create_label("-", font_big_label)
        label_extensionList = __create_label("Lista de archivos y extensiones:", font_label)
        extension_list = ft.ListView(
            height=200,
            controls=[]
        )

        # CLICK EVENTS
        make_button.on_click
        clean_button.on_click

        # UI STRUCTURE
        page.add(
            ft.Container(
                border=ft.Border.all(1,ft.Colors.BLACK),
                padding=inner_padding,
                expand=True,
                content=
                ft.Column(
                    controls=[
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            spacing=block_spacing,
                            tight=True,
                            controls=[
                                ft.Column(
                                    spacing=block_spacing,
                                    alignment=ft.MainAxisAlignment.START,
                                    intrinsic_width=True,
                                    tight=True,
                                    controls=[
                                        ft.Column(
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
                                                )
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                make_button,
                                                clean_button
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            expand=True
                                        ),
                                        ft.Column(
                                            controls=[
                                                label_quantity,
                                                ft.Row(
                                                    controls=[
                                                        label_files       
                                                    ],
                                                    expand=True,
                                                    alignment=ft.MainAxisAlignment.CENTER
                                                )
                                            ],
                                            expand=True
                                        )
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            # Space between storage stats and item list component
                                            spacing=block_spacing,
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
                                                    padding=inner_padding
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
                        ),
                        ft.Column(
                            controls=[
                                label_status,
                                ft.Container(
                                    border=ft.Border.all(1,ft.Colors.BLACK),
                                    content=status_field
                                )
                            ],
                            expand=True
                        )
                    ],
                    spacing=block_spacing,
                    intrinsic_width=True,
                    tight=True,
                    alignment=ft.MainAxisAlignment.START
                )
            )
        )