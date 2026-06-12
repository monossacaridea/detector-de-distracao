Alunas: Beatriz Lisbôa, Gabriela Caldana e Thaís da Mota

Detector de Sono e Distração no Trânsito

Este projeto utiliza visão computacional para detectar a presença de um rosto em tempo real através da webcam, como etapa inicial de um sistema de monitoramento de sono, cansaço e distração no trânsito.

Tecnologias

● Python

● OpenCV

⚙️ Como Executar (Ambiente Local)
Clonar ou criar o arquivo: Salve o código acima em um arquivo chamado main.py.

Instalar Dependências: Abra o terminal da sua IDE e instale o OpenCV rodando o gerenciador de pacotes:

Bash
pip install opencv-python
Executar o Programa: No mesmo terminal, execute o script:

Bash
python main.py
Encerrar: Clique na janela do vídeo e pressione a tecla q do teclado.

🚀 Status de Funcionalidades
🔴 Concluído (Funcionalidades Parciais)
[x] Inicialização e captura estável de fluxo de vídeo via webcam.

[x] Pré-processamento de frames (conversão BGR para Escala de Cinza).

[x] Detecção de presença de rosto em tempo real (Haar Cascade Spatial Filter).

[x] Feedback visual na tela por meio de caixas delimitadoras (bounding boxes).

🟡 Em Desenvolvimento / Próximos Passos
[ ] Detecção de Olhos e Boca: Mapear a região ocular e labial para avaliar abertura.

[ ] Cálculo de EAR (Eye Aspect Ratio): Algoritmo matemático para monitorar a frequência e tempo de fechamento dos olhos.

[ ] Análise Quântica de Piscadas: Diferenciar piscadas naturais de momentos de micro-sono (olhos fechados por mais de 1.5 a 2 segundos).

[ ] Detecção de Distração (Head Pose Estimation): Identificar se o motorista está virando o rosto para os lados ou olhando para baixo por muito tempo.

[ ] Sistema de Alerta Embutido: Emissão de bips sonoros e avisos visuais na tela quando anomalias forem detectadas.

🍓 Planejamento de Hardware: Raspberry Pi
Como o projeto visa uma aplicação real no ecossistema automotivo, o código será embarcado em um Raspberry Pi. Abaixo constam os desafios técnicos e estratégias mapeadas para essa transição:

Otimização de Processamento: O algoritmo Haar Cascade com OpenCV é leve, o que favorece o hardware do Raspberry Pi. No entanto, se utilizarmos modelos baseados em marcos faciais pesados (como Dlib com 68 pontos), configuraremos versões reduzidas de modelos (como o modelo de 5 pontos ou MediaPipe Iris) para manter uma alta taxa de quadros por segundo (FPS).

Alimentação e Periféricos:

Uso de uma Câmera Pi (PiNoIR ou Módulo de Câmera padrão) ou Webcam USB estável.

Acoplamento de um Buzzer Ativo (5V) conectado aos pinos GPIO do Raspberry Pi para atuar como alarme físico sonoro dentro do veículo.

Execução Autônoma: Configuração de scripts de inicialização automática (Systemd Service ou cron) para inicializar a IA assim que o Raspberry Pi receber energia do veículo.


-----------------------------------------------------------------
Projeto desenvolvido para a disciplina de Inteligência Artificial.
