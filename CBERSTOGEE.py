from tkinter import *
import json
import os
import time
import zipfile
from tkinter import Toplevel
import requests
from bs4 import BeautifulSoup
import wget
import shutil
from PIL import Image, ImageTk
import threading
import multiprocessing

task = None
# Para gerar o executavel, digitar no terminal:
# pyinstaller <nome do script>.py
# pyinstaller.exe --icon=favicon.ico CBERSTOGEE.py   // para ter icone

fileConfigName = "config.json"  # ALTERAR DEPOIS DOS TESTES PARA config.json

configJson = json.loads(open(fileConfigName).read())
if configJson["installDependencies"]:

    print("Instalando dependencias.")
    result = os.system("pip install -r dependencies.txt")
    if result == 1:
        print("Erro ao instalar dependencias do Python.")
        exit()

    result = os.system("earthengine ls")
    if result == 1:
        os.system("cls")
        print("Para continuar voce deve fazer sua autenticacao\n")
        os.system("earthengine authenticate")
        os.system("cls")

    currentTime = None
    result = 1
    while result == 1:
        currentTime = str(time.time()).replace(".", "")
        result = os.system("gsutil mb gs://bk{}".format(currentTime))
        result = os.system(
            "gsutil iam ch allUsers:objectViewer gs://bk{}".format(currentTime))
        os.system("cls")

    with open(fileConfigName, "w") as configFile:
        configJson["bucketName"] = "bk" + currentTime
        configJson["installDependencies"] = False
        json.dump(configJson, configFile)

configJson = json.loads(open(fileConfigName).read())

nomeDoUsuarioINPE = configJson["nomeDoUsuarioINPE"].strip()
senhaINPE = configJson["senhaINPE"].strip()
geeUserName = configJson["geeUserName"].strip()
bucketName = configJson["bucketName"].strip()
startDate = configJson["startDate"].strip()
endDate = configJson["endDate"].strip()
startOrbit = configJson["startOrbit"].strip()
endOrbit = configJson["endOrbit"].strip()
startPoint = configJson["startPoint"].strip()
endPoint = configJson["endPoint"].strip()


# ---------------------Execução do programa apos click no botão---------------------


def Carregando():
    textoProgresso = "Carregando...\n"
    print(textoProgresso)
    text_box_Progress.insert(INSERT, textoProgresso)

    # ,senhaINPE,geeUserName,bucketName,startDate,endDate,startOrbit,endOrbit,startPoint,endPoint):


def executeCrawler():
    Carregando()
    # print('teste', entry_1.get())
    nomeDoUsuarioINPE = entry_1.get()
    senhaINPE = entry_2.get()
    geeUserName = entry_3.get()
    startDate = entry_4.get()
    endDate = entry_5.get()
    startOrbit = entry_6.get()
    endOrbit = entry_7.get()
    startPoint = entry_8.get()
    endPoint = entry_9.get()

    with open(fileConfigName, "w") as configFile:
        configJson["nomeDoUsuarioINPE"] = nomeDoUsuarioINPE
        configJson["senhaINPE"] = senhaINPE
        configJson["geeUserName"] = geeUserName
        configJson["startDate"] = startDate
        configJson["endDate"] = endDate
        configJson["startOrbit"] = startOrbit
        configJson["endOrbit"] = endOrbit
        configJson["startPoint"] = startPoint
        configJson["endPoint"] = endPoint
        json.dump(configJson, configFile)

    # ---Inicio do Crawller

    # Post de autenticação do usuário
    nomeDoUsuarioINPE = configJson["nomeDoUsuarioINPE"]
    senhaINPE = configJson["senhaINPE"]

    s = requests.session()
    p = s.post('http://www.dgi.inpe.br/catalogo/login.php',
               {'enviar': 'Realizar+acesso', 'name': nomeDoUsuarioINPE, 'pwd': senhaINPE, 'submitted': '1'})

    phpSessID = p.cookies['PHPSESSID']

    # Definindo as variaveis de busca de imagens.
    startPage = '1'
    startDate = configJson["startDate"]
    endDate = configJson["endDate"]
    startOrbit = configJson["startOrbit"]
    endOrbit = configJson["endOrbit"]
    startPoint = configJson["startPoint"]
    endPoint = configJson["endPoint"]
    imagesPath = configJson["imagesPath"]

    pageSize = '20'  # Quantidade de itens maximo encontrados por pagina web
    zipFolder = 'tempZip'

    # ---------

    # Primeiro link utilizado para obter as infirmações iniciais do processo
    link1 = f'http://www.dgi.inpe.br/catalogo/buscarimagens.php?p=1&pg={startPage}&TRIGGER=BTNOPTODOS&CQA=CA&SATELITE=CB4&SENSOR=MUX&DATAINI={startDate}&DATAFIM={endDate}&Q1=&Q2=&Q3=&Q4=&ORBITAINI={startOrbit}&ORBITAFIM={endOrbit}&PONTOINI={startPoint}&PONTOFIM={endPoint}&TAMPAGINA={pageSize}'

    L1 = s.get(link1)
    html = L1.content
    html = str(html)

    # Codigo html da primeira pagina requisitada
    site = BeautifulSoup(html, 'lxml')
    # Quantidade de paginas.
    totalPages = site.find(id="pgatualtopo").get('max')
    # tag que possui os indices das imagens
    ref = site.find_all(class_="icon-shopping-cart")

    # Fazer loop para obter todos os indices das imagens e adicionar no carrinho.
    for i in ref:
        tagBtn = i.previous_element
        IndiceImg = str(tagBtn).split("chamaAdicionarAoCarrinho")[
            1].split(",")[1].replace("\\'", "").replace("\\'", "")
        IndiceImg = IndiceImg.strip()
        link2 = f'http://www.dgi.inpe.br/catalogo/addtocart.php?ACTION=CART&INDICE={IndiceImg}'
        L2 = s.get(link2)

    if (int(totalPages) > 1):
        for pagina in range(2, int(totalPages) + 1):
            link1 = f'http://www.dgi.inpe.br/catalogo/buscarimagens.php?p=1&pg={str(pagina)}&TRIGGER=BTNOPTODOS&CQA=CA&SATELITE=CB4&SENSOR=MUX&DATAINI={startDate}&DATAFIM={endDate}&Q1=&Q2=&Q3=&Q4=&ORBITAINI={startOrbit}&ORBITAFIM={endOrbit}&PONTOINI={startPoint}&PONTOFIM={endPoint}&TAMPAGINA={pageSize}'
            L1 = s.get(link1)
            html = L1.content
            html = str(html)
            site = BeautifulSoup(html, 'lxml')
            ref = site.find_all(class_="icon-shopping-cart")
            for i in ref:
                tagBtn = i.previous_element
                IndiceImg = str(tagBtn).split("chamaAdicionarAoCarrinho")[1].split(",")[1].replace("\\'", "").replace(
                    "\\'", "")
                IndiceImg = IndiceImg.strip()
                link2 = f'http://www.dgi.inpe.br/catalogo/addtocart.php?ACTION=CART&INDICE={IndiceImg}'
                L2 = s.get(link2)

                # Obter a quantidade de itens/imagens adicionadas no carrinho
    link3 = 'http://www.dgi.inpe.br/catalogo/numeroitenscarrinho.php'
    L3 = s.get(link3)
    strNumItensNoCarrinho = str(L3.content)
    quantDeItensNoCarrinho = strNumItensNoCarrinho.split("\\")[
        0].split("'")[1]

    # Fechar o pedido de imagens
    link4 = 'http://www.dgi.inpe.br/catalogo/cart.php'
    L4 = s.get(link4)

    link5 = 'http://www.dgi.inpe.br/catalogo/cartAddress.php'
    L5 = s.post(link5, {'action': 'Prosseguir',
                        'sesskey': phpSessID, 'userid': nomeDoUsuarioINPE})

    link6 = f'http://www.dgi.inpe.br/catalogo/cartAddress.php?userid={nomeDoUsuarioINPE}&nItens={quantDeItensNoCarrinho}&sesskey={phpSessID}&mediaCD=&total=0&action=Prosseguir'
    L6 = s.get(link6)

    link7 = 'http://www.dgi.inpe.br/catalogo/cartAddress.php'
    p = s.post(link7,
               {'action': 'Fechar+Pedido', 'mediaCD': None, 'nItens': quantDeItensNoCarrinho, 'sesskey': phpSessID,
                'total': '0', 'userid': nomeDoUsuarioINPE})

    link8 = f'http://www.dgi.inpe.br/catalogo/cartAddress.php?action=Fechar+Pedido&mediaCD=&nItens={quantDeItensNoCarrinho}&sesskey={phpSessID}&total=0&userid={nomeDoUsuarioINPE}'
    L8 = s.get(link8)

    # Obter o número do pedido atribuido ao id do usuario logado
    pagWebPedido = L8.content
    pagWebPedido = BeautifulSoup(str(pagWebPedido), 'lxml')
    numeroDoPedido = pagWebPedido.find(
        class_='icon-thumbs-up').previous_element.text
    numeroDoPedido = str(numeroDoPedido).split(
        " foi aceito ")[0].split("número ")[1]

    print(
        f'Número de imagens que serão baixadas: {quantDeItensNoCarrinho} \n')

    # Espera um determinado tempo para o processamento das imagens no servidor
    time.sleep(60)

    # Preparar links das imagens
    link9 = f'http://imagens.dgi.inpe.br/cdsr/{nomeDoUsuarioINPE}{numeroDoPedido}'
    L9 = s.get(link9)
    pagWebLinks = BeautifulSoup(str(L9.content), 'lxml')

    linksImagens = []
    for link in pagWebLinks.find_all('a'):
        strLink = str(link.get('href'))
        if strLink.endswith('.zip'):
            linksImagens.append(
                f'http://imagens.dgi.inpe.br/cdsr/{nomeDoUsuarioINPE}{numeroDoPedido}/{strLink}')

    # Baixar as imagens e dezipar o arquivo .zip
    os.mkdir(imagesPath + zipFolder)
    time.sleep(1)

    def BaixarExtrairImagens(location):
        try:
            filename = wget.download(location, imagesPath + zipFolder)
            zip_ref = zipfile.ZipFile(filename, 'r')
            zip_ref.extractall(imagesPath)
            zip_ref.close()
        except Exception as error:
            print("Não foi possível baixar os arquivos. Verifique sua conexão.")
            exit()

    auxPercenBaixado = 100 / (int(quantDeItensNoCarrinho) * 4)
    for linkImg in linksImagens:
        BaixarExtrairImagens(str(linkImg))
        print(f" Baixando arquivos: {auxPercenBaixado}% \n")

        auxPercenBaixado = auxPercenBaixado + \
            (100 / (int(quantDeItensNoCarrinho) * 4))

    # Mensagem de termino do download das imagens
    print(
        f'Download terminado. Voce baixou: {quantDeItensNoCarrinho} imagens para o seu computador.')
    print(f'Cada imagem possui 4 arquivos .tiff e 4 arquivos .xml.')
    print(
        f'Cada arquivo .tiff corresponde a uma banda da imagem, e cada arquivo .xml corresponde aos metadados de cada banda.')

    # Delata pasta zipada
    time.sleep(1)

    # result = os.system("gsutil rm gs://{}/*".format(configJson["bucketName"]))

    print("Enviando arquivos para o GEE.\n")
    # ADICIONAR AQUI O NOME DE TODAS AS TASKS CRIADAS PELO SISTEMA!!!!!GILBERTO
    taskIDs = []

    for root, dirs, files in os.walk("images"):
        print('iniciando')
        for filename in files:
            print('preparando envio de dados...')
            currentFile = str(filename)
            if currentFile.endswith(".tif"):
                result = os.system(
                    "gsutil cp {} gs://{}".format("images\\" + currentFile, configJson["bucketName"]))
                if result == 0:
                    try:
                        result = os.popen(
                            "earthengine upload image --asset_id=users/{}/{} --pyramiding_policy=sample gs://{}/{}".format(
                                configJson["geeUserName"], currentFile.replace(
                                    ".tif", ""), configJson["bucketName"],
                                currentFile)
                        ).readlines()
                        taskIDs.append(result[0].split('ID: ')[
                                       1].replace("\n'", ''))
                        print('Id adicionado com sucesso.')                        
                    except:
                        result = 1
                    if result == 1:
                        print("Error ao baixar a imagem {} para o GEE.".format(
                            currentFile))
                else:
                    print("Erro ao enviar o arquivo {}".format(currentFile))
            print()

    shutil.rmtree(imagesPath + zipFolder)
    shutil.rmtree(imagesPath)
    print('Ids ', taskIDs)
    textoProgresso = "Imagens transferidas para o GEE com sucesso!\n"
    print(textoProgresso)
    text_box_Progress.insert(INSERT, textoProgresso)

    # CODIGO QUE APAGA AS IMAGENS DO BUCKET --- TESTAR!!!!!
    import re

    tasksCompleds = 0

    taskList = os.popen('earthengine task list').readlines()
    taskList = [re.sub('[^A-Za-z0-9\_\-]+', ' ', task) for task in taskList]

    doTasks = (len(taskIDs) != 0)
    total = len(taskIDs)
    while doTasks:
        for tskId in taskIDs:
            out = os.popen(
                'earthengine task info {}'.format(tskId)).readlines()
            out = out[1].split(': ')[1]            
            if out == 'COMPLETED\n':
                tasksCompleds += 1
            elif out == 'FAILED\n':
                print('A task com o ID {} falhou.'.format(tskId))
                tasksCompleds += 1
        if tasksCompleds == total:
            os.system('gsutil rm -r gs://{}/*.tif'.format(bucketName))
            break
        else:
            tasksCompleds = 0
    # ---sFim do Crawller


def start():
    threading.Thread(target=executeCrawler).start()


# ---------------------Interface---------------------
# -- Janela de Aviso inicial


def Ajuda(txt=''):
    windowWelcome = Toplevel()
    windowWelcome.iconbitmap('favicon.ico')
    windowWelcome.title('Bem vindo ao CEBRS4 to GEE!')

    image = Image.open("banner3_ajudaC4GEE.png")
    photo = ImageTk.PhotoImage(image)
    label = Label(windowWelcome, image=photo)
    label.image = photo  # keep a reference!
    label.pack()

    '''
    img_ajuda = PhotoImage(file='banner3_ajudaC4GEE.png')
    label_ajudaimg = Label(windowWelcome, image=img_ajuda)
    label_ajudaimg.grid(row=2,column=0)'''

    text_box_Welcome = Text(windowWelcome, width=80,
                            height=20, wrap=WORD, background="white")
    text_box_Welcome.pack()  # .grid(row=4,column=0)
    textoInicial = "Bem Vindo ao CBERS4 to GEE! Este programa realiza a importação de imagens do satélite CBERS4 banda MUX para sua conta no Google Earth Engine.\n\n" \
                   "Você precisa preencher requisitos mínimos para utilizar este programa:\n" \
                   "1 - Ter um conta no Google.\n" \
                   "2 - Ter uma conta no Catálogo do INPE (Instituto Nacional de Pesquisas Espaciais). Você pode se cadastrar no catálogo do INPE atravês do site http://www.dgi.inpe.br/CDSR/ clicando em <Cadastro> e registrando-se pelo formulário de cadastro. \n" \
                   "3 - Ter uma conta no Google Earth Engine (GEE). Você pode ter uma conta no Google Earth Engine registrando-se através do site https://earthengine.google.com/ . \n" \
                   "4 - Ter uma conta no Google Cloud. Você pode ter uma conta no Google Cloud registrando-se através do site https://cloud.google.com/. Será solicitado o número do seu cartão de crédito, porém isso é só para registro da conta caso você deseje no futuro obter uma conta Google Cloud com mais recursos. \n"

    textoInicial = textoInicial + txt

    text_box_Welcome.insert(INSERT, textoInicial)

    def closeWindowWelcome():
        windowWelcome.destroy()

    button_1_Welcome = Button(windowWelcome, text="Ok",
                              command=closeWindowWelcome)
    # .grid(row=6,column=0,ipadx=100)#.pack(ipadx=100)#(row=2, column=0)
    button_1_Welcome.pack(ipadx=100)

    windowWelcome.mainloop()
    # --------------------------


# -- Janela do programa principal


def sheet():
    # if threadWorker != None and threadWorker.is_alive():
    #   pass
    # os.system("taskkill /f /im  python.exe")
    os.system('taskkill /f /pid {pid}'.format(pid=os.getpid()))
    # os.system('pkill -TERM -P {pid}'.format(pid=os.getpid()))


main_window = Tk()
main_window.protocol("WM_DELETE_WINDOW", sheet)
main_window.title('CBERS4 To GEE')

img1 = PhotoImage(file="banner1_topC4GEE.png")
label_aux0 = Label(main_window, image=img1)  # text="\n\n")
label_aux0.grid(row=1, column=0)

frameLogin = Frame(main_window, height=100, width=100,
                   borderwidth=4, relief=GROOVE)
frameLogin.grid(row=2, column=0)

img2 = PhotoImage(file="banner2_medC4GEE.png")
label_aux0 = Label(main_window, image=img2)  # ,text="\n\n")
label_aux0.grid(row=3, column=0)

framePesquisa = Frame(main_window, height=100, width=100,
                      borderwidth=4, relief=GROOVE)
framePesquisa.grid(row=4, column=0)

label_1 = Label(frameLogin, text="Nome de usuário do INPE:")
label_1.grid(row=2, column=0, sticky=W)
entry_1 = Entry(frameLogin)
entry_1.grid(row=3, column=0, sticky=W)
entry_1.insert(0, nomeDoUsuarioINPE)

label_2 = Label(frameLogin, text="Senha de usuário do INPE:")
label_2.grid(row=4, column=0, sticky=W)
entry_2 = Entry(frameLogin)  # ,show="*")
entry_2.grid(row=5, column=0, sticky=W)
entry_2.insert(0, senhaINPE)

label_space1 = Label(frameLogin, text="           ")
label_space1.grid(row=2, column=1)
label_space1 = Label(frameLogin, text="            ")
label_space1.grid(row=3, column=1)

label_3 = Label(frameLogin, text="Nome de usuário do GEE :")
label_3.grid(row=2, column=2, sticky=W)
entry_3 = Entry(frameLogin)
entry_3.grid(row=3, column=2, sticky=W)
entry_3.insert(0, geeUserName)

label_4 = Label(framePesquisa, text="Data início. Ex: 01/09/2018 :")
label_4.grid(row=8, column=0, sticky=W)
entry_4 = Entry(framePesquisa)
entry_4.grid(row=9, column=0, sticky=W)
entry_4.insert(0, startDate)

label_space1 = Label(framePesquisa, text="           ")
label_space1.grid(row=8, column=1)
label_space1 = Label(framePesquisa, text="              ")
label_space1.grid(row=9, column=1)

label_5 = Label(framePesquisa, text="Data fim. Ex: 01/10/2018 :")
label_5.grid(row=8, column=2, sticky=W)
entry_5 = Entry(framePesquisa)
entry_5.grid(row=9, column=2, sticky=W)
entry_5.insert(0, endDate)

label_6 = Label(framePesquisa, text="Órbita inicial. Ex: 162 :")
label_6.grid(row=10, column=0, sticky=W)
entry_6 = Entry(framePesquisa)
entry_6.grid(row=11, column=0, sticky=W)
entry_6.insert(0, startOrbit)

label_7 = Label(framePesquisa, text="Órbita final. Ex: 162 :")
label_7.grid(row=10, column=2, sticky=W)
entry_7 = Entry(framePesquisa)
entry_7.grid(row=11, column=2, sticky=W)
entry_7.insert(0, endOrbit)

label_8 = Label(framePesquisa, text="Ponto inicial. Ex: 102 :")
label_8.grid(row=12, column=0, sticky=W)
entry_8 = Entry(framePesquisa)
entry_8.grid(row=13, column=0, sticky=W)
entry_8.insert(0, startPoint)

label_9 = Label(framePesquisa, text="Ponto final. Ex: 102 :")
label_9.grid(row=12, column=2, sticky=W)
entry_9 = Entry(framePesquisa)
entry_9.grid(row=13, column=2, sticky=W)
entry_9.insert(0, endPoint)

label_aux1 = Label(main_window, text=" ")
label_aux1.grid(row=20, column=0)

label_aux2 = Label(main_window, text=" ")
label_aux2.grid(row=22, column=0)

textoAjuda = "\nPara realizar a importação de imagens CBERS para o GEE, é necessário: \n" \
             "1 - Preencher os dados: \n" \
             "    1.1 - Nome de usuário do Catálogo do INPE, \n" \
             "    1.2 - Senha do Catálogo do INPE, \n" \
             "    1.3 - Nome de usuário do GEE, \n" \
             "    1.4 - Um intervalo entre uma data inicial e uma data final do imagiamento do satélite,\n" \
             "    1.5 - Um intervalo com uma orbita inicial e uma orbita final, \n" \
             "    1.6 - Um intervalo do ponto inicial e do ponto final.\n" \
             "2 - Após o preenchimento dos dado clicar no botão <Baixar e importar imagens para o GEE> e aguardar o término da execução.\n" \
             "3 - Após o término da execução, as imagens que você pesquisou estarão na aba <Assets> da sua conta no Google Earth Engine.\n\n" \
             "--Equipe de desenvolvimento--\n" \
             "Cesar Diniz: cesar.diniz@solved.eco.br\n" \
             "Gilberto N de Souza Jr: gilberto.nerino@solved.eco.br\n" \
             "Jhonatan Rodrigues: jhonatan.santos@solved.eco.br\n" \
             "Luis Sadeck: luis.sadeck@solved.eco.br\n" \
             "Luiz Cortinhas: luiz.cortinhas@solved.eco.br\n" \
             "Visite o nosso site: www.solved.eco.br"

button_2 = Button(main_window, text="Ajuda!",
                  command=lambda: Ajuda(textoAjuda))
button_2.grid(row=23, column=0, sticky=N)

label_aux3 = Label(main_window, text=" ")
label_aux3.grid(row=24, column=0)

text_box_Progress = Text(main_window, width=40, height=3,
                         wrap=WORD, background="white")
text_box_Progress.grid(row=25, column=0, columnspan=3)
textoProgresso = "..."
text_box_Progress.insert(INSERT, textoProgresso)

label_aux4 = Label(main_window, text=" ")
label_aux4.grid(row=26, column=0)

button_1 = Button(
    main_window, text="Baixar e importar imagens para o GEE", command=start)
button_1.grid(row=21, column=0)

main_window.iconbitmap('favicon.ico')

# --- Exibe ajuda
if configJson["installDependencies"]:
    Ajuda()

main_window.mainloop()
