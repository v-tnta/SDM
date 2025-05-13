import flet as ft
import asyncio
from google import genai
from google.genai import types

def main(page: ft.Page):
    # アプリのタイトルを設定
    page.title = "Clothing Suggestion App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    # 入力フィールドを作成
    input_field = ft.TextField(
        label="Ask Gemini",
        width=400,
        hint_text="input here",
        multiline=True,
        min_lines=2
    )
    
    # 読み取り専用の出力フィールドを作成
    output_field = ft.TextField(
        label="Gemini response:",
        width=400,
        read_only=True,
        value="N/A",
        multiline=True,
        min_lines=1,
        max_lines=10
    )

    def ask_gemini(input_text):
        # ここにGemini APIを呼び出すコードを追加
        # 例: response = await call_gemini_api(prompt)

        print('status 0') # << - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - debug

        with open('apikey.txt', 'r') as f: 
            apiKEY = f.read()
        with open('prompt.txt', 'r') as f: 
            prompt = f.read()
        with open('userinfo.txt', 'r') as f: 
            userinfo = f.read()

        client = genai.Client(api_key=apiKEY)

        print('status 1')  # << - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - debug

        try:
            print('status 2')  # << - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - debug
        
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents = [
                    #input_text
                    f"「ユーザーが提示したアイテム」: {input_text}"
                    ],
                config = types.GenerateContentConfig(
                        system_instruction=f"{prompt}\n尚、「ユーザー情報」は以下の通り\n{userinfo}", # プロンプト @ here
                ),
            ) # get API result
        
            print('status 3')  # << - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - debug
            res = response.text
            
        except Exception as e:
            res = f"ERROR: {e}"

        return res
    
    # ボタンがクリックされた時の処理
    def interface_gemini(e):
        # 入力フィールドの値を読み取り専用フィールドに転送
        
        response = ask_gemini(input_field.value)
        output_field.value = response
        # UIを更新
        page.update()
    
    # 転送ボタン
    transfer_button = ft.ElevatedButton(
        "送信",
        on_click=interface_gemini,
        icon=ft.icons.SEND
    )
    
    
    # 画像選択ボタン
    def pick_files_result(e: ft.FilePickerResultEvent):
        #  << - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ongoing
        pass
    
    image_button = ft.OutlinedButton(
        "画像選択",
        on_click=pick_files_result,
        icon=ft.icons.IMAGE
    )

    # クリアボタン
    def clear_fields(e):
        input_field.value = ""
        output_field.value = "N/A"
        page.update()
    
    clear_button = ft.OutlinedButton(
        "クリア",
        on_click=clear_fields,
        icon=ft.icons.CLEAR
    )
    
    # 画面のレイアウトを設定
    page.add(
        ft.Column(
            [
                ft.Text("Clothing Suggestion App", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("version  0.1.1", size=16),
                ft.Divider(), # ----------------
                
                ft.Container(height=20),
                
                ft.Text("入力:", size=14),
                input_field,
                
                ft.Container(height=20),
                
                ft.Row(
                    [transfer_button, image_button, clear_button],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
                ft.Container(height=20),
                
                ft.Divider(), # ----------------

                ft.Text("結果:", size=14),
                output_field,

                ft.Divider() # ----------------
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        )
    )

# アプリケーションを実行
ft.app(target=main, port=8500)