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

### Tecnologias usadas
- Python - version 2.7
- pyOSC - version 0.3.6.post6832
- Opencv - version 3.1.0

#### Como instalar Python
    http://askubuntu.com/questions/101591/how-do-i-install-python-2-7-2-on-ubuntu

#### Como instalar pyOSC
    https://github.com/ptone/pyosc

#### Como Instalar Opencv(3.1.0)
    http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/

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
- Caio Henrique Segawa Tonetti
- Marcos Yukio Siraichi

### Colaboradores
- Rael Gimenes Toffolo
- Natália Vieira

### Licença
This project extends GNU GPL v. 3, so be aware of that, regarding copying, modifying and (re)destributing.

