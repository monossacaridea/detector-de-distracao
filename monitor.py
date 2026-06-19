"""
monitor.py
----------
Núcleo de detecção do Detector de Sono e Distração.

Substitui a abordagem antiga de Haar Cascade (que apenas verificava a
presença/ausência de olhos) por um modelo de malha facial (MediaPipe Face Mesh),
que fornece 468 pontos de referência (landmarks) do rosto. Com esses pontos
calculamos métricas reais:

    * EAR  (Eye Aspect Ratio)   -> abertura dos olhos  -> SONO
    * MAR  (Mouth Aspect Ratio) -> abertura da boca    -> BOCEJO
    * presença/ausência do rosto                       -> DISTRAÇÃO

As três funcionalidades originais (sono e distração) são preservadas — apenas
ficaram mais robustas — e a detecção de BOCEJO é a novidade.
"""

import cv2
import numpy as np
import mediapipe as mp

# --------------------------------------------------------------------------- #
# Limiares e configurações (fáceis de ajustar antes da apresentação)
# --------------------------------------------------------------------------- #
EAR_LIMIAR = 0.21          # abaixo disso o olho é considerado fechado
FRAMES_SONO = 15           # frames consecutivos de olho fechado -> SONO

MAR_LIMIAR = 0.60          # acima disso a boca é considerada bem aberta
FRAMES_BOCEJO = 15         # frames consecutivos de boca aberta -> 1 BOCEJO

FRAMES_DISTRACAO = 20      # frames consecutivos sem rosto -> DISTRAÇÃO

# --------------------------------------------------------------------------- #
# Índices dos landmarks no Face Mesh do MediaPipe
# --------------------------------------------------------------------------- #
# Cada olho usa 6 pontos na ordem (p1..p6) exigida pela fórmula do EAR.
OLHO_ESQUERDO = [362, 385, 387, 263, 373, 380]
OLHO_DIREITO = [33, 160, 158, 133, 153, 144]

# Boca: pontos verticais (lábio superior/inferior internos) e cantos.
BOCA_TOPO = 13
BOCA_BASE = 14
BOCA_CANTO_ESQ = 78
BOCA_CANTO_DIR = 308


def _distancia(p1, p2):
    """Distância euclidiana entre dois pontos (x, y)."""
    return np.linalg.norm(np.array(p1) - np.array(p2))


def _calcular_ear(pontos):
    """
    Eye Aspect Ratio.
    pontos: lista de 6 coordenadas (x, y) na ordem p1..p6.
    EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    """
    vertical_1 = _distancia(pontos[1], pontos[5])
    vertical_2 = _distancia(pontos[2], pontos[4])
    horizontal = _distancia(pontos[0], pontos[3])
    if horizontal == 0:
        return 0.0
    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def _calcular_mar(topo, base, canto_esq, canto_dir):
    """
    Mouth Aspect Ratio.
    MAR = ||topo-base|| / ||canto_esq-canto_dir||
    """
    vertical = _distancia(topo, base)
    horizontal = _distancia(canto_esq, canto_dir)
    if horizontal == 0:
        return 0.0
    return vertical / horizontal


class ResultadoFrame:
    """Pequeno contêiner com tudo que o frame produziu (lido pelo HUD/main)."""

    def __init__(self):
        self.face_present = False
        self.ear = 0.0
        self.mar = 0.0
        self.is_sleeping = False
        self.is_yawning = False        # bocejo em andamento (boca aberta agora)
        self.is_distracted = False
        self.novo_bocejo = False       # True apenas no frame em que o bocejo é contado
        self.status_text = "Status: Normal"
        self.status_color = (0, 255, 0)
        # Contadores acumulados na sessão
        self.total_bocejos = 0
        self.total_sono = 0
        self.total_distracao = 0


class DriverMonitor:
    """Processa frames da webcam e mantém a máquina de estados do motorista."""

    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        # Contadores de frames consecutivos
        self.sleep_counter = 0
        self.yawn_counter = 0
        self.distraction_counter = 0

        # Flags de estado
        self.is_sleeping = False
        self.is_distracted = False
        self._bocejo_em_andamento = False  # impede contar o mesmo bocejo várias vezes

        # Estatísticas da sessão
        self.total_bocejos = 0
        self.total_sono = 0          # nº de episódios de sono distintos
        self.total_distracao = 0     # nº de episódios de distração distintos

    def _coords(self, landmarks, indices, w, h):
        """Converte landmarks normalizados (0..1) em coordenadas de pixel."""
        return [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]

    def process_frame(self, frame):
        """
        Processa um frame BGR e retorna (frame_anotado, ResultadoFrame).
        O desenho do rosto/landmarks discretos é feito aqui; o HUD é desenhado
        pelo módulo hud.py a partir do ResultadoFrame.
        """
        res = ResultadoFrame()
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        deteccao = self.face_mesh.process(rgb)

        if deteccao.multi_face_landmarks:
            res.face_present = True
            self.distraction_counter = 0
            self.is_distracted = False

            landmarks = deteccao.multi_face_landmarks[0].landmark

            olho_esq = self._coords(landmarks, OLHO_ESQUERDO, w, h)
            olho_dir = self._coords(landmarks, OLHO_DIREITO, w, h)
            ear = (_calcular_ear(olho_esq) + _calcular_ear(olho_dir)) / 2.0

            topo = (int(landmarks[BOCA_TOPO].x * w), int(landmarks[BOCA_TOPO].y * h))
            base = (int(landmarks[BOCA_BASE].x * w), int(landmarks[BOCA_BASE].y * h))
            c_esq = (int(landmarks[BOCA_CANTO_ESQ].x * w), int(landmarks[BOCA_CANTO_ESQ].y * h))
            c_dir = (int(landmarks[BOCA_CANTO_DIR].x * w), int(landmarks[BOCA_CANTO_DIR].y * h))
            mar = _calcular_mar(topo, base, c_esq, c_dir)

            res.ear = ear
            res.mar = mar

            # --- Lógica de SONO (olhos fechados) ---
            if ear < EAR_LIMIAR:
                self.sleep_counter += 1
            else:
                self.sleep_counter = 0

            if self.sleep_counter >= FRAMES_SONO:
                if not self.is_sleeping:
                    self.total_sono += 1   # novo episódio de sono
                self.is_sleeping = True
            else:
                self.is_sleeping = False

            # --- Lógica de BOCEJO (boca aberta de forma sustentada) ---
            if mar > MAR_LIMIAR:
                self.yawn_counter += 1
            else:
                self.yawn_counter = 0
                self._bocejo_em_andamento = False

            if self.yawn_counter >= FRAMES_BOCEJO and not self._bocejo_em_andamento:
                self.total_bocejos += 1
                self._bocejo_em_andamento = True   # conta só uma vez por bocejo
                res.novo_bocejo = True

            res.is_yawning = self.yawn_counter >= FRAMES_BOCEJO

            # Desenho discreto dos pontos usados (olhos em verde, boca em ciano)
            for p in olho_esq + olho_dir:
                cv2.circle(frame, p, 1, (0, 255, 0), -1)
            for p in (topo, base, c_esq, c_dir):
                cv2.circle(frame, p, 2, (255, 255, 0), -1)

        else:
            # Rosto não detectado -> possível distração
            res.face_present = False
            self.sleep_counter = 0
            self.yawn_counter = 0
            self.is_sleeping = False
            self.distraction_counter += 1

            if self.distraction_counter >= FRAMES_DISTRACAO:
                if not self.is_distracted:
                    self.total_distracao += 1   # novo episódio de distração
                self.is_distracted = True
            else:
                self.is_distracted = False

        # --- Consolidação do estado/cores para exibição ---
        res.is_sleeping = self.is_sleeping
        res.is_distracted = self.is_distracted

        if res.is_sleeping:
            res.status_text = "ALERTA: SONO (OLHOS FECHADOS)!"
            res.status_color = (0, 0, 255)
        elif res.is_distracted:
            res.status_text = "ALERTA: DISTRACAO (ROSTO AUSENTE)!"
            res.status_color = (0, 0, 255)
        elif res.is_yawning:
            res.status_text = "ALERTA: BOCEJO DETECTADO!"
            res.status_color = (0, 165, 255)  # laranja
        else:
            res.status_text = "Status: Normal"
            res.status_color = (0, 255, 0)

        res.total_bocejos = self.total_bocejos
        res.total_sono = self.total_sono
        res.total_distracao = self.total_distracao

        return frame, res

    def fechar(self):
        """Libera os recursos do MediaPipe."""
        self.face_mesh.close()
