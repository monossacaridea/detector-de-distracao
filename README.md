Detector de Sono e Distração no Trânsito

**Alunas:**  
- Beatriz Lisbôa
- Gabriela Caldana
- Thaís da Mota

## Sobre o Projeto

Este projeto utiliza **Visão Computacional** para detectar a presença de um rosto em tempo real através da webcam, servindo como etapa inicial de um sistema de monitoramento de **sono, cansaço e distração no trânsito**.

O objetivo é contribuir para a segurança viária por meio da identificação de sinais que possam indicar fadiga ou falta de atenção do motorista.

---

## Tecnologias Utilizadas

- Python
- OpenCV

---

## Como Executar

### 1. Salve o código

Salve o código em um arquivo chamado:

```bash
main.py
```

### 2. Instale as dependências

Abra o terminal da sua IDE e execute:

```bash
pip install opencv-python
```

### 3. Execute o programa

No mesmo terminal, execute:

```bash
python main.py
```

### 4. Encerrar a aplicação

Clique na janela do vídeo e pressione a tecla:

```text
q
```

---

## Status das Funcionalidades

### Concluído

- [x] Inicialização e captura estável de vídeo via webcam.
- [x] Pré-processamento de frames (conversão de BGR para escala de cinza).
- [x] Detecção de rosto em tempo real utilizando Haar Cascade.
- [x] Feedback visual através de caixas delimitadoras (*bounding boxes*).

### Em Desenvolvimento

- [ ] Detecção de olhos e boca para avaliação de abertura.
- [ ] Implementação do cálculo de **EAR (Eye Aspect Ratio)**.
- [ ] Diferenciação entre piscadas naturais e episódios de micro-sono.
- [ ] Detecção de distração por meio de **Head Pose Estimation**.
- [ ] Sistema de alerta visual e sonoro.

---

## Planejamento de Hardware: Raspberry Pi

Como o projeto possui foco em uma aplicação real no contexto automotivo, está prevista sua execução em um **Raspberry Pi**.

### Otimização de Processamento

O algoritmo **Haar Cascade** apresenta baixo custo computacional, sendo adequado para o Raspberry Pi.

Caso sejam necessários modelos mais avançados para detecção facial, serão avaliadas alternativas leves, como:

- Dlib (modelo de 5 pontos)
- MediaPipe Iris

O objetivo é manter uma boa taxa de quadros por segundo (**FPS**) sem comprometer o desempenho.

### Alimentação e Periféricos

- Utilização de **Câmera Pi (Pi NoIR)** ou webcam USB.
- Integração de um **Buzzer Ativo 5V** aos pinos GPIO para emissão de alertas sonoros.

### Execução Autônoma

Implementação de inicialização automática da aplicação utilizando:

- Systemd Service
- Cron

Dessa forma, o sistema será iniciado automaticamente quando o Raspberry Pi receber energia do veículo.

---

## Objetivo Futuro

Desenvolver um sistema embarcado capaz de:

- Monitorar sinais de fadiga do motorista;
- Detectar distrações prolongadas;
- Emitir alertas preventivos em tempo real;
- Contribuir para a redução de acidentes causados por desatenção ou sonolência.

---

## Disciplina

Projeto desenvolvido para a disciplina de **Inteligência Artificial**.
