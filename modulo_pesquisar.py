import PySimpleGUI as sg

defaut=['0','0']
pesquisa=[]

def pesquisar(dic):

    titulos=[" Cod ","       EAN       ","   Descrição do Produto   "]
    layout=[
        [sg.P(),sg.B('CONCLUIR')], 
        [sg.Frame("",[
        [sg.Table(values=pesquisa, headings=titulos, max_col_width=3, auto_size_columns=True,
            display_row_numbers=False, justification="center",text_color="black",font=("Any",14),
            background_color="lightyellow", num_rows=10, key="-TABELA-", row_height=20)],])],
        ]

    window = sg.Window('PESQUISA POR ITEM', layout, finalize=True)
    pesquisa.clear()  
    for item in dic:
        cod = item['cod']
        ean = item['ean']
        desc = item['item']
        pesquisa.append([cod, ean, desc])
        window['-TABELA-'].update(values=pesquisa)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'SAIR'):
            return defaut[0],defaut[1]
        
        if event =="CONCLUIR":
            if values['-TABELA-']:
                linha_selecionada = values['-TABELA-'][0]               
                escolha = pesquisa[linha_selecionada]               
                return escolha[1],escolha[2]
                
        window.close()  