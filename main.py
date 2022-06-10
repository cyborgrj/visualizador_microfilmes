import PySimpleGUI as sg
import os
import subprocess

encerra_programa = False

while not encerra_programa:

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
            encerra_programa = True
            raise SystemExit()
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

    caminho_mapas = r'\\192.168.1.153\digitalização\Microfilmes\Microfilmes\Mapa Microfilme'

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
            encerra_programa = True
            raise SystemExit()
            break
        if event == 'Ok':
            print('você escolheu o rolo: {}'.format(values[0]))
            programa_fechado = 0
            break
    microfilme.close()

    rolo_microfilme = int(values[0])

    inicios = [1, 97, 431, 840, 1141, 1397, 1631, 1886, 2138, 2386, 2636, 2889, 3126,
                3361, 3611, 3862, 4122, 4382, 4537, 4651, 4921, 5191, 5460, 5733, 6014, 6287,
                6558, 6834, 7101, 7366, 7554, 7751, 7952, 8159, 8366, 8573, 8780, 9004]

    limites = [96, 430, 839, 1140, 1396, 1630, 1885, 2137, 2385, 2635, 2888, 3125, 3360,
               3610, 3861, 4121, 4381, 4536, 4650, 4920, 5190, 5459, 5732, 6013, 6286, 6557,
               6833, 7100, 7365, 7553, 7750, 7951, 8158, 8365, 8572, 8779, 9003, 9227]

    for i, lim in enumerate(limites):
        if rolo_microfilme <= lim:
            pasta_superior = str(inicios[i]) + ' a ' + str(lim)
            break
    print (pasta_superior)
    caminho_microfilmes = r'\\192.168.1.153\digitalização\Microfilmes\Microfilmes'

    thumbArg = r' /filepattern=*.jpg /thumbs'
    # Argumento para abrir a pasta no irfanview no modo de thumbnails (miniaturas)


    if programa_fechado != 1:
        pasta_rolo = '"' + os.path.join(caminho_microfilmes, pasta_superior, str(rolo_microfilme)) + '"'
        print(pasta_rolo)
        argumentos = pasta_rolo + thumbArg
        irfanview_path = r'"C:\Program Files\IrfanView\i_view64.exe"'
        cmd = irfanview_path + " " + argumentos
        print(cmd)
        subprocess.call(cmd)
    else:
        raise SystemExit()