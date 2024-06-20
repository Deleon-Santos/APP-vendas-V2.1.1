
def arquivo(lista_cupom):
    try:
        # Abre o arquivo de vendas em modo de leitura
        with open('dados/bd_vendas.txt', 'w') as arquivo_vendas:
            lista_cupom = arquivo_vendas.readlines()  # Lê todas as linhas do arquivo
            cont=len(lista_cupom)
            print(f'a quantidade de cupuns : : {cont}')
        
        # Adiciona a nova lista de cupons ao conteúdo lido
        lista_cupom.append(str(lista_cupom) + '\n')  # Converte a lista para string e adiciona uma nova linha
        
        # Abre o arquivo de vendas em modo de escrita para salvar as alterações
        with open('dados/bd_vendas.txt', 'w') as arquivo_vendas:
            arquivo_vendas.writelines(lista_cupom)  # Escreve todas as linhas de volta no arquivo
            print(lista_cupom)
        
        return True
    
    except FileNotFoundError:
        return False