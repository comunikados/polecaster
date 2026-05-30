"""
PoleCaster v3.0 — Radio Automation Suite
Diseño: Grup Comunicados
Layout basado en bosquejo oficial + inspiración ZaraRadio + RadioBOSS
"""

import sys, os, json, time, threading, subprocess, random, math
import requests
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QTabWidget, QLineEdit, QComboBox,
    QCheckBox, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QGroupBox, QGridLayout, QSpinBox, QFrame, QProgressBar,
    QDialog, QDialogButtonBox, QTimeEdit, QMessageBox, QSizePolicy,
    QScrollArea, QTreeWidget, QTreeWidgetItem, QToolBar, QStatusBar,
    QStackedWidget, QTextEdit, QAbstractItemView, QMenu
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize, QPoint
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QPainter, QLinearGradient,
    QPen, QAction, QActionGroup, QPixmap, QIcon, QKeySequence
)

APP_NAME    = "PoleCaster"
APP_VERSION = "3.0"
APP_BRAND   = "Grup Comunicados"
CONFIG_FILE = "polecaster_config.json"
DAYS_ES     = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]

# ══════════════════════════════════════════
#  TEMAS: OSCURO Y CLARO
# ══════════════════════════════════════════
THEME_DARK = """
QMainWindow,QWidget{background:#0d0d0d;color:#e8e8e8;font-family:'Segoe UI',sans-serif;font-size:12px;}
QMenuBar{background:#080808;color:#999;border-bottom:1px solid #1a1a1a;padding:2px;}
QMenuBar::item:selected{background:#1a1a1a;color:#ff6600;}
QMenu{background:#111;border:1px solid #2a2a2a;color:#ddd;}
QMenu::item:selected{background:#ff660022;color:#ff6600;}
QMenu::separator{height:1px;background:#2a2a2a;margin:3px 8px;}
QToolBar{background:#0a0a0a;border-bottom:1px solid #1a1a1a;spacing:3px;padding:2px;}
QStatusBar{background:#050505;color:#444;border-top:1px solid #111;font-size:10px;}
QTabWidget::pane{border:1px solid #222;background:#111;}
QTabBar::tab{background:#0a0a0a;color:#666;padding:6px 14px;border:none;font-size:11px;}
QTabBar::tab:selected{color:#ff6600;border-bottom:2px solid #ff6600;background:#111;}
QTabBar::tab:hover{color:#ccc;background:#141414;}
QTableWidget{background:#111;gridline-color:#1a1a1a;border:none;alternate-background-color:#141414;}
QTableWidget::item{padding:3px 5px;border-bottom:1px solid #141414;}
QTableWidget::item:selected{background:#ff660020;color:#fff;}
QHeaderView::section{background:#0a0a0a;color:#555;padding:4px 6px;border:none;font-size:10px;letter-spacing:1px;}
QPushButton{background:#1a1a1a;color:#bbb;border:1px solid #2a2a2a;padding:4px 10px;border-radius:3px;font-size:11px;}
QPushButton:hover{background:#242424;color:#fff;border-color:#444;}
QPushButton:pressed{background:#0f0f0f;}
QPushButton:checked{background:#ff660033;border-color:#ff6600;color:#ff6600;}
QPushButton#btnPlay{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #ff6600,stop:1 #cc4400);color:#fff;font-weight:bold;border-radius:18px;border:none;font-size:14px;}
QPushButton#btnPlay:hover{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #ff8833,stop:1 #ee5500);}
QPushButton#btnStop{background:#1e1e1e;color:#fff;border-radius:18px;border:1px solid #333;}
QPushButton#btnConnect{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #cc4400);color:#fff;font-weight:bold;border:none;border-radius:3px;padding:7px;}
QPushButton#btnDisconnect{background:#6b0000;color:#fff;font-weight:bold;border:none;border-radius:3px;padding:7px;}
QPushButton#btnMic{background:#1a2a1a;color:#00cc66;border:1px solid #00cc6655;border-radius:3px;}
QPushButton#btnMic:checked{background:#cc000022;color:#ff4444;border-color:#ff4444;}
QPushButton.transport{background:#1a1a1a;border:1px solid #2a2a2a;border-radius:3px;padding:4px 8px;font-size:11px;color:#bbb;}
QPushButton.transport:hover{background:#2a2a2a;color:#fff;}
QLineEdit,QComboBox,QSpinBox,QTimeEdit{background:#0a0a0a;color:#e0e0e0;border:1px solid #2a2a2a;padding:4px 7px;border-radius:3px;min-height:20px;}
QLineEdit:focus,QComboBox:focus{border-color:#ff6600;}
QComboBox::drop-down{border:none;width:18px;}
QComboBox QAbstractItemView{background:#111;color:#e0e0e0;border:1px solid #333;selection-background-color:#ff660033;}
QSlider::groove:horizontal{height:4px;background:#1e1e1e;border-radius:2px;}
QSlider::handle:horizontal{background:#ff6600;width:12px;height:12px;border-radius:6px;margin:-4px 0;}
QSlider::sub-page:horizontal{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #ff9933);border-radius:2px;}
QSlider::groove:vertical{width:4px;background:#1e1e1e;border-radius:2px;}
QSlider::handle:vertical{background:#ff6600;width:12px;height:12px;border-radius:6px;margin:0 -4px;}
QSlider::sub-page:vertical{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff9933,stop:1 #ff6600);border-radius:2px;}
QProgressBar{background:#1a1a1a;border:none;border-radius:2px;height:4px;}
QProgressBar::chunk{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #ffaa00);border-radius:2px;}
QGroupBox{border:1px solid #222;border-radius:4px;margin-top:8px;padding-top:8px;color:#555;font-size:10px;letter-spacing:1px;}
QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#ff6600;}
QCheckBox{color:#bbb;}
QCheckBox::indicator{width:13px;height:13px;background:#0a0a0a;border:1px solid #333;border-radius:2px;}
QCheckBox::indicator:checked{background:#ff6600;border-color:#ff6600;}
QTreeWidget{background:#0d0d0d;border:none;color:#ccc;alternate-background-color:#111;}
QTreeWidget::item:selected{background:#ff660020;color:#ff8833;}
QTreeWidget::item:hover{background:#141414;}
QScrollBar:vertical{background:#0a0a0a;width:5px;}
QScrollBar::handle:vertical{background:#2a2a2a;border-radius:2px;min-height:20px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}
QScrollBar:horizontal{background:#0a0a0a;height:5px;}
QScrollBar::handle:horizontal{background:#2a2a2a;border-radius:2px;}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{width:0;}
QScrollArea{border:none;background:transparent;}
QFrame#vSep{background:#1e1e1e;max-width:1px;}
QFrame#hSep{background:#1e1e1e;max-height:1px;}
QSplitter::handle{background:#1a1a1a;}
"""

THEME_LIGHT = """
QMainWindow,QWidget{background:#f0f0f0;color:#1a1a1a;font-family:'Segoe UI',sans-serif;font-size:12px;}
QMenuBar{background:#e0e0e0;color:#333;border-bottom:1px solid #ccc;padding:2px;}
QMenuBar::item:selected{background:#fff;color:#cc4400;}
QMenu{background:#fff;border:1px solid #ccc;color:#222;}
QMenu::item:selected{background:#ff660015;color:#cc4400;}
QMenu::separator{height:1px;background:#ddd;margin:3px 8px;}
QToolBar{background:#e8e8e8;border-bottom:1px solid #ccc;spacing:3px;padding:2px;}
QStatusBar{background:#e0e0e0;color:#888;border-top:1px solid #ccc;font-size:10px;}
QTabWidget::pane{border:1px solid #ccc;background:#fff;}
QTabBar::tab{background:#e0e0e0;color:#888;padding:6px 14px;border:none;font-size:11px;}
QTabBar::tab:selected{color:#cc4400;border-bottom:2px solid #ff6600;background:#fff;}
QTabBar::tab:hover{color:#333;background:#ebebeb;}
QTableWidget{background:#fff;gridline-color:#eee;border:none;alternate-background-color:#f8f8f8;}
QTableWidget::item{padding:3px 5px;border-bottom:1px solid #eee;}
QTableWidget::item:selected{background:#ff660015;color:#cc4400;}
QHeaderView::section{background:#e8e8e8;color:#888;padding:4px 6px;border:none;font-size:10px;letter-spacing:1px;}
QPushButton{background:#e8e8e8;color:#333;border:1px solid #ccc;padding:4px 10px;border-radius:3px;font-size:11px;}
QPushButton:hover{background:#fff;color:#111;border-color:#aaa;}
QPushButton:pressed{background:#e0e0e0;}
QPushButton:checked{background:#ff660015;border-color:#ff6600;color:#cc4400;}
QPushButton#btnPlay{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #ff6600,stop:1 #cc4400);color:#fff;font-weight:bold;border-radius:18px;border:none;font-size:14px;}
QPushButton#btnStop{background:#ddd;color:#333;border-radius:18px;border:1px solid #ccc;}
QPushButton#btnConnect{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #cc4400);color:#fff;font-weight:bold;border:none;border-radius:3px;padding:7px;}
QPushButton#btnDisconnect{background:#cc0000;color:#fff;font-weight:bold;border:none;border-radius:3px;padding:7px;}
QPushButton#btnMic{background:#e8f8e8;color:#009933;border:1px solid #009933;border-radius:3px;}
QPushButton#btnMic:checked{background:#ffe8e8;color:#cc0000;border-color:#cc0000;}
QLineEdit,QComboBox,QSpinBox,QTimeEdit{background:#fff;color:#222;border:1px solid #ccc;padding:4px 7px;border-radius:3px;min-height:20px;}
QLineEdit:focus,QComboBox:focus{border-color:#ff6600;}
QComboBox::drop-down{border:none;width:18px;}
QComboBox QAbstractItemView{background:#fff;color:#222;border:1px solid #ccc;selection-background-color:#ff660015;}
QSlider::groove:horizontal{height:4px;background:#ddd;border-radius:2px;}
QSlider::handle:horizontal{background:#ff6600;width:12px;height:12px;border-radius:6px;margin:-4px 0;}
QSlider::sub-page:horizontal{background:#ff6600;border-radius:2px;}
QSlider::groove:vertical{width:4px;background:#ddd;border-radius:2px;}
QSlider::handle:vertical{background:#ff6600;width:12px;height:12px;border-radius:6px;margin:0 -4px;}
QSlider::sub-page:vertical{background:#ff6600;border-radius:2px;}
QProgressBar{background:#ddd;border:none;border-radius:2px;height:4px;}
QProgressBar::chunk{background:#ff6600;border-radius:2px;}
QGroupBox{border:1px solid #ccc;border-radius:4px;margin-top:8px;padding-top:8px;color:#888;font-size:10px;letter-spacing:1px;}
QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#ff6600;}
QCheckBox{color:#333;}
QCheckBox::indicator{width:13px;height:13px;background:#fff;border:1px solid #ccc;border-radius:2px;}
QCheckBox::indicator:checked{background:#ff6600;border-color:#ff6600;}
QTreeWidget{background:#fff;border:none;color:#333;alternate-background-color:#f8f8f8;}
QTreeWidget::item:selected{background:#ff660015;color:#cc4400;}
QScrollBar:vertical{background:#f0f0f0;width:6px;}
QScrollBar::handle:vertical{background:#ccc;border-radius:3px;min-height:20px;}
QScrollBar:horizontal{background:#f0f0f0;height:6px;}
QScrollBar::handle:horizontal{background:#ccc;border-radius:3px;}
QScrollArea{border:none;background:transparent;}
QFrame#vSep{background:#ddd;max-width:1px;}
QFrame#hSep{background:#ddd;max-height:1px;}
QSplitter::handle{background:#ddd;}
"""

# ══════════════════════════════════════════
#  ECUALIZADOR VISUAL
# ══════════════════════════════════════════
class EqualizerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(70)
        self._bars=28; self._heights=[0.0]*28; self._targets=[0.0]*28
        self._peaks=[0.0]*28; self._peak_hold=[0]*28
        self._playing=False; self._phase=0.0
        t=QTimer(self); t.timeout.connect(self._animate); t.start(40)

    def set_playing(self, v):
        self._playing=v
        if not v: self._targets=[0.0]*self._bars

    def _animate(self):
        self._phase+=0.08
        if self._playing:
            for i in range(self._bars):
                base=0.15+0.6*math.exp(-0.04*i)
                w1=0.25*math.sin(self._phase*1.7+i*0.4)
                w2=0.15*math.sin(self._phase*3.1+i*0.7)
                sp1=0.3*math.exp(-0.5*((i-5)**2))
                sp2=0.2*math.exp(-0.5*((i-13)**2))
                noise=random.gauss(0,0.07)
                self._targets[i]=max(0.0,min(1.0,base+w1+w2+sp1+sp2+noise))
        for i in range(self._bars):
            d=self._targets[i]-self._heights[i]
            self._heights[i]+=d*0.35 if d>0 else d*0.12
            self._heights[i]=max(0.0,min(1.0,self._heights[i]))
            if self._heights[i]>=self._peaks[i]:
                self._peaks[i]=self._heights[i]; self._peak_hold[i]=20
            else:
                if self._peak_hold[i]>0: self._peak_hold[i]-=1
                else: self._peaks[i]=max(0,self._peaks[i]-0.015)
        self.update()

    def paintEvent(self, event):
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w,h=self.width(),self.height()
        p.fillRect(0,0,w,h,QColor("#0a0a0a"))
        n=self._bars; gap=2; bar_w=max(3,(w-gap*(n+1))//n); total=bar_w+gap
        for i in range(n):
            x=gap+i*total; bh=int(self._heights[i]*(h-6))
            if bh<1: p.fillRect(x,h-2,bar_w,2,QColor("#1a1a1a")); continue
            y=h-bh-2; ratio=self._heights[i]
            if ratio<0.5: r=int(ratio*2*200);g=210;b=30
            elif ratio<0.8: r=255;g=int((1-(ratio-0.5)/0.3)*160);b=10
            else: r=255;g=int((1-(ratio-0.8)/0.2)*60);b=0
            grad=QLinearGradient(x,y+bh,x,y)
            grad.setColorAt(0,QColor(r,g,b,180)); grad.setColorAt(1,QColor(min(255,r+50),min(255,g+50),min(255,b+30),255))
            p.fillRect(x,y,bar_w,bh,grad)
            py=int((1-self._peaks[i])*(h-6))
            p.fillRect(x,py,bar_w,2,QColor(255,200,100,200))
        p.end()


# ══════════════════════════════════════════
#  MODELOS DE DATOS
# ══════════════════════════════════════════
class PlaylistItem:
    TYPE_MUSIC="Música"; TYPE_JINGLE="Cuña"; TYPE_SPOT="Spot"
    TYPE_STOP="Stop"; TYPE_STREAM="Radio Internet"; TYPE_PAUSE="Pausa"

    def __init__(self, path, title="", artist="", duration=0, item_type=None, stream_url=""):
        self.path=path; self.title=title or os.path.splitext(os.path.basename(path))[0]
        self.artist=artist; self.duration=duration
        self.item_type=item_type or self.TYPE_MUSIC; self.stream_url=stream_url

    def duration_str(self):
        if self.duration<=0: return "--:--"
        m,s=divmod(int(self.duration),60); return f"{m:02d}:{s:02d}"

    def to_dict(self):
        return {"path":self.path,"title":self.title,"artist":self.artist,
                "duration":self.duration,"type":self.item_type,"stream_url":self.stream_url}

    @classmethod
    def from_dict(cls,d):
        return cls(d["path"],d.get("title",""),d.get("artist",""),
                   d.get("duration",0),d.get("type",cls.TYPE_MUSIC),d.get("stream_url",""))


class SchedulerEvent:
    TYPES=["Cuña","Spot","Playlist","Silencio","Archivo","Locución hora"]
    def __init__(self,time_str,action,file_path="",repeat=False,days=None,event_type="Archivo",interrupt=True):
        self.time_str=time_str; self.action=action; self.file_path=file_path
        self.repeat=repeat; self.days=days if days is not None else [True]*7
        self.event_type=event_type; self.interrupt=interrupt; self.executed_today=False

    def runs_today(self): return self.days[datetime.now().weekday()]

    def to_dict(self):
        return {"time":self.time_str,"action":self.action,"file":self.file_path,
                "repeat":self.repeat,"days":self.days,"type":self.event_type,"interrupt":self.interrupt}

    @classmethod
    def from_dict(cls,d):
        return cls(d["time"],d["action"],d.get("file",""),d.get("repeat",False),
                   d.get("days",[True]*7),d.get("type","Archivo"),d.get("interrupt",True))


# ══════════════════════════════════════════
#  MOTOR AUDIO
# ══════════════════════════════════════════
class AudioEngine(QThread):
    songFinished=pyqtSignal(); positionUpdate=pyqtSignal(float,float)
    def __init__(self):
        super().__init__()
        self._player=None; self._vlc=None; self._volume=85
        self._monitor_volume=85  # volumen local (auriculares/monitores)
        self._playing=False; self._init_vlc()

    def _init_vlc(self):
        try:
            import vlc
            self._vlc=vlc.Instance("--no-xlib"); self._player=self._vlc.media_player_new()
            em=self._player.event_manager()
            em.event_attach(vlc.EventType.MediaPlayerEndReached,lambda e:self.songFinished.emit())
        except Exception as ex: print(f"VLC: {ex}")

    def play(self,path):
        if not os.path.exists(path) and not path.startswith("http"): return False
        try:
            import vlc
            media=self._vlc.media_new(path); self._player.set_media(media)
            self._player.play(); self._player.audio_set_volume(self._monitor_volume)
            self._playing=True
            threading.Thread(target=self._pos_loop,daemon=True).start()
            return True
        except Exception as ex: print(f"Play: {ex}"); return False

    def pause(self):
        if self._player: self._player.pause(); self._playing=not self._playing

    def stop(self):
        if self._player: self._player.stop()
        self._playing=False

    def set_monitor_volume(self,v):
        """Volumen local (auriculares) — NO afecta el streaming"""
        self._monitor_volume=v
        if self._player:
            try: self._player.audio_set_volume(v)
            except: pass

    def get_position(self):
        if self._player:
            try: return self._player.get_time()/1000.0,self._player.get_length()/1000.0
            except: pass
        return 0,0

    def is_playing(self): return self._playing

    def _pos_loop(self):
        while self._playing:
            pos,dur=self.get_position(); self.positionUpdate.emit(pos,dur); time.sleep(0.5)


# ══════════════════════════════════════════
#  MOTOR STREAMING (FFmpeg)
# ══════════════════════════════════════════
class StreamEngine(QThread):
    statusChanged=pyqtSignal(bool,str); listenersUpdate=pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._process=None; self._connected=False; self._cfg={}
        self._stream_volume=100  # volumen de salida al streaming (independiente del monitor)
        self._mon=QTimer(); self._mon.timeout.connect(self._poll)

    def configure(self,cfg): self._cfg=cfg

    def set_stream_volume(self,v):
        """Volumen del streaming — independiente del volumen de monitores"""
        self._stream_volume=v

    def test_connection(self):
        c=self._cfg
        if not c: return False,"Sin configuración"
        try:
            url=f"http://{c['host']}:{c['port']}/"
            r=requests.get(url,timeout=4); return True,f"Servidor OK ({r.status_code})"
        except requests.ConnectionError: return False,"No se pudo conectar"
        except Exception as ex: return False,str(ex)

    def connect_stream(self):
        c=self._cfg
        if not c: return False
        stype=c.get("type","icecast2")
        if "shoutcast_v1" in stype: url=f"icecast://source:{c['password']}@{c['host']}:{c['port']}/"
        elif "shoutcast_v2" in stype: url=f"icecast://source:{c['password']}@{c['host']}:{c['port']}/{c.get('sid','1')}"
        else: url=f"icecast://source:{c['password']}@{c['host']}:{c['port']}{c.get('mountpoint','/stream')}"
        br=c.get("bitrate",128); fmt=c.get("format","mp3").lower()
        codec="libmp3lame" if fmt=="mp3" else ("libfdk_aac" if fmt=="aac" else "libvorbis")
        ofmt="mp3" if fmt=="mp3" else ("adts" if fmt=="aac" else "ogg")
        vol_filter=f"volume={self._stream_volume/100.0:.2f}"
        if sys.platform=="win32": asrc=["-f","dshow","-i","audio=Mezcla estéreo"]
        elif sys.platform=="darwin": asrc=["-f","avfoundation","-i",":0"]
        else: asrc=["-f","pulse","-i","default"]
        cmd=(["ffmpeg","-re"]+asrc+["-af",vol_filter,"-acodec",codec,"-ab",f"{br}k","-ar","44100","-f",ofmt,url,"-y"])
        try:
            self._process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self._connected=True
            label="Shoutcast" if "shoutcast" in stype else "Icecast2"
            self.statusChanged.emit(True,f"Conectado — {label} {c['host']}:{c['port']}")
            self._mon.start(12000); return True
        except FileNotFoundError: self.statusChanged.emit(False,"FFmpeg no encontrado"); return False
        except Exception as ex: self.statusChanged.emit(False,str(ex)); return False

    def disconnect_stream(self):
        if self._process: self._process.terminate(); self._process=None
        self._connected=False; self._mon.stop(); self.statusChanged.emit(False,"Desconectado")

    def is_connected(self): return self._connected

    def _poll(self):
        c=self._cfg
        if not c: return
        try:
            r=requests.get(f"http://{c['host']}:{c['port']}/status-json.xsl",timeout=3)
            sources=r.json().get("icestats",{}).get("source",[])
            if isinstance(sources,dict): sources=[sources]
            for s in sources:
                if c.get("mountpoint","") in str(s.get("listenurl","")):
                    self.listenersUpdate.emit(int(s.get("listeners",0))); return
        except: pass


# ══════════════════════════════════════════
#  DIÁLOGO STREAMING (estilo RadioBOSS)
# ══════════════════════════════════════════
class StreamingDialog(QDialog):
    def __init__(self, parent=None, cfg=None):
        super().__init__(parent); self.setWindowTitle("Configuración de Streaming")
        self.setFixedSize(480,360); self.cfg=cfg or {}
        self.setStyleSheet(parent.styleSheet() if parent else "")
        lay=QVBoxLayout(self)
        tabs=QTabWidget()

        # ── Pestaña Conexión
        conn=QWidget(); cl=QGridLayout(conn); cl.setSpacing(8); cl.setContentsMargins(12,12,12,12)
        cl.addWidget(QLabel("Servidor:"),0,0)
        self.edit_server=QLineEdit(cfg.get("host","localhost")); cl.addWidget(self.edit_server,0,1,1,2)
        cl.addWidget(QLabel("Contraseña:"),1,0)
        self.edit_pass=QLineEdit(cfg.get("password","")); self.edit_pass.setEchoMode(QLineEdit.EchoMode.Password)
        cl.addWidget(self.edit_pass,1,1)
        self.chk_public=QCheckBox("Pública (carpeta)"); cl.addWidget(self.chk_public,1,2)
        cl.addWidget(QLabel("Puerto:"),2,0)
        self.edit_port=QLineEdit(cfg.get("port","8000")); cl.addWidget(self.edit_port,2,1)
        self.edit_name=QLineEdit(cfg.get("name","")); self.edit_name.setPlaceholderText("Nombre para mostrar (opcional)")
        cl.addWidget(QLabel("Nombre:"),3,0); cl.addWidget(self.edit_name,3,1,1,2)
        cl.addWidget(QLabel("Montaje:"),4,0)
        self.edit_mount=QLineEdit(cfg.get("mountpoint","/stream")); cl.addWidget(self.edit_mount,4,1)
        self.spin_reconnect=QSpinBox(); self.spin_reconnect.setRange(0,300); self.spin_reconnect.setSuffix(" s")
        self.spin_reconnect.setValue(cfg.get("reconnect",5))
        cl.addWidget(QLabel("Auto reconectar:"),4,2); cl.addWidget(self.spin_reconnect,4,3) if cl.columnCount()>3 else None

        # Tipo servidor
        cl.addWidget(QLabel("Tipo:"),5,0)
        self.combo_type=QComboBox(); self.combo_type.addItems(["Icecast2","Shoutcast v1","Shoutcast v2"])
        t=cfg.get("type","icecast2")
        if "v1" in t: self.combo_type.setCurrentIndex(1)
        elif "v2" in t: self.combo_type.setCurrentIndex(2)
        cl.addWidget(self.combo_type,5,1)

        # Calidad
        sep=QFrame(); sep.setFrameShape(QFrame.Shape.HLine); cl.addWidget(sep,6,0,1,3)
        cl.addWidget(QLabel("Frecuencia:"),7,0)
        self.combo_freq=QComboBox(); self.combo_freq.addItems(["44100","48000","22050"])
        cl.addWidget(self.combo_freq,7,1)
        cl.addWidget(QLabel("Codificador:"),8,0)
        self.combo_codec=QComboBox(); self.combo_codec.addItems(["MP3","AAC","OGG"])
        cl.addWidget(self.combo_codec,8,1)
        cl.addWidget(QLabel("Bitrate (kbps):"),9,0)
        self.combo_br=QComboBox(); self.combo_br.addItems(["64","96","128","192","320"])
        self.combo_br.setCurrentText(str(cfg.get("bitrate",128))); cl.addWidget(self.combo_br,9,1)
        cl.addWidget(QLabel("Canales:"),10,0)
        self.combo_ch=QComboBox(); self.combo_ch.addItems(["stereo","mono"])
        cl.addWidget(self.combo_ch,10,1)
        tabs.addTab(conn,"Conexión")

        # ── Pestaña Info estación
        info=QWidget(); il=QGridLayout(info); il.setSpacing(8); il.setContentsMargins(12,12,12,12)
        for ri,(lbl,attr,val) in enumerate([("Nombre radio:","edit_rname",cfg.get("radio_name","Mi Radio")),
                                             ("Descripción:", "edit_rdesc",cfg.get("radio_desc","")),
                                             ("Género:",      "edit_rgenre",cfg.get("radio_genre","")),
                                             ("URL:",         "edit_rurl",  cfg.get("radio_url",""))]):
            il.addWidget(QLabel(lbl),ri,0); e=QLineEdit(val); setattr(self,attr,e); il.addWidget(e,ri,1)
        tabs.addTab(info,"Información de la estación")

        # ── Pestaña Metadatos
        meta=QWidget(); ml=QVBoxLayout(meta); ml.setContentsMargins(12,12,12,12)
        self.chk_send_meta=QCheckBox("Enviar metadatos (artista/título) al servidor"); self.chk_send_meta.setChecked(True)
        self.chk_utf8=QCheckBox("Codificación UTF-8"); self.chk_utf8.setChecked(True)
        ml.addWidget(self.chk_send_meta); ml.addWidget(self.chk_utf8); ml.addStretch()
        tabs.addTab(meta,"Metadatos")

        # ── Pestaña Estadística
        stat=QWidget(); sl=QVBoxLayout(stat); sl.setContentsMargins(12,12,12,12)
        self.lbl_stat=QLabel("Conecta el streaming para ver estadísticas."); self.lbl_stat.setStyleSheet("color:#888;")
        sl.addWidget(self.lbl_stat); sl.addStretch()
        tabs.addTab(stat,"Estadística")

        lay.addWidget(tabs)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(self.accept); bb.rejected.connect(self.reject)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        lay.addWidget(bb)

    def get_config(self):
        stype=["icecast2","shoutcast_v1","shoutcast_v2"][self.combo_type.currentIndex()]
        return {"host":self.edit_server.text(),"port":self.edit_port.text(),
                "password":self.edit_pass.text(),"mountpoint":self.edit_mount.text(),
                "type":stype,"bitrate":int(self.combo_br.currentText()),
                "format":self.combo_codec.currentText().lower(),
                "radio_name":self.edit_rname.text(),"radio_desc":self.edit_rdesc.text(),
                "radio_genre":self.edit_rgenre.text(),"radio_url":self.edit_rurl.text(),
                "reconnect":self.spin_reconnect.value(),"name":self.edit_name.text()}


# ══════════════════════════════════════════
#  DIÁLOGO RADIO INTERNET
# ══════════════════════════════════════════
class InternetRadioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Añadir Radio de Internet")
        self.setFixedSize(420,200); self.setStyleSheet(parent.styleSheet() if parent else "")
        lay=QVBoxLayout(self); lay.setSpacing(8); lay.setContentsMargins(14,14,14,14)
        lay.addWidget(QLabel("URL del stream (Icecast/Shoutcast):"))
        self.edit_url=QLineEdit(); self.edit_url.setPlaceholderText("http://radio.servidor.com:8000/stream")
        lay.addWidget(self.edit_url)
        lay.addWidget(QLabel("Nombre de la radio:"))
        self.edit_name=QLineEdit(); self.edit_name.setPlaceholderText("Mi Radio Online")
        lay.addWidget(self.edit_name)
        lay.addWidget(QLabel("Género (opcional):"))
        self.edit_genre=QLineEdit(); lay.addWidget(self.edit_genre)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(self.accept); bb.rejected.connect(self.reject)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Añadir")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        lay.addWidget(bb)

    def get_item(self):
        url=self.edit_url.text().strip(); name=self.edit_name.text().strip() or url
        return PlaylistItem(url,name,"",0,PlaylistItem.TYPE_STREAM,url) if url else None


# ══════════════════════════════════════════
#  VENTANA PRINCIPAL
# ══════════════════════════════════════════
class PoleCasterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION} — {APP_BRAND}")
        self.setMinimumSize(1200,720); self.resize(1400,800)
        self.playlist=[]; self.current_index=-1; self.is_playing=False
        self.jingles=[""]*9; self.jingle_names=["Cuña "+str(i+1) for i in range(9)]
        self.scheduler_events=[]; self._peak_listeners=0
        self._stream_cfg={}; self._theme="dark"
        self._repeat_track=False; self._repeat_list=False
        self._stop_after=False; self._random=False
        self.audio_engine=AudioEngine(); self.stream_engine=StreamEngine()
        self._build_ui(); self._connect_signals(); self._load_config()
        self._clock_timer=QTimer(); self._clock_timer.timeout.connect(self._update_clock); self._clock_timer.start(1000)
        self._sched_timer=QTimer(); self._sched_timer.timeout.connect(self._check_scheduler); self._sched_timer.start(10000)
        self._cd_timer=QTimer(); self._cd_timer.timeout.connect(self._update_countdown); self._cd_timer.start(5000)
        self._update_clock(); self.apply_theme("dark")

    # ══════════════════════════════════════
    #  BUILD UI
    # ══════════════════════════════════════
    def _build_ui(self):
        central=QWidget(); self.setCentralWidget(central)
        root=QVBoxLayout(central); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        self._build_menubar()
        root.addWidget(self._build_header())
        root.addWidget(self._build_top_info())
        root.addWidget(self._build_main_area(), 1)
        self._build_statusbar()

    # ── HEADER ────────────────────────────
    def _build_header(self):
        hdr=QWidget(); hdr.setFixedHeight(44)
        hdr.setObjectName("header")
        hdr.setStyleSheet("#header{background:#080808;border-bottom:1px solid #1a1a1a;}")
        lay=QHBoxLayout(hdr); lay.setContentsMargins(10,4,10,4); lay.setSpacing(10)

        # Logo
        logo_lbl=QLabel()
        logo_path=os.path.join(os.path.dirname(__file__),"assets","logo.png")
        if os.path.exists(logo_path):
            pix=QPixmap(logo_path).scaled(36,36,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
            logo_lbl.setPixmap(pix)
        else:
            logo_lbl.setText("🎙")
            logo_lbl.setStyleSheet("font-size:24px;")
        lay.addWidget(logo_lbl)

        # Marca
        brand_lay=QVBoxLayout(); brand_lay.setSpacing(0)
        lbl_gc=QLabel("GRUP COMUNICADOS"); lbl_gc.setStyleSheet("color:#555;font-size:9px;letter-spacing:2px;")
        lbl_app=QLabel("PoleCaster"); lbl_app.setStyleSheet("color:#ff6600;font-size:18px;font-weight:bold;")
        brand_lay.addWidget(lbl_gc); brand_lay.addWidget(lbl_app)
        lay.addLayout(brand_lay)
        lay.addStretch()

        # Tema claro/oscuro
        self.btn_theme=QPushButton("☀ Tema claro"); self.btn_theme.setFixedHeight(26)
        self.btn_theme.clicked.connect(self._toggle_theme)
        lay.addWidget(self.btn_theme)

        # Versión
        lbl_ver=QLabel(f"v{APP_VERSION}"); lbl_ver.setStyleSheet("color:#333;font-size:10px;")
        lay.addWidget(lbl_ver)
        return hdr

    # ── TOP INFO (3 columnas) ─────────────
    def _build_top_info(self):
        top=QWidget(); top.setFixedHeight(60)
        top.setStyleSheet("background:#080808;border-bottom:1px solid #1a1a1a;")
        lay=QHBoxLayout(top); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)

        # Col 1: En el aire
        col1=QWidget(); c1l=QHBoxLayout(col1); c1l.setContentsMargins(12,6,12,6); c1l.setSpacing(8)
        self.lbl_onair=QLabel("● ON AIR")
        self.lbl_onair.setStyleSheet("color:#fff;background:#cc2200;font-weight:bold;font-size:10px;padding:2px 8px;border-radius:3px;")
        c1l.addWidget(self.lbl_onair)
        inf=QVBoxLayout(); inf.setSpacing(1)
        self.lbl_now_title=QLabel("Esperando..."); self.lbl_now_title.setStyleSheet("color:#fff;font-size:13px;font-weight:bold;")
        self.lbl_now_artist=QLabel(""); self.lbl_now_artist.setStyleSheet("color:#ff6600;font-size:11px;")
        inf.addWidget(self.lbl_now_title); inf.addWidget(self.lbl_now_artist)
        c1l.addLayout(inf); c1l.addStretch()
        lay.addWidget(col1,2)

        lay.addWidget(self._vsep())

        # Col 2: Siguiente
        col2=QWidget(); c2l=QVBoxLayout(col2); c2l.setContentsMargins(12,6,12,6); c2l.setSpacing(1)
        lbl_sig=QLabel("SIGUIENTE"); lbl_sig.setStyleSheet("color:#444;font-size:9px;letter-spacing:1px;")
        self.lbl_next_title=QLabel("—"); self.lbl_next_title.setStyleSheet("color:#ccc;font-size:12px;font-weight:bold;")
        self.lbl_next_dur=QLabel(""); self.lbl_next_dur.setStyleSheet("color:#666;font-size:10px;")
        c2l.addWidget(lbl_sig); c2l.addWidget(self.lbl_next_title); c2l.addWidget(self.lbl_next_dur)
        lay.addWidget(col2,2)

        lay.addWidget(self._vsep())

        # Col 3: Radio name + reloj digital
        col3=QWidget(); c3l=QVBoxLayout(col3); c3l.setContentsMargins(12,4,12,4); c3l.setSpacing(0)
        self.lbl_radio_name=QLabel("Mi Radio Online"); self.lbl_radio_name.setStyleSheet("color:#ff6600;font-size:11px;font-weight:bold;")
        self.lbl_clock=QLabel("--:--:--"); self.lbl_clock.setStyleSheet("color:#fff;font-family:'Courier New';font-size:20px;font-weight:bold;letter-spacing:2px;")
        self.lbl_date=QLabel(""); self.lbl_date.setStyleSheet("color:#555;font-size:10px;")
        c3l.addWidget(self.lbl_radio_name); c3l.addWidget(self.lbl_clock); c3l.addWidget(self.lbl_date)
        lay.addWidget(col3,1)
        return top

    # ── ÁREA PRINCIPAL ────────────────────
    def _build_main_area(self):
        spl=QSplitter(Qt.Orientation.Horizontal)

        # PANEL IZQUIERDO
        left=QWidget(); ll=QVBoxLayout(left); ll.setContentsMargins(0,0,0,0); ll.setSpacing(0)

        # Ecualizador
        eq_container=QWidget(); eq_container.setFixedHeight(80)
        eq_container.setStyleSheet("background:#0a0a0a;border-bottom:1px solid #1a1a1a;")
        eql=QHBoxLayout(eq_container); eql.setContentsMargins(8,4,8,4); eql.setSpacing(8)
        eq_info=QVBoxLayout(); eq_info.setSpacing(2)
        lbl_eq=QLabel("ECUALIZADOR"); lbl_eq.setStyleSheet("color:#333;font-size:9px;letter-spacing:2px;")
        self.lbl_eq_status=QLabel("SILENCIO"); self.lbl_eq_status.setStyleSheet("color:#444;font-size:10px;font-weight:bold;")
        tr=QHBoxLayout(); tr.setSpacing(6)
        lbl_rem=QLabel("Restante"); lbl_rem.setStyleSheet("color:#444;font-size:9px;")
        self.lbl_remaining=QLabel("--:--"); self.lbl_remaining.setStyleSheet("color:#fff;font-family:'Courier New';font-size:14px;font-weight:bold;")
        tr.addWidget(lbl_rem); tr.addWidget(self.lbl_remaining)
        eq_info.addWidget(lbl_eq); eq_info.addWidget(self.lbl_eq_status); eq_info.addLayout(tr)
        eql.addLayout(eq_info)
        self.eq_widget=EqualizerWidget(); eql.addWidget(self.eq_widget,1)
        ll.addWidget(eq_container)

        # Barra de progreso
        self.progress_bar=QProgressBar(); self.progress_bar.setMaximum(1000)
        self.progress_bar.setValue(0); self.progress_bar.setTextVisible(False); self.progress_bar.setFixedHeight(4)
        ll.addWidget(self.progress_bar)

        # Panel tabs izquierdo
        left_tabs=QTabWidget()
        left_tabs.addTab(self._tab_events(),"Eventos")
        left_tabs.addTab(self._tab_upcoming(),"Próximos eventos")
        left_tabs.addTab(self._tab_explorer(),"Explorador")
        ll.addWidget(left_tabs,1)

        # Controles Mic + Silencio
        ll.addWidget(self._build_mic_controls())
        spl.addWidget(left)

        # PANEL DERECHO
        right=QWidget(); rl=QVBoxLayout(right); rl.setContentsMargins(0,0,0,0); rl.setSpacing(0)
        rl.addWidget(self._build_playlist_panel(),1)
        rl.addWidget(self._build_transport())
        spl.addWidget(right)

        spl.setSizes([400,800])
        return spl

    # ── TAB EVENTOS (como ZaraRadio) ──────
    def _tab_events(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(4,4,4,4); lay.setSpacing(4)

        # Botones de control de eventos
        btn_row=QHBoxLayout(); btn_row.setSpacing(3)
        self.btn_repro_event=QPushButton("▶ Reproducción de evento")
        self.btn_repro_event.setCheckable(True)
        self.btn_discard=QPushButton("✕ Descartar evento")
        self.btn_activate=QPushButton("✓ Activar evento")
        self.btn_activate.setCheckable(True); self.btn_activate.setChecked(True)
        self.btn_plan=QPushButton("📅 Planificar evento")
        for b in [self.btn_repro_event,self.btn_discard,self.btn_activate,self.btn_plan]:
            b.setFixedHeight(26); btn_row.addWidget(b)
        lay.addLayout(btn_row)

        # Botón agregar evento
        add_row=QHBoxLayout()
        btn_add_ev=QPushButton("+ Nuevo evento programado"); btn_add_ev.setFixedHeight(26)
        btn_add_ev.clicked.connect(self._add_event)
        add_row.addWidget(btn_add_ev); add_row.addStretch()
        self.lbl_next_event_bar=QLabel("Próximo: —"); self.lbl_next_event_bar.setStyleSheet("color:#ff6600;font-size:11px;")
        add_row.addWidget(self.lbl_next_event_bar)
        lay.addLayout(add_row)
        return w

    # ── TAB PRÓXIMOS EVENTOS (ZaraRadio) ──
    def _tab_upcoming(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        self.events_table=QTableWidget(0,5)
        self.events_table.setHorizontalHeaderLabels(["Hora","Tipo","Fichero","Duración","Días"])
        self.events_table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        self.events_table.setColumnWidth(0,55); self.events_table.setColumnWidth(1,65)
        self.events_table.setColumnWidth(3,60); self.events_table.setColumnWidth(4,100)
        self.events_table.verticalHeader().setVisible(False)
        self.events_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.events_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.events_table.setAlternatingRowColors(True)
        lay.addWidget(self.events_table)

        btn_bar=QWidget(); bl=QHBoxLayout(btn_bar); bl.setContentsMargins(4,4,4,4); bl.setSpacing(4)
        for txt,slot in [("+ Añadir",self._add_event),("✕ Eliminar",self._delete_event),("Limpiar",self._clear_events)]:
            b=QPushButton(txt); b.setFixedHeight(22); b.clicked.connect(slot); bl.addWidget(b)
        bl.addStretch()
        self.lbl_countdown=QLabel(""); self.lbl_countdown.setStyleSheet("color:#ff6600;font-size:10px;"); bl.addWidget(self.lbl_countdown)
        lay.addWidget(btn_bar)
        return w

    # ── TAB EXPLORADOR ────────────────────
    def _tab_explorer(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(4,4,4,4); lay.setSpacing(4)
        hint=QLabel("Doble clic en una carpeta para añadir todos los archivos de audio a la playlist")
        hint.setStyleSheet("color:#555;font-size:10px;"); hint.setWordWrap(True); lay.addWidget(hint)
        self.file_tree=QTreeWidget()
        self.file_tree.setHeaderLabels(["Nombre","Tamaño"])
        self.file_tree.setColumnWidth(0,220); self.file_tree.setAlternatingRowColors(True)
        self.file_tree.itemDoubleClicked.connect(self._on_explorer_double_click)
        self._populate_tree(self.file_tree)
        lay.addWidget(self.file_tree,1)
        btn_row=QHBoxLayout()
        btn_ref=QPushButton("🔄 Actualizar"); btn_ref.setFixedHeight(22)
        btn_ref.clicked.connect(lambda: self._populate_tree(self.file_tree))
        btn_add_sel=QPushButton("+ Añadir selección"); btn_add_sel.setFixedHeight(22)
        btn_add_sel.clicked.connect(self._add_from_explorer)
        btn_row.addWidget(btn_ref); btn_row.addWidget(btn_add_sel); btn_row.addStretch()
        lay.addLayout(btn_row)
        return w

    def _populate_tree(self, tree):
        tree.clear()
        roots=[os.path.expanduser("~"), "C:\\", "/"]
        for root_path in roots:
            if os.path.exists(root_path):
                item=QTreeWidgetItem([os.path.basename(root_path) or root_path,""])
                item.setData(0,Qt.ItemDataRole.UserRole,root_path)
                tree.addTopLevelItem(item)
                self._add_tree_children(item, root_path, depth=0)

    def _add_tree_children(self, parent_item, path, depth=0):
        if depth>2: return
        try:
            audio_exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
            entries=sorted(os.scandir(path), key=lambda e:(not e.is_dir(), e.name.lower()))
            for entry in entries[:50]:
                if entry.name.startswith("."): continue
                if entry.is_dir():
                    ch=QTreeWidgetItem([f"📁 {entry.name}",""])
                    ch.setData(0,Qt.ItemDataRole.UserRole,entry.path)
                    parent_item.addChild(ch)
                    if depth<1: self._add_tree_children(ch,entry.path,depth+1)
                elif os.path.splitext(entry.name)[1].lower() in audio_exts:
                    size=f"{entry.stat().st_size//1024} KB"
                    ch=QTreeWidgetItem([f"🎵 {entry.name}",size])
                    ch.setData(0,Qt.ItemDataRole.UserRole,entry.path)
                    parent_item.addChild(ch)
        except: pass

    def _on_explorer_double_click(self, item, col):
        path=item.data(0,Qt.ItemDataRole.UserRole)
        if not path: return
        if os.path.isdir(path):
            self._add_folder_path(path)
        elif os.path.isfile(path):
            self.playlist.append(PlaylistItem(path))
            self._refresh_playlist()

    def _add_from_explorer(self):
        for item in self.file_tree.selectedItems():
            path=item.data(0,Qt.ItemDataRole.UserRole)
            if path and os.path.isfile(path):
                self.playlist.append(PlaylistItem(path))
        self._refresh_playlist()

    # ── CONTROLES MIC ─────────────────────
    def _build_mic_controls(self):
        mic=QWidget(); mic.setFixedHeight(52); mic.setStyleSheet("background:#080808;border-top:1px solid #1a1a1a;")
        lay=QHBoxLayout(mic); lay.setContentsMargins(8,4,8,4); lay.setSpacing(8)

        # Botón MIC
        self.btn_mic=QPushButton("🎙 MIC"); self.btn_mic.setObjectName("btnMic")
        self.btn_mic.setCheckable(True); self.btn_mic.setFixedSize(60,40)
        lay.addWidget(self.btn_mic)

        sep=QFrame(); sep.setFrameShape(QFrame.Shape.VLine); sep.setObjectName("vSep"); lay.addWidget(sep)

        # Volumen MONITOR (local — auriculares)
        mon_lay=QVBoxLayout(); mon_lay.setSpacing(1)
        lbl_mon=QLabel("Monitor (local)"); lbl_mon.setStyleSheet("color:#555;font-size:9px;")
        mon_row=QHBoxLayout(); mon_row.setSpacing(4)
        self.slider_monitor=QSlider(Qt.Orientation.Horizontal); self.slider_monitor.setRange(0,100)
        self.slider_monitor.setValue(85); self.slider_monitor.setFixedWidth(100)
        self.slider_monitor.valueChanged.connect(self._on_monitor_vol)
        self.lbl_mon_val=QLabel("85%"); self.lbl_mon_val.setStyleSheet("color:#ff6600;font-size:10px;min-width:28px;")
        mon_row.addWidget(self.slider_monitor); mon_row.addWidget(self.lbl_mon_val)
        mon_lay.addWidget(lbl_mon); mon_lay.addLayout(mon_row); lay.addLayout(mon_lay)

        sep2=QFrame(); sep2.setFrameShape(QFrame.Shape.VLine); sep2.setObjectName("vSep"); lay.addWidget(sep2)

        # Volumen STREAMING (salida al servidor — independiente)
        str_lay=QVBoxLayout(); str_lay.setSpacing(1)
        lbl_str=QLabel("Streaming (emisión)"); lbl_str.setStyleSheet("color:#555;font-size:9px;")
        str_row=QHBoxLayout(); str_row.setSpacing(4)
        self.slider_stream_vol=QSlider(Qt.Orientation.Horizontal); self.slider_stream_vol.setRange(0,150)
        self.slider_stream_vol.setValue(100); self.slider_stream_vol.setFixedWidth(100)
        self.slider_stream_vol.valueChanged.connect(self._on_stream_vol)
        self.lbl_str_val=QLabel("100%"); self.lbl_str_val.setStyleSheet("color:#00cc66;font-size:10px;min-width:28px;")
        str_row.addWidget(self.slider_stream_vol); str_row.addWidget(self.lbl_str_val)
        str_lay.addWidget(lbl_str); str_lay.addLayout(str_row); lay.addLayout(str_lay)

        sep3=QFrame(); sep3.setFrameShape(QFrame.Shape.VLine); sep3.setObjectName("vSep"); lay.addWidget(sep3)

        # Botón silencio
        self.btn_silence=QPushButton("🔇 Silencio"); self.btn_silence.setFixedHeight(40)
        self.btn_silence.setCheckable(True); self.btn_silence.clicked.connect(self._toggle_silence)
        lay.addWidget(self.btn_silence)
        lay.addStretch()
        return mic

    def _on_monitor_vol(self,v):
        self.lbl_mon_val.setText(f"{v}%")
        self.audio_engine.set_monitor_volume(v)

    def _on_stream_vol(self,v):
        self.lbl_str_val.setText(f"{v}%")
        self.stream_engine.set_stream_volume(v)

    def _toggle_silence(self, checked):
        if checked:
            self.audio_engine.set_monitor_volume(0)
            self.btn_silence.setText("🔊 Restaurar")
        else:
            v=self.slider_monitor.value()
            self.audio_engine.set_monitor_volume(v)
            self.btn_silence.setText("🔇 Silencio")

    # ── PLAYLIST PANEL ────────────────────
    def _build_playlist_panel(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        # Pestañas de playlist (como RadioBOSS)
        pl_tabs=QTabWidget()
        self.playlist_table=self._make_playlist_table()
        pl_tabs.addTab(self._wrap_playlist(self.playlist_table,"main"),"Playlist 1")
        self.playlist_table2=self._make_playlist_table()
        pl_tabs.addTab(self._wrap_playlist(self.playlist_table2,"sec"),"Playlist 2")
        btn_new=QPushButton("+"); btn_new.setFixedSize(28,28)
        pl_tabs.setCornerWidget(btn_new)
        lay.addWidget(pl_tabs,1)
        return w

    def _make_playlist_table(self):
        t=QTableWidget(0,5)
        t.setHorizontalHeaderLabels(["#","Título","Artista","Tipo","Dur."])
        t.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        t.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        t.setColumnWidth(0,28); t.setColumnWidth(3,72); t.setColumnWidth(4,55)
        t.verticalHeader().setVisible(False)
        t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setAlternatingRowColors(True)
        t.doubleClicked.connect(lambda idx: self._play_index(idx.row()))
        return t

    def _wrap_playlist(self, table, key):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        lay.addWidget(table)
        btn_bar=QWidget(); bl=QHBoxLayout(btn_bar); bl.setContentsMargins(4,3,4,3); bl.setSpacing(3)
        for txt,slot in [("+ Archivos",self._add_files),("+ Carpeta",self._add_folder),
                         ("+ Radio Internet",self._add_internet_radio),
                         ("✕",self._remove_selected),("↑",self._move_up),("↓",self._move_down),("Limpiar",self._clear_playlist)]:
            b=QPushButton(txt); b.setFixedHeight(22); b.clicked.connect(slot); bl.addWidget(b)
        bl.addStretch()
        self.lbl_total=QLabel("0 pistas"); self.lbl_total.setStyleSheet("color:#555;font-size:10px;"); bl.addWidget(self.lbl_total)
        lay.addWidget(btn_bar)
        return w

    # ── TRANSPORT ─────────────────────────
    def _build_transport(self):
        t=QWidget(); t.setFixedHeight(56); t.setStyleSheet("background:#060606;border-top:1px solid #1a1a1a;")
        lay=QHBoxLayout(t); lay.setContentsMargins(8,6,8,6); lay.setSpacing(4)

        def tb(label, tip="", check=False):
            b=QPushButton(label); b.setFixedHeight(36); b.setToolTip(tip)
            if check: b.setCheckable(True)
            return b

        self.btn_play=QPushButton("▶"); self.btn_play.setObjectName("btnPlay"); self.btn_play.setFixedSize(40,40); self.btn_play.clicked.connect(self._toggle_play)
        self.btn_next=tb("⏭","Siguiente"); self.btn_next.setFixedWidth(36); self.btn_next.clicked.connect(self._skip_next)
        self.btn_stop=QPushButton("⏹"); self.btn_stop.setObjectName("btnStop"); self.btn_stop.setFixedSize(40,40); self.btn_stop.clicked.connect(self._stop)
        self.btn_prev=tb("⏮","Anterior"); self.btn_prev.setFixedWidth(36); self.btn_prev.clicked.connect(self._play_prev)

        self.btn_rep_track=tb("🔂","Repetir pista",True); self.btn_rep_track.setFixedWidth(36)
        self.btn_rep_track.clicked.connect(lambda c: setattr(self,'_repeat_track',c))
        self.btn_stop_after=tb("⏹¹","Parar después de la pista actual",True); self.btn_stop_after.setFixedWidth(36)
        self.btn_stop_after.clicked.connect(lambda c: setattr(self,'_stop_after',c))
        self.btn_random=tb("🔀","Reproducción aleatoria",True); self.btn_random.setFixedWidth(36)
        self.btn_random.clicked.connect(lambda c: setattr(self,'_random',c))
        self.btn_rep_list=tb("🔁","Repetir lista",True); self.btn_rep_list.setFixedWidth(36)
        self.btn_rep_list.clicked.connect(lambda c: setattr(self,'_repeat_list',c))

        for b in [self.btn_prev,self.btn_stop,self.btn_play,self.btn_next]: lay.addWidget(b)
        lay.addWidget(self._vsep_small())
        for b in [self.btn_rep_track,self.btn_stop_after,self.btn_random,self.btn_rep_list]: lay.addWidget(b)
        lay.addWidget(self._vsep_small())

        # Posición
        self.lbl_pos=QLabel("00:00 / 00:00"); self.lbl_pos.setStyleSheet("color:#555;font-family:'Courier New';font-size:11px;")
        lay.addWidget(self.lbl_pos)
        lay.addStretch()

        # Stream status pequeño
        self.lbl_stream_dot=QLabel("●"); self.lbl_stream_dot.setStyleSheet("color:#330000;font-size:14px;")
        self.lbl_stream_mini=QLabel("Sin stream"); self.lbl_stream_mini.setStyleSheet("color:#555;font-size:10px;")
        lay.addWidget(self.lbl_stream_dot); lay.addWidget(self.lbl_stream_mini)
        return t

    def _vsep(self):
        f=QFrame(); f.setObjectName("vSep"); f.setFrameShape(QFrame.Shape.VLine); f.setFixedWidth(1); return f

    def _vsep_small(self):
        f=QFrame(); f.setObjectName("vSep"); f.setFrameShape(QFrame.Shape.VLine); f.setFixedWidth(1); f.setFixedHeight(24); return f

    # ── STATUSBAR ─────────────────────────
    def _build_statusbar(self):
        sb=self.statusBar()
        self.lbl_st_play=QLabel("● Detenido"); self.lbl_st_play.setStyleSheet("color:#444;")
        self.lbl_st_stream=QLabel("● Sin conexión"); self.lbl_st_stream.setStyleSheet("color:#444;")
        self.lbl_st_pl=QLabel("Playlist: 0 pistas")
        self.lbl_st_listeners=QLabel("Oyentes: 0")
        sb.addWidget(self.lbl_st_play); sb.addWidget(QLabel(" | "))
        sb.addWidget(self.lbl_st_stream); sb.addWidget(QLabel(" | "))
        sb.addWidget(self.lbl_st_pl); sb.addWidget(QLabel(" | "))
        sb.addWidget(self.lbl_st_listeners)
        sb.addPermanentWidget(QLabel(f"{APP_BRAND} · {APP_NAME} v{APP_VERSION}"))

    # ══════════════════════════════════════
    #  MENUBAR COMPLETO
    # ══════════════════════════════════════
    def _build_menubar(self):
        mb=self.menuBar()

        # ── ARCHIVO ──
        fm=mb.addMenu("Archivo")
        _a=QAction("Nueva playlist",self);_a.triggered.connect(self._new_playlist);_a.setShortcut(QKeySequence("Ctrl+N"));fm.addAction(_a)
        _a=QAction("Abrir playlist",self);_a.triggered.connect(self._open_playlist);_a.setShortcut(QKeySequence("Ctrl+O"));fm.addAction(_a)
        _a=QAction("Guardar playlist",self);_a.triggered.connect(self._save_playlist);_a.setShortcut(QKeySequence("Ctrl+S"));fm.addAction(_a)
        fm.addSeparator(); _a=QAction("Salir",self);_a.triggered.connect(self.close);_a.setShortcut(QKeySequence("Ctrl+Q"));fm.addAction(_a)

        # ── EDICIÓN ──
        em=mb.addMenu("Edición")
        _a=QAction("Seleccionar todo",self);_a.triggered.connect(lambda: self.playlist_table.selectAll());_a.setShortcut(QKeySequence("Ctrl+A"));em.addAction(_a)
        em.addAction("Invertir selección")
        em.addSeparator(); em.addAction("Preferencias")

        # ── VER ──
        vm=mb.addMenu("Ver")
        _a=QAction("Explorador de archivos",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("F1"));vm.addAction(_a)
        _a=QAction("Buscar",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("F2"));vm.addAction(_a)
        _a=QAction("Programador de eventos",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("F3"));vm.addAction(_a)
        _a=QAction("FX",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("F4"));vm.addAction(_a)
        vm.addSeparator()
        areas=vm.addMenu("Áreas de trabajo")
        areas.addAction("Restablecer distribución")
        vm.addSeparator()
        _a=QAction("Información de pista",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("Ctrl+I"));vm.addAction(_a)
        _a=QAction("Panel izquierdo",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("Ctrl+L"));vm.addAction(_a)
        _a=QAction("MIC y VU metros en el centro",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("Ctrl+K"));vm.addAction(_a)
        vm.addAction("Barra de estado")
        _a=QAction("Pantalla completa",self);_a.triggered.connect(self.showFullScreen);_a.setShortcut(QKeySequence("F11"));vm.addAction(_a)
        vm.addSeparator()
        vm.addAction("Colores y fuentes...")
        vm.addAction("Columnas de la lista de reproducción...")
        vm.addSeparator()
        self.act_autoscroll=vm.addAction("Auto-Scroll en Playlist"); self.act_autoscroll.setCheckable(True); self.act_autoscroll.setChecked(True)
        vm.addSeparator()
        # Tema
        theme_menu=vm.addMenu("Tema")
        self.act_dark=theme_menu.addAction("Oscuro"); self.act_dark.setCheckable(True); self.act_dark.setChecked(True)
        self.act_dark.triggered.connect(lambda: self.apply_theme("dark"))
        self.act_light=theme_menu.addAction("Claro"); self.act_light.setCheckable(True)
        self.act_light.triggered.connect(lambda: self.apply_theme("light"))
        vm.addAction("Idioma")

        # ── CUÑAS ──
        cm=mb.addMenu("Cuñas")
        self._cunas_actions=[]
        for i in range(9):
            act=cm.addAction(f"{i+1}. {self.jingle_names[i] if hasattr(self,'jingle_names') else 'Cuña '+str(i+1)}")
            act.triggered.connect(lambda _,idx=i: self._play_jingle(idx))
            self._cunas_actions.append(act)
        cm.addSeparator()
        _a=QAction("Locución de hora",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("H"));cm.addAction(_a)
        cm.addAction("Temperatura")
        cm.addAction("Humedad")
        cm.addSeparator()
        _a=QAction("Editar Cuñas...",self);_a.triggered.connect(self._edit_cunas);cm.addAction(_a)

        # ── LISTA ──
        lm=mb.addMenu("Lista")
        _a=QAction("Añadir pistas...",self);_a.triggered.connect(self._add_files);_a.setShortcut(QKeySequence("Ctrl+A"));lm.addAction(_a)
        lm.addAction("Añadir comando stop")
        _a=QAction("Añadir locución de hora",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("Ctrl+H"));lm.addAction(_a)
        lm.addAction("Añadir locución de temperatura")
        lm.addAction("Añadir locución de humedad")
        lm.addSeparator()
        lm.addAction("Añadir pista aleatoria...")
        lm.addAction("Añadir pausa...")
        lm.addAction("Añadir satélite...")
        lm.addAction("Añadir conexión de satélite")
        lm.addAction("Añadir desconexión del satélite")
        lm.addSeparator()
        _a=QAction("Añadir radio de internet...",self);_a.triggered.connect(self._add_internet_radio);lm.addAction(_a)
        lm.addSeparator()
        _a=QAction("Barajar",self);_a.triggered.connect(self._shuffle);_a.setShortcut(QKeySequence("Ctrl+K"));lm.addAction(_a)
        lm.addSeparator()
        lm.addAction("Ver duración de la selección...")
        lm.addAction("Actualizar duración")
        lm.addAction("Actualizar todas las duraciones")

        # ── MEDIA ──
        mm=mb.addMenu("Media")
        _a=QAction("Reproducir",self);_a.triggered.connect(self._toggle_play);_a.setShortcut(QKeySequence("P"));mm.addAction(_a)
        _a=QAction("Parar",self);_a.triggered.connect(self._stop);_a.setShortcut(QKeySequence("S"));mm.addAction(_a)
        _a=QAction("Siguiente",self);_a.triggered.connect(self._skip_next);_a.setShortcut(QKeySequence("N"));mm.addAction(_a)
        _a=QAction("Pisador",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("T"));mm.addAction(_a)
        _a=QAction("Parar tras la actual",self);_a.triggered.connect(lambda: self.btn_stop_after.setChecked(not self._stop_after));_a.setShortcut(QKeySequence("B"));mm.addAction(_a)
        mm.addSeparator()
        _a=QAction("Renombrar",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("F2"));mm.addAction(_a)

        # ── HERRAMIENTA ──
        hm=mb.addMenu("Herramienta")
        _a=QAction("Mezclador...",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("X"));hm.addAction(_a)
        rep_aux=hm.addMenu("Reproductores auxiliares")
        rep_aux.addAction("Reproductor 1"); rep_aux.addAction("Reproductor 2")
        hm.addAction("Explorador del registro...")
        hm.addAction("Editor de pisadores...")
        hm.addSeparator()
        _a=QAction("Opciones...",self);_a.triggered.connect(lambda: None);_a.setShortcut(QKeySequence("O"));hm.addAction(_a)

        # ── STREAMING ──
        sm=mb.addMenu("Streaming")
        _a=QAction("Configurar streaming...",self);_a.triggered.connect(self._show_stream_dialog);sm.addAction(_a)
        sm.addSeparator()
        _a=QAction("Conectar",self);_a.triggered.connect(self._toggle_stream);sm.addAction(_a)
        _a=QAction("Desconectar",self);_a.triggered.connect(lambda: self.stream_engine.disconnect_stream());sm.addAction(_a)
        sm.addSeparator()
        sm.addAction("Ver estadísticas")

        # ── AYUDA ──
        aym=mb.addMenu("Ayuda")
        aym.addAction("Manual de usuario")
        aym.addAction("Soporte técnico")
        aym.addSeparator()
        _a=QAction(f"Acerca de {APP_NAME}",self)
        _a.triggered.connect(lambda: QMessageBox.about(self,APP_NAME,
            f"<b>{APP_NAME} v{APP_VERSION}</b><br><i>{APP_BRAND}</i><br><br>"
            "Automatizador de Radio Profesional<br>Icecast2 + Shoutcast v1/v2<br><br>"
            "Inspirado en ZaraRadio y RadioBOSS"))
        aym.addAction(_a)

    # ══════════════════════════════════════
    #  TEMA CLARO / OSCURO
    # ══════════════════════════════════════
    def apply_theme(self, theme):
        self._theme=theme
        if theme=="dark":
            QApplication.instance().setStyleSheet(THEME_DARK)
            self.btn_theme.setText("☀ Tema claro")
            if hasattr(self,'act_dark'): self.act_dark.setChecked(True); self.act_light.setChecked(False)
        else:
            QApplication.instance().setStyleSheet(THEME_LIGHT)
            self.btn_theme.setText("🌙 Tema oscuro")
            if hasattr(self,'act_light'): self.act_light.setChecked(True); self.act_dark.setChecked(False)

    def _toggle_theme(self):
        self.apply_theme("light" if self._theme=="dark" else "dark")

    # ══════════════════════════════════════
    #  SIGNALS
    # ══════════════════════════════════════
    def _connect_signals(self):
        self.audio_engine.songFinished.connect(self._on_song_finished)
        self.audio_engine.positionUpdate.connect(self._on_position_update)
        self.stream_engine.statusChanged.connect(self._on_stream_status)
        self.stream_engine.listenersUpdate.connect(self._on_listeners_update)

    # ══════════════════════════════════════
    #  PLAYBACK
    # ══════════════════════════════════════
    def _toggle_play(self):
        if self.is_playing:
            self.audio_engine.pause(); self.is_playing=False; self.btn_play.setText("▶")
            self.eq_widget.set_playing(False); self.lbl_eq_status.setText("PAUSADO")
            self.lbl_st_play.setText("● Pausado")
        else:
            if self.current_index<0 and self.playlist: self._play_index(0); return
            self.audio_engine.pause(); self.is_playing=True; self.btn_play.setText("⏸")
            self.eq_widget.set_playing(True); self._set_playing_status()

    def _stop(self):
        self.audio_engine.stop(); self.is_playing=False; self.btn_play.setText("▶")
        self.progress_bar.setValue(0); self.lbl_pos.setText("00:00 / 00:00")
        self.lbl_remaining.setText("--:--"); self.eq_widget.set_playing(False)
        self.lbl_eq_status.setText("SILENCIO"); self.lbl_st_play.setText("● Detenido")

    def _play_index(self,index):
        if index<0 or index>=len(self.playlist): return
        item=self.playlist[index]
        path=item.stream_url if item.item_type==PlaylistItem.TYPE_STREAM else item.path
        if not path: return
        if item.item_type!=PlaylistItem.TYPE_STREAM and not os.path.exists(path):
            QMessageBox.warning(self,"Archivo no encontrado",path); return
        self.current_index=index; self.audio_engine.play(path)
        self.is_playing=True; self.btn_play.setText("⏸")
        self.lbl_now_title.setText(item.title); self.lbl_now_artist.setText(item.artist or "—")
        self.eq_widget.set_playing(True); self.lbl_eq_status.setText("EN VIVO")
        self._set_playing_status(); self._update_next_info(); self._highlight_row(index)

    def _set_playing_status(self):
        self.lbl_st_play.setText("● Reproduciendo"); self.lbl_st_play.setStyleSheet("color:#00cc66;")

    def _play_prev(self):
        if self.current_index>0: self._play_index(self.current_index-1)

    def _skip_next(self):
        if self._random and self.playlist:
            self._play_index(random.randint(0,len(self.playlist)-1)); return
        ni=self.current_index+1
        if ni<len(self.playlist): self._play_index(ni)
        elif self._repeat_list and self.playlist: self._play_index(0)
        else: self._stop()

    def _on_song_finished(self):
        if self._stop_after: self._stop(); self.btn_stop_after.setChecked(False); self._stop_after=False; return
        if self._repeat_track: self._play_index(self.current_index); return
        self._skip_next()

    def _on_position_update(self,pos,dur):
        if dur>0:
            self.progress_bar.setValue(int(pos/dur*1000))
            self.lbl_pos.setText(f"{int(pos//60):02d}:{int(pos%60):02d} / {int(dur//60):02d}:{int(dur%60):02d}")
            rem=dur-pos; self.lbl_remaining.setText(f"{int(rem//60):02d}:{int(rem%60):02d}")

    # ══════════════════════════════════════
    #  PLAYLIST
    # ══════════════════════════════════════
    def _add_files(self):
        files,_=QFileDialog.getOpenFileNames(self,"Añadir pistas","","Audio (*.mp3 *.wav *.ogg *.flac *.aac *.m4a *.wma)")
        for f in files: self.playlist.append(PlaylistItem(f))
        self._refresh_playlist()

    def _add_folder(self):
        folder=QFileDialog.getExistingDirectory(self,"Seleccionar carpeta")
        if folder: self._add_folder_path(folder)

    def _add_folder_path(self,folder):
        exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
        for fn in sorted(os.listdir(folder)):
            if os.path.splitext(fn)[1].lower() in exts:
                self.playlist.append(PlaylistItem(os.path.join(folder,fn)))
        self._refresh_playlist()

    def _add_internet_radio(self):
        dlg=InternetRadioDialog(self)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            item=dlg.get_item()
            if item: self.playlist.append(item); self._refresh_playlist()

    def _remove_selected(self):
        rows=sorted({i.row() for i in self.playlist_table.selectedIndexes()},reverse=True)
        for r in rows: self.playlist.pop(r)
        self._refresh_playlist()

    def _move_up(self):
        for r in sorted({i.row() for i in self.playlist_table.selectedIndexes()}):
            if r>0: self.playlist[r],self.playlist[r-1]=self.playlist[r-1],self.playlist[r]
        self._refresh_playlist()

    def _move_down(self):
        for r in sorted({i.row() for i in self.playlist_table.selectedIndexes()},reverse=True):
            if r<len(self.playlist)-1: self.playlist[r],self.playlist[r+1]=self.playlist[r+1],self.playlist[r]
        self._refresh_playlist()

    def _clear_playlist(self):
        if QMessageBox.question(self,"Limpiar","¿Limpiar toda la playlist?")==QMessageBox.StandardButton.Yes:
            self.playlist.clear(); self.current_index=-1; self._refresh_playlist()

    def _shuffle(self): random.shuffle(self.playlist); self._refresh_playlist()

    def _update_all_durations(self):
        QMessageBox.information(self,"Actualizar duraciones","Actualizando duraciones de todas las pistas...")

    def _refresh_playlist(self):
        t=self.playlist_table; t.setRowCount(len(self.playlist))
        tc={PlaylistItem.TYPE_MUSIC:"#448888",PlaylistItem.TYPE_JINGLE:"#ff6600",
            PlaylistItem.TYPE_SPOT:"#aa44ff",PlaylistItem.TYPE_STREAM:"#00aaff",
            PlaylistItem.TYPE_STOP:"#cc4444",PlaylistItem.TYPE_PAUSE:"#888888"}
        for i,item in enumerate(self.playlist):
            t.setRowHeight(i,24); t.setItem(i,0,QTableWidgetItem(str(i+1)))
            t.setItem(i,1,QTableWidgetItem(item.title)); t.setItem(i,2,QTableWidgetItem(item.artist))
            ti=QTableWidgetItem(item.item_type); ti.setForeground(QColor(tc.get(item.item_type,"#888"))); t.setItem(i,3,ti)
            t.setItem(i,4,QTableWidgetItem(item.duration_str()))
        td=sum(p.duration for p in self.playlist); h,r=divmod(int(td),3600); m,s=divmod(r,60)
        self.lbl_total.setText(f"{len(self.playlist)} pistas — {h:02d}:{m:02d}:{s:02d}" if h else f"{len(self.playlist)} pistas — {m:02d}:{s:02d}")
        self.lbl_st_pl.setText(f"Playlist: {len(self.playlist)} pistas"); self._update_next_info()

    def _highlight_row(self,index):
        for r in range(self.playlist_table.rowCount()):
            for c in range(self.playlist_table.columnCount()):
                it=self.playlist_table.item(r,c)
                if it:
                    it.setBackground(QColor("#ff660018" if r==index else "transparent"))
                    it.setForeground(QColor("#ff8833" if r==index else "#c0c0c0"))

    def _update_next_info(self):
        ni=self.current_index+1
        if ni<len(self.playlist):
            self.lbl_next_title.setText(self.playlist[ni].title)
            self.lbl_next_dur.setText(f"{self.playlist[ni].artist} — {self.playlist[ni].duration_str()}")
        else:
            self.lbl_next_title.setText("— Fin de playlist —"); self.lbl_next_dur.setText("")

    # ══════════════════════════════════════
    #  CUÑAS / JINGLES
    # ══════════════════════════════════════
    def _play_jingle(self,idx):
        p=self.jingles[idx]
        if p and os.path.exists(p): self.audio_engine.play(p)
        else: QMessageBox.information(self,f"Cuña {idx+1}","Sin archivo asignado. Usa 'Editar Cuñas...' para asignar.")

    def _edit_cunas(self):
        dlg=QDialog(self); dlg.setWindowTitle("Editar Cuñas"); dlg.setFixedSize(500,380)
        dlg.setStyleSheet(QApplication.instance().styleSheet())
        lay=QVBoxLayout(dlg)
        grid=QGridLayout(); grid.setSpacing(6)
        edits=[]
        for i in range(9):
            lbl=QLabel(f"Cuña {i+1}:"); lbl.setStyleSheet("color:#888;font-size:11px;")
            name_edit=QLineEdit(self.jingle_names[i]); name_edit.setFixedWidth(120)
            path_edit=QLineEdit(self.jingles[i]); path_edit.setPlaceholderText("(sin archivo)")
            btn=QPushButton("..."); btn.setFixedWidth(28)
            btn.clicked.connect(lambda _,pe=path_edit: pe.setText(QFileDialog.getOpenFileName(dlg,"","","Audio (*.mp3 *.wav *.ogg)")[0]))
            grid.addWidget(lbl,i,0); grid.addWidget(name_edit,i,1); grid.addWidget(path_edit,i,2); grid.addWidget(btn,i,3)
            edits.append((name_edit,path_edit))
        lay.addLayout(grid)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        lay.addWidget(bb)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            for i,(ne,pe) in enumerate(edits):
                self.jingle_names[i]=ne.text(); self.jingles[i]=pe.text()
            if hasattr(self,'_cunas_actions'):
                for i,act in enumerate(self._cunas_actions):
                    act.setText(f"{i+1}. {self.jingle_names[i]}")

    # ══════════════════════════════════════
    #  SCHEDULER / EVENTOS
    # ══════════════════════════════════════
    def _add_event(self):
        dlg=QDialog(self); dlg.setWindowTitle("Planificar evento"); dlg.setFixedSize(440,420)
        dlg.setStyleSheet(QApplication.instance().styleSheet())
        lay=QVBoxLayout(dlg); lay.setSpacing(8)
        g=QGridLayout(); g.setSpacing(8)
        g.addWidget(QLabel("Hora:"),0,0)
        te=QTimeEdit(); te.setDisplayFormat("HH:mm"); g.addWidget(te,0,1)
        g.addWidget(QLabel("Tipo:"),1,0)
        tc=QComboBox(); tc.addItems(SchedulerEvent.TYPES); g.addWidget(tc,1,1)
        g.addWidget(QLabel("Descripción:"),2,0)
        ae=QLineEdit("Cuña horaria"); g.addWidget(ae,2,1)
        g.addWidget(QLabel("Fichero:"),3,0)
        fr=QHBoxLayout(); fe=QLineEdit()
        fb=QPushButton("..."); fb.setFixedWidth(28)
        fb.clicked.connect(lambda: fe.setText(QFileDialog.getOpenFileName(dlg,"","","Audio (*.mp3 *.wav *.ogg *.flac)")[0]))
        fr.addWidget(fe); fr.addWidget(fb); g.addLayout(fr,3,1)
        lay.addLayout(g)
        lay.addWidget(QLabel("Días activos:"))
        dr=QHBoxLayout()
        dchks=[QCheckBox(d) for d in DAYS_ES]
        for c in dchks: c.setChecked(True); dr.addWidget(c)
        lay.addLayout(dr)
        opt=QHBoxLayout()
        rc=QCheckBox("Repetir semanalmente"); rc.setChecked(True)
        ic=QCheckBox("Interrumpir canción actual"); ic.setChecked(True)
        opt.addWidget(rc); opt.addWidget(ic); lay.addLayout(opt)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        lay.addWidget(bb)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            ev=SchedulerEvent(te.time().toString("HH:mm"),ae.text(),fe.text(),
                rc.isChecked(),[c.isChecked() for c in dchks],tc.currentText(),ic.isChecked())
            self.scheduler_events.append(ev); self._refresh_sched()

    def _delete_event(self):
        rows=sorted({i.row() for i in self.events_table.selectedIndexes()},reverse=True)
        for r in rows:
            if r<len(self.scheduler_events): self.scheduler_events.pop(r)
        self._refresh_sched()

    def _clear_events(self):
        if QMessageBox.question(self,"Limpiar","¿Eliminar todos los eventos?")==QMessageBox.StandardButton.Yes:
            self.scheduler_events.clear(); self._refresh_sched()

    def _refresh_sched(self):
        t=self.events_table; t.setRowCount(len(self.scheduler_events))
        tc={"Cuña":"#ff6600","Spot":"#aa44ff","Playlist":"#00aaff","Silencio":"#888","Archivo":"#00cc66","Locución hora":"#ffcc00"}
        for i,ev in enumerate(self.scheduler_events):
            t.setRowHeight(i,24)
            t.setItem(i,0,QTableWidgetItem(ev.time_str))
            ti=QTableWidgetItem(ev.event_type); ti.setForeground(QColor(tc.get(ev.event_type,"#888"))); t.setItem(i,1,ti)
            fn=os.path.basename(ev.file_path) if ev.file_path else ev.action; t.setItem(i,2,QTableWidgetItem(fn))
            t.setItem(i,3,QTableWidgetItem("--:--"))
            days_str="".join(d for d,v in zip(DAYS_ES,ev.days) if v); t.setItem(i,4,QTableWidgetItem(days_str))
        self._update_countdown()

    def _check_scheduler(self):
        now=datetime.now().strftime("%H:%M")
        for ev in self.scheduler_events:
            if ev.time_str==now and not ev.executed_today and ev.runs_today():
                ev.executed_today=True
                if ev.event_type=="Silencio": self._stop()
                elif ev.file_path and os.path.exists(ev.file_path):
                    if ev.interrupt: self.audio_engine.stop()
                    self.audio_engine.play(ev.file_path)
                    self.lbl_now_title.setText(f"[{ev.event_type}] {ev.action}")
                self._refresh_sched()

    def _update_countdown(self):
        now=datetime.now(); now_str=now.strftime("%H:%M")
        pending=[(ev.time_str,ev) for ev in self.scheduler_events if not ev.executed_today and ev.time_str>now_str and ev.runs_today()]
        pending.sort(key=lambda x:x[0])
        if pending:
            t_str,ev=pending[0]; h,m=map(int,t_str.split(":")); then=now.replace(hour=h,minute=m,second=0)
            mins=int((then-now).total_seconds()//60)
            txt=f"Próximo: [{ev.event_type}] {ev.action} — {t_str} (en {mins} min)"
            self.lbl_countdown.setText(f"En {mins} min")
            self.lbl_next_event_bar.setText(txt)
        else:
            self.lbl_countdown.setText(""); self.lbl_next_event_bar.setText("Sin eventos pendientes")

    # ══════════════════════════════════════
    #  STREAMING
    # ══════════════════════════════════════
    def _show_stream_dialog(self):
        dlg=StreamingDialog(self,self._stream_cfg)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            self._stream_cfg=dlg.get_config()
            self.stream_engine.configure(self._stream_cfg)
            self.lbl_radio_name.setText(self._stream_cfg.get("radio_name","Mi Radio Online"))

    def _toggle_stream(self):
        if self.stream_engine.is_connected():
            self.stream_engine.disconnect_stream()
        else:
            if not self._stream_cfg:
                self._show_stream_dialog()
                if not self._stream_cfg: return
            self.stream_engine.configure(self._stream_cfg)
            self.stream_engine.connect_stream()

    def _on_stream_status(self,connected,msg):
        if connected:
            self.lbl_stream_dot.setStyleSheet("color:#00cc66;font-size:14px;")
            self.lbl_stream_mini.setText(msg); self.lbl_stream_mini.setStyleSheet("color:#00cc66;font-size:10px;")
            self.lbl_st_stream.setText("● Streaming activo"); self.lbl_st_stream.setStyleSheet("color:#00cc66;")
        else:
            self.lbl_stream_dot.setStyleSheet("color:#330000;font-size:14px;")
            self.lbl_stream_mini.setText("Sin stream"); self.lbl_stream_mini.setStyleSheet("color:#555;font-size:10px;")
            self.lbl_st_stream.setText("● Sin conexión"); self.lbl_st_stream.setStyleSheet("color:#444;")

    def _on_listeners_update(self,count):
        if count>self._peak_listeners: self._peak_listeners=count
        self.lbl_st_listeners.setText(f"Oyentes: {count} (pico: {self._peak_listeners})")

    # ══════════════════════════════════════
    #  ARCHIVOS PLAYLIST
    # ══════════════════════════════════════
    def _new_playlist(self): self._clear_playlist()

    def _open_playlist(self):
        p,_=QFileDialog.getOpenFileName(self,"Abrir playlist","","PoleCaster Playlist (*.pcp)")
        if not p: return
        try:
            with open(p,"r",encoding="utf-8") as f: data=json.load(f)
            self.playlist=[PlaylistItem.from_dict(d) for d in data.get("playlist",[])]
            self.scheduler_events=[SchedulerEvent.from_dict(d) for d in data.get("scheduler",[])]
            self._refresh_playlist(); self._refresh_sched()
        except Exception as ex: QMessageBox.critical(self,"Error",str(ex))

    def _save_playlist(self):
        p,_=QFileDialog.getSaveFileName(self,"Guardar playlist","","PoleCaster Playlist (*.pcp)")
        if not p: return
        try:
            with open(p,"w",encoding="utf-8") as f:
                json.dump({"playlist":[i.to_dict() for i in self.playlist],
                           "scheduler":[e.to_dict() for e in self.scheduler_events]},f,indent=2)
        except Exception as ex: QMessageBox.critical(self,"Error",str(ex))

    # ══════════════════════════════════════
    #  CLOCK
    # ══════════════════════════════════════
    def _update_clock(self):
        now=datetime.now()
        self.lbl_clock.setText(now.strftime("%H:%M:%S"))
        self.lbl_date.setText(now.strftime("%A %d de %B de %Y"))
        if now.hour==0 and now.minute==0 and now.second<2:
            for ev in self.scheduler_events: ev.executed_today=False

    # ══════════════════════════════════════
    #  CONFIG
    # ══════════════════════════════════════
    def _load_config(self):
        if not os.path.exists(CONFIG_FILE): return
        try:
            with open(CONFIG_FILE) as f: cfg=json.load(f)
            self._stream_cfg=cfg.get("stream_cfg",{})
            if self._stream_cfg: self.stream_engine.configure(self._stream_cfg)
            self.jingles=cfg.get("jingles",[""]*9)
            self.jingle_names=cfg.get("jingle_names",["Cuña "+str(i+1) for i in range(9)])
            self.lbl_radio_name.setText(self._stream_cfg.get("radio_name","Mi Radio Online"))
            theme=cfg.get("theme","dark"); self.apply_theme(theme)
            for ev_d in cfg.get("scheduler",[]): self.scheduler_events.append(SchedulerEvent.from_dict(ev_d))
            self._refresh_sched()
        except: pass

    def _save_config(self):
        cfg={"stream_cfg":self._stream_cfg,"jingles":self.jingles,"jingle_names":self.jingle_names,
             "theme":self._theme,"scheduler":[e.to_dict() for e in self.scheduler_events]}
        try:
            with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,indent=2)
        except: pass

    def closeEvent(self,event):
        self._save_config(); self.audio_engine.stop()
        if self.stream_engine.is_connected(): self.stream_engine.disconnect_stream()
        event.accept()


# ══════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════
def main():
    app=QApplication(sys.argv)
    app.setApplicationName(APP_NAME); app.setApplicationVersion(APP_VERSION)
    pal=app.palette()
    pal.setColor(QPalette.ColorRole.Window,QColor("#0d0d0d"))
    pal.setColor(QPalette.ColorRole.WindowText,QColor("#e8e8e8"))
    pal.setColor(QPalette.ColorRole.Base,QColor("#0a0a0a"))
    pal.setColor(QPalette.ColorRole.Text,QColor("#e8e8e8"))
    pal.setColor(QPalette.ColorRole.Highlight,QColor("#ff6600"))
    pal.setColor(QPalette.ColorRole.HighlightedText,QColor("#ffffff"))
    app.setPalette(pal)
    win=PoleCasterWindow(); win.show(); sys.exit(app.exec())

if __name__=="__main__":
    main()
