import flet as ft # pip install flet
from google import genai
from google.genai import types # pip install google-genai
from PIL import Image # pip install Pillow


def main(page: ft.Page):
    page.title = "Coordinate Suggestion App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    #FilePicker
    def pick_file_result(e: ft.FilePickerResultEvent):
        selected_files.value = e.files[0].path if e.files else ""
        selected_files.update()
    
    coordinate_path = ""

    def pick_file_result_main(e: ft.FilePickerResultEvent):
        nonlocal coordinate_path # needed if you want to modify the outer variable
        coordinate_path = e.files[0].path if e.files else ""
        print(f"Selected coordinate file: {coordinate_path}")

    file_picker = ft.FilePicker(
        on_result=pick_file_result
    )
    
    file_picker_main = ft.FilePicker(
        on_result=pick_file_result_main
    )

    selected_files = ft.Text("picked files here") # 選択されたファイル名を表示するテキスト
    pic_text = ft.Text("N/A") # 画像の説明を表示するテキスト


    #送信ボタン
    send_button = ft.ElevatedButton(
        "送信", icon=ft.Icons.SEND
    )

    send_button2 = ft.ElevatedButton(
        "Ask Gemini", icon=ft.Icons.SEND
    )

    # 入力フィールド
    input_field = ft.TextField(
        label="Ask Gemini",
        width=400,
        hint_text="input here",
        multiline=True,
        min_lines=2
    )

    # Markdown出力欄（中身は後で更新）
    output_markdown = ft.Markdown(
        value="N/A",
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data)
    )

    # Markdownを囲む青い枠＋スクロール対応
    output_dialog = ft.AlertDialog(
        title=ft.Text("提案されたコーディネート:"),
        actions=[
            ft.TextButton("閉じる", on_click=lambda e:page.close(output_dialog)),
        ],
        content=ft.Container( 
            ft.Container(
                content=ft.Column([output_markdown],scroll=ft.ScrollMode.ALWAYS),
                padding=10,
                border=ft.border.all(2, ft.Colors.INDIGO),
                border_radius=8,
                width=500,
                height=300,  # 固定高さ（超えたらスクロール）
            )
        )
    )

    # ボタンをローディング表示に切り替え
    def change_button(onchange, instruction_type):
        if instruction_type == 0:

            if (onchange==1):
                send_button.disabled = True
                send_button.icon = None
                send_button.text = ""
                send_button.content = ft.Row(
                    [ft.ProgressRing(width=16, height=16)],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            else:
                send_button.content = None
                send_button.icon = ft.Icons.SEND
                send_button.text = "送信"
                send_button.disabled = False

        elif   instruction_type == 1:
            if (onchange==1):
                send_button2.disabled = True
                send_button2.icon = None
                send_button2.text = ""
                send_button2.content = ft.Row(
                    [ft.ProgressRing(width=16, height=16)],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            else:          
                send_button2.content = None
                send_button2.icon = ft.Icons.SEND
                send_button2.text = "Ask Gemini"
                send_button2.disabled = False

        page.update()

    # Gemini呼び出し関数
    def ask_gemini_coordinate(input_text):
        try:
            with open("apikey.txt", "r", encoding='utf-8') as f:
                apiKEY = f.read()
            with open("promptC.txt", "r", encoding='utf-8') as f:
                prompt = f.read()
            with open("userinfo.txt", "r", encoding='utf-8') as f:
                userinfo = f.read()

            client = genai.Client(api_key=apiKEY)
            image = Image.open(coordinate_path) if coordinate_path else None

            if not image:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"「ユーザーが提示したアイテム」:【{input_text}】"],
                    config=types.GenerateContentConfig(
                        system_instruction=f"{prompt}\n尚、「ユーザー情報」は【\n{userinfo}\n】",
                    ),
                )
            else:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[image, f"「ユーザーが提示したアイテム」:【{input_text}】"],
                    config=types.GenerateContentConfig(
                        system_instruction=f"{prompt}\n尚、「ユーザー情報」は【\n{userinfo}\n】",
                    ),
                )
            return response.text
        
        except Exception as e:
            return f"ERROR: {e}"

    def ask_gemini_description():
        try:
            with open("apikey.txt", "r", encoding='utf-8') as f:
                apiKEY = f.read()
            with open("promptD.txt", "r", encoding='utf-8') as f:
                prompt = f.read()

            client = genai.Client(api_key=apiKEY)

            image = Image.open(selected_files.value)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[image, prompt]
            )
            return response.text
        except Exception as e:
            return f"ERROR: {e}"


    # 送信処理
    def interface_gemini(instruction_type):
        if instruction_type == 0:
            change_button(onchange=1, instruction_type=0)
            response = ask_gemini_coordinate(input_field.value)
            change_button(onchange=0, instruction_type=0)
            output_markdown.value = response
            page.open(output_dialog)  # ダイアログを設定
            # output_dialog.open = True  # ダイアログを開く

        elif instruction_type == 1:
            change_button(onchange=1, instruction_type=1)
            response = ask_gemini_description()
            change_button(onchange=0, instruction_type=1)
            pic_text.value = response
        page.update()

    # クリア処理
    def clear_fields(e):
        nonlocal coordinate_path
        coordinate_path = ""  # 選択された画像のパスをクリア
        selected_files.value = ""
        pic_text.value = "N/A"
        input_field.value = ""
        output_markdown.value = "N/A"
        page.update()


    #関数登録
    send_button.on_click = lambda e: interface_gemini(0)
    send_button2.on_click = lambda e: interface_gemini(1)

    # HOME page
    def show_route_page():
        page.overlay.append(file_picker_main)
        page.update()
        # ファイルピッカーをオーバーレイに追加して表示
        return ft.View(
            "/home",
            [
                ft.AppBar(
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda e: page.go("/settings"))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER)
                    ),

                ft.Column(
                    [
                        ft.Text("Coordinate Suggestion App", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text("version 0.1.5 | powered by gemini-2.0-flash", size=16),
                        ft.Divider(),
                        ft.Container(height=20),
                        ft.Text("入力:", size=14),
                        input_field,
                        ft.Container(height=20),
                        ft.Row(
                            [
                                send_button,
                                ft.OutlinedButton("クリア", on_click=clear_fields, icon=ft.Icons.CLEAR),
                                ft.OutlinedButton("アイテム登録", on_click=lambda e: page.go("/additems"), icon=ft.Icons.ADD),
                                ft.OutlinedButton(
                                    "参考にするコーデ", 
                                    icon=ft.Icons.UPLOAD_FILE,
                                    on_click=lambda e :file_picker_main.pick_files(
                                        allow_multiple=False,
                                        allowed_extensions=["jpg", "jpeg", "png", "bmp", "webp"]
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(height=20),
                        ft.Divider()
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
            ]
        )
    
    #settings page
    def show_settings_page():
        return ft.View(
            "/settings",
            [
                ft.Column(
                    [
                        ft.Divider(),
                        ft.Text("This is the page for settings"),
                        ft.ElevatedButton("Go Back", on_click=lambda e: page.go("/home")),
                        ft.Divider()
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                )
            ]
        )
    

    def show_additems_page():
        page.overlay.append(file_picker)
        page.update() # page.overlayへの追加を反映させる

        return ft.View(
            "/additems",
            [
                ft.Column(
                    [
                        ft.Divider(),
                        ft.Text("This is the page to adding items"),
                        # fileupload button
                        ft.ElevatedButton(
                            "pick a picture", 
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=lambda e :file_picker.pick_files(
                                allow_multiple=False,   
                                allowed_extensions=["jpg", "jpeg", "png", "bmp", "webp"])
                        ),
                        selected_files,
                        send_button2,
                        pic_text,
                        ft.Divider(),
                        ft.ElevatedButton("Go Back", on_click=lambda e: page.go("/home")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                )
            ]
        )
    
    def route_change(hnd):
        page.views.clear()
        if hnd.route == "/home":
            page.views.append(show_route_page())
        elif hnd.route == "/settings":
            page.views.append(show_settings_page())
        elif hnd.route == "/additems":
            page.views.append(show_additems_page())       
        page.update()

    page.on_route_change = route_change
    page.go("/home")

ft.app(target=main, port=8500)