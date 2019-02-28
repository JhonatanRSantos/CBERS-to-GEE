Este programa realiza a importação de imagens do satélite CBERS para sua conta no Google Earth Entine. 

###Cadastro em plataformas###

Você precisa preencher requisitos minimos para utilizar o programa desenvolvido:

1 - Ter um conta no Google.
2 - Ter uma conta no Catálogo do INPE (Instituto Nacional de Pesquisas Espaciais). Você pode se cadastrar no catálogo do INPE atravês do site http://www.dgi.inpe.br/CDSR/ clicando em "Cadastro" e registrando-se pelo formulário de cadastro.
3 - Ter uma conta no Google Earth Engine (GEE). Você pode ter uma conta no Google Earth Engine registrando-se através do site https://earthengine.google.com/ .
4 - Ter uma conta no Google Cloud. Você pode ter uma conta no Google Cloud registrando-se através do site https://cloud.google.com/. Será solicitado o número do seu cartão de crédito, porém isso é só para registro da conta, caso você deseje no futuro obter uma conta paga do Google Cloud.

Atenção1: Os passos acima devem ser feitos somente uma vez.

###Instalação de programas###

Você precisa instalar os sequintes programas:

1 - Instalar o Python 3.7.1. Você pode baixar esta versão do Python atravês do site https://www.python.org/downloads/ .
2 - Instalar a ferramenta "gsutil" do Google Cloud SDK. Você pode baixar este instalador Cloud SDK atravês do site https://cloud.google.com/storage/docs/gsutil_install#windows clicando no link em "Download the Cloud SDK installer. The installer is signed by Google Inc."
3 - Após a instalação do "gsutil" você deve seguir os passos (next, next, next ...) e realizar o login da sua conta google neste processo quando for requisitado.

Atenção2: Os passos acima devem ser feitos somente uma vez.


###Execução do programa###

1 - Entre com as configurações da sua pesquisa no arquivo "config.json" e salve o arquivo. Você pode modificar o arquivo "config.json" com um editor de texto comum como o bloco de notas do Windows. Não modifique as variáveis "installDependencies" e "bucketName".
	1.1 - No arquivo "config.json", é necessário fornecer: nome de usuário e senha do Catálogo do INPE, e, nome de usuário do GEE.   
	1.2 - Para realizar a importação de imagens para o GEE, é necessário fornecer um intervalo entre uma data inicial e uma data final do imagiamento do satélite. É necessário também fornecer uma orbita inicial e orbita final, e, um ponto inicial e ponto final.
2 - Certifique-se de estar conectado a internet.
3 - Execute o programa CBERSTOGEE.exe.
4 - Aguarde o término da execução.
5 - Após o término da execução, as imagens que você pesquisou vão estar na aba "Assets" da sua conta no Google Earth Engine.

Atenção3: Estes passos pode ser executado várias vezes, conforme necessidade do usuário. 
Atenção4: Não modifique o arquivo dependencies.txt.
