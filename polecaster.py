"""
PoleCaster v2.0 — Radio Automation Suite
Diseño: Grup Comunikados
Soporte: Icecast2 + Shoutcast v1/v2 + Ecualizador visual animado
Requiere: pip install PyQt6 python-vlc requests
"""

import sys, os, json, time, threading, subprocess, random, math
import requests
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QTabWidget, QLineEdit, QComboBox,
    QCheckBox, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QGroupBox, QGridLayout, QSpinBox, QFrame, QProgressBar,
    QDialog, QDialogButtonBox, QTimeEdit, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSettings, QSize, QRect, QPoint
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QPainter, QLinearGradient, QBrush,
    QPen, QRadialGradient, QFontDatabase, QAction
)

APP_NAME    = "PoleCaster"
APP_VERSION = "2.0"
APP_BRAND   = "Grup Comunikados"
CONFIG_FILE = "polecaster_config.json"

# ══════════════════════════════════════════
#  ESTILO OSCURO — Grup Comunikados
# ══════════════════════════════════════════
DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #0d0d0d;
    color: #e8e8e8;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
}
QTabWidget::pane { border: 1px solid #2a2a2a; background-color: #111; }
QTabBar::tab { background: #0a0a0a; color: #666; padding: 7px 16px; border: none; font-size: 11px; }
QTabBar::tab:selected { color: #ff6600; border-bottom: 2px solid #ff6600; background: #111; }
QTabBar::tab:hover { color: #ccc; background: #161616; }
QTableWidget { background-color: #111; gridline-color: #1a1a1a; border: none; selection-background-color: #1e1e1e; }
QTableWidget::item { padding: 4px 6px; border-bottom: 1px solid #141414; }
QTableWidget::item:selected { background-color: #ff660015; color: #fff; }
QHeaderView::section { background-color: #0a0a0a; color: #555; padding: 4px 6px; border: none; font-size: 10px; letter-spacing: 1px; }
QPushButton { background-color: #1a1a1a; color: #bbb; border: 1px solid #333; padding: 5px 12px; border-radius: 4px; }
QPushButton:hover { background-color: #242424; color: #fff; border-color: #444; }
QPushButton:pressed { background-color: #0f0f0f; }
QPushButton#btnPlay { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #ff6600,stop:1 #cc4400); color:#fff; font-weight:bold; border-radius:20px; border:none; }
QPushButton#btnPlay:hover { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #ff8833,stop:1 #ee5500); }
QPushButton#btnStop { background:#1e1e1e; color:#fff; border-radius:20px; border:1px solid #333; }
QPushButton#btnConnect { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #cc4400); color:#fff; font-weight:bold; border:none; border-radius:4px; padding:8px; }
QPushButton#btnDisconnect { background:#8b0000; color:#fff; font-weight:bold; border:none; border-radius:4px; padding:8px; }
QLineEdit, QComboBox, QSpinBox, QTimeEdit { background:#0a0a0a; color:#e0e0e0; border:1px solid #2a2a2a; padding:4px 8px; border-radius:3px; }
QLineEdit:focus, QComboBox:focus { border-color:#ff6600; }
QComboBox::drop-down { border:none; width:20px; }
QComboBox QAbstractItemView { background:#111; color:#e0e0e0; border:1px solid #333; selection-background-color:#ff660033; }
QSlider::groove:horizontal { height:4px; background:#1e1e1e; border-radius:2px; }
QSlider::handle:horizontal { background:#ff6600; width:13px; height:13px; border-radius:7px; margin:-5px 0; }
QSlider::sub-page:horizontal { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #ff9933); border-radius:2px; }
QProgressBar { background:#1a1a1a; border:none; border-radius:2px; height:4px; }
QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #ffaa00); border-radius:2px; }
QGroupBox { border:1px solid #2a2a2a; border-radius:5px; margin-top:10px; padding-top:10px; color:#555; font-size:10px; letter-spacing:1px; }
QGroupBox::title { subcontrol-origin:margin; left:10px; padding:0 5px; color:#ff6600; }
QCheckBox { color:#bbb; }
QCheckBox::indicator { width:14px; height:14px; background:#0a0a0a; border:1px solid #333; border-radius:2px; }
QCheckBox::indicator:checked { background:#ff6600; border-color:#ff6600; }
QScrollBar:vertical { background:#0a0a0a; width:5px; border-radius:3px; }
QScrollBar::handle:vertical { background:#2a2a2a; border-radius:3px; min-height:20px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
QFrame#vSep { background-color:#1e1e1e; }
QFrame#hSep { background-color:#1e1e1e; }
"""

# ══════════════════════════════════════════
#  WIDGET: Ecualizador Visual Animado
# ══════════════════════════════════════════
class EqualizerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)
        self._bars      = 32
        self._heights   = [0.0] * self._bars
        self._targets   = [0.0] * self._bars
        self._peaks     = [0.0] * self._bars
        self._peak_hold = [0 ] * self._bars
        self._playing   = False
        self._phase     = 0.0

        self._timer = QTimer()
        self._timer.timeout.connect(self._animate)
        self._timer.start(40)  # 25 fps

    def set_playing(self, playing):
        self._playing = playing
        if not playing:
            self._targets = [0.0] * self._bars

    def _animate(self):
        self._phase += 0.08
        if self._playing:
            for i in range(self._bars):
                # Simular espectro musical realista
                base   = 0.15 + 0.6 * math.exp(-0.04 * i)
                wave1  = 0.25 * math.sin(self._phase * 1.7 + i * 0.4)
                wave2  = 0.15 * math.sin(self._phase * 3.1 + i * 0.7)
                wave3  = 0.10 * math.sin(self._phase * 5.3 + i * 1.1)
                spike  = 0.3  * math.exp(-0.5 * ((i - 6) ** 2))   # bombo
                spike2 = 0.2  * math.exp(-0.5 * ((i - 14) ** 2))  # medio
                noise  = random.gauss(0, 0.08)
                target = max(0.0, min(1.0, base + wave1 + wave2 + wave3 + spike + spike2 + noise))
                self._targets[i] = target

        for i in range(self._bars):
            diff = self._targets[i] - self._heights[i]
            if diff > 0:
                self._heights[i] += diff * 0.35   # sube rápido
            else:
                self._heights[i] += diff * 0.12   # baja lento
            self._heights[i] = max(0.0, min(1.0, self._heights[i]))

            # Picos que caen lentamente
            if self._heights[i] >= self._peaks[i]:
                self._peaks[i]    = self._heights[i]
                self._peak_hold[i] = 18
            else:
                if self._peak_hold[i] > 0:
                    self._peak_hold[i] -= 1
                else:
                    self._peaks[i] = max(0, self._peaks[i] - 0.018)

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        p.fillRect(0, 0, w, h, QColor("#0d0d0d"))

        n      = self._bars
        gap    = 2
        bar_w  = max(3, (w - gap * (n + 1)) // n)
        total  = bar_w + gap

        for i in range(n):
            x      = gap + i * total
            bh     = int(self._heights[i] * (h - 8))
            if bh < 1:
                # Barra mínima
                p.fillRect(x, h - 2, bar_w, 2, QColor("#1e1e1e"))
                continue

            y = h - bh - 2

            # Gradiente: verde→naranja→rojo según altura
            ratio = self._heights[i]
            if ratio < 0.5:
                r = int(ratio * 2 * 255)
                g = 200
                b = 20
            elif ratio < 0.8:
                r = 255
                g = int((1 - (ratio - 0.5) / 0.3) * 180)
                b = 10
            else:
                r = 255
                g = int((1 - (ratio - 0.8) / 0.2) * 80)
                b = 0

            grad = QLinearGradient(x, y + bh, x, y)
            base_c = QColor(r, g, b, 200)
            top_c  = QColor(min(255, r + 60), min(255, g + 60), min(255, b + 60), 255)
            grad.setColorAt(0, base_c)
            grad.setColorAt(1, top_c)
            p.fillRect(x, y, bar_w, bh, grad)

            # Reflejo sutil en la base
            ref_grad = QLinearGradient(x, h - 1, x, h - int(bh * 0.25))
            ref_grad.setColorAt(0, QColor(r, g, b, 60))
            ref_grad.setColorAt(1, QColor(r, g, b, 0))
            p.fillRect(x, h - int(bh * 0.25), bar_w, int(bh * 0.25), ref_grad)

            # Pico
            peak_y = int((1 - self._peaks[i]) * (h - 8))
            p.fillRect(x, peak_y, bar_w, 2, QColor(min(255, r + 80), min(255, g + 80), 255, 220))

        p.end()


# ══════════════════════════════════════════
#  WIDGET: Logo animado Grup Comunikados
# ══════════════════════════════════════════
class BrandHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self._phase = 0.0
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(50)

    def _tick(self):
        self._phase += 0.05
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor("#080808"))

        # Línea decorativa animada inferior
        for x in range(0, w, 3):
            t    = x / w
            wave = math.sin(t * 12 - self._phase * 2) * 3
            alpha = int(80 + 60 * math.sin(t * 6 - self._phase))
            p.setPen(QPen(QColor(255, 102, 0, alpha), 1))
            p.drawPoint(x, int(h - 4 + wave))

        # Línea naranja base
        p.setPen(QPen(QColor("#ff6600"), 1))
        p.drawLine(0, h - 1, w, h - 1)

        # Texto marca
        f_brand = QFont("Segoe UI", 10, QFont.Weight.Normal)
        f_brand.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 3)
        p.setFont(f_brand)
        p.setPen(QColor("#555"))
        p.drawText(14, 16, "GRUP COMUNIKADOS")

        # Texto app
        f_app = QFont("Segoe UI", 18, QFont.Weight.Bold)
        p.setFont(f_app)

        # Sombra
        p.setPen(QColor(255, 102, 0, 40))
        p.drawText(15, 40, "PoleCaster")

        # Gradiente en el texto principal (simulado con dos colores)
        p.setPen(QColor("#ff6600"))
        p.drawText(14, 39, "Pole")
        p.setPen(QColor("#ffaa33"))
        fm = p.fontMetrics()
        offset = fm.horizontalAdvance("Pole")
        p.drawText(14 + offset, 39, "Caster")

        # Versión
        f_ver = QFont("Segoe UI", 8)
        p.setFont(f_ver)
        p.setPen(QColor("#444"))
        p.drawText(w - 60, 38, f"v{APP_VERSION}")

        p.end()


# ══════════════════════════════════════════
#  MODELOS DE DATOS
# ══════════════════════════════════════════
class PlaylistItem:
    TYPE_MUSIC  = "Música"
    TYPE_JINGLE = "Jingle"
    TYPE_SPOT   = "Spot"

    def __init__(self, path, title="", artist="", duration=0, item_type=None):
        self.path      = path
        self.title     = title or os.path.splitext(os.path.basename(path))[0]
        self.artist    = artist
        self.duration  = duration
        self.item_type = item_type or self.TYPE_MUSIC

    def duration_str(self):
        if self.duration <= 0:
            return "--:--"
        m, s = divmod(int(self.duration), 60)
        return f"{m:02d}:{s:02d}"

    def to_dict(self):
        return {"path": self.path, "title": self.title,
                "artist": self.artist, "duration": self.duration, "type": self.item_type}

    @classmethod
    def from_dict(cls, d):
        return cls(d["path"], d.get("title",""), d.get("artist",""),
                   d.get("duration",0), d.get("type", cls.TYPE_MUSIC))


class SchedulerEvent:
    def __init__(self, time_str, action, file_path="", repeat=False):
        self.time_str = time_str
        self.action   = action
        self.file_path = file_path
        self.repeat   = repeat
        self.executed_today = False

    def to_dict(self):
        return {"time": self.time_str, "action": self.action,
                "file": self.file_path, "repeat": self.repeat}

    @classmethod
    def from_dict(cls, d):
        return cls(d["time"], d["action"], d.get("file",""), d.get("repeat", False))


# ══════════════════════════════════════════
#  MOTOR DE AUDIO
# ══════════════════════════════════════════
class AudioEngine(QThread):
    songFinished   = pyqtSignal()
    positionUpdate = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self._player  = None
        self._vlc     = None
        self._volume  = 85
        self._playing = False
        self._init_vlc()

    def _init_vlc(self):
        try:
            import vlc
            self._vlc    = vlc.Instance("--no-xlib")
            self._player = self._vlc.media_player_new()
            em = self._player.event_manager()
            em.event_attach(vlc.EventType.MediaPlayerEndReached,
                            lambda e: self.songFinished.emit())
        except Exception as ex:
            print(f"VLC: {ex}")

    def play(self, path):
        if not os.path.exists(path):
            return False
        try:
            import vlc
            media = self._vlc.media_new(path)
            self._player.set_media(media)
            self._player.play()
            self._player.audio_set_volume(self._volume)
            self._playing = True
            threading.Thread(target=self._pos_loop, daemon=True).start()
            return True
        except Exception as ex:
            print(f"Play error: {ex}")
            return False

    def pause(self):
        if self._player:
            self._player.pause()
            self._playing = not self._playing

    def stop(self):
        if self._player:
            self._player.stop()
        self._playing = False

    def set_volume(self, v):
        self._volume = v
        if self._player:
            try:
                self._player.audio_set_volume(v)
            except:
                pass

    def get_position(self):
        if self._player:
            try:
                return self._player.get_time()/1000.0, self._player.get_length()/1000.0
            except:
                pass
        return 0, 0

    def is_playing(self):
        return self._playing

    def _pos_loop(self):
        while self._playing:
            pos, dur = self.get_position()
            self.positionUpdate.emit(pos, dur)
            time.sleep(0.5)


# ══════════════════════════════════════════
#  MOTOR DE STREAMING
# ══════════════════════════════════════════
class StreamEngine(QThread):
    statusChanged   = pyqtSignal(bool, str)
    listenersUpdate = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._process   = None
        self._connected = False
        self._cfg       = {}
        self._mon_timer = QTimer()
        self._mon_timer.timeout.connect(self._poll_listeners)

    def configure(self, cfg: dict):
        self._cfg = cfg

    def connect_stream(self):
        c = self._cfg
        if not c:
            return False

        stype = c.get("type", "icecast2")

        if "shoutcast" in stype:
            # Shoutcast URL: http://source:pass@host:port/
            version = "1" if "v1" in stype else "2"
            if version == "1":
                url = f"icecast://source:{c['password']}@{c['host']}:{c['port']}/"
            else:
                url = (f"icecast://source:{c['password']}@"
                       f"{c['host']}:{c['port']}/{c.get('sid','1')}")
        else:
            # Icecast2
            url = (f"icecast://source:{c['password']}@"
                   f"{c['host']}:{c['port']}{c.get('mountpoint','/stream')}")

        bitrate = c.get("bitrate", 128)
        fmt     = c.get("format", "mp3").lower()
        codec   = "libmp3lame" if fmt == "mp3" else ("libfdk_aac" if fmt == "aac" else "libvorbis")
        ofmt    = "mp3" if fmt == "mp3" else ("adts" if fmt == "aac" else "ogg")

        # Capturar audio del sistema (loopback) o dispositivo
        if sys.platform == "win32":
            audio_src = ["-f", "dshow", "-i", "audio=Mezcla estéreo"]
        elif sys.platform == "darwin":
            audio_src = ["-f", "avfoundation", "-i", ":0"]
        else:
            audio_src = ["-f", "pulse", "-i", "default"]

        cmd = (["ffmpeg", "-re"] + audio_src +
               ["-acodec", codec, "-ab", f"{bitrate}k",
                "-ar", "44100", "-f", ofmt, url, "-y"])
        try:
            self._process = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._connected = True
            label = "Shoutcast" if "shoutcast" in stype else "Icecast2"
            self.statusChanged.emit(True, f"Conectado — {label} {c['host']}:{c['port']}")
            self._mon_timer.start(12000)
            return True
        except FileNotFoundError:
            self.statusChanged.emit(False, "FFmpeg no encontrado")
            return False
        except Exception as ex:
            self.statusChanged.emit(False, str(ex))
            return False

    def disconnect_stream(self):
        if self._process:
            self._process.terminate()
            self._process = None
        self._connected = False
        self._mon_timer.stop()
        self.statusChanged.emit(False, "Desconectado")

    def is_connected(self):
        return self._connected

    def _poll_listeners(self):
        c = self._cfg
        if not c:
            return
        try:
            stype = c.get("type","icecast2")
            if "shoutcast" in stype:
                url = f"http://{c['host']}:{c['port']}/stats"
            else:
                url = f"http://{c['host']}:{c['port']}/status-json.xsl"
            r = requests.get(url, timeout=3)
            data = r.json()
            sources = data.get("icestats",{}).get("source",[])
            if isinstance(sources, dict):
                sources = [sources]
            for s in sources:
                if c.get("mountpoint","") in str(s.get("listenurl","")):
                    self.listenersUpdate.emit(int(s.get("listeners",0)))
                    return
        except:
            pass


# ══════════════════════════════════════════
#  VENTANA PRINCIPAL
# ══════════════════════════════════════════
class PoleCasterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION} — {APP_BRAND}")
        self.setMinimumSize(1120, 700)
        self.resize(1300, 760)

        self.playlist         = []
        self.current_index    = -1
        self.is_playing       = False
        self.jingles          = [""] * 9
        self.scheduler_events = []
        self._peak_listeners  = 0

        self.audio_engine  = AudioEngine()
        self.stream_engine = StreamEngine()

        self._build_ui()
        self._connect_signals()
        self._load_config()

        self._clock_timer = QTimer()
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)

        self._sched_timer = QTimer()
        self._sched_timer.timeout.connect(self._check_scheduler)
        self._sched_timer.start(15000)

        self._update_clock()

    # ──────────────────────────────────────
    #  BUILD UI
    # ──────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._build_menubar()

        # Header de marca
        self._brand_header = BrandHeader()
        root.addWidget(self._brand_header)

        # Toolbar
        root.addWidget(self._build_toolbar())

        # Paneles superiores
        root.addWidget(self._build_top_panels())

        # ECUALIZADOR VISUAL
        root.addWidget(self._build_equalizer_section())

        sep = QFrame(); sep.setObjectName("hSep")
        sep.setFrameShape(QFrame.Shape.HLine); sep.setFixedHeight(1)
        root.addWidget(sep)

        # Panel principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_left_panel())
        splitter.addWidget(self._build_right_panel())
        splitter.setSizes([780, 360])
        root.addWidget(splitter, 1)

        root.addWidget(self._build_status_bar())

    def _build_menubar(self):
        mb = self.menuBar()
        mb.setStyleSheet("""
            QMenuBar { background:#050505; color:#888; border-bottom:1px solid #1a1a1a; padding:2px 4px; }
            QMenuBar::item:selected { background:#1a1a1a; color:#ff6600; }
            QMenu { background:#111; border:1px solid #2a2a2a; }
            QMenu::item { padding:6px 20px; color:#bbb; }
            QMenu::item:selected { background:#1e1e1e; color:#ff6600; }
            QMenu::separator { height:1px; background:#2a2a2a; margin:3px 0; }
        """)
        fm = mb.addMenu("Archivo")
        fm.addAction("Nueva playlist",   self._new_playlist)
        fm.addAction("Abrir playlist",   self._open_playlist)
        fm.addAction("Guardar playlist", self._save_playlist)
        fm.addSeparator()
        fm.addAction("Salir", self.close)
        mb.addMenu("Editar")
        mb.addMenu("Streaming")
        mb.addMenu("Herramientas")
        hm = mb.addMenu("Ayuda")
        hm.addAction(f"Acerca de {APP_NAME}", lambda: QMessageBox.about(
            self, APP_NAME,
            f"<b>{APP_NAME} v{APP_VERSION}</b><br>"
            f"<i>{APP_BRAND}</i><br><br>"
            "Automatizador de Radio con soporte<br>"
            "Icecast2 + Shoutcast v1/v2<br><br>"
            "Inspirado en ZaraRadio y RadioBOSS"))

    def _build_toolbar(self):
        bar = QWidget()
        bar.setFixedHeight(32)
        bar.setStyleSheet("background:#0a0a0a;border-bottom:1px solid #1a1a1a;")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(8, 2, 8, 2)
        lay.setSpacing(4)
        for lbl, slot in [("+ Agregar", self._add_files),
                           ("Abrir PL",  self._open_playlist),
                           ("Guardar PL",self._save_playlist)]:
            b = QPushButton(lbl)
            b.setFixedHeight(24)
            b.clicked.connect(slot)
            lay.addWidget(b)
        sep = QFrame(); sep.setObjectName("vSep"); sep.setFrameShape(QFrame.Shape.VLine); sep.setFixedWidth(1)
        lay.addWidget(sep)
        for lbl in ["Normalizar", "Crossfade", "Explorador"]:
            b = QPushButton(lbl); b.setFixedHeight(24); lay.addWidget(b)
        lay.addStretch()
        self.lbl_date  = QLabel()
        self.lbl_date.setStyleSheet("color:#444;font-size:11px;")
        self.lbl_clock = QLabel("--:--:--")
        self.lbl_clock.setStyleSheet("color:#ff6600;font-family:'Courier New';font-size:13px;font-weight:bold;")
        lay.addWidget(self.lbl_date)
        lay.addWidget(self.lbl_clock)
        return bar

    def _build_top_panels(self):
        top = QWidget()
        top.setFixedHeight(138)
        top.setStyleSheet("background:#0d0d0d;")
        lay = QHBoxLayout(top)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self._panel_now_playing(), 1)
        lay.addWidget(self._vsep())
        lay.addWidget(self._panel_next(), 1)
        lay.addWidget(self._vsep())
        lay.addWidget(self._panel_stream_status(), 1)
        return top

    def _vsep(self):
        f = QFrame(); f.setObjectName("vSep")
        f.setFrameShape(QFrame.Shape.VLine); f.setFixedWidth(1)
        return f

    def _panel_now_playing(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(5)

        lbl = QLabel("EN EL AIRE")
        lbl.setStyleSheet("color:#444;font-size:9px;letter-spacing:2px;")
        lay.addWidget(lbl)

        row = QHBoxLayout()
        self.lbl_onair = QLabel("● ON AIR")
        self.lbl_onair.setStyleSheet(
            "color:#fff;background:#cc3300;font-weight:bold;font-size:10px;"
            "padding:2px 8px;border-radius:3px;")
        row.addWidget(self.lbl_onair)
        row.addStretch()
        lay.addLayout(row)

        self.lbl_now_title  = QLabel("Esperando...")
        self.lbl_now_title.setStyleSheet("color:#fff;font-size:14px;font-weight:bold;")
        self.lbl_now_artist = QLabel("")
        self.lbl_now_artist.setStyleSheet("color:#ff6600;font-size:12px;")
        lay.addWidget(self.lbl_now_title)
        lay.addWidget(self.lbl_now_artist)

        time_row = QHBoxLayout()
        for attr, lbl_txt in [("lbl_remaining","Restante"), ("lbl_endtime","Fin a las")]:
            box = QVBoxLayout()
            l1  = QLabel(lbl_txt)
            l1.setStyleSheet("color:#444;font-size:9px;")
            l2  = QLabel("--:--")
            l2.setStyleSheet("color:#fff;font-family:'Courier New';font-size:16px;font-weight:bold;")
            setattr(self, attr, l2)
            box.addWidget(l1); box.addWidget(l2)
            time_row.addLayout(box)
        lay.addLayout(time_row)
        return w

    def _panel_next(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(5)
        lbl = QLabel("SIGUIENTE")
        lbl.setStyleSheet("color:#444;font-size:9px;letter-spacing:2px;")
        lay.addWidget(lbl)
        self.lbl_next_title  = QLabel("—")
        self.lbl_next_title.setStyleSheet("color:#fff;font-size:13px;font-weight:bold;")
        self.lbl_next_artist = QLabel("")
        self.lbl_next_artist.setStyleSheet("color:#777;font-size:11px;")
        lay.addWidget(self.lbl_next_title)
        lay.addWidget(self.lbl_next_artist)
        lbl2 = QLabel("DESPUÉS")
        lbl2.setStyleSheet("color:#444;font-size:9px;letter-spacing:2px;margin-top:4px;")
        lay.addWidget(lbl2)
        self.lbl_after_next = QLabel("—")
        self.lbl_after_next.setStyleSheet("color:#555;font-size:11px;")
        lay.addWidget(self.lbl_after_next)
        lay.addStretch()
        row = QHBoxLayout()
        for txt, slot in [("⏭ Saltar", self._skip_next),("🔀 Aleatorio", self._shuffle)]:
            b = QPushButton(txt); b.setFixedHeight(24); b.clicked.connect(slot)
            row.addWidget(b)
        lay.addLayout(row)
        return w

    def _panel_stream_status(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(5)
        lbl = QLabel("STREAMING")
        lbl.setStyleSheet("color:#444;font-size:9px;letter-spacing:2px;")
        lay.addWidget(lbl)
        sr = QHBoxLayout()
        self.lbl_sdot = QLabel("●")
        self.lbl_sdot.setStyleSheet("color:#550000;font-size:16px;")
        self.lbl_stext = QLabel("Desconectado")
        self.lbl_stext.setStyleSheet("color:#777;font-size:12px;")
        sr.addWidget(self.lbl_sdot); sr.addWidget(self.lbl_stext); sr.addStretch()
        lay.addLayout(sr)
        grid = QGridLayout(); grid.setSpacing(4)
        for ri, (k, attr) in enumerate([
            ("Servidor", "lbl_si_server"), ("Puerto",   "lbl_si_port"),
            ("Bitrate",  "lbl_si_bitrate"),("Oyentes", "lbl_si_listeners")]):
            lk = QLabel(k); lk.setStyleSheet("color:#444;font-size:10px;")
            lv = QLabel("—"); lv.setStyleSheet("color:#ff6600;font-size:11px;font-weight:bold;")
            setattr(self, attr, lv)
            grid.addWidget(lk, ri, 0); grid.addWidget(lv, ri, 1)
        lay.addLayout(grid)
        lay.addStretch()
        return w

    # ── ECUALIZADOR ───────────────────────
    def _build_equalizer_section(self):
        container = QWidget()
        container.setFixedHeight(100)
        container.setStyleSheet("background:#0d0d0d;border-bottom:1px solid #1a1a1a;")
        lay = QHBoxLayout(container)
        lay.setContentsMargins(10, 6, 10, 6)
        lay.setSpacing(10)

        # Etiqueta izquierda
        left = QVBoxLayout()
        lbl_eq = QLabel("ECUALIZADOR")
        lbl_eq.setStyleSheet("color:#333;font-size:9px;letter-spacing:2px;")
        self.lbl_eq_status = QLabel("SILENCIO")
        self.lbl_eq_status.setStyleSheet("color:#444;font-size:10px;font-weight:bold;")
        left.addWidget(lbl_eq)
        left.addWidget(self.lbl_eq_status)
        left.addStretch()
        lay.addLayout(left)

        # Widget ecualizador
        self.eq_widget = EqualizerWidget()
        lay.addWidget(self.eq_widget, 1)

        # Etiqueta derecha
        right = QVBoxLayout()
        lbl_gc = QLabel(APP_BRAND.upper())
        lbl_gc.setStyleSheet("color:#2a2a2a;font-size:9px;letter-spacing:1px;")
        lbl_gc.setAlignment(Qt.AlignmentFlag.AlignRight)
        right.addWidget(lbl_gc)
        right.addStretch()
        lay.addLayout(right)
        return container

    # ── PANEL IZQUIERDO ───────────────────
    def _build_left_panel(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        tabs = QTabWidget()
        tabs.addTab(self._tab_playlist(),  "Playlist")
        tabs.addTab(self._tab_scheduler(), "Scheduler")
        tabs.addTab(self._tab_jingles(),   "Jingles F1–F9")
        lay.addWidget(tabs, 1)
        lay.addWidget(self._build_transport())
        return w

    def _tab_playlist(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self.playlist_table = QTableWidget(0, 5)
        self.playlist_table.setHorizontalHeaderLabels(["#","Título","Artista","Tipo","Dur."])
        self.playlist_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.playlist_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.playlist_table.setColumnWidth(0, 28); self.playlist_table.setColumnWidth(3, 68)
        self.playlist_table.setColumnWidth(4, 55)
        self.playlist_table.verticalHeader().setVisible(False)
        self.playlist_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.playlist_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.playlist_table.doubleClicked.connect(lambda idx: self._play_index(idx.row()))
        lay.addWidget(self.playlist_table)

        btn_bar = QWidget(); btn_bar.setStyleSheet("background:#0a0a0a;")
        bl = QHBoxLayout(btn_bar); bl.setContentsMargins(6,4,6,4); bl.setSpacing(4)
        for txt, slot in [("+ Archivos", self._add_files), ("+ Carpeta", self._add_folder),
                           ("✕ Quitar", self._remove_selected), ("↑", self._move_up),
                           ("↓", self._move_down), ("Limpiar", self._clear_playlist)]:
            b = QPushButton(txt); b.setFixedHeight(22); b.clicked.connect(slot); bl.addWidget(b)
        bl.addStretch()
        self.lbl_total = QLabel("0 pistas")
        self.lbl_total.setStyleSheet("color:#444;font-size:10px;")
        bl.addWidget(self.lbl_total)
        lay.addWidget(btn_bar)
        return w

    def _tab_scheduler(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(8,8,8,8); lay.setSpacing(6)
        top = QHBoxLayout()
        top.addWidget(QLabel("Eventos programados"))
        top.addStretch()
        b = QPushButton("+ Nuevo"); b.setFixedHeight(24); b.clicked.connect(self._add_event)
        top.addWidget(b)
        lay.addLayout(top)
        self.sched_table = QTableWidget(0, 4)
        self.sched_table.setHorizontalHeaderLabels(["Hora","Acción","Archivo","Estado"])
        self.sched_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.sched_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.sched_table.setColumnWidth(0,55); self.sched_table.setColumnWidth(3,75)
        self.sched_table.verticalHeader().setVisible(False)
        lay.addWidget(self.sched_table)
        return w

    def _tab_jingles(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(10,10,10,10); lay.setSpacing(8)
        hint = QLabel("Presiona F1–F9 para disparar jingles en vivo. Clic derecho para asignar archivo.")
        hint.setStyleSheet("color:#555;font-size:11px;"); hint.setWordWrap(True)
        lay.addWidget(hint)
        grid = QGridLayout(); grid.setSpacing(6)
        self.jingle_btns = []
        for i in range(9):
            btn = QPushButton(f"  F{i+1}\nJingle {i+1}\n(vacío)")
            btn.setStyleSheet("""
                QPushButton { background:#141414; color:#ff6600; border:1px solid #2a2a2a;
                              padding:8px 4px; border-radius:5px; min-height:58px; font-size:11px; }
                QPushButton:hover { background:#1e1e1e; border-color:#ff6600; }
                QPushButton:pressed { background:#0a0a0a; }
            """)
            btn.clicked.connect(lambda _, idx=i: self._play_jingle(idx))
            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda _, idx=i: self._assign_jingle(idx))
            self.jingle_btns.append(btn)
            grid.addWidget(btn, i//3, i%3)
        lay.addLayout(grid)
        lay.addStretch()
        return w

    def _build_transport(self):
        w = QWidget(); w.setFixedHeight(68)
        w.setStyleSheet("background:#080808;border-top:1px solid #1a1a1a;")
        lay = QVBoxLayout(w); lay.setContentsMargins(10,4,10,4); lay.setSpacing(4)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(1000); self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False); self.progress_bar.setFixedHeight(4)
        lay.addWidget(self.progress_bar)

        row = QHBoxLayout(); row.setSpacing(6)
        self.btn_prev = QPushButton("⏮"); self.btn_prev.setFixedSize(28,28); self.btn_prev.clicked.connect(self._play_prev)
        self.btn_stop = QPushButton("⏹"); self.btn_stop.setObjectName("btnStop"); self.btn_stop.setFixedSize(38,38); self.btn_stop.clicked.connect(self._stop)
        self.btn_play = QPushButton("▶"); self.btn_play.setObjectName("btnPlay"); self.btn_play.setFixedSize(38,38); self.btn_play.clicked.connect(self._toggle_play)
        self.btn_next = QPushButton("⏭"); self.btn_next.setFixedSize(28,28); self.btn_next.clicked.connect(self._skip_next)
        self.btn_mic  = QPushButton("🎙"); self.btn_mic.setFixedSize(28,28)
        for b in [self.btn_prev,self.btn_stop,self.btn_play,self.btn_next,self.btn_mic]:
            row.addWidget(b)
        sep = QFrame(); sep.setObjectName("vSep"); sep.setFrameShape(QFrame.Shape.VLine); sep.setFixedWidth(1)
        row.addWidget(sep)
        lv = QLabel("Vol"); lv.setStyleSheet("color:#444;font-size:11px;"); row.addWidget(lv)
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0,100); self.vol_slider.setValue(85); self.vol_slider.setFixedWidth(90)
        self.vol_slider.valueChanged.connect(lambda v: (
            self.lbl_vol_val.setText(f"{v}%"), self.audio_engine.set_volume(v)))
        row.addWidget(self.vol_slider)
        self.lbl_vol_val = QLabel("85%")
        self.lbl_vol_val.setStyleSheet("color:#ff6600;font-size:11px;min-width:32px;")
        row.addWidget(self.lbl_vol_val)
        row.addStretch()
        self.lbl_pos = QLabel("00:00 / 00:00")
        self.lbl_pos.setStyleSheet("color:#444;font-family:'Courier New';font-size:11px;")
        row.addWidget(self.lbl_pos)
        lay.addLayout(row)
        return w

    # ── PANEL DERECHO ─────────────────────
    def _build_right_panel(self):
        w = QWidget(); w.setStyleSheet("background:#0d0d0d;")
        lay = QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        tabs = QTabWidget()
        tabs.addTab(self._tab_streaming(),    "Streaming")
        tabs.addTab(self._tab_metadata(),     "Metadatos")
        tabs.addTab(self._tab_stream_cfg(),   "Configuración")
        lay.addWidget(tabs)
        return w

    def _tab_streaming(self):
        w = QWidget()
        lay = QVBoxLayout(w); lay.setContentsMargins(10,10,10,10); lay.setSpacing(8)

        grp = QGroupBox("SERVIDOR")
        gl  = QGridLayout(grp); gl.setSpacing(6)

        gl.addWidget(QLabel("Tipo:"), 0, 0)
        self.combo_stype = QComboBox()
        self.combo_stype.addItems(["Icecast2", "Shoutcast v1", "Shoutcast v2"])
        self.combo_stype.currentIndexChanged.connect(self._on_stype_change)
        gl.addWidget(self.combo_stype, 0, 1, 1, 2)

        gl.addWidget(QLabel("Host / IP:"), 1, 0)
        self.edit_host = QLineEdit("localhost")
        gl.addWidget(self.edit_host, 1, 1, 1, 2)

        gl.addWidget(QLabel("Puerto:"), 2, 0)
        self.edit_port = QLineEdit("8000")
        gl.addWidget(self.edit_port, 2, 1)

        # Mountpoint (Icecast) / SID (Shoutcast v2)
        self.lbl_mount_label = QLabel("Montaje:")
        gl.addWidget(self.lbl_mount_label, 3, 0)
        self.edit_mountpoint = QLineEdit("/stream")
        gl.addWidget(self.edit_mountpoint, 3, 1, 1, 2)

        gl.addWidget(QLabel("Contraseña:"), 4, 0)
        self.edit_password = QLineEdit("hackme")
        self.edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        gl.addWidget(self.edit_password, 4, 1, 1, 2)

        lay.addWidget(grp)

        grp2 = QGroupBox("CALIDAD")
        q2 = QGridLayout(grp2); q2.setSpacing(6)
        q2.addWidget(QLabel("Formato:"), 0, 0)
        self.combo_fmt = QComboBox()
        self.combo_fmt.addItems(["MP3","AAC","OGG Vorbis"])
        q2.addWidget(self.combo_fmt, 0, 1)
        q2.addWidget(QLabel("Bitrate:"), 1, 0)
        br_row = QHBoxLayout()
        self.br_btns = []
        for br in ["64k","128k","192k","320k"]:
            b = QPushButton(br); b.setCheckable(True); b.setFixedHeight(24)
            b.setChecked(br == "128k")
            b.clicked.connect(lambda _,btn=b: self._select_br(btn))
            br_row.addWidget(b); self.br_btns.append(b)
        q2.addLayout(br_row, 1, 1)
        lay.addWidget(grp2)

        grp3 = QGroupBox("OYENTES EN VIVO")
        g3 = QHBoxLayout(grp3)
        self.lbl_listeners = QLabel("0")
        self.lbl_listeners.setStyleSheet("color:#00cc66;font-size:28px;font-family:'Courier New';font-weight:bold;")
        g3.addWidget(self.lbl_listeners)
        u = QLabel("oyentes\nactivos"); u.setStyleSheet("color:#444;font-size:10px;")
        g3.addWidget(u); g3.addStretch()
        self.lbl_peak = QLabel("Pico: 0")
        self.lbl_peak.setStyleSheet("color:#ff6600;font-size:11px;")
        g3.addWidget(self.lbl_peak)
        lay.addWidget(grp3)

        self.btn_stream = QPushButton("Conectar streaming")
        self.btn_stream.setObjectName("btnConnect")
        self.btn_stream.clicked.connect(self._toggle_stream)
        lay.addWidget(self.btn_stream)
        lay.addStretch()
        return w

    def _tab_metadata(self):
        w = QWidget(); lay = QVBoxLayout(w)
        lay.setContentsMargins(10,10,10,10); lay.setSpacing(6)
        for lbl, attr, val in [
            ("Nombre de la radio","edit_rname","Mi Radio Online"),
            ("Descripción",       "edit_rdesc","Radio 24/7"),
            ("Género musical",    "edit_rgenre","Pop / Rock"),
            ("Sitio web",         "edit_rurl","http://miradio.com")]:
            l = QLabel(lbl); l.setStyleSheet("color:#555;font-size:10px;")
            e = QLineEdit(val); setattr(self, attr, e)
            lay.addWidget(l); lay.addWidget(e)
        grp = QGroupBox("METADATA ACTUAL"); g = QVBoxLayout(grp)
        self.lbl_meta_artist = QLabel("Artista: —")
        self.lbl_meta_title  = QLabel("Título: —")
        self.lbl_meta_artist.setStyleSheet("color:#ff6600;")
        self.lbl_meta_title.setStyleSheet("color:#ff6600;")
        g.addWidget(self.lbl_meta_artist); g.addWidget(self.lbl_meta_title)
        hint = QLabel("Se actualiza automáticamente con cada canción")
        hint.setStyleSheet("color:#333;font-size:10px;"); g.addWidget(hint)
        lay.addWidget(grp); lay.addStretch()
        return w

    def _tab_stream_cfg(self):
        w = QWidget(); lay = QVBoxLayout(w)
        lay.setContentsMargins(10,10,10,10); lay.setSpacing(8)
        grp = QGroupBox("COMPORTAMIENTO"); g = QVBoxLayout(grp)
        for lbl, attr, val in [
            ("Reconexión automática",    "chk_reconnect", True),
            ("Crossfade entre canciones","chk_crossfade", True),
            ("Normalización de volumen", "chk_normalize", False),
            ("Modo 24/7 sin pausas",     "chk_247",       True),
            ("Silencio automático 2–6 AM","chk_silence",  False)]:
            c = QCheckBox(lbl); c.setChecked(val); setattr(self, attr, c); g.addWidget(c)
        lay.addWidget(grp)
        grp2 = QGroupBox("CROSSFADE"); g2 = QHBoxLayout(grp2)
        l = QLabel("Duración:"); l.setStyleSheet("color:#555;font-size:11px;"); g2.addWidget(l)
        self.spin_xfade = QSpinBox(); self.spin_xfade.setRange(0,10); self.spin_xfade.setValue(3)
        self.spin_xfade.setSuffix(" seg"); g2.addWidget(self.spin_xfade); g2.addStretch()
        lay.addWidget(grp2); lay.addStretch()
        return w

    def _build_status_bar(self):
        bar = QWidget(); bar.setFixedHeight(20)
        bar.setStyleSheet("background:#050505;border-top:1px solid #111;")
        lay = QHBoxLayout(bar); lay.setContentsMargins(10,0,10,0); lay.setSpacing(16)
        self.lbl_st_play   = QLabel("● Detenido")
        self.lbl_st_stream = QLabel("● Sin conexión")
        self.lbl_st_pl     = QLabel("Playlist: 0 pistas")
        for l in [self.lbl_st_play, self.lbl_st_stream, self.lbl_st_pl]:
            l.setStyleSheet("color:#333;font-size:10px;"); lay.addWidget(l)
        lay.addStretch()
        brand_lbl = QLabel(f"{APP_BRAND} · {APP_NAME} v{APP_VERSION}")
        brand_lbl.setStyleSheet("color:#2a2a2a;font-size:10px;")
        lay.addWidget(brand_lbl)
        return bar

    # ── SIGNALS ───────────────────────────
    def _connect_signals(self):
        self.audio_engine.songFinished.connect(self._on_song_finished)
        self.audio_engine.positionUpdate.connect(self._on_position_update)
        self.stream_engine.statusChanged.connect(self._on_stream_status)
        self.stream_engine.listenersUpdate.connect(self._on_listeners_update)

    # ── PLAYBACK ──────────────────────────
    def _toggle_play(self):
        if self.is_playing:
            self.audio_engine.pause()
            self.is_playing = False
            self.btn_play.setText("▶")
            self.eq_widget.set_playing(False)
            self.lbl_eq_status.setText("PAUSADO")
            self.lbl_eq_status.setStyleSheet("color:#555;font-size:10px;font-weight:bold;")
            self.lbl_st_play.setText("● Pausado")
            self.lbl_st_play.setStyleSheet("color:#cc8800;font-size:10px;")
        else:
            if self.current_index < 0 and self.playlist:
                self._play_index(0); return
            self.audio_engine.pause()
            self.is_playing = True
            self.btn_play.setText("⏸")
            self.eq_widget.set_playing(True)
            self._set_playing_status()

    def _stop(self):
        self.audio_engine.stop()
        self.is_playing = False
        self.btn_play.setText("▶")
        self.progress_bar.setValue(0)
        self.lbl_pos.setText("00:00 / 00:00")
        self.lbl_remaining.setText("--:--")
        self.eq_widget.set_playing(False)
        self.lbl_eq_status.setText("SILENCIO")
        self.lbl_eq_status.setStyleSheet("color:#333;font-size:10px;font-weight:bold;")
        self.lbl_st_play.setText("● Detenido")
        self.lbl_st_play.setStyleSheet("color:#333;font-size:10px;")

    def _play_index(self, index):
        if index < 0 or index >= len(self.playlist):
            return
        item = self.playlist[index]
        if not os.path.exists(item.path):
            QMessageBox.warning(self,"Archivo no encontrado", item.path); return
        self.current_index = index
        self.audio_engine.play(item.path)
        self.is_playing = True
        self.btn_play.setText("⏸")
        self.lbl_now_title.setText(item.title)
        self.lbl_now_artist.setText(item.artist or "—")
        self.lbl_meta_artist.setText(f"Artista: {item.artist}")
        self.lbl_meta_title.setText(f"Título: {item.title}")
        self.eq_widget.set_playing(True)
        self.lbl_eq_status.setText("EN VIVO")
        self.lbl_eq_status.setStyleSheet("color:#ff6600;font-size:10px;font-weight:bold;")
        self._set_playing_status()
        self._update_next_info()
        self._highlight_row(index)

    def _set_playing_status(self):
        self.lbl_st_play.setText("● Reproduciendo")
        self.lbl_st_play.setStyleSheet("color:#00cc66;font-size:10px;")

    def _play_prev(self):
        if self.current_index > 0:
            self._play_index(self.current_index - 1)

    def _skip_next(self):
        ni = self.current_index + 1
        if ni < len(self.playlist):
            self._play_index(ni)
        else:
            self._stop()

    def _on_song_finished(self):
        if hasattr(self,"chk_247") and self.chk_247.isChecked():
            self._skip_next()

    def _on_position_update(self, pos, dur):
        if dur > 0:
            self.progress_bar.setValue(int(pos / dur * 1000))
            self.lbl_pos.setText(f"{int(pos//60):02d}:{int(pos%60):02d} / {int(dur//60):02d}:{int(dur%60):02d}")
            rem = dur - pos
            self.lbl_remaining.setText(f"{int(rem//60):02d}:{int(rem%60):02d}")
            et = datetime.now() + timedelta(seconds=rem)
            self.lbl_endtime.setText(et.strftime("%H:%M"))

    # ── PLAYLIST ──────────────────────────
    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,"Agregar audio","","Audio (*.mp3 *.wav *.ogg *.flac *.aac *.m4a *.wma)")
        for f in files:
            self.playlist.append(PlaylistItem(f))
        self._refresh_playlist()

    def _add_folder(self):
        folder = QFileDialog.getExistingDirectory(self,"Seleccionar carpeta")
        if not folder: return
        for fn in sorted(os.listdir(folder)):
            if os.path.splitext(fn)[1].lower() in {".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}:
                self.playlist.append(PlaylistItem(os.path.join(folder, fn)))
        self._refresh_playlist()

    def _remove_selected(self):
        rows = sorted({i.row() for i in self.playlist_table.selectedIndexes()}, reverse=True)
        for r in rows: self.playlist.pop(r)
        self._refresh_playlist()

    def _move_up(self):
        for r in sorted({i.row() for i in self.playlist_table.selectedIndexes()}):
            if r > 0: self.playlist[r], self.playlist[r-1] = self.playlist[r-1], self.playlist[r]
        self._refresh_playlist()

    def _move_down(self):
        for r in sorted({i.row() for i in self.playlist_table.selectedIndexes()}, reverse=True):
            if r < len(self.playlist)-1: self.playlist[r], self.playlist[r+1] = self.playlist[r+1], self.playlist[r]
        self._refresh_playlist()

    def _clear_playlist(self):
        if QMessageBox.question(self,"Limpiar","¿Limpiar toda la playlist?") == QMessageBox.StandardButton.Yes:
            self.playlist.clear(); self.current_index = -1; self._refresh_playlist()

    def _shuffle(self):
        random.shuffle(self.playlist); self._refresh_playlist()

    def _refresh_playlist(self):
        t = self.playlist_table
        t.setRowCount(len(self.playlist))
        tc_map = {PlaylistItem.TYPE_JINGLE:"#ff6600",
                  PlaylistItem.TYPE_SPOT:"#aa44ff",
                  PlaylistItem.TYPE_MUSIC:"#448888"}
        for i, item in enumerate(self.playlist):
            t.setRowHeight(i, 26)
            t.setItem(i,0,QTableWidgetItem(str(i+1)))
            t.setItem(i,1,QTableWidgetItem(item.title))
            t.setItem(i,2,QTableWidgetItem(item.artist))
            ti = QTableWidgetItem(item.item_type)
            ti.setForeground(QColor(tc_map.get(item.item_type,"#888")))
            t.setItem(i,3,ti)
            t.setItem(i,4,QTableWidgetItem(item.duration_str()))
        td = sum(p.duration for p in self.playlist)
        h,r = divmod(int(td),3600); m,s = divmod(r,60)
        ds  = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        self.lbl_total.setText(f"{len(self.playlist)} pistas — {ds}")
        self.lbl_st_pl.setText(f"Playlist: {len(self.playlist)} pistas")
        self._update_next_info()

    def _highlight_row(self, index):
        for r in range(self.playlist_table.rowCount()):
            for c in range(self.playlist_table.columnCount()):
                it = self.playlist_table.item(r,c)
                if it:
                    it.setBackground(QColor("#ff660015" if r==index else "transparent"))
                    it.setForeground(QColor("#ff8833" if r==index else "#c0c0c0"))

    def _update_next_info(self):
        ni = self.current_index + 1
        if ni < len(self.playlist):
            self.lbl_next_title.setText(self.playlist[ni].title)
            self.lbl_next_artist.setText(f"{self.playlist[ni].artist} — {self.playlist[ni].duration_str()}")
        else:
            self.lbl_next_title.setText("— Fin de playlist —"); self.lbl_next_artist.setText("")
        ai = ni + 1
        self.lbl_after_next.setText(self.playlist[ai].title if ai < len(self.playlist) else "—")

    # ── JINGLES ───────────────────────────
    def _play_jingle(self, idx):
        p = self.jingles[idx]
        if p and os.path.exists(p):
            self.audio_engine.play(p)
        else:
            QMessageBox.information(self,f"Jingle F{idx+1}","Sin archivo. Clic derecho para asignar.")

    def _assign_jingle(self, idx):
        p,_ = QFileDialog.getOpenFileName(self,f"Jingle F{idx+1}","","Audio (*.mp3 *.wav *.ogg *.flac)")
        if p:
            self.jingles[idx] = p
            name = os.path.splitext(os.path.basename(p))[0][:11]
            self.jingle_btns[idx].setText(f"  F{idx+1}\n{name}")

    def keyPressEvent(self, event):
        k = event.key()
        if Qt.Key.Key_F1 <= k <= Qt.Key.Key_F9:
            self._play_jingle(k - Qt.Key.Key_F1)
        super().keyPressEvent(event)

    # ── SCHEDULER ─────────────────────────
    def _add_event(self):
        dlg = QDialog(self); dlg.setWindowTitle("Nuevo evento")
        dlg.setStyleSheet(DARK_STYLE); dlg.setFixedSize(360,230)
        lay = QVBoxLayout(dlg)
        lay.addWidget(QLabel("Hora (HH:MM):"))
        te = QTimeEdit(); te.setDisplayFormat("HH:mm"); lay.addWidget(te)
        lay.addWidget(QLabel("Descripción:"))
        ae = QLineEdit("Jingle horario"); lay.addWidget(ae)
        lay.addWidget(QLabel("Archivo (opcional):"))
        fr = QHBoxLayout(); fe = QLineEdit()
        fb = QPushButton("..."); fb.setFixedWidth(30)
        fb.clicked.connect(lambda: fe.setText(
            QFileDialog.getOpenFileName(dlg,"","","Audio (*.mp3 *.wav *.ogg)")[0]))
        fr.addWidget(fe); fr.addWidget(fb); lay.addLayout(fr)
        rc = QCheckBox("Repetir todos los días"); lay.addWidget(rc)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject); lay.addWidget(bb)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.scheduler_events.append(SchedulerEvent(
                te.time().toString("HH:mm"), ae.text(), fe.text(), rc.isChecked()))
            self._refresh_sched()

    def _refresh_sched(self):
        t = self.sched_table; t.setRowCount(len(self.scheduler_events))
        now = datetime.now().strftime("%H:%M")
        for i, ev in enumerate(self.scheduler_events):
            t.setRowHeight(i,26)
            t.setItem(i,0,QTableWidgetItem(ev.time_str))
            t.setItem(i,1,QTableWidgetItem(ev.action))
            t.setItem(i,2,QTableWidgetItem(os.path.basename(ev.file_path) if ev.file_path else "—"))
            done = ev.executed_today or ev.time_str < now
            si = QTableWidgetItem("Ejecutado" if done else "Pendiente")
            si.setForeground(QColor("#00cc66" if done else "#ff6600")); t.setItem(i,3,si)

    def _check_scheduler(self):
        now = datetime.now().strftime("%H:%M")
        for ev in self.scheduler_events:
            if ev.time_str == now and not ev.executed_today:
                ev.executed_today = True
                if ev.file_path and os.path.exists(ev.file_path):
                    self.audio_engine.play(ev.file_path)
                self._refresh_sched()

    # ── STREAMING ─────────────────────────
    def _on_stype_change(self, idx):
        stype = self.combo_stype.currentText().lower()
        if "shoutcast v2" in stype:
            self.lbl_mount_label.setText("Station ID:")
            self.edit_mountpoint.setText("1")
        elif "shoutcast v1" in stype:
            self.lbl_mount_label.setText("Contraseña fuente:")
            self.edit_mountpoint.setText("")
            self.edit_mountpoint.setPlaceholderText("(misma contraseña)")
        else:
            self.lbl_mount_label.setText("Montaje:")
            self.edit_mountpoint.setText("/stream")

    def _select_br(self, clicked):
        for b in self.br_btns:
            b.setChecked(False)
            b.setStyleSheet("")
        clicked.setChecked(True)
        clicked.setStyleSheet("background:#ff660022;border-color:#ff6600;color:#ff6600;")

    def _toggle_stream(self):
        if self.stream_engine.is_connected():
            self.stream_engine.disconnect_stream()
        else:
            stype = self.combo_stype.currentText().lower()
            br    = int(next((b.text().replace("k","") for b in self.br_btns if b.isChecked()), "128"))
            cfg = {
                "type":       "shoutcast_v1" if "v1" in stype else ("shoutcast_v2" if "v2" in stype else "icecast2"),
                "host":       self.edit_host.text(),
                "port":       int(self.edit_port.text()),
                "mountpoint": self.edit_mountpoint.text(),
                "password":   self.edit_password.text(),
                "bitrate":    br,
                "format":     self.combo_fmt.currentText().lower().split()[0],
            }
            if "v2" in stype:
                cfg["sid"] = self.edit_mountpoint.text()
            self.stream_engine.configure(cfg)
            self.stream_engine.connect_stream()

    def _on_stream_status(self, connected, msg):
        self.lbl_stext.setText(msg)
        if connected:
            self.lbl_sdot.setStyleSheet("color:#00cc66;font-size:16px;")
            self.btn_stream.setText("Desconectar streaming")
            self.btn_stream.setObjectName("btnDisconnect")
            self.lbl_st_stream.setText("● Streaming activo")
            self.lbl_st_stream.setStyleSheet("color:#ff6600;font-size:10px;")
            self.lbl_si_server.setText(self.edit_host.text())
            self.lbl_si_port.setText(self.edit_port.text())
            br = next((b.text() for b in self.br_btns if b.isChecked()), "128k")
            self.lbl_si_bitrate.setText(br + "ps")
        else:
            self.lbl_sdot.setStyleSheet("color:#550000;font-size:16px;")
            self.btn_stream.setText("Conectar streaming")
            self.btn_stream.setObjectName("btnConnect")
            self.lbl_st_stream.setText("● Sin conexión")
            self.lbl_st_stream.setStyleSheet("color:#333;font-size:10px;")
            for l in [self.lbl_si_server,self.lbl_si_port,self.lbl_si_bitrate,self.lbl_si_listeners]:
                l.setText("—")
        self.btn_stream.setStyleSheet("")

    def _on_listeners_update(self, count):
        self.lbl_listeners.setText(str(count))
        self.lbl_si_listeners.setText(str(count))
        if count > self._peak_listeners:
            self._peak_listeners = count
            self.lbl_peak.setText(f"Pico: {count}")

    # ── PLAYLIST FILES ────────────────────
    def _new_playlist(self): self._clear_playlist()

    def _open_playlist(self):
        p,_ = QFileDialog.getOpenFileName(self,"Abrir playlist","","PoleCaster Playlist (*.pcp)")
        if not p: return
        try:
            with open(p,"r",encoding="utf-8") as f: data = json.load(f)
            self.playlist = [PlaylistItem.from_dict(d) for d in data.get("playlist",[])]
            self._refresh_playlist()
        except Exception as ex:
            QMessageBox.critical(self,"Error",str(ex))

    def _save_playlist(self):
        p,_ = QFileDialog.getSaveFileName(self,"Guardar playlist","","PoleCaster Playlist (*.pcp)")
        if not p: return
        try:
            with open(p,"w",encoding="utf-8") as f:
                json.dump({"playlist":[i.to_dict() for i in self.playlist]},f,indent=2)
        except Exception as ex:
            QMessageBox.critical(self,"Error",str(ex))

    # ── CONFIG ────────────────────────────
    def _load_config(self):
        if not os.path.exists(CONFIG_FILE): return
        try:
            with open(CONFIG_FILE) as f: cfg = json.load(f)
            self.edit_host.setText(cfg.get("host","localhost"))
            self.edit_port.setText(cfg.get("port","8000"))
            self.edit_mountpoint.setText(cfg.get("mountpoint","/stream"))
            self.edit_rname.setText(cfg.get("radio_name","Mi Radio Online"))
            self.jingles = cfg.get("jingles",[""] * 9)
            for i,p in enumerate(self.jingles):
                if p:
                    self.jingle_btns[i].setText(f"  F{i+1}\n{os.path.splitext(os.path.basename(p))[0][:11]}")
        except: pass

    def _save_config(self):
        cfg = {"host":self.edit_host.text(),"port":self.edit_port.text(),
               "mountpoint":self.edit_mountpoint.text(),"password":self.edit_password.text(),
               "radio_name":self.edit_rname.text(),"jingles":self.jingles}
        with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,indent=2)

    # ── CLOCK ─────────────────────────────
    def _update_clock(self):
        now = datetime.now()
        self.lbl_clock.setText(now.strftime("%H:%M:%S"))
        self.lbl_date.setText(now.strftime("%a %d %b"))
        if now.hour == 0 and now.minute == 0 and now.second < 2:
            for ev in self.scheduler_events: ev.executed_today = False

    def closeEvent(self, event):
        self._save_config()
        self.audio_engine.stop()
        if self.stream_engine.is_connected(): self.stream_engine.disconnect_stream()
        event.accept()


# ══════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setStyleSheet(DARK_STYLE)
    pal = app.palette()
    pal.setColor(QPalette.ColorRole.Window,        QColor("#0d0d0d"))
    pal.setColor(QPalette.ColorRole.WindowText,    QColor("#e8e8e8"))
    pal.setColor(QPalette.ColorRole.Base,          QColor("#0a0a0a"))
    pal.setColor(QPalette.ColorRole.Text,          QColor("#e8e8e8"))
    pal.setColor(QPalette.ColorRole.Button,        QColor("#1a1a1a"))
    pal.setColor(QPalette.ColorRole.ButtonText,    QColor("#e8e8e8"))
    pal.setColor(QPalette.ColorRole.Highlight,     QColor("#ff6600"))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)
    win = PoleCasterWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
