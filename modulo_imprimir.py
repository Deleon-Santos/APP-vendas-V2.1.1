from reportlab.lib.pagesizes import letter,A6
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def pdf(informacao, pesquisa_cupom):
  # Função para criar e estilizar a tabela
  def create_table(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=A6)
    elements = []

    style = TableStyle([
      ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
      ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
      ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ])

    # Formatação dos dados
    formatacao = [[str(item) for item in row] for row in data]
    table = Table(formatacao)
    table.setStyle(style)
    
    elements.append(table)
    doc.build(elements)

  # Função para criar o PDF com cabeçalho e tabela
  def create_pdf(content, table_data, filename):
    pdf_filename = filename
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Cabeçalho centralizado
    c.setFont("Helvetica-Bold", 12)
    title_text = "CUPOM FISCAL"
    title_width = c.stringWidth(title_text,"Helvetica", 12)
    
    c.drawCentredString(letter[0] / 2, 750, title_text)

    c.setFont("Helvetica", 12)
    # Texto de conteúdo
    text_object = c.beginText(50, 720)  # Ajuste a margem esquerda
    text_object.textLines(content)
    c.drawText(text_object)

    # Desenhando a tabela alinhada à esquerda
    available_width, available_height = letter[0] - 2 * 50, letter[1] - 30  # Margem de 50
    table = Table(table_data)
    table.wrapOn(c, available_width, available_height)
    table.drawOn(c, 50, 50)  # Margem esquerda e superior

    # Verificação de paginação (opcional)
    print('documento impresso')

    c.save()
  
  # Gera o PDF final com a tabela alinhada à esquerda
  
  create_table(informacao, "informacao.pdf")
  create_pdf(informacao, pesquisa_cupom, "Cupom_Impresso.pdf")
  
  return True

