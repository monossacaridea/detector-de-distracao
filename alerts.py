"""
alerts.py
---------
Camada de alertas do Detector de Sono e Distração.

Responsabilidades:
    1. Emitir alarmes sonoros NÃO-BLOQUEANTES (em thread separada), com sons
       distintos para cada tipo de evento e um tempo de espera (cooldown) para
       não repetir o som em loop.
    2. Registrar os eventos detectados em um arquivo de log CSV, útil para
       apresentar dados/resultados da sessão.

Observação sobre o som:
    Usamos o módulo `winsound`, nativo do Windows (sem instalar nada extra).
    Em outros sistemas operacionais o alarme sonoro é simplesmente ignorado,
    mantendo o restante da aplicação funcional. O código está encapsulado para
    facilitar a troca por outra biblioteca de áudio no futuro.
"""

import csv
import os
import threading
import time
from datetime import datetime

# winsound só existe no Windows. Importação protegida para não quebrar em outros SOs.
try:
    import winsound

    _SOM_DISPONIVEL = True
except ImportError:  # Linux / macOS
    _SOM_DISPONIVEL = False


# Perfis de som por tipo de evento: (frequência em Hz, duração em ms).
# Frequências diferentes ajudam a distinguir o alerta de ouvido.
_PERFIS_SOM = {
    "SONO": (1200, 600),       # tom agudo e mais longo (mais crítico)
    "BOCEJO": (800, 300),      # tom médio e curto
    "DISTRACAO": (500, 400),   # tom grave
}


class GerenciadorAlertas:
    """Centraliza o disparo de sons e o registro de eventos em CSV."""

    def __init__(self, arquivo_log="eventos_sessao.csv", cooldown_segundos=3.0):
        self.cooldown = cooldown_segundos
        # Guarda o instante do último alerta de cada tipo para respeitar o cooldown.
        self._ultimo_alerta = {}

        # --- Preparação do log CSV ---
        self.arquivo_log = arquivo_log
        # Abrimos em modo append para não apagar sessões anteriores; escrevemos o
        # cabeçalho apenas se o arquivo ainda não existir.
        arquivo_novo = not os.path.exists(self.arquivo_log)
        self._csv_file = open(self.arquivo_log, "a", newline="", encoding="utf-8")
        self._csv_writer = csv.writer(self._csv_file)
        if arquivo_novo:
            self._csv_writer.writerow(["timestamp", "tipo_evento", "ear", "mar"])
            self._csv_file.flush()

    # ------------------------------------------------------------------ #
    # Som
    # ------------------------------------------------------------------ #
    def _tocar_som(self, tipo):
        """Toca o som correspondente em uma thread separada (não trava o vídeo)."""
        if not _SOM_DISPONIVEL:
            return
        freq, dur = _PERFIS_SOM.get(tipo, (700, 300))

        def _worker():
            try:
                winsound.Beep(freq, dur)
            except RuntimeError:
                # Em alguns ambientes Beep pode falhar; ignoramos silenciosamente.
                pass

        threading.Thread(target=_worker, daemon=True).start()

    # ------------------------------------------------------------------ #
    # API principal
    # ------------------------------------------------------------------ #
    def disparar(self, tipo, ear=None, mar=None):
        """
        Dispara um alerta do tipo informado, respeitando o cooldown.

        Retorna True se o alerta foi efetivamente disparado (som + log) e False
        se foi suprimido por ainda estar dentro do tempo de espera.
        """
        agora = time.time()
        ultimo = self._ultimo_alerta.get(tipo, 0)
        if agora - ultimo < self.cooldown:
            return False

        self._ultimo_alerta[tipo] = agora
        self._tocar_som(tipo)
        self._registrar_log(tipo, ear, mar)
        return True

    # ------------------------------------------------------------------ #
    # Log
    # ------------------------------------------------------------------ #
    def _registrar_log(self, tipo, ear, mar):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ear_str = f"{ear:.3f}" if ear is not None else ""
        mar_str = f"{mar:.3f}" if mar is not None else ""
        self._csv_writer.writerow([timestamp, tipo, ear_str, mar_str])
        self._csv_file.flush()

    def fechar(self):
        """Fecha o arquivo de log com segurança ao encerrar a aplicação."""
        try:
            self._csv_file.close()
        except Exception:
            pass
