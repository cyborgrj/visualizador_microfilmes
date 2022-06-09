import PySimpleGUI as sg
from tkinter import *
import os
from PIL import Image, ImageTk
import io
import subprocess

# usar o PIL para ler cada imagem...
def get_img_data(f, maxsize=(1200, 850), first=False):
# Gerar imagem usando o PIL
        img = Image.open(f)
        img.thumbnail(maxsize)
        if first:
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
        return ImageTk.PhotoImage(img)

programa_fechado = 2

sg.theme('Reddit')

layout = [[sg.Text('Digite o dia, mês e ano da matrícula desejada.')],
            [sg.Text('Formato: dd/mm/aaaa'), sg.InputText()],
            [sg.Text('')],
            [sg.Text('Atenção! No arquivo PDF que será aberto, verifique o número do rolo!')],
            [sg.Button('Ok'), sg.Button('Cancelar')]
            ]

data = sg.Window('Visualizador de microfilmes', layout)

while True:
    event, values = data.read()
    if programa_fechado == 2 and event == sg.WIN_CLOSED or event == 'Cancelar':
        programa_fechado = 1
        break
    if event == 'Ok':
        print('você escolheu a data {}'.format(values[0]))
        programa_fechado = 2
        break
data.close()

data_split = values[0].split(r'/')  # dividir a data em dia, mês e ano
dia = str(data_split[0])
mes = str(data_split[1])
ano = str(data_split[2])

nome_pdf = dia + mes + ano[2] + ano[3] + '.pdf'  # pegar somente os últimos 2 caracteres do ano

# De acordo com dia mês e ano informados na janela anterior, começa a exibição das imagens encontradas

caminho_mapas = r'C:\Visualizador de Microfilmes\Mapa Microfilme'

if programa_fechado !=1:
    PDFMicro = os.path.join(caminho_mapas, ano, nome_pdf)
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    p = subprocess.Popen([chrome_path, PDFMicro])  # Abrir janela do Chrome com o PDF
    aguardar = p.wait()  # Espera o processo fechar para continuar o programa.
else:
    raise SystemExit()

layout = [[sg.Text('Digite o número do rolo do microfilme desejado.')],
            [sg.Text('Rolo do microfilme nº:'), sg.InputText()],
            [sg.Text('')],
            [sg.Text('Atenção! Na próxima janela serão exibidas todas as imagens do rolo infomado!')],
            [sg.Button('Ok'), sg.Button('Cancelar')]]

microfilme = sg.Window('Visualizador de matrículas', layout)

while True:
    event, values = microfilme.read()
    if programa_fechado == 2 and event == sg.WIN_CLOSED or event == 'Cancelar':
        programa_fechado = 1
        break
    if event == 'Ok':
        arquivo = r"C:\Visualizador de Microfilmes\Mapa Microfilme\2009\030609.PDF"
        print('você escolheu o rolo: {}'.format(values[0]))
        programa_fechado = 0
        break
microfilme.close()

rolo_microfilme = values[0]
caminho_microfilmes = r'C:\Visualizador de Microfilmes\Microfilmes'

thumbArg = r' /filepattern=*.jpg /thumbs'
# Argumento para abrir a pasta no irfanview no modo de thumbnails (miniaturas)


if programa_fechado != 1:
    pasta_rolo = '"' + os.path.join(caminho_microfilmes, rolo_microfilme) + '"'
    argumentos = pasta_rolo + thumbArg
    irfanview_path = r'"C:\Program Files\IrfanView\i_view64.exe"'
    cmd = irfanview_path + " " + argumentos
    print(cmd)
    subprocess.call(cmd)
else:
    raise SystemExit()