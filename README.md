# Optical Read

## Índice

- [Sobre](#sobre)
- __O Projeto__
    - [Tecnologias Usadas](#tecnologias-usadas)
    - [Fluxo Óptico](#fluxo-óptico)
    - [Protocolo](#protocolo)
- [Cŕeditos](#créditos)
- [Colaboradores](#colaboradores)
- [Licença](#licença)

### Sobre

Algoritmo para extrair informações de um vídeo e enviá-las por protocolo OSC a um servidor

<p align="center">
    <img src="example.gif" alt="Example gif"/>
</p>

### Tecnologias usadas
- Python - version 2.7
- pyOSC - version 0.3.6.post6832
- Opencv - version 3.1.0

#### Como instalar Python 2
##### Linux (Ubuntu)
Geralmente, as distribuições do Ubuntu já vem com o Python instalado. Para verificar se o Python já está instalado na sua máquina, use o comando `$ python2 --version` no seu terminal. Caso esteja instalado, retornará uma saída com a versão do Python2.

Se retornar outros valores, tente instalar pelos seguintes comandos, no terminal:
`$ sudo apt-get update`
`$ sudo apt-get install python2`

#### Como instalar pyOSC
    https://github.com/ptone/pyosc

#### Como Instalar Opencv(3.4.1)
Para instalar o Opencv no Ubuntu, basta executar o seguinte comando no terminal:

`$ sudo apt-get install python-opencv`

Após o término da instalação, digite: 

`$ python2`

Para executar o Python e execute os seguintes comandos:

`>>> import cv2 as cv`

`>>> print(cv.__version__)`

Se o comando retornar a versão do Opencv, parabéns! O Opencv foi instalado corretamente.

Caso não, tente...
- Verificar a versão do Python instalado;
- Reinstalar o Opencv;
- Buscar informações no site oficial do Opencv: https://docs.opencv.org/3.4.1/d6/d00/tutorial_py_root.html

### Fluxo Óptico
Para este projeto foi utilizado o método [Lucas-Kanade](https://en.wikipedia.org/wiki/Lucas%E2%80%93Kanade_method), um método diferencial para estimar fluxos ópticos. Utilizamos o algoritmo presente no Opencv.

### Protocolo
O protocolo [OSC](https://en.wikipedia.org/wiki/Open_Sound_Control) é utilizado para envio das informações extraídas do vídeo. Utilizamos 3 tipos de mensagens:

- "/config": 
    - Height: Altura de cada frame;
    - Width: Largura de cada frame;
    - Span: Distância entre cada ponto de análise do Lucas-Kanade;
    - MinThreshold: Limite mínimo de intensidade para envio;
    - MaxThreshold: Limite máximo de intensidade para envio;
- "/payload":
    - Vetor com informações dos movimentos detectados em cada frame.
    - Coordenada X, coordenada Y, intensidade e angulo de cada ponto que detectou movimento significativo.
- "/quit":
    - Mensagem de finalização de análise para o servidor.

### Créditos
- [Caio Henrique Segawa Tonetti](https://github.com/LionsWrath)
- [Marcos Yukio Siraichi](https://github.com/YuKill)

### Colaboradores
- Rael Gimenes Toffolo
- Natália Vieira

### Licença
This project extends GNU GPL v. 3, so be aware of that, regarding copying, modifying and (re)destributing.

