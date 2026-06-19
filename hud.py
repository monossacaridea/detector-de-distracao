"""
hud.py
------
Interface (HUD - Heads-Up Display) profissional desenhada sobre o vídeo.

Mostra um painel inferior semitransparente com:
    * Status principal (com cor e indicação clara de alerta);
    * Indicadores acesos/apagados para SONO, BOCEJO e DISTRAÇÃO;
    * Contadores acumulados da sessão;
    * Métricas ao vivo (EAR, MAR, FPS) e o relógio;
    * Rodapé com instruções.

Tudo é desenhado com OpenCV (sem GUI extra), mantendo a aplicação leve.
"""

from datetime import datetime
import cv2

# Paleta de cores (BGR)
COR_PAINEL = (30, 30, 30)
COR_TEXTO = (235, 235, 235)
COR_TEXTO_FRACO = (160, 160, 160)
COR_OK = (0, 200, 0)
COR_ALERTA = (0, 0, 255)
COR_BOCEJO = (0, 165, 255)
COR_APAGADO = (90, 90, 90)

FONTE = cv2.FONT_HERSHEY_SIMPLEX


def _painel_translucido(frame, x1, y1, x2, y2, cor, alpha=0.55):
    """Desenha um retângulo semitransparente (efeito de painel)."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), cor, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def _indicador(frame, x, y, ligado, rotulo, cor_ligado):
    """Desenha uma 'luz' (círculo) com rótulo: acesa se 'ligado' for True."""
    cor = cor_ligado if ligado else COR_APAGADO
    cv2.circle(frame, (x, y), 9, cor, -1)
    cv2.circle(frame, (x, y), 9, (20, 20, 20), 1)
    cv2.putText(frame, rotulo, (x + 18, y + 5), FONTE, 0.55, COR_TEXTO, 1, cv2.LINE_AA)


def desenhar_hud(frame, res, fps):
    """
    Desenha o HUD completo sobre 'frame' a partir do ResultadoFrame 'res'.
    Retorna o próprio frame (modificado in-place).
    """
    h, w = frame.shape[:2]

    # ---------- Barra superior: título + status ----------
    _painel_translucido(frame, 0, 0, w, 50, COR_PAINEL, alpha=0.6)
    cv2.putText(frame, "Monitor de Motorista - IA", (15, 32),
                FONTE, 0.7, COR_TEXTO, 2, cv2.LINE_AA)

    # Status à direita, com cor do estado
    (tw, _), _ = cv2.getTextSize(res.status_text, FONTE, 0.7, 2)
    cv2.putText(frame, res.status_text, (w - tw - 15, 32),
                FONTE, 0.7, res.status_color, 2, cv2.LINE_AA)

    # ---------- Painel inferior ----------
    painel_top = h - 120
    _painel_translucido(frame, 0, painel_top, w, h, COR_PAINEL, alpha=0.6)

    # Linha 1 - Indicadores de estado
    y_ind = painel_top + 28
    _indicador(frame, 25, y_ind, res.is_sleeping, "SONO", COR_ALERTA)
    _indicador(frame, 170, y_ind, res.is_yawning, "BOCEJO", COR_BOCEJO)
    _indicador(frame, 330, y_ind, res.is_distracted, "DISTRACAO", COR_ALERTA)

    # Linha 2 - Contadores da sessão
    y_cont = painel_top + 62
    texto_contadores = (
        f"Bocejos: {res.total_bocejos}    "
        f"Episodios de Sono: {res.total_sono}    "
        f"Distracoes: {res.total_distracao}"
    )
    cv2.putText(frame, texto_contadores, (25, y_cont),
                FONTE, 0.55, COR_TEXTO, 1, cv2.LINE_AA)

    # Linha 3 - Métricas ao vivo
    y_met = painel_top + 92
    relogio = datetime.now().strftime("%H:%M:%S")
    texto_metricas = (
        f"EAR: {res.ear:.2f}   MAR: {res.mar:.2f}   "
        f"FPS: {int(fps)}   Hora: {relogio}"
    )
    cv2.putText(frame, texto_metricas, (25, y_met),
                FONTE, 0.5, COR_TEXTO_FRACO, 1, cv2.LINE_AA)

    # Rodapé direito - instrução
    cv2.putText(frame, "Q = sair", (w - 110, h - 15),
                FONTE, 0.55, COR_TEXTO_FRACO, 1, cv2.LINE_AA)

    return frame
