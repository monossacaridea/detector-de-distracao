"""
main.py
-------
Ponto de entrada do Detector de Sono e Distração.

Fluxo:
    1. Inicializa câmera, detector (MediaPipe), HUD e gerenciador de alertas.
    2. Loop principal: lê o frame, processa, dispara alertas (som + log) e
       desenha o HUD profissional.
    3. Ao sair (tecla Q), exibe um resumo da sessão e fecha os recursos.

Como executar:
    pip install -r requirements.txt
    python main.py
"""

import time
from datetime import datetime

import cv2

from monitor import DriverMonitor
from hud import desenhar_hud
from alerts import GerenciadorAlertas


def imprimir_resumo(res, duracao_segundos):
    """Imprime no console um resumo da sessão de monitoramento."""
    minutos = int(duracao_segundos // 60)
    segundos = int(duracao_segundos % 60)
    print("\n" + "=" * 45)
    print("        RESUMO DA SESSAO DE MONITORAMENTO")
    print("=" * 45)
    print(f"  Duracao total .......: {minutos}m {segundos}s")
    print(f"  Bocejos detectados ..: {res.total_bocejos}")
    print(f"  Episodios de sono ...: {res.total_sono}")
    print(f"  Distracoes ..........: {res.total_distracao}")
    print(f"  Encerrado em ........: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("  Log detalhado .......: eventos_sessao.csv")
    print("=" * 45 + "\n")


def main():
    monitor = DriverMonitor()
    alertas = GerenciadorAlertas()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        monitor.fechar()
        alertas.fechar()
        return

    print("Monitoramento iniciado. Pressione 'Q' na janela do vídeo para sair.")

    prev_time = time.time()
    inicio_sessao = prev_time
    ultimo_resultado = None

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Erro: falha ao ler o frame da câmera.")
                break

            # Espelhar a imagem (efeito espelho, mais natural para o usuário)
            frame = cv2.flip(frame, 1)

            # FPS
            curr_time = time.time()
            delta = curr_time - prev_time
            fps = 1 / delta if delta > 0 else 0
            prev_time = curr_time

            # Processamento e estado
            frame, res = monitor.process_frame(frame)
            ultimo_resultado = res

            # Disparo de alertas (som + log), respeitando o cooldown interno
            if res.is_sleeping:
                alertas.disparar("SONO", ear=res.ear, mar=res.mar)
            if res.novo_bocejo:
                alertas.disparar("BOCEJO", ear=res.ear, mar=res.mar)
            if res.is_distracted:
                alertas.disparar("DISTRACAO", ear=res.ear, mar=res.mar)

            # HUD profissional
            frame = desenhar_hud(frame, res, fps)

            cv2.imshow("Monitor de Motorista - IA", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        # Encerramento limpo, mesmo em caso de erro
        camera.release()
        cv2.destroyAllWindows()
        monitor.fechar()
        alertas.fechar()

        if ultimo_resultado is not None:
            imprimir_resumo(ultimo_resultado, time.time() - inicio_sessao)


if __name__ == "__main__":
    main()
