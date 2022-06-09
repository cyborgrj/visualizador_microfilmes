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
#  "" "C:\Visualizador de Microfilmes\Microfilmes\7864" /filepattern=*.jpg /thumbs
rolo_microfilme = values[0]

if programa_fechado != 1:
    folder = os.path.join(caminho_microfilmes, rolo_microfilme)
    if not folder:
        sg.popup_cancel('Pasta de arquivos inválida, cancelando...')
        raise SystemExit()

    # Possíveis tipos de imagem em que os arquivos de microfilmes normalmente são gravados.
    img_types = (".png", ".jpg", "jpeg", ".tiff")

    # Gerar lista de arquivos na pasta
    flist0 = os.listdir(folder)

    # Criar uma sub-lista somente com os arquivos válidos, verificando o final da string do arquivo.
    fnames = [f for f in flist0 if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(img_types)]

    num_files = len(fnames)                # quantidade de imagens encontradas
    if num_files == 0:
        sg.popup('No files in folder')
        raise SystemExit()
    del flist0                             # Apagar a lista inicial (antes de limpar o "lixo")

    # Criar 2 elementos fora o layout que serão utilizados para lista de arquivos e visualização da imagem
    # começar com o primeiro arquivo da lista, para não exibir o frame em branco
    filename = os.path.join(folder, fnames[0])  # nome do primeiro arquivo na lista
    image_elem = sg.Image(data=get_img_data(filename, first=True))
    filename_display_elem = sg.Text(filename, size=(50, 3))
    file_num_display_elem = sg.Text('Arquivo 1 de {}'.format(num_files), size=(15, 1))

    # define o layout, formulário de exibição e seleção
    col = [[filename_display_elem],
        [image_elem]]

    col_files = [[sg.Listbox(values=fnames, change_submits=True, size=(20, 35), key='listbox')],
                 [sg.Button('Anterior', size=(8, 2)), sg.Button('Próximo', size=(8, 2)), file_num_display_elem]]

    layout = [[sg.Column(col_files), sg.Column(col)]]
    window = sg.Window('Visualizador de imagens dos protocolos', layout, size=(1300, 760), return_keyboard_events=True,
                       location=(0, 0), use_default_focus=False)
    # Entrer em loop "infinito" enquanto lê a entrada de comandos do usuário e exibe as imagens.
    i = 0
    while True:
        event, values = window.read()
        print(event, values)
        # Ler ações do mouse e teclado
        if event == sg.WIN_CLOSED:
            break
        elif event in ('Próximo', 'MouseWheel:Down', 'Down:40', 'Next:34'):
            i += 1
            if i >= num_files:
                i -= num_files
            filename = os.path.join(folder, fnames[i])
        elif event in ('Anterior', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
            i -= 1
            if i < 0:
                i = num_files + i
            filename = os.path.join(folder, fnames[i])
        elif event == 'listbox':            # Caso escolha um arquivo na caixa de seleção à esquerda
            f = values["listbox"][0]            # pegar o valor selecionado
            filename = os.path.join(folder, f)  # ler o arquivo
            i = fnames.index(f)                 # atualizar o índice
        else:
            filename = os.path.join(folder, fnames[i])

        # atualizar a janela com a nova imagem
        image_elem.update(data=get_img_data(filename, first=True))
        # atualizar a janela com o nome do arquivo
        filename_display_elem.update(filename)
        # atualizar a exibição de quantidade de arquivos
        file_num_display_elem.update('Arquivo {} de {}'.format(i+1, num_files))
    window.close()