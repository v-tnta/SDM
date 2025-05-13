import flet as ft
import asyncio
from google import genai

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
        min_lines=4
    )

    def ask_gemini(input_text):
        # ここにGemini APIを呼び出すコードを追加
        # 例: response = await call_gemini_api(prompt)
        print('status 0')
        with open('apikey.txt', 'r') as f: 
            apiKEY = f.read()
        client = genai.Client(api_key=apiKEY)
        print('status 1')

        try:
            print('status 2')
        
            response = client.models.generate_content(model="gemini-2.0-flash", contents = [input_text]) # get API result
        
            print('status 3')
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
    
    # クリアボタンを作成
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
                ft.Text("version  0.1.0", size=16),
                ft.Divider(), # ----------------
                
                ft.Container(height=20),
                
                ft.Text("入力:", size=14),
                input_field,
                
                ft.Container(height=20),
                
                ft.Row(
                    [transfer_button, clear_button],
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