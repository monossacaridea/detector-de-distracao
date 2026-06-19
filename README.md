# Detector de Sono, Bocejo e Distração no Trânsito

**Alunas:**
- Beatriz Lisbôa
- Gabriela Caldana
- Thaís da Mota

## Sobre o Projeto

Este projeto utiliza **Visão Computacional** e **Inteligência Artificial** para monitorar, em tempo real através da webcam, sinais de **sono, cansaço (bocejo) e distração** de um motorista.

A partir da imagem da câmera, o sistema localiza o rosto, mede a abertura dos olhos e da boca e identifica comportamentos de risco, emitindo **alertas visuais e sonoros** imediatos. O objetivo é contribuir para a segurança viária, ajudando a reduzir acidentes causados por fadiga ou desatenção.

---

## Tecnologias Utilizadas

- **Python**
- **OpenCV** — captura de vídeo e desenho da interface (HUD)
- **MediaPipe Face Mesh** — malha facial de 468 pontos (landmarks)
- **NumPy** — cálculos das métricas EAR e MAR

---

## Como Funciona

Em vez de apenas verificar a presença de olhos/rosto, o sistema calcula **métricas reais** a partir dos pontos faciais detectados pelo MediaPipe:

| Sinal | Métrica | Como é detectado |
|-------|---------|------------------|
| **Sono** | **EAR** (Eye Aspect Ratio) | Olhos fechados por vários frames consecutivos (EAR abaixo do limiar). |
| **Bocejo** | **MAR** (Mouth Aspect Ratio) | Boca bem aberta de forma sustentada (MAR acima do limiar), evitando confundir com fala. |
| **Distração** | Presença do rosto | Rosto ausente do enquadramento por vários frames consecutivos. |

Cada evento gera:
- **Alerta visual** no painel (HUD), com cores e indicadores;
- **Alerta sonoro** pelo computador (tons distintos para sono, bocejo e distração);
- **Registro em log** (`eventos_sessao.csv`) com horário e métricas.

Ao encerrar, é exibido um **resumo da sessão** (total de bocejos, episódios de sono e distrações).

---

## Como Executar

### 1. Instale as dependências

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

### 2. Execute o programa

```bash
python main.py
```

### 3. Encerrar a aplicação

Clique na janela do vídeo e pressione a tecla **Q**. O resumo da sessão aparecerá no terminal.

> **Observação sobre o som:** o alerta sonoro utiliza o módulo `winsound`, nativo do **Windows**. Em outros sistemas operacionais o programa continua funcionando normalmente, apenas sem o som.

---

## Ajuste de Sensibilidade

Os limiares ficam no topo de [`monitor.py`](monitor.py) e podem ser ajustados conforme a iluminação e a câmera usadas na apresentação:

```python
EAR_LIMIAR = 0.21       # menor = mais sensível a olhos fechados
FRAMES_SONO = 15
MAR_LIMIAR = 0.60       # menor = mais sensível a bocejos
FRAMES_BOCEJO = 15
FRAMES_DISTRACAO = 20
```

---

## Estrutura do Projeto

| Arquivo | Responsabilidade |
|---------|------------------|
| `main.py` | Ponto de entrada: câmera, loop principal e resumo da sessão. |
| `monitor.py` | Detecção facial (MediaPipe), cálculo de EAR/MAR e máquina de estados. |
| `hud.py` | Interface profissional (HUD) desenhada sobre o vídeo. |
| `alerts.py` | Alertas sonoros não-bloqueantes e registro em log CSV. |
| `requirements.txt` | Dependências do projeto. |
| `detector_rosto_legado.py` | Versão inicial (Haar Cascade), mantida como referência histórica. |

---

## Status das Funcionalidades

### Concluído

- [x] Captura estável de vídeo via webcam.
- [x] Detecção facial em tempo real com **MediaPipe Face Mesh** (468 pontos).
- [x] Cálculo de **EAR (Eye Aspect Ratio)** para detecção de sono.
- [x] Cálculo de **MAR (Mouth Aspect Ratio)** para detecção de **bocejo**.
- [x] Detecção de distração por ausência prolongada do rosto.
- [x] Sistema de **alerta visual e sonoro**.
- [x] Interface profissional (HUD) com status, indicadores, contadores e métricas.
- [x] Registro de eventos em log (CSV) e resumo de sessão.

### Possíveis evoluções futuras

- [ ] Detecção de distração por **Head Pose Estimation** (cabeça virada, não só ausente).
- [ ] Diferenciação fina entre piscadas naturais e episódios de micro-sono.
- [ ] Dashboard de estatísticas pós-sessão a partir do log.

---

## Disciplina

Projeto desenvolvido para a disciplina de **Inteligência Artificial**.
