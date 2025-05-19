import flet as ft
from google import genai
from google.genai import types
#from settings import show_settings_page

def main(page: ft.Page):
    page.title = "Clothing Suggestion App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    #送信ボタン
    send_button = ft.ElevatedButton(
        "送信", icon=ft.icons.SEND
    )

    # 入力フィールド
    input_field = ft.TextField(
        label="Ask Gemini",
        width=400,
        hint_text="input here",
        multiline=True,
        min_lines=2,
    )

    # Markdown出力欄（中身は後で更新）
    output_markdown = ft.Markdown(
        value="N/A",
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data),
    )

    # Markdownを囲む青い枠＋スクロール対応
    output_box = ft.Container(
        content=ft.Column([output_markdown], scroll=ft.ScrollMode.ALWAYS),
        padding=10,
        border=ft.border.all(2, ft.colors.INDIGO),
        border_radius=8,
        width=600,
        height=400,  # 固定高さ（超えたらスクロール）
    )

    # Gemini呼び出し関数
    def ask_gemini(input_text):
        try:
            with open("apikey.txt", "r", encoding='utf-8') as f:
                apiKEY = f.read()
            with open("prompt.txt", "r", encoding='utf-8') as f:
                prompt = f.read()
            with open("userinfo.txt", "r", encoding='utf-8') as f:
                userinfo = f.read()

            client = genai.Client(api_key=apiKEY)

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[f"「ユーザーが提示したアイテム」:【{input_text}】"],
                config=types.GenerateContentConfig(
                    system_instruction=f"{prompt}\n尚、「ユーザー情報」は【\n{userinfo}\n】",
                ),
            )
            return response.text
        except Exception as e:
            return f"ERROR: {e}"

    def change_button(onchange):
        if (onchange==1):
            # ボタンをローディング表示に切り替え
            send_button.disabled = True
            send_button.icon = None
            send_button.text = ""
            send_button.content = ft.Row(
                [ft.ProgressRing(width=16, height=16)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        else:          
            send_button.content = None
            send_button.icon =ft.icons.SEND
            send_button.text = "送信"
            send_button.disabled = False

        
        page.update()
            

    # 送信処理
    def interface_gemini(e):
        change_button(onchange=1)
        response = ask_gemini(input_field.value)
        change_button(onchange=0)
        output_markdown.value = response
        page.update()

    # クリア処理
    def clear_fields(e):
        input_field.value = ""
        output_markdown.value = "N/A"
        page.update()


    #関数登録
    send_button.on_click = lambda e: interface_gemini(e)

    # HOME page
    def show_route_page():
        return ft.View(
            "/home",
            [
                ft.AppBar(
                    ft.IconButton(icon=ft.icons.SETTINGS, on_click=lambda e:page.go("/settings"))
                ),

                ft.Column(
                    [
                        ft.Text("Clothing Suggestion App", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text("version 0.1.2 | powered by gemini-2.0-flash", size=16),
                        ft.Divider(),
                        ft.Container(height=20),
                        ft.Text("入力:", size=14),
                        input_field,
                        ft.Container(height=20),
                        ft.Row(
                            [
                                send_button,
                                ft.OutlinedButton("クリア", on_click=clear_fields, icon=ft.icons.CLEAR),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(height=20),
                        ft.Divider(),
                        ft.Text("結果:", size=14),
                        output_box,
                        ft.Divider(),
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
    
    def route_change(hnd):
        page.views.clear()
        if hnd.route == "/home":
            page.views.append(show_route_page())
        elif hnd.route == "/settings":
            page.views.append(show_settings_page())
        page.update()

    page.on_route_change = route_change
    page.go("/home")

ft.app(target=main, port=8500)