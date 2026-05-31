"""
PoleCaster v3.2 — Radio Automation Suite
Diseño: Grup Comunikados con K
En memoria de Polechita — 10 de Mayo 2026
"""

import sys, os, json, time, threading, subprocess, random, math, socket
import requests
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QTabWidget, QLineEdit, QComboBox,
    QCheckBox, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QGroupBox, QGridLayout, QSpinBox, QFrame, QProgressBar,
    QDialog, QDialogButtonBox, QTimeEdit, QMessageBox, QSizePolicy,
    QScrollArea, QTreeWidget, QTreeWidgetItem, QStatusBar, QMenu,
    QAbstractItemView, QDockWidget, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize, QMimeData, QUrl
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QPainter, QLinearGradient,
    QPen, QAction, QPixmap, QIcon, QKeySequence, QBrush, QPainterPath,
    QDrag
)

APP_NAME    = "PoleCaster"
APP_VERSION = "3.2"
APP_BRAND   = "Grup Comunikados con K"
APP_MEMORY  = "En memoria de Polechita — 10 de Mayo 2026"
CONFIG_FILE = "polecaster_config.json"
DAYS_ES     = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]

# ══════════════════════════════════════════════════════
#  TEMAS
# ══════════════════════════════════════════════════════
THEME_DARK = """
QMainWindow,QWidget{background:#0d0d0d;color:#e8e8e8;font-family:'Segoe UI';font-size:12px;}
QMenuBar{background:#080808;color:#aaa;border-bottom:1px solid #1a1a1a;padding:2px 6px;}
QMenuBar::item{padding:4px 10px;border-radius:3px;}
QMenuBar::item:selected{background:#ff660033;color:#ff6600;}
QMenu{background:#161616;border:1px solid #2a2a2a;color:#ddd;padding:4px 0;}
QMenu::item{padding:7px 20px 7px 14px;}
QMenu::item:selected{background:#ff660033;color:#ff6600;}
QMenu::separator{height:1px;background:#2a2a2a;margin:3px 8px;}
QStatusBar{background:#050505;color:#555;border-top:1px solid #111;font-size:10px;}
QTabWidget::pane{border:1px solid #222;background:#111;}
QTabBar::tab{background:#0a0a0a;color:#666;padding:7px 16px;border:none;font-size:11px;}
QTabBar::tab:selected{color:#ff6600;border-bottom:2px solid #ff6600;background:#111;}
QTabBar::tab:hover{color:#ccc;background:#141414;}
QTableWidget{background:#111;gridline-color:#1a1a1a;border:none;alternate-background-color:#141414;}
QTableWidget::item{padding:4px 6px;border-bottom:1px solid #1a1a1a;color:#dddddd;}
QTableWidget::item:selected{background:#ff660030;color:#ffffff;}
QHeaderView::section{background:#0a0a0a;color:#666;padding:5px 6px;border:none;font-size:10px;letter-spacing:1px;}
QPushButton{background:#1e1e1e;color:#cccccc;border:1px solid #3a3a3a;padding:5px 12px;border-radius:4px;font-size:11px;}
QPushButton:hover{background:#2a2a2a;color:#ffffff;border-color:#ff6600;}
QPushButton:pressed{background:#111;}
QPushButton:checked{background:#ff660033;border-color:#ff6600;color:#ff8833;}
QLineEdit,QComboBox,QSpinBox,QTimeEdit{background:#0a0a0a;color:#e0e0e0;border:1px solid #2a2a2a;padding:5px 8px;border-radius:3px;min-height:22px;}
QLineEdit:focus,QComboBox:focus{border-color:#ff6600;}
QComboBox::drop-down{border:none;width:20px;}
QComboBox QAbstractItemView{background:#111;color:#e0e0e0;border:1px solid #333;selection-background-color:#ff660033;}
QSlider::groove:horizontal{height:4px;background:#1e1e1e;border-radius:2px;}
QSlider::handle:horizontal{background:#ff6600;width:14px;height:14px;border-radius:7px;margin:-5px 0;}
QSlider::sub-page:horizontal{background:#ff6600;border-radius:2px;}
QProgressBar{background:#1a1a1a;border:none;border-radius:2px;height:4px;}
QProgressBar::chunk{background:#ff6600;border-radius:2px;}
QGroupBox{border:1px solid #222;border-radius:4px;margin-top:8px;padding-top:8px;color:#555;font-size:10px;}
QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#ff6600;}
QCheckBox{color:#bbb;}
QCheckBox::indicator{width:14px;height:14px;background:#0a0a0a;border:1px solid #333;border-radius:2px;}
QCheckBox::indicator:checked{background:#ff6600;border-color:#ff6600;}
QTreeWidget{background:#0d0d0d;border:none;color:#cccccc;alternate-background-color:#111;}
QTreeWidget::item{padding:3px 0;}
QTreeWidget::item:selected{background:#ff660030;color:#ff8833;}
QTreeWidget::item:hover{background:#1a1a1a;}
QListWidget{background:#0d0d0d;border:none;color:#cccccc;alternate-background-color:#111;}
QListWidget::item{padding:4px 6px;}
QListWidget::item:selected{background:#ff660030;color:#ff8833;}
QListWidget::item:hover{background:#1a1a1a;}
QScrollBar:vertical{background:#0a0a0a;width:6px;}
QScrollBar::handle:vertical{background:#2a2a2a;border-radius:3px;min-height:20px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}
QScrollBar:horizontal{background:#0a0a0a;height:6px;}
QScrollBar::handle:horizontal{background:#2a2a2a;border-radius:3px;}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{width:0;}
QScrollArea{border:none;background:transparent;}
QSplitter::handle{background:#1a1a1a;width:2px;}
QDockWidget{color:#e8e8e8;font-size:11px;}
QDockWidget::title{background:#111;padding:4px 8px;border-bottom:1px solid #222;}
"""

THEME_LIGHT = """
QMainWindow,QWidget{background:#f5f5f5;color:#1a1a1a;font-family:'Segoe UI';font-size:12px;}
QMenuBar{background:#ffffff;color:#333;border-bottom:1px solid #ddd;padding:2px 6px;}
QMenuBar::item{padding:4px 10px;border-radius:3px;}
QMenuBar::item:selected{background:#ff660020;color:#cc4400;}
QMenu{background:#ffffff;border:1px solid #ccc;color:#222;padding:4px 0;}
QMenu::item{padding:7px 20px 7px 14px;}
QMenu::item:selected{background:#ff660015;color:#cc4400;}
QMenu::separator{height:1px;background:#eee;margin:3px 8px;}
QStatusBar{background:#ffffff;color:#888;border-top:1px solid #ddd;font-size:10px;}
QTabWidget::pane{border:1px solid #ddd;background:#ffffff;}
QTabBar::tab{background:#f0f0f0;color:#888;padding:7px 16px;border:none;font-size:11px;}
QTabBar::tab:selected{color:#cc4400;border-bottom:2px solid #ff6600;background:#ffffff;}
QTabBar::tab:hover{color:#333;background:#e8e8e8;}
QTableWidget{background:#ffffff;gridline-color:#eee;border:none;alternate-background-color:#fafafa;}
QTableWidget::item{padding:4px 6px;border-bottom:1px solid #eeeeee;color:#222222;}
QTableWidget::item:selected{background:#ff660020;color:#cc4400;}
QHeaderView::section{background:#f0f0f0;color:#888;padding:5px 6px;border:none;font-size:10px;}
QPushButton{background:#ffffff;color:#333333;border:1px solid #cccccc;padding:5px 12px;border-radius:4px;font-size:11px;}
QPushButton:hover{background:#f5f5f5;color:#000;border-color:#ff6600;}
QPushButton:pressed{background:#e8e8e8;}
QPushButton:checked{background:#ff660015;border-color:#ff6600;color:#cc4400;}
QLineEdit,QComboBox,QSpinBox,QTimeEdit{background:#ffffff;color:#222;border:1px solid #ccc;padding:5px 8px;border-radius:3px;min-height:22px;}
QLineEdit:focus,QComboBox:focus{border-color:#ff6600;}
QComboBox::drop-down{border:none;width:20px;}
QComboBox QAbstractItemView{background:#fff;color:#222;border:1px solid #ccc;selection-background-color:#ff660015;}
QSlider::groove:horizontal{height:4px;background:#ddd;border-radius:2px;}
QSlider::handle:horizontal{background:#ff6600;width:14px;height:14px;border-radius:7px;margin:-5px 0;}
QSlider::sub-page:horizontal{background:#ff6600;border-radius:2px;}
QProgressBar{background:#e0e0e0;border:none;border-radius:2px;height:4px;}
QProgressBar::chunk{background:#ff6600;border-radius:2px;}
QGroupBox{border:1px solid #ddd;border-radius:4px;margin-top:8px;padding-top:8px;color:#888;font-size:10px;}
QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#ff6600;}
QCheckBox{color:#333;}
QCheckBox::indicator{width:14px;height:14px;background:#fff;border:1px solid #ccc;border-radius:2px;}
QCheckBox::indicator:checked{background:#ff6600;border-color:#ff6600;}
QTreeWidget{background:#ffffff;border:none;color:#222222;alternate-background-color:#fafafa;}
QTreeWidget::item{padding:3px 0;}
QTreeWidget::item:selected{background:#ff660015;color:#cc4400;}
QTreeWidget::item:hover{background:#f5f5f5;}
QListWidget{background:#ffffff;border:none;color:#222222;}
QListWidget::item{padding:4px 6px;}
QListWidget::item:selected{background:#ff660015;color:#cc4400;}
QScrollBar:vertical{background:#f5f5f5;width:6px;}
QScrollBar::handle:vertical{background:#ccc;border-radius:3px;min-height:20px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}
QScrollBar:horizontal{background:#f5f5f5;height:6px;}
QScrollBar::handle:horizontal{background:#ccc;border-radius:3px;}
QScrollArea{border:none;background:transparent;}
QSplitter::handle{background:#ddd;width:2px;}
QDockWidget{color:#1a1a1a;font-size:11px;}
QDockWidget::title{background:#f0f0f0;padding:4px 8px;border-bottom:1px solid #ddd;}
"""

# ══════════════════════════════════════════════════════
#  LOGO CIRCULAR
# ══════════════════════════════════════════════════════
class CircularLogo(QWidget):
    def __init__(self,logo_path,size=40,parent=None):
        super().__init__(parent); self.setFixedSize(size,size)
        self._pix=None; self._size=size
        if logo_path and os.path.exists(logo_path):
            self._pix=QPixmap(logo_path).scaled(size,size,Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)

    def paintEvent(self,event):
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        s=self._size; path=QPainterPath(); path.addEllipse(1,1,s-2,s-2)
        p.setClipPath(path)
        if self._pix: p.drawPixmap(0,0,self._pix)
        else:
            p.fillRect(0,0,s,s,QColor("#ff6600"))
            p.setPen(QColor("#fff")); p.setFont(QFont("Segoe UI",14,QFont.Weight.Bold))
            p.drawText(0,0,s,s,Qt.AlignmentFlag.AlignCenter,"P")
        p.setClipping(False); p.setPen(QPen(QColor("#ff6600"),2))
        p.drawEllipse(1,1,s-2,s-2); p.end()


# ══════════════════════════════════════════════════════
#  ECUALIZADOR
# ══════════════════════════════════════════════════════
class EqualizerWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent); self.setMinimumHeight(60)
        self._bars=28; self._h=[0.0]*28; self._t=[0.0]*28
        self._pk=[0.0]*28; self._pkh=[0]*28
        self._playing=False; self._mic_active=False; self._phase=0.0
        t=QTimer(self); t.timeout.connect(self._animate); t.start(40)

    def set_playing(self,v): self._playing=v
    def set_mic(self,v): self._mic_active=v

    def _animate(self):
        self._phase+=0.08
        active=self._playing or self._mic_active
        if active:
            for i in range(self._bars):
                if self._mic_active:
                    base=0.3+0.5*math.sin(self._phase*2.1+i*0.3)
                    noise=random.gauss(0,0.15)
                    self._t[i]=max(0.0,min(1.0,base+noise))
                else:
                    base=0.15+0.6*math.exp(-0.04*i)
                    w1=0.25*math.sin(self._phase*1.7+i*0.4)
                    w2=0.15*math.sin(self._phase*3.1+i*0.7)
                    sp1=0.3*math.exp(-0.5*((i-5)**2))
                    sp2=0.2*math.exp(-0.5*((i-13)**2))
                    self._t[i]=max(0.0,min(1.0,base+w1+w2+sp1+sp2+random.gauss(0,0.07)))
        else:
            self._t=[0.0]*self._bars
        for i in range(self._bars):
            d=self._t[i]-self._h[i]
            self._h[i]+=d*0.35 if d>0 else d*0.12
            self._h[i]=max(0.0,min(1.0,self._h[i]))
            if self._h[i]>=self._pk[i]: self._pk[i]=self._h[i]; self._pkh[i]=20
            else:
                if self._pkh[i]>0: self._pkh[i]-=1
                else: self._pk[i]=max(0,self._pk[i]-0.015)
        self.update()

    def paintEvent(self,event):
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w,h=self.width(),self.height()
        p.fillRect(0,0,w,h,QColor("#0a0a0a"))
        n=self._bars; gap=2; bw=max(3,(w-gap*(n+1))//n); total=bw+gap
        for i in range(n):
            x=gap+i*total; bh=int(self._h[i]*(h-6))
            if bh<1: p.fillRect(x,h-2,bw,2,QColor("#1a1a1a")); continue
            y=h-bh-2; ratio=self._h[i]
            if self._mic_active:
                if ratio<0.5: r=0;g=180;b=255
                elif ratio<0.8: r=0;g=100;b=255
                else: r=100;g=0;b=255
            else:
                if ratio<0.5: r=int(ratio*2*200);g=210;b=30
                elif ratio<0.8: r=255;g=int((1-(ratio-0.5)/0.3)*160);b=10
                else: r=255;g=int((1-(ratio-0.8)/0.2)*60);b=0
            grad=QLinearGradient(x,y+bh,x,y)
            grad.setColorAt(0,QColor(r,g,b,180))
            grad.setColorAt(1,QColor(min(255,r+50),min(255,g+50),min(255,b+30),255))
            p.fillRect(x,y,bw,bh,grad)
            py=int((1-self._pk[i])*(h-6))
            p.fillRect(x,py,bw,2,QColor(255,200,100,200))
        p.end()


# ══════════════════════════════════════════════════════
#  PLAYLIST CON DRAG & DROP
# ══════════════════════════════════════════════════════
class DragDropPlaylistTable(QTableWidget):
    filesDropped = pyqtSignal(list)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)

    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()
        else: super().dragEnterEvent(event)

    def dragOverEvent(self,event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    def dropEvent(self,event):
        if event.mimeData().hasUrls():
            paths=[]
            for url in event.mimeData().urls():
                path=url.toLocalFile()
                if os.path.isfile(path):
                    paths.append(path)
                elif os.path.isdir(path):
                    exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
                    for fn in sorted(os.listdir(path)):
                        if os.path.splitext(fn)[1].lower() in exts:
                            paths.append(os.path.join(path,fn))
            if paths: self.filesDropped.emit(paths)
            event.acceptProposedAction()
        else: super().dropEvent(event)


# ══════════════════════════════════════════════════════
#  MODELOS
# ══════════════════════════════════════════════════════
class PlaylistItem:
    TYPE_MUSIC="Música"; TYPE_JINGLE="Cuña"; TYPE_SPOT="Spot"
    TYPE_STOP="Stop"; TYPE_STREAM="Radio Internet"; TYPE_PAUSE="Pausa"

    def __init__(self,path,title="",artist="",duration=0,item_type=None,stream_url=""):
        self.path=path
        self.title=title or os.path.splitext(os.path.basename(path))[0]
        self.artist=artist; self.duration=duration
        self.item_type=item_type or self.TYPE_MUSIC; self.stream_url=stream_url
        self._stream_duration=0  # duración en segundos de la conexión a radio internet

    def duration_str(self):
        if self.item_type==self.TYPE_STREAM:
            h,r=divmod(self._stream_duration,3600); m,s=divmod(r,60)
            return f"{h:02d}:{m:02d}:{s:02d}"
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


# ══════════════════════════════════════════════════════
#  MOTOR AUDIO
# ══════════════════════════════════════════════════════
class AudioEngine(QThread):
    songFinished=pyqtSignal(); positionUpdate=pyqtSignal(float,float)

    def __init__(self):
        super().__init__()
        self._player=None; self._vlc=None
        self._monitor_vol=85; self._playing=False
        self._audio_output=""
        self._init_vlc()

    def _init_vlc(self):
        try:
            import vlc
            self._vlc=vlc.Instance("--no-xlib"); self._player=self._vlc.media_player_new()
            em=self._player.event_manager()
            em.event_attach(vlc.EventType.MediaPlayerEndReached,lambda e:self.songFinished.emit())
        except Exception as ex: print(f"VLC: {ex}")

    def get_audio_devices(self):
        """Lista dispositivos de audio disponibles"""
        devices=["Default (sistema)"]
        if sys.platform=="win32":
            try:
                import winreg
                # Intenta obtener dispositivos de Windows
                pass
            except: pass
        return devices

    def set_audio_output(self,device):
        self._audio_output=device

    def play(self,path):
        if not path: return False
        if not path.startswith("http") and not os.path.exists(path): return False
        try:
            import vlc
            media=self._vlc.media_new(path); self._player.set_media(media)
            self._player.play(); self._player.audio_set_volume(self._monitor_vol)
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
        self._monitor_vol=v
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


# ══════════════════════════════════════════════════════
#  MOTOR STREAMING
# ══════════════════════════════════════════════════════
class StreamEngine(QThread):
    statusChanged=pyqtSignal(bool,str); listenersUpdate=pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._process=None; self._connected=False; self._cfg={}
        self._stream_vol=100
        self._mon=QTimer(); self._mon.timeout.connect(self._poll)

    def configure(self,cfg): self._cfg=cfg

    def set_stream_volume(self,v): self._stream_vol=v

    def test_connection(self):
        """Prueba si el servidor es accesible"""
        c=self._cfg
        if not c: return False,"Sin configuración"
        try:
            host=c.get("host",""); port=int(c.get("port",8000))
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(5)
            result=sock.connect_ex((host,port))
            sock.close()
            if result==0: return True,f"Puerto {port} accesible en {host}"
            else: return False,f"No se puede conectar a {host}:{port}"
        except Exception as ex: return False,str(ex)

    def connect_stream(self):
        c=self._cfg
        if not c: return False
        stype=c.get("type","icecast2")

        # Para Shoutcast v1 y v2 se usa protocolo diferente
        if "shoutcast_v1" in stype:
            # Shoutcast v1: PUT /
            url=f"icecast://source:{c['password']}@{c['host']}:{c['port']}/"
        elif "shoutcast_v2" in stype:
            sid=c.get("sid","1")
            url=f"icecast://source:{c['password']}@{c['host']}:{c['port']}/{sid}"
        else:
            # Icecast2
            mount=c.get("mountpoint","/stream")
            if not mount.startswith("/"): mount="/"+mount
            url=f"icecast://source:{c['password']}@{c['host']}:{c['port']}{mount}"

        br=c.get("bitrate",128)
        fmt=c.get("format","mp3").lower()
        if fmt=="mp3": codec="libmp3lame"; ofmt="mp3"
        elif fmt=="aac": codec="aac"; ofmt="adts"
        else: codec="libvorbis"; ofmt="ogg"

        vol_filter=f"volume={self._stream_vol/100.0:.2f}"

        # Fuente de audio del sistema
        audio_device=c.get("audio_device","")
        if sys.platform=="win32":
            if audio_device and audio_device!="Default (sistema)":
                asrc=["-f","dshow","-i",f"audio={audio_device}"]
            else:
                asrc=["-f","dshow","-i","audio=Mezcla estéreo"]
        elif sys.platform=="darwin":
            asrc=["-f","avfoundation","-i",":0"]
        else:
            asrc=["-f","pulse","-i","default"]

        cmd=(["ffmpeg","-re"]+asrc+
             ["-af",vol_filter,"-acodec",codec,"-ab",f"{br}k",
              "-ar","44100","-f",ofmt,url,"-y"])

        print(f"Conectando: {' '.join(cmd)}")
        try:
            self._process=subprocess.Popen(
                cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            # Esperar un momento para ver si falló
            time.sleep(2)
            if self._process.poll() is not None:
                err=self._process.stderr.read().decode("utf-8","ignore")[-300:]
                self.statusChanged.emit(False,f"Error FFmpeg: {err[:100]}")
                return False
            self._connected=True
            label="Shoutcast" if "shoutcast" in stype else "Icecast2"
            self.statusChanged.emit(True,f"Conectado — {label} {c['host']}:{c['port']}")
            self._mon.start(12000); return True
        except FileNotFoundError:
            self.statusChanged.emit(False,"FFmpeg no encontrado — instálalo primero")
            return False
        except Exception as ex:
            self.statusChanged.emit(False,str(ex)); return False

    def disconnect_stream(self):
        if self._process:
            self._process.terminate()
            try: self._process.wait(timeout=3)
            except: self._process.kill()
            self._process=None
        self._connected=False; self._mon.stop()
        self.statusChanged.emit(False,"Desconectado")

    def is_connected(self): return self._connected

    def _poll(self):
        c=self._cfg
        if not c: return
        # Verificar si FFmpeg sigue corriendo
        if self._process and self._process.poll() is not None:
            self._connected=False
            self.statusChanged.emit(False,"Streaming interrumpido — reconectando...")
            if c.get("reconnect",True): self.connect_stream()
            return
        try:
            r=requests.get(f"http://{c['host']}:{c['port']}/status-json.xsl",timeout=3)
            sources=r.json().get("icestats",{}).get("source",[])
            if isinstance(sources,dict): sources=[sources]
            for s in sources:
                if c.get("mountpoint","") in str(s.get("listenurl","")):
                    self.listenersUpdate.emit(int(s.get("listeners",0))); return
        except: pass


# ══════════════════════════════════════════════════════
#  DIÁLOGO STREAMING
# ══════════════════════════════════════════════════════
class StreamingDialog(QDialog):
    def __init__(self,parent=None,cfg=None):
        super().__init__(parent); self.setWindowTitle("Configuración de Streaming")
        self.setFixedSize(520,420); self.cfg=cfg or {}
        lay=QVBoxLayout(self); tabs=QTabWidget()

        # ── Conexión
        conn=QWidget(); cl=QGridLayout(conn); cl.setSpacing(10); cl.setContentsMargins(16,16,16,16)

        cl.addWidget(QLabel("Tipo de servidor:"),0,0)
        self.combo_type=QComboBox(); self.combo_type.addItems(["Icecast2","Shoutcast v1","Shoutcast v2"])
        t=cfg.get("type","icecast2")
        if "v1" in t: self.combo_type.setCurrentIndex(1)
        elif "v2" in t: self.combo_type.setCurrentIndex(2)
        self.combo_type.currentIndexChanged.connect(self._on_type)
        cl.addWidget(self.combo_type,0,1,1,2)

        cl.addWidget(QLabel("Servidor / IP:"),1,0)
        self.edit_server=QLineEdit(cfg.get("host",""))
        self.edit_server.setPlaceholderText("radio.tuservidor.com o IP")
        cl.addWidget(self.edit_server,1,1,1,2)

        cl.addWidget(QLabel("Puerto:"),2,0)
        self.edit_port=QLineEdit(cfg.get("port","8000")); self.edit_port.setFixedWidth(90)
        cl.addWidget(self.edit_port,2,1)

        cl.addWidget(QLabel("Contraseña:"),3,0)
        self.edit_pass=QLineEdit(cfg.get("password",""))
        self.edit_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.chk_show=QCheckBox("Mostrar"); self.chk_show.toggled.connect(
            lambda v: self.edit_pass.setEchoMode(QLineEdit.EchoMode.Normal if v else QLineEdit.EchoMode.Password))
        ph=QHBoxLayout(); ph.addWidget(self.edit_pass); ph.addWidget(self.chk_show)
        cl.addLayout(ph,3,1,1,2)

        self.lbl_mount=QLabel("Punto de montaje:")
        cl.addWidget(self.lbl_mount,4,0)
        self.edit_mount=QLineEdit(cfg.get("mountpoint","/stream"))
        self.edit_mount.setPlaceholderText("/stream")
        cl.addWidget(self.edit_mount,4,1,1,2)

        cl.addWidget(QLabel("Nombre (opcional):"),5,0)
        self.edit_name=QLineEdit(cfg.get("name",""))
        cl.addWidget(self.edit_name,5,1,1,2)

        self.chk_reconnect=QCheckBox("Reconectar automáticamente si se cae")
        self.chk_reconnect.setChecked(cfg.get("reconnect",True))
        cl.addWidget(self.chk_reconnect,6,0,1,3)

        # Botón prueba
        self.btn_test=QPushButton("🔍 Probar conexión")
        self.btn_test.clicked.connect(self._test)
        cl.addWidget(self.btn_test,7,0,1,2)
        self.lbl_test=QLabel(""); cl.addWidget(self.lbl_test,7,2)
        tabs.addTab(conn,"Conexión")

        # ── Calidad
        qual=QWidget(); ql=QGridLayout(qual); ql.setSpacing(10); ql.setContentsMargins(16,16,16,16)
        ql.addWidget(QLabel("Frecuencia:"),0,0)
        self.combo_freq=QComboBox(); self.combo_freq.addItems(["44100","48000","22050"])
        ql.addWidget(self.combo_freq,0,1)
        ql.addWidget(QLabel("Codificador:"),1,0)
        self.combo_codec=QComboBox(); self.combo_codec.addItems(["MP3","OGG"])
        idx=0 if cfg.get("format","mp3")=="mp3" else 1; self.combo_codec.setCurrentIndex(idx)
        ql.addWidget(self.combo_codec,1,1)
        ql.addWidget(QLabel("Bitrate (kbps):"),2,0)
        self.combo_br=QComboBox(); self.combo_br.addItems(["64","96","128","192","320"])
        self.combo_br.setCurrentText(str(cfg.get("bitrate",128))); ql.addWidget(self.combo_br,2,1)
        ql.addWidget(QLabel("Canales:"),3,0)
        self.combo_ch=QComboBox(); self.combo_ch.addItems(["stereo","mono"]); ql.addWidget(self.combo_ch,3,1)

        # Dispositivo de audio
        ql.addWidget(QLabel("Dispositivo de audio:"),4,0)
        self.combo_audio=QComboBox()
        self.combo_audio.addItems(["Default (sistema)","Mezcla estéreo","Micrófono"])
        saved_dev=cfg.get("audio_device","Default (sistema)")
        idx=self.combo_audio.findText(saved_dev)
        if idx>=0: self.combo_audio.setCurrentIndex(idx)
        ql.addWidget(self.combo_audio,4,1)
        ql.setRowStretch(5,1)
        tabs.addTab(qual,"Calidad de audio")

        # ── Info estación
        info=QWidget(); il=QGridLayout(info); il.setSpacing(10); il.setContentsMargins(16,16,16,16)
        for ri,(lbl,attr,key) in enumerate([
            ("Nombre de la radio:","edit_rname","radio_name"),
            ("Descripción:","edit_rdesc","radio_desc"),
            ("Género musical:","edit_rgenre","radio_genre"),
            ("Sitio web:","edit_rurl","radio_url")]):
            il.addWidget(QLabel(lbl),ri,0); e=QLineEdit(cfg.get(key,"")); setattr(self,attr,e); il.addWidget(e,ri,1)
        il.setRowStretch(4,1)
        tabs.addTab(info,"Información de la estación")

        # ── Metadatos
        meta=QWidget(); ml=QVBoxLayout(meta); ml.setContentsMargins(16,16,16,16)
        self.chk_meta=QCheckBox("Enviar metadatos al servidor (artista/título)"); self.chk_meta.setChecked(cfg.get("send_meta",True))
        ml.addWidget(self.chk_meta); ml.addStretch()
        tabs.addTab(meta,"Metadatos")

        lay.addWidget(tabs)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(self.accept); bb.rejected.connect(self.reject)
        lay.addWidget(bb)

    def _on_type(self,idx):
        labels=["Punto de montaje:","Contraseña fuente:","Station ID (SID):"]
        placeholders=["/stream","(contraseña)","1"]
        self.lbl_mount.setText(labels[idx])
        self.edit_mount.setPlaceholderText(placeholders[idx])

    def _test(self):
        cfg=self.get_config()
        try:
            host=cfg["host"]; port=int(cfg["port"])
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(5); result=sock.connect_ex((host,port)); sock.close()
            if result==0:
                self.lbl_test.setText("✅ OK")
                self.lbl_test.setStyleSheet("color:#00cc66;font-weight:bold;")
            else:
                self.lbl_test.setText("❌ Sin respuesta")
                self.lbl_test.setStyleSheet("color:#cc3333;")
        except Exception as ex:
            self.lbl_test.setText(f"❌ {str(ex)[:40]}")
            self.lbl_test.setStyleSheet("color:#cc3333;")

    def get_config(self):
        stype=["icecast2","shoutcast_v1","shoutcast_v2"][self.combo_type.currentIndex()]
        return {
            "host":self.edit_server.text().strip(),
            "port":self.edit_port.text().strip(),
            "password":self.edit_pass.text(),
            "mountpoint":self.edit_mount.text().strip(),
            "type":stype,
            "bitrate":int(self.combo_br.currentText()),
            "format":self.combo_codec.currentText().lower(),
            "radio_name":self.edit_rname.text(),
            "radio_desc":self.edit_rdesc.text(),
            "radio_genre":self.edit_rgenre.text(),
            "radio_url":self.edit_rurl.text(),
            "name":self.edit_name.text(),
            "reconnect":self.chk_reconnect.isChecked(),
            "send_meta":self.chk_meta.isChecked(),
            "audio_device":self.combo_audio.currentText(),
        }


# ══════════════════════════════════════════════════════
#  DIÁLOGO RADIO INTERNET
# ══════════════════════════════════════════════════════
class InternetRadioDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent); self.setWindowTitle("Añadir Radio de Internet")
        self.setFixedSize(440,220)
        lay=QVBoxLayout(self); lay.setSpacing(8); lay.setContentsMargins(16,16,16,16)
        lay.addWidget(QLabel("URL del stream (Icecast/Shoutcast):"))
        self.edit_url=QLineEdit(); self.edit_url.setPlaceholderText("http://radio.servidor.com:8000/stream")
        lay.addWidget(self.edit_url)
        lay.addWidget(QLabel("Nombre de la radio:"))
        self.edit_name=QLineEdit(); self.edit_name.setPlaceholderText("Mi Radio Online")
        lay.addWidget(self.edit_name)
        lay.addWidget(QLabel("Género (opcional):"))
        self.edit_genre=QLineEdit(); lay.addWidget(self.edit_genre)
        # Mostrar duración en tiempo real 00:00:00
        dur_row=QHBoxLayout()
        lbl_dur=QLabel("Duración conexión:"); lbl_dur.setStyleSheet("color:#888;font-size:10px;")
        self.lbl_dur_val=QLabel("00:00:00"); self.lbl_dur_val.setStyleSheet("color:#ff6600;font-family:'Courier New';font-weight:bold;")
        dur_row.addWidget(lbl_dur); dur_row.addWidget(self.lbl_dur_val); dur_row.addStretch()
        lay.addLayout(dur_row)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Añadir")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(self.accept); bb.rejected.connect(self.reject)
        lay.addWidget(bb)

    def get_item(self):
        url=self.edit_url.text().strip(); name=self.edit_name.text().strip() or url
        return PlaylistItem(url,name,self.edit_genre.text(),0,PlaylistItem.TYPE_STREAM,url) if url else None


# ══════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ══════════════════════════════════════════════════════
class PoleCasterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PoleCaster v{APP_VERSION} — {APP_BRAND}")
        self.setMinimumSize(1200,720); self.resize(1440,820)

        self.playlist=[]; self.current_index=-1; self.is_playing=False
        self.jingles=[""]*9; self.jingle_names=["Cuña "+str(i+1) for i in range(9)]
        self.scheduler_events=[]; self._peak_listeners=0
        self._stream_cfg={}; self._theme="dark"
        self._repeat_track=False; self._repeat_list=False
        self._stop_after=False; self._random=False
        self._time_folder=""
        self._stream_timer_secs=0
        self._current_stream_item_idx=-1

        self.audio_engine=AudioEngine(); self.stream_engine=StreamEngine()
        self._logo_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets","logo.png")

        self._build_ui(); self._connect_signals(); self._load_config()

        self._clock_timer=QTimer(); self._clock_timer.timeout.connect(self._update_clock); self._clock_timer.start(1000)
        self._sched_timer=QTimer(); self._sched_timer.timeout.connect(self._check_scheduler); self._sched_timer.start(10000)
        self._stream_dur_timer=QTimer(); self._stream_dur_timer.timeout.connect(self._update_stream_duration); self._stream_dur_timer.start(1000)
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
        root.addWidget(self._build_main_area(),1)
        self._build_statusbar()

    # ── HEADER ────────────────────────────
    def _build_header(self):
        hdr=QWidget(); hdr.setObjectName("hdr")
        hdr.setStyleSheet("#hdr{background:#080808;border-bottom:1px solid #1a1a1a;}")
        hdr.setFixedHeight(52)
        lay=QHBoxLayout(hdr); lay.setContentsMargins(10,6,10,6); lay.setSpacing(10)

        self.logo_widget=CircularLogo(self._logo_path,40)
        lay.addWidget(self.logo_widget)

        bl=QVBoxLayout(); bl.setSpacing(0)
        lbl_gc=QLabel(APP_BRAND); lbl_gc.setStyleSheet("color:#555;font-size:9px;letter-spacing:1px;")
        lbl_app=QLabel("PoleCaster"); lbl_app.setStyleSheet("color:#ff6600;font-size:18px;font-weight:bold;")
        bl.addWidget(lbl_gc); bl.addWidget(lbl_app); lay.addLayout(bl)
        lay.addStretch()

        # Botón HORA
        self.btn_hora=QPushButton("🕐  HORA")
        self.btn_hora.setFixedHeight(32)
        self.btn_hora.setStyleSheet("QPushButton{background:#1a2a1a;color:#00cc66;border:1px solid #00cc6644;border-radius:4px;padding:4px 12px;font-size:11px;font-weight:bold;}QPushButton:hover{background:#00cc6622;border-color:#00cc66;}")
        self.btn_hora.clicked.connect(self._play_hour)
        lay.addWidget(self.btn_hora)

        # Botón STREAM ON/OFF
        self.btn_stream_quick=QPushButton("⬤  STREAM OFF")
        self.btn_stream_quick.setFixedHeight(32); self.btn_stream_quick.setCheckable(True)
        self.btn_stream_quick.setStyleSheet("""
            QPushButton{background:#1a0000;color:#cc4444;border:1px solid #cc444433;border-radius:4px;padding:4px 12px;font-size:11px;font-weight:bold;}
            QPushButton:checked{background:#001a00;color:#00cc66;border-color:#00cc6633;}
            QPushButton:hover{border-color:#888;}
        """)
        self.btn_stream_quick.clicked.connect(self._toggle_stream)
        lay.addWidget(self.btn_stream_quick)

        # Tema
        self.btn_theme=QPushButton("☀  Tema claro")
        self.btn_theme.setFixedHeight(32); self.btn_theme.clicked.connect(self._toggle_theme)
        lay.addWidget(self.btn_theme)

        lbl_ver=QLabel(f"v{APP_VERSION}"); lbl_ver.setStyleSheet("color:#333;font-size:10px;")
        lay.addWidget(lbl_ver)
        return hdr

    # ── TOP INFO ──────────────────────────
    def _build_top_info(self):
        top=QWidget(); top.setObjectName("topinfo")
        top.setStyleSheet("#topinfo{background:#080808;border-bottom:1px solid #1a1a1a;}")
        top.setFixedHeight(64)
        lay=QHBoxLayout(top); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)

        col1=QWidget(); c1l=QHBoxLayout(col1); c1l.setContentsMargins(12,6,12,6); c1l.setSpacing(8)
        self.lbl_onair=QLabel("● ON AIR")
        self.lbl_onair.setStyleSheet("color:#fff;background:#cc2200;font-weight:bold;font-size:10px;padding:3px 10px;border-radius:3px;")
        c1l.addWidget(self.lbl_onair)
        inf=QVBoxLayout(); inf.setSpacing(1)
        self.lbl_now_title=QLabel("Esperando..."); self.lbl_now_title.setStyleSheet("color:#ffffff;font-size:13px;font-weight:bold;")
        self.lbl_now_artist=QLabel(""); self.lbl_now_artist.setStyleSheet("color:#ff6600;font-size:11px;")
        inf.addWidget(self.lbl_now_title); inf.addWidget(self.lbl_now_artist)
        c1l.addLayout(inf); c1l.addStretch()
        lay.addWidget(col1,2)

        sep1=QFrame(); sep1.setFrameShape(QFrame.Shape.VLine); sep1.setStyleSheet("background:#1e1e1e;"); lay.addWidget(sep1)

        col2=QWidget(); c2l=QVBoxLayout(col2); c2l.setContentsMargins(12,6,12,6); c2l.setSpacing(1)
        lbl_sig=QLabel("SIGUIENTE"); lbl_sig.setStyleSheet("color:#444;font-size:9px;letter-spacing:1px;")
        self.lbl_next_title=QLabel("—"); self.lbl_next_title.setStyleSheet("color:#cccccc;font-size:12px;font-weight:bold;")
        self.lbl_next_dur=QLabel(""); self.lbl_next_dur.setStyleSheet("color:#666;font-size:10px;")
        c2l.addWidget(lbl_sig); c2l.addWidget(self.lbl_next_title); c2l.addWidget(self.lbl_next_dur)
        lay.addWidget(col2,2)

        sep2=QFrame(); sep2.setFrameShape(QFrame.Shape.VLine); sep2.setStyleSheet("background:#1e1e1e;"); lay.addWidget(sep2)

        col3=QWidget(); c3l=QHBoxLayout(col3); c3l.setContentsMargins(10,4,10,4); c3l.setSpacing(8)
        self.logo_clock=CircularLogo(self._logo_path,38); c3l.addWidget(self.logo_clock)
        clock_lay=QVBoxLayout(); clock_lay.setSpacing(0)
        self.lbl_radio_name=QLabel("Mi Radio Online"); self.lbl_radio_name.setStyleSheet("color:#ff6600;font-size:10px;font-weight:bold;")
        self.lbl_clock=QLabel("--:--:--"); self.lbl_clock.setStyleSheet("color:#ffffff;font-family:'Courier New';font-size:20px;font-weight:bold;")
        self.lbl_date=QLabel(""); self.lbl_date.setStyleSheet("color:#555;font-size:10px;")
        clock_lay.addWidget(self.lbl_radio_name); clock_lay.addWidget(self.lbl_clock); clock_lay.addWidget(self.lbl_date)
        c3l.addLayout(clock_lay)
        lay.addWidget(col3,1)
        return top

    # ── ÁREA PRINCIPAL ────────────────────
    def _build_main_area(self):
        spl=QSplitter(Qt.Orientation.Horizontal)
        left=QWidget(); ll=QVBoxLayout(left); ll.setContentsMargins(0,0,0,0); ll.setSpacing(0)

        # Ecualizador
        eq_c=QWidget(); eq_c.setFixedHeight(78); eq_c.setObjectName("eqbar")
        eq_c.setStyleSheet("#eqbar{background:#0a0a0a;border-bottom:1px solid #1a1a1a;}")
        eql=QHBoxLayout(eq_c); eql.setContentsMargins(8,4,8,4); eql.setSpacing(8)
        eq_info=QVBoxLayout(); eq_info.setSpacing(2)
        lbl_eq=QLabel("ECUALIZADOR"); lbl_eq.setStyleSheet("color:#333;font-size:9px;letter-spacing:2px;")
        self.lbl_eq_status=QLabel("SILENCIO"); self.lbl_eq_status.setStyleSheet("color:#444;font-size:10px;font-weight:bold;")
        tr=QHBoxLayout(); tr.setSpacing(4)
        lbl_rem=QLabel("Restante"); lbl_rem.setStyleSheet("color:#444;font-size:9px;")
        self.lbl_remaining=QLabel("--:--"); self.lbl_remaining.setStyleSheet("color:#ffffff;font-family:'Courier New';font-size:14px;font-weight:bold;")
        tr.addWidget(lbl_rem); tr.addWidget(self.lbl_remaining)
        eq_info.addWidget(lbl_eq); eq_info.addWidget(self.lbl_eq_status); eq_info.addLayout(tr)
        eql.addLayout(eq_info)
        self.eq_widget=EqualizerWidget(); eql.addWidget(self.eq_widget,1)
        ll.addWidget(eq_c)

        self.progress_bar=QProgressBar(); self.progress_bar.setMaximum(1000)
        self.progress_bar.setValue(0); self.progress_bar.setTextVisible(False); self.progress_bar.setFixedHeight(4)
        ll.addWidget(self.progress_bar)

        left_tabs=QTabWidget()
        left_tabs.addTab(self._tab_events(),"Eventos")
        left_tabs.addTab(self._tab_upcoming(),"Próximos eventos")
        left_tabs.addTab(self._tab_explorer(),"Explorador")
        ll.addWidget(left_tabs,1)
        ll.addWidget(self._build_mic_controls())
        spl.addWidget(left)

        right=QWidget(); rl=QVBoxLayout(right); rl.setContentsMargins(0,0,0,0); rl.setSpacing(0)
        rl.addWidget(self._build_playlist_panel(),1)
        rl.addWidget(self._build_transport())
        spl.addWidget(right)
        spl.setSizes([420,820])
        return spl

    # ── TAB EVENTOS ───────────────────────
    def _tab_events(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(6,6,6,6); lay.setSpacing(6)
        btn_row=QHBoxLayout(); btn_row.setSpacing(4)
        self.btn_repro_event=QPushButton("▶ Evento"); self.btn_repro_event.setCheckable(True)
        self.btn_discard=QPushButton("✕ Descartar")
        self.btn_activate=QPushButton("✓ Activar"); self.btn_activate.setCheckable(True); self.btn_activate.setChecked(True)
        self.btn_plan=QPushButton("📅 Planificar"); self.btn_plan.clicked.connect(self._add_event)
        for b in [self.btn_repro_event,self.btn_discard,self.btn_activate,self.btn_plan]:
            b.setFixedHeight(28); btn_row.addWidget(b)
        lay.addLayout(btn_row)

        add_row=QHBoxLayout()
        btn_add=QPushButton("+ Nuevo evento"); btn_add.setFixedHeight(26); btn_add.clicked.connect(self._add_event)
        add_row.addWidget(btn_add); add_row.addStretch()
        self.lbl_next_event_bar=QLabel("Sin eventos")
        self.lbl_next_event_bar.setStyleSheet("color:#ff6600;font-size:10px;")
        add_row.addWidget(self.lbl_next_event_bar)
        lay.addLayout(add_row)

        # Carpeta hora
        hora_grp=QGroupBox("CARPETA DE LOCUCIONES DE HORA")
        hora_lay=QVBoxLayout(hora_grp)
        hint=QLabel("Archivos: 00.mp3, 01.mp3 ... 23.mp3")
        hint.setStyleSheet("color:#666;font-size:10px;"); hora_lay.addWidget(hint)
        fr=QHBoxLayout()
        self.edit_time_folder=QLineEdit()
        self.edit_time_folder.setPlaceholderText("C:\\PoleCaster\\time\\")
        btn_h=QPushButton("📁 Seleccionar"); btn_h.setFixedWidth(110)
        btn_h.clicked.connect(self._select_time_folder)
        fr.addWidget(self.edit_time_folder); fr.addWidget(btn_h); hora_lay.addLayout(fr)
        lay.addWidget(hora_grp)
        lay.addStretch()
        return w

    # ── TAB PRÓXIMOS EVENTOS ──────────────
    def _tab_upcoming(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        self.events_table=QTableWidget(0,5)
        self.events_table.setHorizontalHeaderLabels(["Hora","Tipo","Fichero","Dur.","Días"])
        self.events_table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        self.events_table.setColumnWidth(0,55); self.events_table.setColumnWidth(1,65)
        self.events_table.setColumnWidth(3,55); self.events_table.setColumnWidth(4,100)
        self.events_table.verticalHeader().setVisible(False)
        self.events_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.events_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.events_table.setAlternatingRowColors(True)
        lay.addWidget(self.events_table)
        btn_bar=QWidget(); bl=QHBoxLayout(btn_bar); bl.setContentsMargins(4,4,4,4); bl.setSpacing(4)
        for txt,slot in [("+ Añadir",self._add_event),("✕ Eliminar",self._delete_event),("Limpiar todo",self._clear_events)]:
            b=QPushButton(txt); b.setFixedHeight(22); b.clicked.connect(slot); bl.addWidget(b)
        bl.addStretch()
        self.lbl_countdown=QLabel(""); self.lbl_countdown.setStyleSheet("color:#ff6600;font-size:10px;"); bl.addWidget(self.lbl_countdown)
        lay.addWidget(btn_bar)
        return w

    # ── TAB EXPLORADOR (con drag) ─────────
    def _tab_explorer(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(4,4,4,4); lay.setSpacing(4)
        hint=QLabel("Arrastra carpetas o archivos a la Playlist · Doble clic para añadir")
        hint.setStyleSheet("color:#666;font-size:10px;"); hint.setWordWrap(True); lay.addWidget(hint)

        self.file_tree=QTreeWidget()
        self.file_tree.setHeaderLabels(["Nombre","Tamaño"])
        self.file_tree.setColumnWidth(0,230); self.file_tree.setAlternatingRowColors(True)
        self.file_tree.itemDoubleClicked.connect(self._on_explorer_dbl)
        self.file_tree.itemExpanded.connect(self._on_item_expanded)
        # Habilitar drag desde el árbol
        self.file_tree.setDragEnabled(True)
        self.file_tree.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self._populate_tree()
        lay.addWidget(self.file_tree,1)

        btn_row=QHBoxLayout()
        for txt,slot in [("🔄 Actualizar",self._populate_tree),("+ Añadir selección",self._add_from_explorer)]:
            b=QPushButton(txt); b.setFixedHeight(24); b.clicked.connect(slot); btn_row.addWidget(b)
        btn_row.addStretch(); lay.addLayout(btn_row)
        return w

    def _get_all_drives(self):
        drives=[]
        if sys.platform=="win32":
            import string
            for letter in string.ascii_uppercase:
                path=f"{letter}:\\";
                if os.path.exists(path): drives.append(path)
        else:
            drives=["/"]
        return drives

    def _populate_tree(self):
        self.file_tree.clear()
        # Todos los discos + home + carpeta PoleCaster
        pole_dir=os.path.dirname(os.path.abspath(__file__))
        home=os.path.expanduser("~")
        roots=[]
        for d in self._get_all_drives():
            name=f"💾 Disco {d}" if sys.platform=="win32" else f"📂 {d}"
            roots.append((d,name))
        roots.append((home,f"🏠 Mi carpeta ({os.path.basename(home)})"))
        if pole_dir!=home: roots.append((pole_dir,f"📻 PoleCaster"))

        for path,name in roots:
            if not os.path.exists(path): continue
            item=QTreeWidgetItem([name,""]); item.setData(0,Qt.ItemDataRole.UserRole,path)
            dummy=QTreeWidgetItem(["⏳ Cargando...",""]); item.addChild(dummy)
            self.file_tree.addTopLevelItem(item)

    def _on_item_expanded(self,item):
        if item.childCount()==1 and item.child(0).text(0).startswith("⏳"):
            item.takeChild(0); path=item.data(0,Qt.ItemDataRole.UserRole)
            self._load_tree_children(item,path)

    def _load_tree_children(self,parent,path,max_items=100):
        audio_exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
        try:
            entries=sorted(os.scandir(path),key=lambda e:(not e.is_dir(),e.name.lower()))
            count=0
            for entry in entries:
                if entry.name.startswith("."): continue
                if count>=max_items: break
                if entry.is_dir():
                    ch=QTreeWidgetItem([f"📁 {entry.name}",""]); ch.setData(0,Qt.ItemDataRole.UserRole,entry.path)
                    dummy=QTreeWidgetItem(["⏳ Cargando...",""]); ch.addChild(dummy)
                    parent.addChild(ch); count+=1
                elif os.path.splitext(entry.name)[1].lower() in audio_exts:
                    size=f"{entry.stat().st_size//1024} KB"
                    ch=QTreeWidgetItem([f"🎵 {entry.name}",size]); ch.setData(0,Qt.ItemDataRole.UserRole,entry.path)
                    parent.addChild(ch); count+=1
        except: pass

    def _on_explorer_dbl(self,item,col):
        path=item.data(0,Qt.ItemDataRole.UserRole)
        if not path: return
        if os.path.isdir(path): self._add_folder_path(path)
        elif os.path.isfile(path): self.playlist.append(PlaylistItem(path)); self._refresh_playlist()

    def _add_from_explorer(self):
        for item in self.file_tree.selectedItems():
            path=item.data(0,Qt.ItemDataRole.UserRole)
            if path:
                if os.path.isdir(path): self._add_folder_path(path)
                elif os.path.isfile(path): self.playlist.append(PlaylistItem(path))
        self._refresh_playlist()

    # ── MIC CONTROLS ─────────────────────
    def _build_mic_controls(self):
        mic=QWidget(); mic.setFixedHeight(56); mic.setObjectName("micbar")
        mic.setStyleSheet("#micbar{background:#080808;border-top:1px solid #1a1a1a;}")
        lay=QHBoxLayout(mic); lay.setContentsMargins(8,6,8,6); lay.setSpacing(8)

        self.btn_mic=QPushButton("🎙 MIC"); self.btn_mic.setCheckable(True); self.btn_mic.setFixedSize(64,40)
        self.btn_mic.setStyleSheet("""
            QPushButton{background:#1a2a1a;color:#00cc66;border:1px solid #00cc6644;border-radius:4px;font-size:11px;font-weight:bold;}
            QPushButton:checked{background:#cc000022;color:#ff4444;border-color:#ff4444;}
            QPushButton:hover{border-color:#00cc66;}
        """)
        self.btn_mic.clicked.connect(self._on_mic_toggle)
        lay.addWidget(self.btn_mic)

        def vsep():
            f=QFrame(); f.setFrameShape(QFrame.Shape.VLine); f.setStyleSheet("background:#1e1e1e;max-width:1px;"); return f

        lay.addWidget(vsep())

        # Configurar micrófono
        mic_cfg=QVBoxLayout(); mic_cfg.setSpacing(1)
        lbl_dev=QLabel("Dispositivo mic:"); lbl_dev.setStyleSheet("color:#555;font-size:9px;")
        self.combo_mic_dev=QComboBox(); self.combo_mic_dev.setFixedHeight(22)
        self.combo_mic_dev.addItems(["Default","Micrófono","Entrada línea","Mezcla estéreo"])
        self.combo_mic_dev.setFixedWidth(140)
        mic_cfg.addWidget(lbl_dev); mic_cfg.addWidget(self.combo_mic_dev); lay.addLayout(mic_cfg)

        lay.addWidget(vsep())

        # Monitor (local)
        mon_lay=QVBoxLayout(); mon_lay.setSpacing(1)
        lbl_mon=QLabel("Monitor (local)"); lbl_mon.setStyleSheet("color:#555;font-size:9px;")
        mon_row=QHBoxLayout(); mon_row.setSpacing(4)
        self.slider_monitor=QSlider(Qt.Orientation.Horizontal)
        self.slider_monitor.setRange(0,100); self.slider_monitor.setValue(85); self.slider_monitor.setFixedWidth(90)
        self.slider_monitor.valueChanged.connect(self._on_monitor_vol)
        self.lbl_mon_val=QLabel("85%"); self.lbl_mon_val.setStyleSheet("color:#ff6600;font-size:10px;min-width:30px;")
        mon_row.addWidget(self.slider_monitor); mon_row.addWidget(self.lbl_mon_val)
        mon_lay.addWidget(lbl_mon); mon_lay.addLayout(mon_row); lay.addLayout(mon_lay)

        lay.addWidget(vsep())

        # Streaming (emisión independiente)
        str_lay=QVBoxLayout(); str_lay.setSpacing(1)
        lbl_str=QLabel("Streaming (emisión)"); lbl_str.setStyleSheet("color:#555;font-size:9px;")
        str_row=QHBoxLayout(); str_row.setSpacing(4)
        self.slider_stream_vol=QSlider(Qt.Orientation.Horizontal)
        self.slider_stream_vol.setRange(0,150); self.slider_stream_vol.setValue(100); self.slider_stream_vol.setFixedWidth(90)
        self.slider_stream_vol.valueChanged.connect(self._on_stream_vol)
        self.lbl_str_val=QLabel("100%"); self.lbl_str_val.setStyleSheet("color:#00cc66;font-size:10px;min-width:30px;")
        str_row.addWidget(self.slider_stream_vol); str_row.addWidget(self.lbl_str_val)
        str_lay.addWidget(lbl_str); str_lay.addLayout(str_row); lay.addLayout(str_lay)

        lay.addWidget(vsep())

        self.btn_silence=QPushButton("🔇 Silencio")
        self.btn_silence.setCheckable(True); self.btn_silence.setFixedHeight(40)
        self.btn_silence.clicked.connect(self._toggle_silence)
        lay.addWidget(self.btn_silence)
        lay.addStretch()
        return mic

    def _on_mic_toggle(self,checked):
        self.eq_widget.set_mic(checked)
        if checked:
            self.lbl_eq_status.setText("🎙 MICRÓFONO")
            self.lbl_eq_status.setStyleSheet("color:#00aaff;font-size:10px;font-weight:bold;")
        else:
            if self.is_playing:
                self.lbl_eq_status.setText("EN VIVO")
                self.lbl_eq_status.setStyleSheet("color:#ff6600;font-size:10px;font-weight:bold;")
            else:
                self.lbl_eq_status.setText("SILENCIO")
                self.lbl_eq_status.setStyleSheet("color:#444;font-size:10px;font-weight:bold;")

    def _on_monitor_vol(self,v):
        self.lbl_mon_val.setText(f"{v}%")
        if not self.btn_silence.isChecked(): self.audio_engine.set_monitor_volume(v)

    def _on_stream_vol(self,v):
        self.lbl_str_val.setText(f"{v}%"); self.stream_engine.set_stream_volume(v)

    def _toggle_silence(self,checked):
        if checked: self.audio_engine.set_monitor_volume(0); self.btn_silence.setText("🔊 Restaurar")
        else: self.audio_engine.set_monitor_volume(self.slider_monitor.value()); self.btn_silence.setText("🔇 Silencio")

    # ── PLAYLIST PANEL ────────────────────
    def _build_playlist_panel(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        pl_tabs=QTabWidget()

        self.playlist_table=self._make_pl_table()
        self.playlist_table.filesDropped.connect(self._on_files_dropped)
        pl_tabs.addTab(self._wrap_pl(self.playlist_table),"Playlist 1")

        self.playlist_table2=self._make_pl_table()
        pl_tabs.addTab(self._wrap_pl(self.playlist_table2),"Playlist 2")

        # Botón + para nueva playlist
        btn_new=QPushButton("+"); btn_new.setFixedSize(28,26)
        btn_new.setToolTip("Nueva playlist"); pl_tabs.setCornerWidget(btn_new)

        lay.addWidget(pl_tabs,1)
        return w

    def _make_pl_table(self):
        t=DragDropPlaylistTable(0,5)
        t.setHorizontalHeaderLabels(["#","Título","Artista","Tipo","Dur."])
        t.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        t.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        t.setColumnWidth(0,28); t.setColumnWidth(3,72); t.setColumnWidth(4,65)
        t.verticalHeader().setVisible(False)
        t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setAlternatingRowColors(True)
        t.doubleClicked.connect(lambda idx: self._play_index(idx.row()))
        return t

    def _wrap_pl(self,table):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        lay.addWidget(table)
        btn_bar=QWidget(); bl=QHBoxLayout(btn_bar); bl.setContentsMargins(4,3,4,3); bl.setSpacing(3)
        btns=[("+ Archivos",self._add_files),("+ Carpeta",self._add_folder),
              ("+ Radio Internet",self._add_internet_radio),
              ("✕",self._remove_selected),("↑",self._move_up),("↓",self._move_down),("Limpiar",self._clear_playlist)]
        for txt,slot in btns:
            b=QPushButton(txt); b.setFixedHeight(24); b.clicked.connect(slot); bl.addWidget(b)
        bl.addStretch()
        self.lbl_total=QLabel("0 pistas"); self.lbl_total.setStyleSheet("color:#555;font-size:10px;"); bl.addWidget(self.lbl_total)
        lay.addWidget(btn_bar)
        return w

    def _on_files_dropped(self,paths):
        audio_exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
        for path in paths:
            if os.path.splitext(path)[1].lower() in audio_exts:
                self.playlist.append(PlaylistItem(path))
        self._refresh_playlist()

    # ── TRANSPORT ─────────────────────────
    def _build_transport(self):
        t=QWidget(); t.setFixedHeight(60); t.setObjectName("transport")
        t.setStyleSheet("#transport{background:#060606;border-top:1px solid #1a1a1a;}")
        lay=QHBoxLayout(t); lay.setContentsMargins(8,6,8,6); lay.setSpacing(5)

        s_round="QPushButton{background:#1e1e1e;color:#ffffff;border:1px solid #3a3a3a;border-radius:20px;font-size:15px;}QPushButton:hover{background:#2a2a2a;border-color:#ff6600;}QPushButton:pressed{background:#111;}"
        s_play ="QPushButton{background:#ff6600;color:#ffffff;border:none;border-radius:22px;font-size:18px;font-weight:bold;}QPushButton:hover{background:#ff8833;}QPushButton:pressed{background:#cc4400;}"
        s_sq   ="QPushButton{background:#1e1e1e;color:#dddddd;border:1px solid #3a3a3a;border-radius:4px;font-size:14px;min-width:32px;min-height:32px;}QPushButton:hover{background:#2a2a2a;border-color:#ff6600;}QPushButton:checked{background:#ff660033;border-color:#ff6600;color:#ff8833;}"

        self.btn_prev=QPushButton("⏮"); self.btn_prev.setFixedSize(38,38); self.btn_prev.setStyleSheet(s_round); self.btn_prev.clicked.connect(self._play_prev)
        self.btn_stop=QPushButton("⏹"); self.btn_stop.setFixedSize(42,42); self.btn_stop.setStyleSheet(s_round); self.btn_stop.clicked.connect(self._stop)
        self.btn_play=QPushButton("▶"); self.btn_play.setFixedSize(46,46); self.btn_play.setStyleSheet(s_play); self.btn_play.clicked.connect(self._toggle_play)
        self.btn_next=QPushButton("⏭"); self.btn_next.setFixedSize(38,38); self.btn_next.setStyleSheet(s_round); self.btn_next.clicked.connect(self._skip_next)

        self.btn_rep_track=QPushButton("🔂"); self.btn_rep_track.setFixedSize(34,34); self.btn_rep_track.setStyleSheet(s_sq); self.btn_rep_track.setCheckable(True); self.btn_rep_track.setToolTip("Repetir pista"); self.btn_rep_track.clicked.connect(lambda c:setattr(self,'_repeat_track',c))
        self.btn_stop_after=QPushButton("⏹¹"); self.btn_stop_after.setFixedSize(34,34); self.btn_stop_after.setStyleSheet(s_sq); self.btn_stop_after.setCheckable(True); self.btn_stop_after.setToolTip("Parar tras pista actual"); self.btn_stop_after.clicked.connect(lambda c:setattr(self,'_stop_after',c))
        self.btn_random=QPushButton("🔀"); self.btn_random.setFixedSize(34,34); self.btn_random.setStyleSheet(s_sq); self.btn_random.setCheckable(True); self.btn_random.setToolTip("Aleatorio"); self.btn_random.clicked.connect(lambda c:setattr(self,'_random',c))
        self.btn_rep_list=QPushButton("🔁"); self.btn_rep_list.setFixedSize(34,34); self.btn_rep_list.setStyleSheet(s_sq); self.btn_rep_list.setCheckable(True); self.btn_rep_list.setToolTip("Repetir lista"); self.btn_rep_list.clicked.connect(lambda c:setattr(self,'_repeat_list',c))

        for b in [self.btn_prev,self.btn_stop,self.btn_play,self.btn_next]: lay.addWidget(b)
        def vsep():
            f=QFrame(); f.setFrameShape(QFrame.Shape.VLine); f.setStyleSheet("background:#222;max-width:1px;min-height:24px;"); return f
        lay.addWidget(vsep())
        for b in [self.btn_rep_track,self.btn_stop_after,self.btn_random,self.btn_rep_list]: lay.addWidget(b)
        lay.addWidget(vsep())
        self.lbl_pos=QLabel("00:00 / 00:00"); self.lbl_pos.setStyleSheet("color:#555;font-family:'Courier New';font-size:11px;"); lay.addWidget(self.lbl_pos)
        lay.addStretch()
        self.lbl_stream_dot=QLabel("⬤"); self.lbl_stream_dot.setStyleSheet("color:#330000;font-size:14px;")
        self.lbl_stream_mini=QLabel("Sin stream"); self.lbl_stream_mini.setStyleSheet("color:#555;font-size:10px;")
        lay.addWidget(self.lbl_stream_dot); lay.addWidget(self.lbl_stream_mini)
        return t

    # ── STATUSBAR ─────────────────────────
    def _build_statusbar(self):
        sb=self.statusBar()
        self.lbl_st_play=QLabel("⬤ Detenido"); self.lbl_st_stream=QLabel("⬤ Sin conexión")
        self.lbl_st_pl=QLabel("Playlist: 0 pistas"); self.lbl_st_listeners=QLabel("Oyentes: 0")
        sb.addWidget(self.lbl_st_play); sb.addWidget(QLabel("  |  "))
        sb.addWidget(self.lbl_st_stream); sb.addWidget(QLabel("  |  "))
        sb.addWidget(self.lbl_st_pl); sb.addWidget(QLabel("  |  "))
        sb.addWidget(self.lbl_st_listeners)
        sb.addPermanentWidget(QLabel(f"{APP_BRAND} · {APP_NAME} v{APP_VERSION}"))

    # ══════════════════════════════════════
    #  MENUBAR
    # ══════════════════════════════════════
    def _build_menubar(self):
        mb=self.menuBar()
        def act(text,slot=None,shortcut=None):
            a=QAction(text,self)
            if slot: a.triggered.connect(slot)
            if shortcut: a.setShortcut(QKeySequence(shortcut))
            return a

        fm=mb.addMenu("Archivo")
        fm.addAction(act("Nueva playlist",self._new_playlist,"Ctrl+N"))
        fm.addAction(act("Abrir playlist",self._open_playlist,"Ctrl+O"))
        fm.addAction(act("Guardar playlist",self._save_playlist,"Ctrl+S"))
        fm.addSeparator(); fm.addAction(act("Salir",self.close,"Ctrl+Q"))

        em=mb.addMenu("Edición")
        em.addAction(act("Seleccionar todo",lambda: self.playlist_table.selectAll()))
        em.addSeparator(); em.addAction("Preferencias")

        # ── VER con Áreas de trabajo como RadioBOSS
        vm=mb.addMenu("Ver")
        vm.addAction(act("Explorador de archivos",lambda: None,"F1"))
        vm.addAction(act("Programador de eventos",lambda: None,"F3"))
        vm.addSeparator()
        areas=vm.addMenu("Áreas de trabajo")
        for i in range(1,5):
            a=QAction(f"Área {i}",self); a.setShortcut(QKeySequence(f"Ctrl+{i}")); areas.addAction(a)
        areas.addSeparator(); areas.addAction("Área adicional")
        vm.addAction(act("Información de pista",lambda: None,"Ctrl+I"))
        vm.addAction(act("Panel izquierdo",lambda: None,"Ctrl+L"))
        vm.addAction(act("MIC y VU metros en el centro",lambda: None,"Ctrl+K"))
        vm.addAction("Barra de estado"); vm.addAction("Barra de herramientas")
        vm.addAction(act("Pantalla completa",self.showFullScreen,"F11"))
        vm.addSeparator()
        vm.addAction("Colores y fuentes..."); vm.addAction("Columnas de la lista de reproducción...")
        vm.addSeparator()
        self.act_autoscroll=QAction("Auto-Scroll en Playlist",self); self.act_autoscroll.setCheckable(True); self.act_autoscroll.setChecked(True); vm.addAction(self.act_autoscroll)
        vm.addAction("Selección sigue a la reproducción")
        vm.addSeparator()
        theme_m=vm.addMenu("Tema")
        self.act_dark=QAction("🌙 Oscuro",self); self.act_dark.setCheckable(True); self.act_dark.setChecked(True)
        self.act_dark.triggered.connect(lambda: self.apply_theme("dark")); theme_m.addAction(self.act_dark)
        self.act_light=QAction("☀ Claro",self); self.act_light.setCheckable(True)
        self.act_light.triggered.connect(lambda: self.apply_theme("light")); theme_m.addAction(self.act_light)
        vm.addAction("Idioma")

        cm=mb.addMenu("Cuñas")
        self._cunas_actions=[]
        for i in range(9):
            name=self.jingle_names[i] if hasattr(self,'jingle_names') else f"Cuña {i+1}"
            a=QAction(f"{i+1}. {name}",self); a.triggered.connect(lambda _,idx=i: self._play_jingle(idx)); cm.addAction(a); self._cunas_actions.append(a)
        cm.addSeparator()
        cm.addAction(act("Locución de hora",self._play_hour,"H"))
        cm.addAction("Temperatura"); cm.addAction("Humedad")
        cm.addSeparator(); cm.addAction(act("Editar Cuñas...",self._edit_cunas))

        # ── LISTA con opción hora
        lm=mb.addMenu("Lista")
        lm.addAction(act("Añadir pistas...",self._add_files,"Ctrl+A"))
        lm.addAction(act("Añadir comando stop"))
        lm.addAction(act("Añadir locución de hora",self._play_hour,"Ctrl+H"))
        lm.addAction("Añadir locución de temperatura")
        lm.addAction("Añadir locución de humedad")
        lm.addSeparator()
        lm.addAction(act("Añadir pista aleatoria..."))
        lm.addAction(act("Añadir pausa..."))
        lm.addSeparator()
        lm.addAction(act("Añadir radio de internet...",self._add_internet_radio))
        lm.addSeparator()
        lm.addAction(act("Barajar",self._shuffle,"Ctrl+K"))
        lm.addSeparator()
        lm.addAction("Ver duración de la selección...")
        lm.addAction("Actualizar duración")
        lm.addAction("Actualizar todas las duraciones")

        mm=mb.addMenu("Media")
        mm.addAction(act("Reproducir",self._toggle_play,"P"))
        mm.addAction(act("Parar",self._stop,"S"))
        mm.addAction(act("Siguiente",self._skip_next,"N"))
        mm.addAction(act("Pisador",lambda: None,"T"))
        mm.addAction(act("Parar tras la actual",lambda: self.btn_stop_after.setChecked(not self._stop_after),"B"))
        mm.addSeparator(); mm.addAction(act("Renombrar",lambda: None,"F2"))

        hm=mb.addMenu("Herramienta")
        hm.addAction("Mezclador..."); hm.addAction("Reproductores auxiliares")
        hm.addAction("Explorador del registro..."); hm.addAction("Editor de pisadores...")
        hm.addSeparator(); hm.addAction("Opciones...")

        sm=mb.addMenu("Streaming")
        sm.addAction(act("Configurar streaming...",self._show_stream_dialog))
        sm.addSeparator()
        sm.addAction(act("Conectar / Desconectar",self._toggle_stream))
        sm.addSeparator(); sm.addAction("Ver estadísticas")

        aym=mb.addMenu("Ayuda")
        aym.addAction("Manual de usuario"); aym.addAction("Soporte técnico")
        aym.addSeparator()
        # Proyecto en memoria de Polechita
        mem_action=QAction(f"Proyecto hecho en memoria de Polechita — 10 de Mayo 2026",self)
        mem_action.triggered.connect(lambda: QMessageBox.information(self,
            f"En memoria de Polechita",
            f"<b>PoleCaster v{APP_VERSION}</b><br>"
            f"<i>{APP_BRAND}</i><br><br>"
            f"<b>Proyecto hecho en memoria de Polechita</b><br>"
            f"<i>10 de Mayo 2026</i><br><br>"
            "Automatizador de Radio Profesional<br>"
            "Soporte: Icecast2 + Shoutcast v1/v2<br><br>"
            "Con amor y dedicación. 🐾"))
        aym.addAction(mem_action)
        aym.addSeparator()
        aym.addAction(act(f"Acerca de {APP_NAME}",lambda: QMessageBox.about(self,APP_NAME,
            f"<b>{APP_NAME} v{APP_VERSION}</b><br>"
            f"<i>{APP_BRAND}</i><br><br>"
            f"{APP_MEMORY}<br><br>"
            "Radio Automation Suite")))

    # ══════════════════════════════════════
    #  TEMA
    # ══════════════════════════════════════
    def apply_theme(self,theme):
        self._theme=theme; app=QApplication.instance()
        if theme=="dark":
            app.setStyleSheet(THEME_DARK)
            pal=app.palette()
            pal.setColor(QPalette.ColorRole.Window,QColor("#0d0d0d"))
            pal.setColor(QPalette.ColorRole.WindowText,QColor("#e8e8e8"))
            pal.setColor(QPalette.ColorRole.Base,QColor("#0a0a0a"))
            pal.setColor(QPalette.ColorRole.AlternateBase,QColor("#111111"))
            pal.setColor(QPalette.ColorRole.Text,QColor("#e0e0e0"))
            pal.setColor(QPalette.ColorRole.Button,QColor("#1e1e1e"))
            pal.setColor(QPalette.ColorRole.ButtonText,QColor("#cccccc"))
            app.setPalette(pal)
            self.btn_theme.setText("☀  Tema claro")
            if hasattr(self,'act_dark'): self.act_dark.setChecked(True); self.act_light.setChecked(False)
            hdr_style="#hdr{background:#080808;border-bottom:1px solid #1a1a1a;}"
            top_style="#topinfo{background:#080808;border-bottom:1px solid #1a1a1a;}"
            mic_style="#micbar{background:#080808;border-top:1px solid #1a1a1a;}"
            tr_style="#transport{background:#060606;border-top:1px solid #1a1a1a;}"
            eq_style="#eqbar{background:#0a0a0a;border-bottom:1px solid #1a1a1a;}"
            clk_c="#ffffff"; title_c="#ffffff"
        else:
            app.setStyleSheet(THEME_LIGHT)
            pal=app.palette()
            pal.setColor(QPalette.ColorRole.Window,QColor("#f5f5f5"))
            pal.setColor(QPalette.ColorRole.WindowText,QColor("#1a1a1a"))
            pal.setColor(QPalette.ColorRole.Base,QColor("#ffffff"))
            pal.setColor(QPalette.ColorRole.AlternateBase,QColor("#fafafa"))
            pal.setColor(QPalette.ColorRole.Text,QColor("#222222"))
            pal.setColor(QPalette.ColorRole.Button,QColor("#ffffff"))
            pal.setColor(QPalette.ColorRole.ButtonText,QColor("#333333"))
            app.setPalette(pal)
            self.btn_theme.setText("🌙  Tema oscuro")
            if hasattr(self,'act_light'): self.act_light.setChecked(True); self.act_dark.setChecked(False)
            hdr_style="#hdr{background:#ffffff;border-bottom:1px solid #ddd;}"
            top_style="#topinfo{background:#f0f0f0;border-bottom:1px solid #ddd;}"
            mic_style="#micbar{background:#f0f0f0;border-top:1px solid #ddd;}"
            tr_style="#transport{background:#ffffff;border-top:1px solid #ddd;}"
            eq_style="#eqbar{background:#f5f5f5;border-bottom:1px solid #ddd;}"
            clk_c="#111111"; title_c="#111111"

        # Aplicar a cada widget nombrado
        for name,style in [("hdr",hdr_style),("topinfo",top_style),("micbar",mic_style),("transport",tr_style),("eqbar",eq_style)]:
            for child in self.findChildren(QWidget,name): child.setStyleSheet(style)

        # Actualizar colores de texto
        if hasattr(self,'lbl_clock'): self.lbl_clock.setStyleSheet(f"color:{clk_c};font-family:'Courier New';font-size:20px;font-weight:bold;")
        if hasattr(self,'lbl_now_title'): self.lbl_now_title.setStyleSheet(f"color:{title_c};font-size:13px;font-weight:bold;")
        if hasattr(self,'lbl_remaining'): self.lbl_remaining.setStyleSheet(f"color:{clk_c};font-family:'Courier New';font-size:14px;font-weight:bold;")

        # Ecualizador fondo
        if hasattr(self,'eq_widget'):
            eq_bg="#0a0a0a" if theme=="dark" else "#e8e8e8"
            # El ecualizador siempre pinta su propio fondo, OK

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
            self.lbl_st_play.setText("⬤ Pausado"); self.lbl_st_play.setStyleSheet("color:#cc8800;")
        else:
            if self.current_index<0 and self.playlist: self._play_index(0); return
            self.audio_engine.pause(); self.is_playing=True; self.btn_play.setText("⏸")
            self.eq_widget.set_playing(True); self._set_playing_status()

    def _stop(self):
        self.audio_engine.stop(); self.is_playing=False; self.btn_play.setText("▶")
        self.progress_bar.setValue(0); self.lbl_pos.setText("00:00 / 00:00")
        self.lbl_remaining.setText("--:--"); self.eq_widget.set_playing(False)
        self.lbl_eq_status.setText("SILENCIO")
        self.lbl_st_play.setText("⬤ Detenido"); self.lbl_st_play.setStyleSheet("color:#555;")

    def _play_index(self,index):
        if index<0 or index>=len(self.playlist): return
        item=self.playlist[index]
        path=item.stream_url if item.item_type==PlaylistItem.TYPE_STREAM else item.path
        if not path: return
        if item.item_type!=PlaylistItem.TYPE_STREAM and not os.path.exists(path):
            QMessageBox.warning(self,"Archivo no encontrado",path); return
        self.current_index=index; self.audio_engine.play(path)
        self.is_playing=True; self.btn_play.setText("⏸")
        # Iniciar contador de duración para radio internet
        if item.item_type==PlaylistItem.TYPE_STREAM:
            self._current_stream_item_idx=index; item._stream_duration=0
        self.lbl_now_title.setText(item.title); self.lbl_now_artist.setText(item.artist or "—")
        self.eq_widget.set_playing(True); self.lbl_eq_status.setText("EN VIVO")
        self.lbl_eq_status.setStyleSheet("color:#ff6600;font-size:10px;font-weight:bold;")
        self._set_playing_status(); self._update_next_info(); self._highlight_row(index)

    def _set_playing_status(self):
        self.lbl_st_play.setText("⬤ Reproduciendo"); self.lbl_st_play.setStyleSheet("color:#00cc66;")

    def _play_prev(self):
        if self.current_index>0: self._play_index(self.current_index-1)

    def _skip_next(self):
        if self._random and self.playlist: self._play_index(random.randint(0,len(self.playlist)-1)); return
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

    def _update_stream_duration(self):
        """Actualiza el contador de duración de la radio por internet"""
        if self.is_playing and self._current_stream_item_idx>=0:
            idx=self._current_stream_item_idx
            if idx<len(self.playlist):
                item=self.playlist[idx]
                if item.item_type==PlaylistItem.TYPE_STREAM:
                    item._stream_duration+=1
                    # Actualizar celda de duración en la tabla
                    dur_item=self.playlist_table.item(idx,4)
                    if dur_item: dur_item.setText(item.duration_str())

    # ══════════════════════════════════════
    #  HORA
    # ══════════════════════════════════════
    def _select_time_folder(self):
        folder=QFileDialog.getExistingDirectory(self,"Seleccionar carpeta de locuciones de hora")
        if folder: self._time_folder=folder; self.edit_time_folder.setText(folder)

    def _play_hour(self):
        now=datetime.now(); hour=now.hour
        folder=self._time_folder
        if hasattr(self,"edit_time_folder"): folder=self.edit_time_folder.text().strip() or folder
        if not folder or not os.path.exists(folder):
            QMessageBox.information(self,"Carpeta de hora no configurada",
                "Ve a la pestaña 'Eventos' y configura la carpeta de locuciones.\n\n"
                "La carpeta debe contener archivos nombrados:\n"
                "00.mp3, 01.mp3, 02.mp3 ... 23.mp3\n\n"
                "También puedes copiar la carpeta 'time' junto al programa instalado.")
            return
        possible=[f"{hour:02d}.mp3",f"{hour}.mp3",f"hora_{hour:02d}.mp3",
                  f"{hour:02d}.wav",f"{hour:02d}.ogg",f"hora_{hour:02d}.wav"]
        found=None
        for name in possible:
            full=os.path.join(folder,name)
            if os.path.exists(full): found=full; break
        if found:
            self.audio_engine.play(found)
            self.lbl_now_title.setText(f"🕐 Hora: {hour:02d}:00")
            self.lbl_now_artist.setText("Locución automática")
            self.eq_widget.set_playing(True)
        else:
            QMessageBox.warning(self,"No encontrado",
                f"No hay archivo de audio para las {hour:02d}:00\nCarpeta: {folder}\nBuscado: {possible[0]}")

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
        added=0
        for fn in sorted(os.listdir(folder)):
            if os.path.splitext(fn)[1].lower() in exts:
                self.playlist.append(PlaylistItem(os.path.join(folder,fn))); added+=1
        if added>0: self._refresh_playlist()

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
            self.playlist.clear(); self.current_index=-1; self._current_stream_item_idx=-1; self._refresh_playlist()

    def _shuffle(self): random.shuffle(self.playlist); self._refresh_playlist()

    def _refresh_playlist(self):
        t=self.playlist_table; t.setRowCount(len(self.playlist))
        tc={PlaylistItem.TYPE_MUSIC:"#44aaaa",PlaylistItem.TYPE_JINGLE:"#ff8833",
            PlaylistItem.TYPE_SPOT:"#bb55ff",PlaylistItem.TYPE_STREAM:"#44aaff",
            PlaylistItem.TYPE_STOP:"#ff5555",PlaylistItem.TYPE_PAUSE:"#888888"}
        for i,item in enumerate(self.playlist):
            t.setRowHeight(i,24); t.setItem(i,0,QTableWidgetItem(str(i+1)))
            t.setItem(i,1,QTableWidgetItem(item.title)); t.setItem(i,2,QTableWidgetItem(item.artist))
            ti=QTableWidgetItem(item.item_type); ti.setForeground(QColor(tc.get(item.item_type,"#888"))); t.setItem(i,3,ti)
            t.setItem(i,4,QTableWidgetItem(item.duration_str()))
        td=sum(p.duration for p in self.playlist if p.item_type!=PlaylistItem.TYPE_STREAM)
        h,r=divmod(int(td),3600); m,s=divmod(r,60)
        self.lbl_total.setText(f"{len(self.playlist)} pistas — {h:02d}:{m:02d}:{s:02d}" if h else f"{len(self.playlist)} pistas — {m:02d}:{s:02d}")
        self.lbl_st_pl.setText(f"Playlist: {len(self.playlist)} pistas"); self._update_next_info()

    def _highlight_row(self,index):
        for r in range(self.playlist_table.rowCount()):
            for c in range(self.playlist_table.columnCount()):
                it=self.playlist_table.item(r,c)
                if it:
                    it.setBackground(QColor("#ff660025" if r==index else "transparent"))
                    it.setForeground(QColor("#ff9944" if r==index else "#dddddd"))

    def _update_next_info(self):
        ni=self.current_index+1
        if ni<len(self.playlist):
            self.lbl_next_title.setText(self.playlist[ni].title)
            self.lbl_next_dur.setText(f"{self.playlist[ni].artist} — {self.playlist[ni].duration_str()}")
        else: self.lbl_next_title.setText("— Fin de playlist —"); self.lbl_next_dur.setText("")

    # ══════════════════════════════════════
    #  CUÑAS
    # ══════════════════════════════════════
    def _play_jingle(self,idx):
        p=self.jingles[idx]
        if p and os.path.exists(p): self.audio_engine.play(p)
        else: QMessageBox.information(self,f"Cuña {idx+1}","Sin archivo. Usa 'Editar Cuñas...' para asignar.")

    def _edit_cunas(self):
        dlg=QDialog(self); dlg.setWindowTitle("Editar Cuñas"); dlg.setFixedSize(540,420)
        lay=QVBoxLayout(dlg); grid=QGridLayout(); grid.setSpacing(6)
        edits=[]
        for i in range(9):
            lbl=QLabel(f"Cuña {i+1}:"); lbl.setStyleSheet("color:#888;")
            ne=QLineEdit(self.jingle_names[i]); ne.setFixedWidth(130)
            pe=QLineEdit(self.jingles[i]); pe.setPlaceholderText("(sin archivo)")
            btn=QPushButton("..."); btn.setFixedWidth(28)
            btn.clicked.connect(lambda _,p=pe: p.setText(QFileDialog.getOpenFileName(dlg,"","","Audio (*.mp3 *.wav *.ogg)")[0]))
            grid.addWidget(lbl,i,0); grid.addWidget(ne,i,1); grid.addWidget(pe,i,2); grid.addWidget(btn,i,3)
            edits.append((ne,pe))
        lay.addLayout(grid)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject); lay.addWidget(bb)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            for i,(ne,pe) in enumerate(edits):
                self.jingle_names[i]=ne.text(); self.jingles[i]=pe.text()
            if hasattr(self,'_cunas_actions'):
                for i,a in enumerate(self._cunas_actions): a.setText(f"{i+1}. {self.jingle_names[i]}")

    # ══════════════════════════════════════
    #  SCHEDULER
    # ══════════════════════════════════════
    def _add_event(self):
        dlg=QDialog(self); dlg.setWindowTitle("Planificar evento"); dlg.setFixedSize(450,410)
        lay=QVBoxLayout(dlg); lay.setSpacing(8)
        g=QGridLayout(); g.setSpacing(8)
        g.addWidget(QLabel("Hora:"),0,0); te=QTimeEdit(); te.setDisplayFormat("HH:mm"); g.addWidget(te,0,1)
        g.addWidget(QLabel("Tipo:"),1,0); tc=QComboBox(); tc.addItems(SchedulerEvent.TYPES); g.addWidget(tc,1,1)
        g.addWidget(QLabel("Descripción:"),2,0); ae=QLineEdit("Cuña horaria"); g.addWidget(ae,2,1)
        g.addWidget(QLabel("Fichero:"),3,0)
        fr=QHBoxLayout(); fe=QLineEdit()
        fb=QPushButton("..."); fb.setFixedWidth(28)
        fb.clicked.connect(lambda: fe.setText(QFileDialog.getOpenFileName(dlg,"","","Audio (*.mp3 *.wav *.ogg *.flac)")[0]))
        fr.addWidget(fe); fr.addWidget(fb); g.addLayout(fr,3,1); lay.addLayout(g)
        lay.addWidget(QLabel("Días activos:"))
        dr=QHBoxLayout(); dchks=[QCheckBox(d) for d in DAYS_ES]
        for c in dchks: c.setChecked(True); dr.addWidget(c)
        lay.addLayout(dr)
        opt=QHBoxLayout()
        rc=QCheckBox("Repetir semanalmente"); rc.setChecked(True)
        ic=QCheckBox("Interrumpir canción actual"); ic.setChecked(True)
        opt.addWidget(rc); opt.addWidget(ic); lay.addLayout(opt)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject); lay.addWidget(bb)
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
        tc={"Cuña":"#ff8833","Spot":"#bb55ff","Playlist":"#44aaff","Silencio":"#888","Archivo":"#44cc66","Locución hora":"#ffcc00"}
        for i,ev in enumerate(self.scheduler_events):
            t.setRowHeight(i,24); t.setItem(i,0,QTableWidgetItem(ev.time_str))
            ti=QTableWidgetItem(ev.event_type); ti.setForeground(QColor(tc.get(ev.event_type,"#888"))); t.setItem(i,1,ti)
            fn=os.path.basename(ev.file_path) if ev.file_path else ev.action; t.setItem(i,2,QTableWidgetItem(fn))
            t.setItem(i,3,QTableWidgetItem("--:--"))
            days_str="".join(d for d,v in zip(DAYS_ES,ev.days) if v); t.setItem(i,4,QTableWidgetItem(days_str))

    def _check_scheduler(self):
        now=datetime.now().strftime("%H:%M")
        for ev in self.scheduler_events:
            if ev.time_str==now and not ev.executed_today and ev.runs_today():
                ev.executed_today=True
                if ev.event_type=="Silencio": self._stop()
                elif ev.event_type=="Locución hora": self._play_hour()
                elif ev.file_path and os.path.exists(ev.file_path):
                    if ev.interrupt: self.audio_engine.stop()
                    self.audio_engine.play(ev.file_path)
                    self.lbl_now_title.setText(f"[{ev.event_type}] {ev.action}")
                self._refresh_sched()

    # ══════════════════════════════════════
    #  STREAMING
    # ══════════════════════════════════════
    def _show_stream_dialog(self):
        dlg=StreamingDialog(self,self._stream_cfg)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            self._stream_cfg=dlg.get_config()
            self.stream_engine.configure(self._stream_cfg)
            self.lbl_radio_name.setText(self._stream_cfg.get("radio_name","Mi Radio Online"))
            self._save_config()

    def _toggle_stream(self):
        if self.stream_engine.is_connected():
            self.stream_engine.disconnect_stream()
        else:
            if not self._stream_cfg or not self._stream_cfg.get("host",""):
                reply=QMessageBox.question(self,"Configurar streaming",
                    "No hay configuración de streaming guardada.\n¿Abrir configuración ahora?")
                if reply==QMessageBox.StandardButton.Yes: self._show_stream_dialog()
                if not self._stream_cfg or not self._stream_cfg.get("host",""): return
            self.stream_engine.configure(self._stream_cfg)
            # Ejecutar en hilo separado para no bloquear UI
            threading.Thread(target=self.stream_engine.connect_stream,daemon=True).start()

    def _on_stream_status(self,connected,msg):
        if connected:
            self.lbl_stream_dot.setStyleSheet("color:#00cc66;font-size:14px;")
            self.lbl_stream_mini.setText(msg); self.lbl_stream_mini.setStyleSheet("color:#00cc66;font-size:10px;")
            self.lbl_st_stream.setText("⬤ Streaming activo"); self.lbl_st_stream.setStyleSheet("color:#00cc66;")
            self.btn_stream_quick.setChecked(True); self.btn_stream_quick.setText("⬤  STREAM ON")
        else:
            self.lbl_stream_dot.setStyleSheet("color:#330000;font-size:14px;")
            self.lbl_stream_mini.setText(msg or "Sin stream"); self.lbl_stream_mini.setStyleSheet("color:#555;font-size:10px;")
            self.lbl_st_stream.setText("⬤ Sin conexión"); self.lbl_st_stream.setStyleSheet("color:#444;")
            self.btn_stream_quick.setChecked(False); self.btn_stream_quick.setText("⬤  STREAM OFF")

    def _on_listeners_update(self,count):
        if count>self._peak_listeners: self._peak_listeners=count
        self.lbl_st_listeners.setText(f"Oyentes: {count} (pico: {self._peak_listeners})")

    # ══════════════════════════════════════
    #  FILES
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
    #  CONFIG
    # ══════════════════════════════════════
    def _load_config(self):
        if not os.path.exists(CONFIG_FILE): return
        try:
            with open(CONFIG_FILE) as f: cfg=json.load(f)
            self._stream_cfg=cfg.get("stream_cfg",{})
            if self._stream_cfg:
                self.stream_engine.configure(self._stream_cfg)
                self.lbl_radio_name.setText(self._stream_cfg.get("radio_name","Mi Radio Online"))
            self.jingles=cfg.get("jingles",[""]*9)
            self.jingle_names=cfg.get("jingle_names",["Cuña "+str(i+1) for i in range(9)])
            self._time_folder=cfg.get("time_folder","")
            if hasattr(self,"edit_time_folder") and self._time_folder:
                self.edit_time_folder.setText(self._time_folder)
            theme=cfg.get("theme","dark"); self.apply_theme(theme)
            for ev_d in cfg.get("scheduler",[]): self.scheduler_events.append(SchedulerEvent.from_dict(ev_d))
            self._refresh_sched()
            if hasattr(self,'_cunas_actions'):
                for i,a in enumerate(self._cunas_actions): a.setText(f"{i+1}. {self.jingle_names[i]}")
        except: pass

    def _save_config(self):
        tf=self._time_folder
        if hasattr(self,"edit_time_folder"): tf=self.edit_time_folder.text().strip() or tf
        cfg={"stream_cfg":self._stream_cfg,"jingles":self.jingles,
             "jingle_names":self.jingle_names,"theme":self._theme,
             "time_folder":tf,"scheduler":[e.to_dict() for e in self.scheduler_events]}
        try:
            with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,indent=2)
        except: pass

    # ══════════════════════════════════════
    #  CLOCK
    # ══════════════════════════════════════
    def _update_clock(self):
        now=datetime.now()
        self.lbl_clock.setText(now.strftime("%H:%M:%S"))
        self.lbl_date.setText(now.strftime("%A %d de %B de %Y"))
        if now.hour==0 and now.minute==0 and now.second<2:
            for ev in self.scheduler_events: ev.executed_today=False
        self._update_countdown()

    def _update_countdown(self):
        now=datetime.now(); now_str=now.strftime("%H:%M")
        pending=[(ev.time_str,ev) for ev in self.scheduler_events
                 if not ev.executed_today and ev.time_str>now_str and ev.runs_today()]
        pending.sort(key=lambda x:x[0])
        if pending:
            t_str,ev=pending[0]; h,m=map(int,t_str.split(":")); then=now.replace(hour=h,minute=m,second=0)
            mins=int((then-now).total_seconds()//60)
            self.lbl_next_event_bar.setText(f"[{ev.event_type}] {ev.action} — {mins} min")
            self.lbl_countdown.setText(f"En {mins} min")
        else:
            self.lbl_next_event_bar.setText("Sin eventos pendientes"); self.lbl_countdown.setText("")

    def closeEvent(self,event):
        self._save_config(); self.audio_engine.stop()
        if self.stream_engine.is_connected(): self.stream_engine.disconnect_stream()
        event.accept()


# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
def main():
    app=QApplication(sys.argv)
    app.setApplicationName(APP_NAME); app.setApplicationVersion(APP_VERSION)
    win=PoleCasterWindow(); win.show(); sys.exit(app.exec())

if __name__=="__main__":
    main()
