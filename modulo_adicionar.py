
def achar(material,dic):
        for item in dic:
            if material in (item["cod"],item["ean"]) :
                return item["cod"]  # busca o produto dentro do cadastro
        return False