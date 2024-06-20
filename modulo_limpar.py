
def limpar_saida(carrinho,window,num_item):
        carrinho.clear()
        window["-CUPOM-"].update("")
        window["-SUBTOTAL-"].update("")
        window["-DESCRICAO-"].update("")
        window['-VALORUNITARIO-'].update('')
        window['-PRECO-'].update('')
        num_item = 0