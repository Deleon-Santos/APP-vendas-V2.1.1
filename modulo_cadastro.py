import PySimpleGUI as sg
import json

carrinho=[]

def novo_item():
    titulos=[' cod ','     ean     ',"               Descrição           "," preço "]
    layout = [
        [sg.Frame('',[
            [sg.T("Descrição:", size=(43, 1)),sg.T("EAN:", size=(23, 1)),sg.T("Preço R$:", size=(10, 1)),
                sg.P(),sg.B("SAIR", size=(6, 1),button_color='red')],
            [sg.InputText(background_color='White', key="-PRODUTO-", size=(25, 1), font=("Any", 17)),sg.P(),
                sg.InputText(background_color='White', key="-EAN-", size=(13, 1), font=("Any", 17)),sg.P(),
                sg.InputText(background_color='White', key="-PRECO-", size=(6, 1), font=("Any", 17)),sg.P(),
                sg.B("CADASTRAR", size=(12, 1)),],
            [sg.Table(values=carrinho, headings=titulos, max_col_width=10, auto_size_columns=True,
                display_row_numbers=False, justification="center",text_color="black",font=("Any",11),background_color="lightyellow",
                num_rows=10, key="-TABELA-", row_height=20)],
                ])],
    ]
    
    with open("dados/bd.txt", 'r') as arquivo:# abre os itens existentes do arquivo JSON
        dic = json.load(arquivo)

    window = sg.Window("CADASTRAR ITENS", layout)
    while True:
        try:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "SAIR"):
                break

            if event == "CADASTRAR":
                if not values['-PRODUTO-'] or not values['-PRECO-'] or not values['-EAN-']:
                    sg.popup_error('Preencha os campos necessarios!',font=('Any',12),title='ERRO CADASTRO')
                
                preco_material, descricao_material, ean_material =str (values["-PRECO-"]), values["-PRODUTO-"], int(values['-EAN-'])
                preco_material = float(preco_material.replace(',','.'))
                ean_material=str(ean_material) 
                codigo_material = str(len(dic) + 101)  # conta os itens e adiciona "101"      
                carrinho.append([codigo_material, ean_material, descricao_material, preco_material])

                window['-PRODUTO-'].Update('')
                window['-PRECO-'].Update('')
                window['-EAN-'].Update('')
            cadastro_item = {"cod": codigo_material, "ean": ean_material, "item": descricao_material, "preco": preco_material}          
            dic.append(cadastro_item) # Adicione o novo item ao dicionário

            with open("dados/bd.txt", 'w') as arquivo:
                json.dump(dic, arquivo, indent=4)

            window['-TABELA-'].update(values=carrinho)

        except ValueError:
            sg.popup_error("Informe Preço ou EAN\n em valor numérico",font=('Any',12),title='ERRO CADASTRO')
    window.close()
