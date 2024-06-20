import PySimpleGUI as sg
import modulo_imprimir as imprimir

pesquisa_cupom=[]

def venda_cupom(lista_cupom,lista_dados,usuario):

    titulos = ["Item", "COD","    EAN    "," Descrição do Produto","QTD","PUni R$","Preço R$"]
    layout=[
        [sg.T("CNPJ ",size=(24,1)),sg.T("Empresa ",size=(39,1)),sg.T("Cliente")],
        [sg.I(key="-CNPJ-",size=(15,1),font=("Any",18),justification='right'),sg.I(key="-EMPRESA-",size=(24,1),font=("Any",18),justification='right'),
            sg.I(key="-CPF-",size=(15,1),font=("Any",18),justification='right')],
        
        [sg.T("Valor da Compra R$",size=(15,1)),sg.T("Data da Compra",size=(29,1)),sg.T("Operador",size=(31,1)),sg.T("N° Cupom")],
        [sg.I(key="-VALOR-",size=(9,1),font=("Any",18),justification='right'),sg.I(key="-DATA-",size=(18,1),font=("Any",17),justification='right'),
            sg.I(key="-USUARIO-",size=(18,1),font=("Any",19),justification='right'),sg.I("1001",key="-CUPOM-",size=(6,1),font=("Any",18),justification='right')],
        
        [sg.P(),sg.B("PESQUISAR",size=(10,1)),sg.B("IMPRIMIR",size=(10,1)),sg.B("SAIR",size=(10,1),button_color='red')],
        [sg.Table(values=pesquisa_cupom, headings=titulos, max_col_width=10, auto_size_columns=True,
            display_row_numbers=False, justification="center",text_color="black",font=("Any",11),background_color="lightyellow", num_rows=15, key="-TABELA-", row_height=20)],
        ] 
    
    window = sg.Window("VENDA CUPOM",layout,finalize=True)                                                      
    while True:
        event,values = window.read()
        if event in (sg.WIN_CLOSED,"SAIR"):
            pesquisa_cupom.clear()
            break
        
        cupom=values["-CUPOM-"]
        if not cupom:
            sg.popup_error("Cupom Invalido!",font=('Any',12),title='ERRO')     
            continue

        if event == "PESQUISAR":
            try:
                for dado in (lista_dados):
                    if dado[0] == int(cupom):                   
                        d=dado 
                        
                        window["-CUPOM-"].update(d[0])                      
                        window["-DATA-"].update(d[1])
                        window["-USUARIO-"].update(d[2])
                        window["-CNPJ-"].update(d[3])
                        window["-CPF-"].update(d[4])
                        window["-VALOR-"].update(d[5])
                        window["-EMPRESA-"].update(d[6])
                        
                        for compra in lista_cupom:
                            if compra[0] == int(cupom):
                                pesquisa_cupom.clear()
                                pesquisa_cupom.extend(compra[1:])
                                window["-TABELA-"].update(values=pesquisa_cupom)      
                                break
            except ValueError:
                sg.popup_error('Cupom Invalido!',font=('Any',12),title='ERRO')

        elif event == 'IMPRIMIR':
            if not values['-CNPJ-']or not values["-DATA-"]or not values["-DATA-"] or not values["-CUPOM-"] or not values["-CPF-"] or not values["-VALOR-"]:
                sg.popup_error('Cupom Invalido!',font=('Any',12),title='ERRO')

            else:
                cnpj = values["-CNPJ-"]
                data = values["-DATA-"]
                cupom = values["-CUPOM-"]
                cpf = values["-CPF-"]
                valor = values["-VALOR-"]
                informacao =f"========================================================\n"
                informacao += f"Razão Social:      ........................................................ TEM DE TUDO ME\n"
                informacao += f"END:      ......................................... AV. Boa Vista n-1012 Santa Rosa/SP\n\n"
                informacao += f"CNPJ:         ................................ {cnpj}  IE : 07.112.888/000-00\n"
                informacao += f"Data:     {data}                              Cliente:  {cpf}\n"
                informacao += f"CUPOM:  000{cupom}"                
                informacao += f"Valor:  {valor}\n"
                informacao += f"Operador: {usuario}\n"
                informacao+=f"========================================================\n"
                print(informacao)
                
                gerar_pdf=imprimir.pdf(informacao,pesquisa_cupom)
                if gerar_pdf ==True:
                    sg.popup("PDF Salvo",font=('Any',12),title='IMPRIMIR PDF')
                else:
                    sg.popup_error("erro ao imprimir",font=('Any',12),title='ERRO')
    window.close()