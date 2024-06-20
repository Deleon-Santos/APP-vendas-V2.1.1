import PySimpleGUI as sg

condicao_pagamento=['Dinheiro', 'Cartão á Vista', 'Cartão á Prazo', 'Pix' ]

def pagar(valor_pagar):
    
    frame6=[
            [sg.T("Valor da Compra R$:  ", size=(23, 1), font=("Any", 12))],
            [sg.I(f" {valor_pagar:.2f}", size=(10, 1), justification='right', key="valor", font=("Any", 30)),sg.P()],
            [sg.T("Valor Recabido R$: ", size=(23, 1), font=("Any", 12))],
            [sg.I(f' 0.00', size=(10, 1), key="recebido", justification='right', font=("Any", 30)),sg.P()],
            [sg.T("Troco Devolvido R$: ", size=(23, 1), font=("Any", 12))],
            [sg.I(f' 0.00', size=(10, 1), key="R$", justification='right', font=("Any", 30)),sg.P()],
            [sg.T("", size=(10, 1))],]
        
    col2=[[sg.Image(filename="imagem/imagem_login.png",size=(340,240))]]

    layout = [
        [sg.T("Forma de pagamento")]
        [sg.DD(default_value="",values=condicao_pagamento,size=(21,1),font=('any',22),key='-CONDICAO-'),
        sg.P(),sg.B("PAGAR", font=("Any", 13),size=(14, 1))],
        [sg.Col(col2),sg.Col(frame6)],
        ]

    window = sg.Window("PAGAMENTO", layout, finalize=True)

    while True:
        event, values = window.read()
        pago = valor_pagar
        troco = 0
        
        if event in (sg.WIN_CLOSED,"CONCLUIR"):
            sg.popup("Continuar Comprando ",font=('Any',12),title='CONTINUAR')
            break
            
        if event == 'PAGAR' and values['-CONDICAO-'] in ('Cartão á Vista', 'Cartão á Prazo', 'Pix'):  # para cartão e pix o valor e descontado itegralmente
            if( (valor_pagar  > 0), None):  # somente se o subtotal existir e for maior que "0"
                valor_pagar = 0
                window["valor"].update(f"R$ {valor_pagar:.2f}")
                window["recebido"].update(f"R$ {pago:.2f}")
                sg.popup("Autorizado", font=("Any", 12),title='ORDEM DE PAGAMENTO')
                return valor_pagar
            else:
                sg.popup('Informe o Valor da Compra',font=('Any',12),title='ORDEM DE PAGAMENTO')
        
        elif event == 'PAGAR' and values['-CONDICAO-'] =='Dinheiro' :
            try:
                dinheiro =str (sg.popup_get_text("Valor Recebido", font=("Any", 18),default_text='0,00',title='ENTRADA DE VALOR'))
                if dinheiro is not None:  # verifica se tem valores
                    dinheiro = dinheiro.replace(',', '.')  # Troca a vírgula pelo ponto
                    dinheiro = float(dinheiro)
                    if dinheiro < valor_pagar:
                        sg.popup("Valor Insuficiente",font=('Any',12),title='ORDEM DE PAGAMENTO')
                        continue
                        
                    else: # desconta o subtotal e retorna o troco
                        troco = dinheiro - valor_pagar
                        valor_pagar = 0
                        window["valor"].update(f"R$ {valor_pagar:.2f}")
                        window["recebido"].update(f"R$ {dinheiro:.2f}")
                        window["R$"].update(f"R$ {troco:.2f}")
                        sg.popup("Autorizado",font=('Any',12),title='ORDEM DE PAGAMENTO')  
                        return valor_pagar
                else:
                    sg.popup("Informe o valor recebido",font=('Any',12),title='ORDEM DE PAGAMENTO')

            except Exception as erro:
                sg.popup_error(f"Erro Inesperado: {erro}", )
                continue

        else:
            sg.popup_error('Condição de pagamento!',font=('Any',12),title='ORDEM DE PAGAMENTO')
        window.close()

