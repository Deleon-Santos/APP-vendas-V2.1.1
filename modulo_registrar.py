    #SISTEMA DE COBRAÇA EM CAIXA DE SUPERMERCADOS E AFINS
    #Este sistema esta em desenvolvimento em carater academico 
    
def sistema(usuario,data,empresa):
    import PySimpleGUI as sg
    import json
    import modulo_pagar as pagar
    import modulo_remover as remover
    import modulo_pesquisar as pesquisar
    import modulo_cadastro as cadastrar
    import modulo_limpar as limpar
    import modulo_adicionar as adicionar
    import modulo_visualisar as visualizar
    import modulo_arquivar as arquivar
    
    lista_cupom = []
    carrinho = []
    cupom = int(1000)
    valor_pagar = 0
    num_item = int(0)
    lista=[]
    
    cpf="000.000.000-00"
    cnpj='45.333.0001/45'
    lista_dados=[]

    # ===================================== Inicio da Interface Grafica=========================================
    
    titulos = ["Item","Cod","   EAN   ","Descrição do Produto"," QTD ","PUni R$","Preço R$"]

    menu_layout = [
        ["Novo", ["Nova Compra",'Nova Pesquisa','Novo Item']],
        ["Totais", ["Venda Cupom"]], 
        ["Suporte", ["Ajuda"]],
        ["Fechar",["Fechar"]]]

    bloco_1=[   
                [sg.T('CAIXA FECHADO',key='-CAIXA-', size=(25, 1),font=("Any",18,'bold')),sg.T("Cupom",font=("Any",18,'bold')), sg.I(size=(17, 1), key="-CUPOM-", font=("Any", 20),justification="right")],
                [sg.Table(values=carrinho, headings=titulos, max_col_width=10, auto_size_columns=True,
                display_row_numbers=False, justification="center",text_color="black",font=("Any",11),background_color="lightyellow", num_rows=24, key="-TABELA-", row_height=20)],
                [sg.T(" Preço Unitário R$",size=(65,1),font=("Any",12)),sg.T("SubTotal Item R$",size=(13,1),font=("Any",12))],
                [sg.I(key="-VALORUNITARIO-",size=(10,1),font=("Any",18),justification="right"),sg.T(" ",size=(54,1)),sg.I(key="-PRECO-",size=(10,1),font=("Any",18),justification="right")],
                [sg.T("TOTAL R$", size=(12, 1), font=("Any", 40,'bold')),
                sg.I(size=(13, 1), key="-SUBTOTAL-", font=("Any", 40,'bold'), justification='right')],]
                
    bloco_2=[   
        
                
                [sg.T('Código do Produto', size=(25, 1), font=("Any", 12)),sg.P(),
                sg.T('  Quantidade', size=(10, 1), font=("Any", 12))],
                [sg.InputText(background_color='White', size=(14,2 ), key='-EAN-', font=("Any", 25)),
                sg.T("", size=(46, 1)),sg.InputText("1", size=(2, 2), key='-QTD-', font=("Any", 25),justification="right")],
                [sg.T('Descrição do Produto', size=(25, 1), font=("Any", 12))],
                
                [sg.I(size=(34, 2), key='-DESCRICAO-', font=("Any", 26)), sg.Button(">",tooltip='F1:112',font=("Any", 18))],]
    bloco_4=[   ]
    bloco_3=[ [sg.Image(filename="imagem/tdt.png",size=(706,297))],  
                ]

    

    bloco_5=[  [sg.Button('ADICIONAR', size=(12,1),font=("Any",20,'bold')),sg.T('',size=(30,1)),sg.Button('DELETE', size=(12, 1),font=("Any",20,'bold'))],
        [sg.Button('PAGAR', size=(12, 1),font=("Any",20,'bold')),sg.T('',size=(30,1)), sg.Button('VOLTAR', size=(12, 1),font=("Any",20,'bold'))],
         
                [sg.T("Data",font=('Any',12)),sg.P(),sg.T('Operador',font=('Any',12))],
                [sg.I(key="-DATA-",font=("Any",14),size=(18,1)),sg.P(),sg.I(key="-USUARIO-",font=("Any",14),size=(20,1))],]
                
    frame1=[   [sg.Frame("",bloco_3)],
                [sg.Frame("",bloco_2)],
                
                [sg.Frame("",bloco_4)],
                [sg.Frame("",bloco_5)]]

    frame2=[    [sg.Frame("",bloco_1)] , ]

    layout = [  
                [sg.Menu(menu_layout,font=('Any',12))],           
                [sg.Col(frame1),sg.Col(frame2)],
                [sg.P(),sg.Text("linkedin.com/in/deleon-santos-1b835a290"),sg.P()]]

    #====================================================================================================================================
    try:
        with open('dados/bd.txt', 'r') as adic:# Seu código para ler o arquivo
            dic = json.load(adic)
    except FileNotFoundError:
        sg.popup_error("O arquivo 'comanda.txt' não foi encontrado.\n Verifique o caminho ou crie o arquivo.",font=('Any',12),title='ERRO DE CARREGAMENTO')

    window = sg.Window("NOVO PEDIDO", layout,size=(800,800), resizable=True,finalize=True)
    
    while True:
        event, values = window.read()
        window['-DATA-'].update(data)
        window['-USUARIO-'].update(usuario)
        if event in (sg.WIN_CLOSED, "Fechar"):
            resposta=sg.popup_ok_cancel("  Se seguir com o evento,\nas configurações não salvas\nserão perdidas.",font=('Any',12),title='FECHAR E SAIR')
            if resposta=="OK":
                break  
            else:
                continue  
        elif event in('ADICIONAR','DELETAR','PAGAR','VOLTAR'):
            sg.popup_ok('Selecione uma Opção na barra de "Menu"',font=('Any',12),title='REGISTRAR')           
        elif event in ("Nova Compra", 'n:78'):

            
            cupom += 1           
            window['-CUPOM-'].update(f'{cupom}')
            window['-CAIXA-'].update('   CAIXA ABERTO')
            window['-SUBTOTAL-'].update(f'R$ {valor_pagar:.2f}')
            window["-TABELA-"].update("")
            cpf=sg.popup_get_text("Deseja adicionar um CPF na nota?",size=(15,1),font=('Any',18),title='CPF')
            if not cpf:
                cpf ="000.000.000-00"

            while True: #  Dentro deste bloco de eventos serão registrados apenas os botoes (OK,DELETE,PAGAR,VOLTAR)
                try:
                    event, values = window.read()
                    if event in('ADICIONAR','o:79'):                   
                        material, descricao, qtd = values['-EAN-'], values["-DESCRICAO-"], int(values['-QTD-'])                      
                        if not material:
                            sg.popup_error("Erro no campo material!", title="ERRO", font=("Any", 12))
                            continue
                        if qtd <1  or qtd > 99 or qtd == "none":
                            sg.popup_error("Erro no campo Quantidade!", title="ERRO", font=("Any", 12),)
                            continue                       
                        plu_pro = adicionar.achar(material,dic)
                        if plu_pro == False:
                            sg.popup_error("Erro no campo material", title="ERRO", font=("Any", 12))
                            continue
                    
                        for item in dic: # coleta os valores 
                            if item["cod"] == plu_pro:
                                num_item += 1
                                ean = item["ean"]
                                material = item["item"]
                                preco_unitario=item["preco"]
                                preco = item['preco'] * qtd
                                valor_pagar += preco
                        produto=[ num_item , plu_pro ,  ean ,  material , qtd , preco_unitario , preco ]
                                        
                        carrinho.append(produto)
                        window['-TABELA-'].update(values=carrinho)
                        window['-VALORUNITARIO-'].update(f"{preco_unitario:.2f}")
                        window['-PRECO-'].update(f"{preco:.2f}")
                        window['-SUBTOTAL-'].update(f" {valor_pagar:.2f}")
                        window['-DESCRICAO-'].update(material)
                        window["-EAN-"].update('')
                        
                    elif event in ('>','F1:112') :
                        desc,descricao=pesquisar.pesquisar(dic)
                        window['-EAN-'].update(desc)
                        window['-DESCRICAO-'].update(descricao)
                                       
                    elif event in ('DELETE','d:68'):
                        valor_pagar = remover.remover(valor_pagar,carrinho,window["-TABELA-"])
                        window['-SUBTOTAL-'].update(f"R$ {valor_pagar:.2f}")
                        window["-TABELA-"].update(values=carrinho)
                        continue

                    elif event in ('PAGAR','p:80'):
                        v_pago=f"{valor_pagar:.2f}"
                        # condição para conciderar o cupom com "pago"
                        valor_pagar = pagar.pagar(valor_pagar)
                        if valor_pagar == float(0):                           
                            lista_dados.append([cupom, data , usuario ,  cnpj , cpf, v_pago, empresa])                           
                            lista.append(cupom)
                            lista.extend(carrinho)
                            lista_cupom.extend([lista.copy()])
                            lista.clear()
                            limpar.limpar_saida(carrinho,window,num_item)                           
                            num_item=0
                            window['-CAIXA-'].update(' CAIXA FECHADO')
                            sg.popup("Voltar",title="ORDEM DE PAGAMENTO",font=('Any',12))
                            break
                            
                        else:
                            valor_pagar=float(v_pago)
                            continue

                    elif event in ("VOLTAR",'Escape:27'):  # limpa todos os valores e lista local
                        limpar.limpar_saida(carrinho,window,num_item)
                        valor_pagar = 0
                        cupom -= 1
                        break

                    elif event == (sg.WIN_CLOSED):
                        sg.popup_ok("ENCERRAR", font=("Any", 12),title='FECHAR E SAIR')   
                        break
                       
                except ValueError:  # trata erro de valor não numerico
                    sg.popup_error('Erro na quantidade', title="ERROR", font=("Any", 12))
                    continue
        elif event == "Venda Cupom":
            visualizar.venda_cupom(lista_cupom,lista_dados,usuario)
            continue

        elif event in ("VOLTAR",'Escape:27'):
            window['-CAIXA-'].update('CAIXA FECHADO')
            limpar.limpar_saida(carrinho,window,num_item)
            continue

        elif event == "Nova Pesquisa" :
            pesquisar.pesquisar(dic)
            continue

        elif event == 'Novo Item':
            cadastrar.novo_item()
            with open('dados/bd.txt', 'r') as adic: # Atualiza o Dic sempre que um novo item e cadastrado
                dic = json.load(adic)

        elif event == "Ajuda":
            try:
                with open('dados/ajuda.txt', 'r') as legenda:
                    arquivo = legenda.read()
                    sg.popup_scrolled(arquivo, title="Ajuda")
                # Seu código para ler o arquivo
            except FileNotFoundError:
                sg.popup_error("O arquivo 'SUPORTE' não foi encontrado.\n Verifique o caminho ou crie o arquivo.",font=('Any',12),title='ERRO')
            continue

    window.close()