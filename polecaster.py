"""
PoleCaster v4.0 — Radio Automation Suite
Diseño: Grup Comunikados con K
En memoria de Polechita — 10 de Mayo 2026
Layout definitivo basado en diseño aprobado
"""
import sys, os, json, time, threading, subprocess, random, math, socket, shutil
import requests
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QTabWidget, QLineEdit, QComboBox,
    QCheckBox, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QGroupBox, QGridLayout, QSpinBox, QFrame, QProgressBar,
    QDialog, QDialogButtonBox, QTimeEdit, QMessageBox, QSizePolicy,
    QScrollArea, QTreeWidget, QTreeWidgetItem, QStatusBar, QMenu,
    QAbstractItemView, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QPainter, QLinearGradient,
    QPen, QAction, QPixmap, QIcon, QKeySequence, QPainterPath, QBrush
)

APP_NAME    = "PoleCaster"
APP_VERSION = "4.0"
APP_BRAND   = "Grup Comunikados con K"
APP_MEMORY  = "En memoria de Polechita — 10 de Mayo 2026"
CONFIG_FILE = "polecaster_config.json"
DAYS_ES     = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]

def resource_path(rel):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)

LOGO_PATH = resource_path(os.path.join("assets","logo.png"))

# ══════════════════════════════════════════
#  ESTILOS
# ══════════════════════════════════════════
DARK = """
QMainWindow,QWidget{background:#111111;color:#dddddd;font-family:'Segoe UI';font-size:11px;}
QMenuBar{background:#080808;color:#999;border-bottom:1px solid #1a1a1a;padding:2px 4px;}
QMenuBar::item{padding:4px 10px;border-radius:3px;}
QMenuBar::item:selected{background:#ff660033;color:#ff6600;}
QMenu{background:#161616;border:1px solid #2a2a2a;color:#ccc;padding:4px 0;}
QMenu::item{padding:6px 20px;}
QMenu::item:selected{background:#ff660033;color:#ff8833;}
QMenu::separator{height:1px;background:#2a2a2a;margin:3px 8px;}
QStatusBar{background:#050505;color:#444;font-size:10px;border-top:1px solid #111;}
QTabWidget::pane{border:1px solid #1a1a1a;background:#111;}
QTabBar::tab{background:#0a0a0a;color:#555;padding:6px 14px;border:none;font-size:10px;}
QTabBar::tab:selected{color:#ff6600;border-bottom:2px solid #ff6600;background:#111;}
QTabBar::tab:hover{color:#ccc;background:#141414;}
QTableWidget{background:#111;gridline-color:#1a1a1a;border:none;alternate-background-color:#141414;}
QTableWidget::item{padding:4px 6px;border-bottom:1px solid #151515;color:#cccccc;}
QTableWidget::item:selected{background:#ff660025;color:#fff;}
QHeaderView::section{background:#0a0a0a;color:#555;padding:4px 6px;border:none;font-size:10px;letter-spacing:1px;}
QPushButton{background:#1a1a1a;color:#bbbbbb;border:1px solid #2a2a2a;padding:5px 10px;border-radius:4px;font-size:11px;}
QPushButton:hover{background:#242424;color:#fff;border-color:#ff6600;}
QPushButton:pressed{background:#0f0f0f;}
QPushButton:checked{background:#ff660033;border-color:#ff6600;color:#ff8833;}
QLineEdit,QComboBox,QSpinBox,QTimeEdit{background:#0a0a0a;color:#ddd;border:1px solid #222;padding:5px 8px;border-radius:3px;min-height:22px;}
QLineEdit:focus,QComboBox:focus{border-color:#ff6600;}
QComboBox::drop-down{border:none;width:18px;}
QComboBox QAbstractItemView{background:#111;color:#ddd;border:1px solid #222;selection-background-color:#ff660033;}
QSlider::groove:horizontal{height:4px;background:#1e1e1e;border-radius:2px;}
QSlider::handle:horizontal{background:#ff6600;width:13px;height:13px;border-radius:7px;margin:-5px 0;}
QSlider::sub-page:horizontal{background:#ff6600;border-radius:2px;}
QProgressBar{background:#1a1a1a;border:none;border-radius:2px;height:5px;}
QProgressBar::chunk{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6600,stop:1 #ffaa00);border-radius:2px;}
QGroupBox{border:1px solid #1e1e1e;border-radius:4px;margin-top:8px;padding-top:8px;color:#444;font-size:10px;}
QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#ff6600;}
QCheckBox{color:#aaa;}
QCheckBox::indicator{width:13px;height:13px;background:#0a0a0a;border:1px solid #2a2a2a;border-radius:2px;}
QCheckBox::indicator:checked{background:#ff6600;border-color:#ff6600;}
QTreeWidget{background:#0d0d0d;border:none;color:#bbb;alternate-background-color:#111;}
QTreeWidget::item{padding:3px 2px;}
QTreeWidget::item:selected{background:#ff660025;color:#ff8833;}
QTreeWidget::item:hover{background:#1a1a1a;}
QScrollBar:vertical{background:#0a0a0a;width:5px;}
QScrollBar::handle:vertical{background:#2a2a2a;border-radius:3px;min-height:20px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}
QScrollBar:horizontal{background:#0a0a0a;height:5px;}
QScrollBar::handle:horizontal{background:#2a2a2a;border-radius:3px;}
QScrollArea{border:none;background:transparent;}
QSplitter::handle{background:#1a1a1a;}
"""

LIGHT = """
QMainWindow,QWidget{background:#f0f0f0;color:#1a1a1a;font-family:'Segoe UI';font-size:11px;}
QMenuBar{background:#fff;color:#333;border-bottom:1px solid #ddd;padding:2px 4px;}
QMenuBar::item{padding:4px 10px;border-radius:3px;}
QMenuBar::item:selected{background:#ff660020;color:#cc4400;}
QMenu{background:#fff;border:1px solid #ccc;color:#222;padding:4px 0;}
QMenu::item{padding:6px 20px;}
QMenu::item:selected{background:#ff660015;color:#cc4400;}
QMenu::separator{height:1px;background:#eee;margin:3px 8px;}
QStatusBar{background:#fff;color:#888;font-size:10px;border-top:1px solid #ddd;}
QTabWidget::pane{border:1px solid #ddd;background:#fff;}
QTabBar::tab{background:#e8e8e8;color:#888;padding:6px 14px;border:none;font-size:10px;}
QTabBar::tab:selected{color:#cc4400;border-bottom:2px solid #ff6600;background:#fff;}
QTabBar::tab:hover{color:#333;background:#ebebeb;}
QTableWidget{background:#fff;gridline-color:#eee;border:none;alternate-background-color:#fafafa;}
QTableWidget::item{padding:4px 6px;border-bottom:1px solid #eee;color:#222;}
QTableWidget::item:selected{background:#ff660015;color:#cc4400;}
QHeaderView::section{background:#e8e8e8;color:#888;padding:4px 6px;border:none;font-size:10px;}
QPushButton{background:#fff;color:#333;border:1px solid #ccc;padding:5px 10px;border-radius:4px;font-size:11px;}
QPushButton:hover{background:#f5f5f5;color:#000;border-color:#ff6600;}
QPushButton:pressed{background:#e8e8e8;}
QPushButton:checked{background:#ff660015;border-color:#ff6600;color:#cc4400;}
QLineEdit,QComboBox,QSpinBox,QTimeEdit{background:#fff;color:#222;border:1px solid #ccc;padding:5px 8px;border-radius:3px;min-height:22px;}
QLineEdit:focus,QComboBox:focus{border-color:#ff6600;}
QComboBox::drop-down{border:none;width:18px;}
QComboBox QAbstractItemView{background:#fff;color:#222;border:1px solid #ccc;selection-background-color:#ff660015;}
QSlider::groove:horizontal{height:4px;background:#ddd;border-radius:2px;}
QSlider::handle:horizontal{background:#ff6600;width:13px;height:13px;border-radius:7px;margin:-5px 0;}
QSlider::sub-page:horizontal{background:#ff6600;border-radius:2px;}
QProgressBar{background:#e0e0e0;border:none;border-radius:2px;height:5px;}
QProgressBar::chunk{background:#ff6600;border-radius:2px;}
QGroupBox{border:1px solid #ddd;border-radius:4px;margin-top:8px;padding-top:8px;color:#888;font-size:10px;}
QGroupBox::title{subcontrol-origin:margin;left:8px;padding:0 4px;color:#ff6600;}
QCheckBox{color:#333;}
QCheckBox::indicator{width:13px;height:13px;background:#fff;border:1px solid #ccc;border-radius:2px;}
QCheckBox::indicator:checked{background:#ff6600;border-color:#ff6600;}
QTreeWidget{background:#fff;border:none;color:#222;alternate-background-color:#fafafa;}
QTreeWidget::item{padding:3px 2px;}
QTreeWidget::item:selected{background:#ff660015;color:#cc4400;}
QTreeWidget::item:hover{background:#f5f5f5;}
QScrollBar:vertical{background:#f0f0f0;width:5px;}
QScrollBar::handle:vertical{background:#ccc;border-radius:3px;min-height:20px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}
QSplitter::handle{background:#ddd;}
"""

# ══════════════════════════════════════════
#  LOGO CIRCULAR
# ══════════════════════════════════════════
class CircularLogo(QWidget):
    def __init__(self, size=36, parent=None):
        super().__init__(parent); self.setFixedSize(size, size); self._s = size
        self._pix = None
        if os.path.exists(LOGO_PATH):
            self._pix = QPixmap(LOGO_PATH).scaled(size, size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation)

    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        s = self._s; path = QPainterPath(); path.addEllipse(1,1,s-2,s-2)
        p.setClipPath(path)
        if self._pix: p.drawPixmap(0,0,self._pix)
        else:
            p.fillRect(0,0,s,s,QColor("#ff6600"))
            p.setPen(QColor("#fff")); p.setFont(QFont("Segoe UI",int(s*0.45),QFont.Weight.Bold))
            p.drawText(0,0,s,s,Qt.AlignmentFlag.AlignCenter,"P")
        p.setClipping(False); p.setPen(QPen(QColor("#ff6600"),2))
        p.drawEllipse(1,1,s-2,s-2); p.end()

# ══════════════════════════════════════════
#  ECUALIZADOR
# ══════════════════════════════════════════
class EQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.setMinimumHeight(56)
        self._b=26; self._h=[0.0]*26; self._t=[0.0]*26
        self._pk=[0.0]*26; self._pkh=[0]*26
        self._playing=False; self._mic=False; self._ph=0.0; self._dark=True
        t=QTimer(self); t.timeout.connect(self._anim); t.start(40)

    def set_playing(self,v): self._playing=v
    def set_mic(self,v): self._mic=v
    def set_dark(self,v): self._dark=v; self.update()

    def _anim(self):
        self._ph+=0.09
        if self._playing or self._mic:
            for i in range(self._b):
                if self._mic:
                    self._t[i]=max(0,min(1,0.3+0.5*math.sin(self._ph*2.1+i*0.3)+random.gauss(0,0.12)))
                else:
                    base=0.1+0.55*math.exp(-0.04*i)
                    w=0.2*math.sin(self._ph*1.7+i*0.4)+0.12*math.sin(self._ph*3.1+i*0.7)
                    sp=0.28*math.exp(-0.5*(i-5)**2)+0.18*math.exp(-0.5*(i-13)**2)
                    self._t[i]=max(0,min(1,base+w+sp+random.gauss(0,0.06)))
        else:
            self._t=[0.0]*self._b
        for i in range(self._b):
            d=self._t[i]-self._h[i]
            self._h[i]+=d*0.38 if d>0 else d*0.11
            self._h[i]=max(0,min(1,self._h[i]))
            if self._h[i]>=self._pk[i]: self._pk[i]=self._h[i]; self._pkh[i]=22
            else:
                if self._pkh[i]>0: self._pkh[i]-=1
                else: self._pk[i]=max(0,self._pk[i]-0.014)
        self.update()

    def paintEvent(self, e):
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w,h=self.width(),self.height()
        bg=QColor("#0a0a0a") if self._dark else QColor("#1c1c1c")
        p.fillRect(0,0,w,h,bg)
        p.setPen(QPen(QColor("#2a2a2a"),1)); p.drawRect(0,0,w-1,h-1)
        n=self._b; gap=2; bw=max(3,(w-gap*(n+1))//n); tot=bw+gap
        for i in range(n):
            x=gap+i*tot; bh=int(self._h[i]*(h-8))
            if bh<1:
                p.fillRect(x,h-3,bw,2,QColor("#1a1a1a")); continue
            y=h-bh-3; r2=self._h[i]
            if self._mic:
                r=0;g=int(r2*180);b2=255
            elif r2<0.5: r=int(r2*2*200);g=210;b2=30
            elif r2<0.8: r=255;g=int((1-(r2-0.5)/0.3)*150);b2=10
            else: r=255;g=int((1-(r2-0.8)/0.2)*50);b2=0
            grad=QLinearGradient(x,y+bh,x,y)
            grad.setColorAt(0,QColor(r,g,b2,170))
            grad.setColorAt(1,QColor(min(255,r+55),min(255,g+55),min(255,b2+30),255))
            p.fillRect(x,y,bw,bh,grad)
            py=int((1-self._pk[i])*(h-8))
            p.fillRect(x,py,bw,2,QColor(255,210,110,210))
        p.end()

# ══════════════════════════════════════════
#  PLAYLIST CON DRAG & DROP
# ══════════════════════════════════════════
class PLTable(QTableWidget):
    filesDropped=pyqtSignal(list)
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
    def dragEnterEvent(self,e):
        if e.mimeData().hasUrls(): e.acceptProposedAction()
        else: super().dragEnterEvent(e)
    def dragMoveEvent(self,e):
        if e.mimeData().hasUrls(): e.acceptProposedAction()
    def dropEvent(self,e):
        if e.mimeData().hasUrls():
            paths=[]
            exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
            for url in e.mimeData().urls():
                path=url.toLocalFile()
                if os.path.isfile(path) and os.path.splitext(path)[1].lower() in exts:
                    paths.append(path)
                elif os.path.isdir(path):
                    for fn in sorted(os.listdir(path)):
                        if os.path.splitext(fn)[1].lower() in exts:
                            paths.append(os.path.join(path,fn))
            if paths: self.filesDropped.emit(paths)
            e.acceptProposedAction()
        else: super().dropEvent(e)

# ══════════════════════════════════════════
#  MODELOS
# ══════════════════════════════════════════
class PLItem:
    M="Música"; J="Cuña"; S="Spot"; R="Radio"; P="Pausa"
    def __init__(self,path,title="",artist="",dur=0,typ=None,url=""):
        self.path=path; self.title=title or os.path.splitext(os.path.basename(path))[0]
        self.artist=artist; self.dur=dur; self.typ=typ or self.M; self.url=url
        self._sdur=0
    def dur_str(self):
        if self.typ==self.R:
            h,r=divmod(self._sdur,3600); m,s=divmod(r,60); return f"{h:02d}:{m:02d}:{s:02d}"
        if self.dur<=0: return "--:--"
        m,s=divmod(int(self.dur),60); return f"{m:02d}:{s:02d}"
    def to_dict(self): return {"path":self.path,"title":self.title,"artist":self.artist,"dur":self.dur,"typ":self.typ,"url":self.url}
    @classmethod
    def from_dict(cls,d): return cls(d["path"],d.get("title",""),d.get("artist",""),d.get("dur",0),d.get("typ",cls.M),d.get("url",""))

class SchEvent:
    TYPES=["Cuña","Spot","Silencio","Archivo","Locución hora"]
    def __init__(self,ts,action,fp="",repeat=False,days=None,etype="Archivo",interrupt=True):
        self.ts=ts; self.action=action; self.fp=fp; self.repeat=repeat
        self.days=days if days else [True]*7; self.etype=etype; self.interrupt=interrupt; self.done=False
    def runs_today(self): return self.days[datetime.now().weekday()]
    def to_dict(self): return {"ts":self.ts,"action":self.action,"fp":self.fp,"repeat":self.repeat,"days":self.days,"etype":self.etype,"interrupt":self.interrupt}
    @classmethod
    def from_dict(cls,d): return cls(d["ts"],d["action"],d.get("fp",""),d.get("repeat",False),d.get("days",[True]*7),d.get("etype","Archivo"),d.get("interrupt",True))

# ══════════════════════════════════════════
#  AUDIO ENGINE
# ══════════════════════════════════════════
class AudioEngine(QThread):
    songFinished=pyqtSignal(); posUpdate=pyqtSignal(float,float)
    def __init__(self):
        super().__init__()
        self._p=None; self._vlc=None; self._vol=85; self._playing=False
        try:
            import vlc
            self._vlc=vlc.Instance("--no-xlib"); self._p=self._vlc.media_player_new()
            self._p.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached,lambda e:self.songFinished.emit())
        except Exception as ex: print(f"VLC: {ex}")

    def play(self,path):
        if not path: return False
        if not path.startswith("http") and not os.path.exists(path): return False
        try:
            import vlc
            m=self._vlc.media_new(path); self._p.set_media(m)
            self._p.play(); self._p.audio_set_volume(self._vol)
            self._playing=True
            threading.Thread(target=self._loop,daemon=True).start(); return True
        except Exception as ex: print(f"Play:{ex}"); return False

    def pause(self):
        if self._p: self._p.pause(); self._playing=not self._playing

    def stop(self):
        if self._p: self._p.stop()
        self._playing=False

    def set_vol(self,v):
        self._vol=v
        if self._p:
            try: self._p.audio_set_volume(v)
            except: pass

    def get_pos(self):
        if self._p:
            try: return self._p.get_time()/1000.0,self._p.get_length()/1000.0
            except: pass
        return 0,0

    def is_playing(self): return self._playing

    def _loop(self):
        while self._playing:
            self.posUpdate.emit(*self.get_pos()); time.sleep(0.5)

# ══════════════════════════════════════════
#  STREAM ENGINE
# ══════════════════════════════════════════
class StreamEngine(QThread):
    statusChanged=pyqtSignal(bool,str); listenersUpdate=pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self._proc=None; self._connected=False; self._cfg={}; self._svol=100
        self._mon=QTimer(); self._mon.timeout.connect(self._poll)

    def configure(self,cfg): self._cfg=cfg
    def set_svol(self,v): self._svol=v
    def is_connected(self): return self._connected

    def connect_bg(self):
        threading.Thread(target=self._connect_thread,daemon=True).start()

    def _connect_thread(self):
        ok,msg=self._do_connect()
        if not ok: self.statusChanged.emit(False,msg)

    def _do_connect(self):
        c=self._cfg
        if not c: return False,"Sin configuración"
        host=c.get("host","").strip(); port_s=c.get("port","8000").strip()
        passwd=c.get("password","").strip(); stype=c.get("type","icecast2")
        mount=c.get("mountpoint","1").strip(); br=int(c.get("bitrate",128))
        fmt=c.get("format","mp3").lower()
        if not host: return False,"❌ Falta el servidor"
        try: port=int(port_s)
        except: return False,f"❌ Puerto inválido: {port_s}"

        # URL según tipo
        if "shoutcast_v1" in stype:
            url=f"icecast://source:{passwd}@{host}:{port}/"
        elif "shoutcast_v2" in stype:
            sid=mount.lstrip("/").strip() or "1"
            try: int(sid)
            except: sid="1"
            url=f"icecast://source:{passwd}@{host}:{port}/{sid}"
        else:
            if not mount.startswith("/"): mount="/"+mount
            url=f"icecast://source:{passwd}@{host}:{port}{mount}"

        codec="libmp3lame" if fmt=="mp3" else "libvorbis"
        ofmt="mp3" if fmt=="mp3" else "ogg"
        vol=f"volume={self._svol/100.0:.2f}"

        # Buscar ffmpeg
        ffmpeg=self._find_ffmpeg()
        if not ffmpeg:
            return False,("❌ FFmpeg no encontrado.\n"
                         "Descarga ffmpeg.exe y ponlo en:\nC:\\PoleCaster\\ffmpeg.exe\n"
                         "https://ffmpeg.org/download.html")

        # Probar dispositivos de audio
        devices=[
            ["-f","dshow","-i","audio=Mezcla estéreo"],
            ["-f","dshow","-i","audio=Stereo Mix"],
            ["-f","dshow","-i","audio=What U Hear"],
            ["-f","lavfi","-i","sine=frequency=1:duration=9999"],
        ]
        flags=subprocess.CREATE_NO_WINDOW if sys.platform=="win32" else 0
        last_err=""
        for asrc in devices:
            cmd=[ffmpeg,"-re"]+asrc+["-af",vol,"-acodec",codec,"-ab",f"{br}k","-ar","44100","-f",ofmt,url,"-y"]
            try:
                proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=flags)
                time.sleep(3)
                if proc.poll() is None:
                    self._proc=proc; self._connected=True
                    lbl="Shoutcast v2" if "v2" in stype else ("Shoutcast v1" if "v1" in stype else "Icecast2")
                    msg=f"✅ Conectado — {lbl} {host}:{port}"
                    self.statusChanged.emit(True,msg)
                    self._mon.start(15000); return True,msg
                last_err=proc.stderr.read().decode("utf-8","ignore")[-200:]
                proc.terminate()
            except Exception as ex: last_err=str(ex)

        # Analizar error
        if "refused" in last_err.lower(): return False,"❌ Conexión rechazada — verifica host y puerto"
        if "401" in last_err or "Unauthorized" in last_err: return False,"❌ Contraseña incorrecta"
        return False,f"❌ Error: {last_err[-120:].strip()}"

    def _find_ffmpeg(self):
        exe_dir=os.path.dirname(sys.executable)
        candidates=[
            resource_path("ffmpeg.exe"),
            os.path.join(exe_dir,"ffmpeg.exe"),
            r"C:\PoleCaster\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            "ffmpeg","ffmpeg.exe",
        ]
        for p in candidates:
            try:
                r=subprocess.run([p,"-version"],capture_output=True,timeout=3)
                if r.returncode==0: return p
            except: continue
        return shutil.which("ffmpeg")

    def disconnect(self):
        self._connected=False; self._mon.stop()
        if self._proc:
            try: self._proc.terminate(); self._proc.wait(timeout=3)
            except: pass
            self._proc=None
        self.statusChanged.emit(False,"Desconectado")

    def _poll(self):
        if not self._connected: return
        if self._proc and self._proc.poll() is not None:
            self._connected=False
            self.statusChanged.emit(False,"Streaming interrumpido")
            if self._cfg.get("reconnect",True):
                time.sleep(3); threading.Thread(target=self._connect_thread,daemon=True).start()
            return
        try:
            c=self._cfg
            r=requests.get(f"http://{c['host']}:{c['port']}/status-json.xsl",timeout=3)
            srcs=r.json().get("icestats",{}).get("source",[])
            if isinstance(srcs,dict): srcs=[srcs]
            for s in srcs:
                if c.get("mountpoint","") in str(s.get("listenurl","")):
                    self.listenersUpdate.emit(int(s.get("listeners",0))); return
        except: pass

# ══════════════════════════════════════════
#  DIÁLOGOS
# ══════════════════════════════════════════
class StreamDlg(QDialog):
    def __init__(self,parent=None,cfg=None):
        super().__init__(parent); self.setWindowTitle("Configuración de Streaming"); self.setFixedSize(480,420)
        lay=QVBoxLayout(self); tabs=QTabWidget(); cfg=cfg or {}

        # Conexión
        c=QWidget(); cl=QGridLayout(c); cl.setSpacing(10); cl.setContentsMargins(14,14,14,14)
        cl.addWidget(QLabel("Tipo:"),0,0)
        self.ctype=QComboBox(); self.ctype.addItems(["Icecast2","Shoutcast v1","Shoutcast v2"])
        t=cfg.get("type","icecast2")
        if "v1" in t: self.ctype.setCurrentIndex(1)
        elif "v2" in t: self.ctype.setCurrentIndex(2)
        self.ctype.currentIndexChanged.connect(self._on_type); cl.addWidget(self.ctype,0,1,1,2)
        cl.addWidget(QLabel("Servidor:"),1,0)
        self.ehost=QLineEdit(cfg.get("host","")); self.ehost.setPlaceholderText("radio.servidor.com"); cl.addWidget(self.ehost,1,1,1,2)
        cl.addWidget(QLabel("Puerto:"),2,0)
        self.eport=QLineEdit(cfg.get("port","8000")); cl.addWidget(self.eport,2,1)
        cl.addWidget(QLabel("Contraseña:"),3,0)
        self.epass=QLineEdit(cfg.get("password","")); self.epass.setEchoMode(QLineEdit.EchoMode.Password)
        self.chkshow=QCheckBox("Ver"); self.chkshow.toggled.connect(lambda v: self.epass.setEchoMode(QLineEdit.EchoMode.Normal if v else QLineEdit.EchoMode.Password))
        ph=QHBoxLayout(); ph.addWidget(self.epass); ph.addWidget(self.chkshow); cl.addLayout(ph,3,1,1,2)
        self.lmount=QLabel("Montaje/SID:"); cl.addWidget(self.lmount,4,0)
        self.emount=QLineEdit(cfg.get("mountpoint","1")); cl.addWidget(self.emount,4,1,1,2)
        cl.addWidget(QLabel("Nombre:"),5,0)
        self.ename=QLineEdit(cfg.get("name","")); cl.addWidget(self.ename,5,1,1,2)
        self.chkrecon=QCheckBox("Reconectar automáticamente"); self.chkrecon.setChecked(cfg.get("reconnect",True)); cl.addWidget(self.chkrecon,6,0,1,3)
        # Prueba
        self.btntest=QPushButton("🔍 Probar conexión"); self.btntest.clicked.connect(self._test); cl.addWidget(self.btntest,7,0,1,2)
        self.ltestres=QLabel(""); cl.addWidget(self.ltestres,7,2)
        tabs.addTab(c,"Conexión")

        # Calidad
        q=QWidget(); ql=QGridLayout(q); ql.setSpacing(10); ql.setContentsMargins(14,14,14,14)
        ql.addWidget(QLabel("Codificador:"),0,0); self.cfmt=QComboBox(); self.cfmt.addItems(["MP3","OGG"]); ql.addWidget(self.cfmt,0,1)
        ql.addWidget(QLabel("Bitrate:"),1,0); self.cbr=QComboBox(); self.cbr.addItems(["64","96","128","192","320"]); self.cbr.setCurrentText(str(cfg.get("bitrate",128))); ql.addWidget(self.cbr,1,1)
        ql.addWidget(QLabel("Frecuencia:"),2,0); self.cfreq=QComboBox(); self.cfreq.addItems(["44100","48000","22050"]); ql.addWidget(self.cfreq,2,1)
        ql.addWidget(QLabel("Canales:"),3,0); self.cch=QComboBox(); self.cch.addItems(["stereo","mono"]); ql.addWidget(self.cch,3,1)
        ql.addWidget(QLabel("Dispositivo audio:"),4,0); self.cdev=QComboBox(); self.cdev.addItems(["Mezcla estéreo","Stereo Mix","Default","Micrófono"]); ql.addWidget(self.cdev,4,1)
        ql.setRowStretch(5,1); tabs.addTab(q,"Calidad")

        # Info
        i=QWidget(); il=QGridLayout(i); il.setSpacing(8); il.setContentsMargins(14,14,14,14)
        for ri,(lbl,attr,key) in enumerate([("Nombre radio:","ernname","radio_name"),("Descripción:","erndesc","radio_desc"),("Género:","erngenre","radio_genre"),("Sitio web:","ernurl","radio_url")]):
            il.addWidget(QLabel(lbl),ri,0); e=QLineEdit(cfg.get(key,"")); setattr(self,attr,e); il.addWidget(e,ri,1)
        il.setRowStretch(4,1); tabs.addTab(i,"Información")

        lay.addWidget(tabs)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(self.accept); bb.rejected.connect(self.reject); lay.addWidget(bb)
        self._on_type(self.ctype.currentIndex())

    def _on_type(self,idx):
        labels=["Montaje:","Contraseña fuente:","Station ID (ej: 1):"]
        phs=["/stream","(contraseña)","1"]
        self.lmount.setText(labels[idx]); self.emount.setPlaceholderText(phs[idx])

    def _test(self):
        try:
            s=socket.socket(); s.settimeout(5)
            r=s.connect_ex((self.ehost.text().strip(),int(self.eport.text())))
            s.close()
            if r==0: self.ltestres.setText("✅ OK"); self.ltestres.setStyleSheet("color:#00cc66;font-weight:bold;")
            else: self.ltestres.setText("❌ Sin resp."); self.ltestres.setStyleSheet("color:#cc3333;")
        except Exception as ex: self.ltestres.setText(f"❌ {str(ex)[:30]}"); self.ltestres.setStyleSheet("color:#cc3333;")

    def get_cfg(self):
        stype=["icecast2","shoutcast_v1","shoutcast_v2"][self.ctype.currentIndex()]
        return {"host":self.ehost.text().strip(),"port":self.eport.text().strip(),
                "password":self.epass.text(),"mountpoint":self.emount.text().strip(),
                "type":stype,"bitrate":int(self.cbr.currentText()),"format":self.cfmt.currentText().lower(),
                "radio_name":self.ernname.text(),"radio_desc":self.erndesc.text(),
                "radio_genre":self.erngenre.text(),"radio_url":self.ernurl.text(),
                "name":self.ename.text(),"reconnect":self.chkrecon.isChecked()}

class RadioDlg(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent); self.setWindowTitle("Añadir Radio de Internet"); self.setFixedSize(420,200)
        lay=QVBoxLayout(self); lay.setSpacing(8); lay.setContentsMargins(14,14,14,14)
        lay.addWidget(QLabel("URL del stream:")); self.eurl=QLineEdit(); self.eurl.setPlaceholderText("http://radio.servidor.com:8000/stream"); lay.addWidget(self.eurl)
        lay.addWidget(QLabel("Nombre:")); self.ename=QLineEdit(); self.ename.setPlaceholderText("Mi Radio Online"); lay.addWidget(self.ename)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Añadir")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(self.accept); bb.rejected.connect(self.reject); lay.addWidget(bb)
    def get_item(self):
        url=self.eurl.text().strip(); name=self.ename.text().strip() or url
        return PLItem(url,name,"",0,PLItem.R,url) if url else None

# ══════════════════════════════════════════
#  VENTANA PRINCIPAL
# ══════════════════════════════════════════
class PoleCaster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PoleCaster v{APP_VERSION} — {APP_BRAND}")
        self.setMinimumSize(1200,700); self.resize(1440,820)
        if os.path.exists(LOGO_PATH): self.setWindowIcon(QIcon(LOGO_PATH))

        self.playlist=[]; self.ci=-1; self.playing=False
        self.jingles=[""]*9; self.jnames=["Cuña "+str(i+1) for i in range(9)]
        self.sched=[]; self._peak=0; self._scfg={}; self._theme="dark"
        self._rep=False; self._repl=False; self._stopafer=False; self._rnd=False
        self._time_folder=""; self._norm=False; self._stream_idx=-1

        self.audio=AudioEngine(); self.stream=StreamEngine()
        self._build(); self._signals(); self._load_cfg()

        self._clk=QTimer(); self._clk.timeout.connect(self._tick); self._clk.start(1000)
        self._scht=QTimer(); self._scht.timeout.connect(self._check_sched); self._scht.start(10000)
        self._sdurt=QTimer(); self._sdurt.timeout.connect(self._update_sdur); self._sdurt.start(1000)
        self._tick(); self.apply_theme("dark")

    # ══════════════════════════════════════
    #  BUILD UI
    # ══════════════════════════════════════
    def _build(self):
        c=QWidget(); self.setCentralWidget(c)
        r=QVBoxLayout(c); r.setContentsMargins(0,0,0,0); r.setSpacing(0)
        self._menubar()
        r.addWidget(self._header())
        r.addWidget(self._topinfo())
        r.addWidget(self._main(),1)
        self._statusbar()

    # ── HEADER ────────────────────────────
    def _header(self):
        h=QWidget(); h.setObjectName("HDR"); h.setFixedHeight(50)
        h.setStyleSheet("#HDR{background:#080808;border-bottom:1px solid #1a1a1a;}")
        lay=QHBoxLayout(h); lay.setContentsMargins(10,5,10,5); lay.setSpacing(10)
        self.logo_hdr=CircularLogo(38); lay.addWidget(self.logo_hdr)
        bl=QVBoxLayout(); bl.setSpacing(0)
        lbl_b=QLabel(APP_BRAND); lbl_b.setStyleSheet("color:#444;font-size:9px;letter-spacing:1px;")
        lbl_n=QLabel("PoleCaster"); lbl_n.setStyleSheet("color:#ff6600;font-size:17px;font-weight:700;")
        bl.addWidget(lbl_b); bl.addWidget(lbl_n); lay.addLayout(bl)
        lay.addStretch()

        self.btn_hora=QPushButton("🕐  HORA"); self.btn_hora.setFixedHeight(32)
        self.btn_hora.setStyleSheet("QPushButton{background:#1a2a1a;color:#00cc66;border:1px solid #00cc6633;border-radius:4px;padding:4px 12px;font-size:11px;font-weight:700;}QPushButton:hover{background:#00cc6618;}")
        self.btn_hora.clicked.connect(self._play_hour); lay.addWidget(self.btn_hora)

        self.btn_stream=QPushButton("⬤  STREAM OFF"); self.btn_stream.setFixedHeight(32)
        self.btn_stream.setCheckable(True)
        self._upd_stream_btn(False); self.btn_stream.clicked.connect(self._toggle_stream); lay.addWidget(self.btn_stream)

        self.btn_theme=QPushButton("☀  Tema claro"); self.btn_theme.setFixedHeight(32)
        self.btn_theme.clicked.connect(self._toggle_theme); lay.addWidget(self.btn_theme)
        lv=QLabel(f"v{APP_VERSION}"); lv.setStyleSheet("color:#2a2a2a;font-size:10px;"); lay.addWidget(lv)
        return h

    def _upd_stream_btn(self,on):
        if on:
            self.btn_stream.setText("⬤  STREAM ON"); self.btn_stream.setChecked(True)
            self.btn_stream.setStyleSheet("QPushButton{background:#002200;color:#00cc66;border:1px solid #00cc6633;border-radius:4px;padding:4px 12px;font-size:11px;font-weight:700;}QPushButton:hover{border-color:#00cc66;}")
        else:
            self.btn_stream.setText("⬤  STREAM OFF"); self.btn_stream.setChecked(False)
            self.btn_stream.setStyleSheet("QPushButton{background:#220000;color:#ff4444;border:1px solid #ff444433;border-radius:4px;padding:4px 12px;font-size:11px;font-weight:700;}QPushButton:hover{border-color:#ff4444;}")

    # ── TOP INFO ──────────────────────────
    def _topinfo(self):
        w=QWidget(); w.setObjectName("TINF"); w.setFixedHeight(62)
        w.setStyleSheet("#TINF{background:#0d0d0d;border-bottom:1px solid #1a1a1a;}")
        lay=QHBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)

        def vsep():
            f=QFrame(); f.setFrameShape(QFrame.Shape.VLine); f.setStyleSheet("background:#1a1a1a;max-width:1px;"); return f

        # Col1: On Air
        c1=QWidget(); c1l=QHBoxLayout(c1); c1l.setContentsMargins(12,6,12,6); c1l.setSpacing(8)
        self.lbl_onair=QLabel("● ON AIR"); self.lbl_onair.setStyleSheet("background:#cc2200;color:#fff;font-size:9px;font-weight:700;padding:3px 10px;border-radius:3px;")
        c1l.addWidget(self.lbl_onair)
        inf=QVBoxLayout(); inf.setSpacing(1)
        self.lbl_title=QLabel("Esperando..."); self.lbl_title.setStyleSheet("color:#fff;font-size:13px;font-weight:700;")
        self.lbl_artist=QLabel(""); self.lbl_artist.setStyleSheet("color:#ff6600;font-size:10px;")
        inf.addWidget(self.lbl_title); inf.addWidget(self.lbl_artist)
        c1l.addLayout(inf); c1l.addStretch(); lay.addWidget(c1,2); lay.addWidget(vsep())

        # Col2: Siguiente
        c2=QWidget(); c2l=QVBoxLayout(c2); c2l.setContentsMargins(12,6,12,6); c2l.setSpacing(1)
        QLabel("SIGUIENTE",styleSheet="color:#444;font-size:9px;letter-spacing:1px;"); lb=QLabel("SIGUIENTE"); lb.setStyleSheet("color:#444;font-size:9px;letter-spacing:1px;")
        self.lbl_next=QLabel("—"); self.lbl_next.setStyleSheet("color:#ccc;font-size:11px;font-weight:600;")
        self.lbl_nextd=QLabel(""); self.lbl_nextd.setStyleSheet("color:#555;font-size:10px;")
        c2l.addWidget(lb); c2l.addWidget(self.lbl_next); c2l.addWidget(self.lbl_nextd)
        lay.addWidget(c2,2); lay.addWidget(vsep())

        # Col3: Clock + Logo
        c3=QWidget(); c3l=QHBoxLayout(c3); c3l.setContentsMargins(10,4,10,4); c3l.setSpacing(8)
        self.logo_clk=CircularLogo(36); c3l.addWidget(self.logo_clk)
        cl=QVBoxLayout(); cl.setSpacing(0)
        self.lbl_rname=QLabel("Mi Radio Online"); self.lbl_rname.setStyleSheet("color:#ff6600;font-size:9px;font-weight:700;")
        self.lbl_clk=QLabel("--:--:--"); self.lbl_clk.setStyleSheet("color:#fff;font-family:'Courier New';font-size:20px;font-weight:700;")
        self.lbl_date=QLabel(""); self.lbl_date.setStyleSheet("color:#444;font-size:9px;")
        cl.addWidget(self.lbl_rname); cl.addWidget(self.lbl_clk); cl.addWidget(self.lbl_date)
        c3l.addLayout(cl); lay.addWidget(c3,1)
        return w

    # ── MAIN AREA ─────────────────────────
    def _main(self):
        spl=QSplitter(Qt.Orientation.Horizontal)

        # ── LEFT ──
        left=QWidget(); ll=QVBoxLayout(left); ll.setContentsMargins(0,0,0,0); ll.setSpacing(0)
        # Ecualizador en caja
        eq_box=QWidget(); eq_box.setObjectName("EQBOX"); eq_box.setFixedHeight(82)
        eq_box.setStyleSheet("#EQBOX{background:#0a0a0a;border-bottom:1px solid #1a1a1a;}")
        eql=QHBoxLayout(eq_box); eql.setContentsMargins(8,6,8,6); eql.setSpacing(8)
        eq_info=QVBoxLayout(); eq_info.setSpacing(2)
        lbl_eq=QLabel("ECUALIZADOR"); lbl_eq.setStyleSheet("color:#2a2a2a;font-size:9px;letter-spacing:2px;")
        self.lbl_eqst=QLabel("SILENCIO"); self.lbl_eqst.setStyleSheet("color:#333;font-size:10px;font-weight:700;")
        remr=QHBoxLayout(); remr.setSpacing(4)
        lr=QLabel("Restante"); lr.setStyleSheet("color:#333;font-size:9px;")
        self.lbl_rem=QLabel("--:--"); self.lbl_rem.setStyleSheet("color:#fff;font-family:'Courier New';font-size:13px;font-weight:700;")
        remr.addWidget(lr); remr.addWidget(self.lbl_rem)
        eq_info.addWidget(lbl_eq); eq_info.addWidget(self.lbl_eqst); eq_info.addLayout(remr)
        eql.addLayout(eq_info)
        self.eq=EQWidget(); eql.addWidget(self.eq,1)
        ll.addWidget(eq_box)
        self.prog=QProgressBar(); self.prog.setMaximum(1000); self.prog.setValue(0)
        self.prog.setTextVisible(False); self.prog.setFixedHeight(5); ll.addWidget(self.prog)

        # Tabs izquierdo
        ltabs=QTabWidget()
        ltabs.addTab(self._tab_explorer(),"Explorador")
        ltabs.addTab(self._tab_events(),"Eventos")
        ltabs.addTab(self._tab_sched(),"Scheduler")
        ll.addWidget(ltabs,1)
        ll.addWidget(self._mic_bar())
        spl.addWidget(left)

        # ── CENTER ──
        center=QWidget(); cl=QVBoxLayout(center); cl.setContentsMargins(0,0,0,0); cl.setSpacing(0)
        cl.addWidget(self._playlist_panel(),1)
        cl.addWidget(self._transport())
        spl.addWidget(center)

        # ── RIGHT (Botonera + Streaming) ──
        spl.addWidget(self._right_panel())
        spl.setSizes([240,860,220])
        return spl

    # ── EXPLORADOR ────────────────────────
    def _tab_explorer(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(4,4,4,4); lay.setSpacing(4)
        hint=QLabel("Arrastra archivos/carpetas a la Playlist · Doble clic para añadir")
        hint.setStyleSheet("color:#555;font-size:10px;"); hint.setWordWrap(True); lay.addWidget(hint)
        self.tree=QTreeWidget(); self.tree.setHeaderLabels(["Nombre","Tam."])
        self.tree.setColumnWidth(0,200); self.tree.setAlternatingRowColors(True)
        self.tree.setDragEnabled(True)
        self.tree.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.tree.itemDoubleClicked.connect(self._tree_dbl)
        self.tree.itemExpanded.connect(self._tree_expand)
        self._tree_populate(); lay.addWidget(self.tree,1)
        br=QHBoxLayout()
        b1=QPushButton("🔄 Actualizar"); b1.setFixedHeight(24); b1.clicked.connect(self._tree_populate)
        b2=QPushButton("+ Añadir selección"); b2.setFixedHeight(24); b2.clicked.connect(self._tree_add_sel)
        br.addWidget(b1); br.addWidget(b2); br.addStretch(); lay.addLayout(br)
        return w

    def _tree_populate(self):
        self.tree.clear()
        drives=[]
        if sys.platform=="win32":
            import string
            for lt in string.ascii_uppercase:
                p=f"{lt}:\\"
                if os.path.exists(p): drives.append((p,f"💾 Disco {lt}:"))
        else: drives=[("/","📂 /")]
        home=os.path.expanduser("~")
        pole=os.path.dirname(os.path.abspath(__file__))
        drives.append((home,f"🏠 {os.path.basename(home)}"))
        if pole!=home: drives.append((pole,f"📻 PoleCaster"))
        for path,name in drives:
            if not os.path.exists(path): continue
            it=QTreeWidgetItem([name,""]); it.setData(0,Qt.ItemDataRole.UserRole,path)
            dummy=QTreeWidgetItem(["⏳",""]);it.addChild(dummy); self.tree.addTopLevelItem(it)

    def _tree_expand(self,it):
        if it.childCount()==1 and it.child(0).text(0)=="⏳":
            it.takeChild(0); path=it.data(0,Qt.ItemDataRole.UserRole)
            self._tree_load(it,path)

    def _tree_load(self,parent,path,maxn=120):
        exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
        try:
            ents=sorted(os.scandir(path),key=lambda e:(not e.is_dir(),e.name.lower()))
            for e in ents[:maxn]:
                if e.name.startswith("."): continue
                if e.is_dir():
                    ch=QTreeWidgetItem([f"📁 {e.name}",""]); ch.setData(0,Qt.ItemDataRole.UserRole,e.path)
                    ch.addChild(QTreeWidgetItem(["⏳",""])); parent.addChild(ch)
                elif os.path.splitext(e.name)[1].lower() in exts:
                    sz=f"{e.stat().st_size//1024}K"
                    ch=QTreeWidgetItem([f"🎵 {e.name}",sz]); ch.setData(0,Qt.ItemDataRole.UserRole,e.path)
                    parent.addChild(ch)
        except: pass

    def _tree_dbl(self,it,col):
        path=it.data(0,Qt.ItemDataRole.UserRole)
        if not path: return
        if os.path.isdir(path): self._add_folder_path(path)
        elif os.path.isfile(path): self.playlist.append(PLItem(path)); self._refresh_pl()

    def _tree_add_sel(self):
        for it in self.tree.selectedItems():
            p=it.data(0,Qt.ItemDataRole.UserRole)
            if p:
                if os.path.isdir(p): self._add_folder_path(p)
                elif os.path.isfile(p): self.playlist.append(PLItem(p))
        self._refresh_pl()

    # ── EVENTOS ───────────────────────────
    def _tab_events(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(6,6,6,6); lay.setSpacing(6)
        row=QHBoxLayout(); row.setSpacing(4)
        self.btn_ev_rep=QPushButton("▶ Evento"); self.btn_ev_rep.setCheckable(True)
        self.btn_ev_dis=QPushButton("✕ Descartar")
        self.btn_ev_act=QPushButton("✓ Activar"); self.btn_ev_act.setCheckable(True); self.btn_ev_act.setChecked(True)
        self.btn_ev_new=QPushButton("+ Nuevo"); self.btn_ev_new.clicked.connect(self._add_event)
        for b in [self.btn_ev_rep,self.btn_ev_dis,self.btn_ev_act,self.btn_ev_new]:
            b.setFixedHeight(28); row.addWidget(b)
        lay.addLayout(row)
        self.lbl_next_ev=QLabel("Sin eventos"); self.lbl_next_ev.setStyleSheet("color:#ff6600;font-size:10px;"); lay.addWidget(self.lbl_next_ev)
        # Carpeta hora
        hg=QGroupBox("CARPETA DE LOCUCIONES DE HORA"); hlay=QVBoxLayout(hg)
        hint=QLabel("Archivos: 00.mp3, 01.mp3 ... 23.mp3"); hint.setStyleSheet("color:#555;font-size:9px;"); hlay.addWidget(hint)
        fr=QHBoxLayout()
        self.edit_tf=QLineEdit(); self.edit_tf.setPlaceholderText("C:\\PoleCaster\\time\\")
        btn_tf=QPushButton("📁"); btn_tf.setFixedWidth(30); btn_tf.clicked.connect(self._sel_tf)
        fr.addWidget(self.edit_tf); fr.addWidget(btn_tf); hlay.addLayout(fr)
        lay.addWidget(hg); lay.addStretch()
        return w

    # ── SCHEDULER ─────────────────────────
    def _tab_sched(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        self.sched_tbl=QTableWidget(0,5); self.sched_tbl.setHorizontalHeaderLabels(["Hora","Tipo","Fichero","Dur.","Días"])
        self.sched_tbl.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        self.sched_tbl.setColumnWidth(0,55); self.sched_tbl.setColumnWidth(1,65); self.sched_tbl.setColumnWidth(3,50); self.sched_tbl.setColumnWidth(4,100)
        self.sched_tbl.verticalHeader().setVisible(False); self.sched_tbl.setAlternatingRowColors(True)
        lay.addWidget(self.sched_tbl)
        bb=QWidget(); bl=QHBoxLayout(bb); bl.setContentsMargins(4,4,4,4); bl.setSpacing(4)
        for txt,slot in [("+ Añadir",self._add_event),("✕ Eliminar",self._del_event),("Limpiar",self._clr_events)]:
            b=QPushButton(txt); b.setFixedHeight(22); b.clicked.connect(slot); bl.addWidget(b)
        bl.addStretch()
        self.lbl_cd=QLabel(""); self.lbl_cd.setStyleSheet("color:#ff6600;font-size:10px;"); bl.addWidget(self.lbl_cd)
        lay.addWidget(bb)
        return w

    # ── MIC BAR ───────────────────────────
    def _mic_bar(self):
        m=QWidget(); m.setObjectName("MICBAR"); m.setFixedHeight(56)
        m.setStyleSheet("#MICBAR{background:#080808;border-top:1px solid #1a1a1a;}")
        lay=QHBoxLayout(m); lay.setContentsMargins(8,6,8,6); lay.setSpacing(8)

        self.btn_mic=QPushButton("🎙 MIC"); self.btn_mic.setCheckable(True); self.btn_mic.setFixedSize(64,40)
        self.btn_mic.setStyleSheet("QPushButton{background:#1a2a1a;color:#00cc66;border:1px solid #00cc6633;border-radius:4px;font-size:10px;font-weight:700;}QPushButton:checked{background:#cc000018;color:#ff4444;border-color:#ff4444;}")
        self.btn_mic.clicked.connect(lambda c: self.eq.set_mic(c)); lay.addWidget(self.btn_mic)

        def vsep():
            f=QFrame(); f.setFrameShape(QFrame.Shape.VLine); f.setStyleSheet("background:#1e1e1e;max-width:1px;"); return f

        lay.addWidget(vsep())
        # Selector dispositivo mic
        dc=QVBoxLayout(); dc.setSpacing(1)
        dc.addWidget(QLabel("Dispositivo:",styleSheet="color:#444;font-size:9px;"))
        self.cmic=QComboBox(); self.cmic.addItems(["Default","Mezcla estéreo","Micrófono","Entrada línea"]); self.cmic.setFixedHeight(22); self.cmic.setFixedWidth(130)
        dc.addWidget(self.cmic); lay.addLayout(dc)
        lay.addWidget(vsep())

        # Monitor (local)
        mc=QVBoxLayout(); mc.setSpacing(1)
        mc.addWidget(QLabel("Monitor (local)",styleSheet="color:#444;font-size:9px;"))
        mr=QHBoxLayout(); mr.setSpacing(4)
        self.sl_mon=QSlider(Qt.Orientation.Horizontal); self.sl_mon.setRange(0,100); self.sl_mon.setValue(85); self.sl_mon.setFixedWidth(90)
        self.sl_mon.valueChanged.connect(lambda v:(self.lbl_mon.setText(f"{v}%"),self.audio.set_vol(v) if not self.btn_sil.isChecked() else None))
        self.lbl_mon=QLabel("85%"); self.lbl_mon.setStyleSheet("color:#ff6600;font-size:9px;min-width:28px;")
        mr.addWidget(self.sl_mon); mr.addWidget(self.lbl_mon); mc.addLayout(mr); lay.addLayout(mc)
        lay.addWidget(vsep())

        # Streaming (emisión)
        sc=QVBoxLayout(); sc.setSpacing(1)
        sc.addWidget(QLabel("Streaming (emisión)",styleSheet="color:#444;font-size:9px;"))
        sr=QHBoxLayout(); sr.setSpacing(4)
        self.sl_str=QSlider(Qt.Orientation.Horizontal); self.sl_str.setRange(0,150); self.sl_str.setValue(100); self.sl_str.setFixedWidth(90)
        self.sl_str.valueChanged.connect(lambda v:(self.lbl_str.setText(f"{v}%"),self.stream.set_svol(v)))
        self.lbl_str=QLabel("100%"); self.lbl_str.setStyleSheet("color:#00cc66;font-size:9px;min-width:28px;")
        sr.addWidget(self.sl_str); sr.addWidget(self.lbl_str); sc.addLayout(sr); lay.addLayout(sc)
        lay.addWidget(vsep())

        self.btn_sil=QPushButton("🔇 Silencio"); self.btn_sil.setCheckable(True); self.btn_sil.setFixedHeight(40)
        self.btn_sil.clicked.connect(lambda c:(self.audio.set_vol(0) if c else self.audio.set_vol(self.sl_mon.value()),self.btn_sil.setText("🔊 Restaurar" if c else "🔇 Silencio")))
        lay.addWidget(self.btn_sil); lay.addStretch()
        return m

    # ── PLAYLIST PANEL ────────────────────
    def _playlist_panel(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        ptabs=QTabWidget()
        self.pltbl=self._make_pltbl(); self.pltbl.filesDropped.connect(self._files_dropped)
        ptabs.addTab(self._wrap_pl(self.pltbl),"Playlist 1")
        self.pltbl2=self._make_pltbl()
        ptabs.addTab(self._wrap_pl(self.pltbl2),"Playlist 2")
        btn_new=QPushButton("+"); btn_new.setFixedSize(26,24); btn_new.setToolTip("Nueva playlist")
        ptabs.setCornerWidget(btn_new)
        lay.addWidget(ptabs,1)
        return w

    def _make_pltbl(self):
        t=PLTable(0,5); t.setHorizontalHeaderLabels(["#","TÍTULO","ARTISTA","TIPO","DUR."])
        t.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        t.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        t.setColumnWidth(0,28); t.setColumnWidth(3,65); t.setColumnWidth(4,65)
        t.verticalHeader().setVisible(False)
        t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setAlternatingRowColors(True)
        t.doubleClicked.connect(lambda idx: self._play_idx(idx.row()))
        return t

    def _wrap_pl(self,tbl):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        lay.addWidget(tbl)
        bb=QWidget(); bl=QHBoxLayout(bb); bl.setContentsMargins(4,3,4,3); bl.setSpacing(3)
        for txt,slot in [("+ Archivos",self._add_files),("+ Carpeta",self._add_folder),
                         ("+ Radio",self._add_radio),("✕",self._rem_sel),
                         ("↑",self._mv_up),("↓",self._mv_dn),("Limpiar",self._clr_pl)]:
            b=QPushButton(txt); b.setFixedHeight(24); b.clicked.connect(slot); bl.addWidget(b)
        bl.addStretch()
        self.lbl_tot=QLabel("0 pistas"); self.lbl_tot.setStyleSheet("color:#444;font-size:10px;"); bl.addWidget(self.lbl_tot)
        lay.addWidget(bb)
        return w

    # ── TRANSPORT ─────────────────────────
    def _transport(self):
        t=QWidget(); t.setObjectName("TRANS"); t.setFixedHeight(62)
        t.setStyleSheet("#TRANS{background:#060606;border-top:1px solid #1a1a1a;}")
        lay=QHBoxLayout(t); lay.setContentsMargins(8,6,8,6); lay.setSpacing(5)

        sr="QPushButton{background:#1a1a1a;color:#fff;border:1px solid #2a2a2a;border-radius:20px;font-size:15px;}QPushButton:hover{background:#252525;border-color:#ff6600;}QPushButton:pressed{background:#111;}"
        sp="QPushButton{background:#ff6600;color:#fff;border:none;border-radius:22px;font-size:18px;font-weight:700;}QPushButton:hover{background:#ff7722;}QPushButton:pressed{background:#cc4400;}"
        ss="QPushButton{background:#1a1a1a;color:#ccc;border:1px solid #2a2a2a;border-radius:4px;font-size:13px;min-width:33px;min-height:33px;}QPushButton:hover{background:#222;border-color:#ff6600;}QPushButton:checked{background:#ff660033;border-color:#ff6600;color:#ff8833;}"

        self.btn_prev=QPushButton("⏮"); self.btn_prev.setFixedSize(38,38); self.btn_prev.setStyleSheet(sr); self.btn_prev.clicked.connect(self._play_prev)
        self.btn_stop=QPushButton("⏹"); self.btn_stop.setFixedSize(42,42); self.btn_stop.setStyleSheet(sr); self.btn_stop.clicked.connect(self._stop)
        self.btn_play=QPushButton("▶"); self.btn_play.setFixedSize(46,46); self.btn_play.setStyleSheet(sp); self.btn_play.clicked.connect(self._toggle_play)
        self.btn_next=QPushButton("⏭"); self.btn_next.setFixedSize(38,38); self.btn_next.setStyleSheet(sr); self.btn_next.clicked.connect(self._skip)

        self.btn_rt=QPushButton("🔂"); self.btn_rt.setFixedSize(33,33); self.btn_rt.setStyleSheet(ss); self.btn_rt.setCheckable(True); self.btn_rt.setToolTip("Repetir pista"); self.btn_rt.clicked.connect(lambda c:setattr(self,'_rep',c))
        self.btn_sa=QPushButton("⏹¹"); self.btn_sa.setFixedSize(33,33); self.btn_sa.setStyleSheet(ss); self.btn_sa.setCheckable(True); self.btn_sa.setToolTip("Parar tras pista actual"); self.btn_sa.clicked.connect(lambda c:setattr(self,'_stopafer',c))
        self.btn_rnd=QPushButton("🔀"); self.btn_rnd.setFixedSize(33,33); self.btn_rnd.setStyleSheet(ss); self.btn_rnd.setCheckable(True); self.btn_rnd.setToolTip("Aleatorio"); self.btn_rnd.clicked.connect(lambda c:setattr(self,'_rnd',c))
        self.btn_rl=QPushButton("🔁"); self.btn_rl.setFixedSize(33,33); self.btn_rl.setStyleSheet(ss); self.btn_rl.setCheckable(True); self.btn_rl.setToolTip("Repetir lista"); self.btn_rl.clicked.connect(lambda c:setattr(self,'_repl',c))
        self.btn_norm=QPushButton("⚡"); self.btn_norm.setFixedSize(33,33); self.btn_norm.setStyleSheet(ss); self.btn_norm.setCheckable(True); self.btn_norm.setToolTip("Normalizar volumen")

        for b in [self.btn_prev,self.btn_stop,self.btn_play,self.btn_next]: lay.addWidget(b)
        def vsep():
            f=QFrame(); f.setFrameShape(QFrame.Shape.VLine); f.setStyleSheet("background:#222;max-width:1px;min-height:22px;"); return f
        lay.addWidget(vsep())
        for b in [self.btn_rt,self.btn_sa,self.btn_rnd,self.btn_rl,self.btn_norm]: lay.addWidget(b)
        lay.addWidget(vsep())
        self.lbl_pos=QLabel("00:00 / 00:00"); self.lbl_pos.setStyleSheet("color:#444;font-family:'Courier New';font-size:10px;"); lay.addWidget(self.lbl_pos)
        lay.addStretch()
        self.lbl_sdot=QLabel("⬤"); self.lbl_sdot.setStyleSheet("color:#220000;font-size:12px;")
        self.lbl_smin=QLabel("Sin stream"); self.lbl_smin.setStyleSheet("color:#444;font-size:10px;")
        lay.addWidget(self.lbl_sdot); lay.addWidget(self.lbl_smin)
        return t

    # ── RIGHT PANEL ───────────────────────
    def _right_panel(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        w.setStyleSheet("background:#0d0d0d;border-left:1px solid #1a1a1a;")

        # Header con selector
        hdr=QWidget(); hdr.setStyleSheet("background:#0a0a0a;border-bottom:1px solid #1a1a1a;")
        hl=QHBoxLayout(hdr); hl.setContentsMargins(6,4,6,4); hl.setSpacing(6)
        lbl_r=QLabel("PANEL DERECHO"); lbl_r.setStyleSheet("color:#444;font-size:9px;letter-spacing:1px;")
        self.combo_right=QComboBox(); self.combo_right.addItems(["Botonera/Cuñas","Streaming","Playlist AUX"])
        self.combo_right.currentIndexChanged.connect(self._switch_right)
        hl.addWidget(lbl_r); hl.addStretch(); hl.addWidget(self.combo_right)
        lay.addWidget(hdr)

        self.right_stack=QStackedWidget()
        self.right_stack.addWidget(self._right_jingles())
        self.right_stack.addWidget(self._right_stream())
        self.right_stack.addWidget(self._right_aux())
        lay.addWidget(self.right_stack,1)
        return w

    def _switch_right(self,idx): self.right_stack.setCurrentIndex(idx)

    def _right_jingles(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(6,6,6,6); lay.setSpacing(4)
        grid=QGridLayout(); grid.setSpacing(5)
        self.jbns=[]
        for i in range(9):
            btn=QPushButton(f"F{i+1}\n{self.jnames[i]}\n(vacío)")
            btn.setStyleSheet("""QPushButton{background:#141414;color:#ff6600;border:1px solid #2a2a2a;
                border-radius:5px;padding:6px 4px;min-height:58px;font-size:10px;}
                QPushButton:hover{background:#1e1e1e;border-color:#ff6600;}
                QPushButton:pressed{background:#0a0a0a;}""")
            btn.clicked.connect(lambda _,idx=i: self._play_jingle(idx))
            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda _,idx=i: self._assign_jingle(idx))
            self.jbns.append(btn); grid.addWidget(btn,i//3,i%3)
        lay.addLayout(grid)
        hint=QLabel("Clic derecho para asignar archivo"); hint.setStyleSheet("color:#333;font-size:9px;")
        lay.addWidget(hint); lay.addStretch()
        return w

    def _right_stream(self):
        sa=QScrollArea(); sa.setWidgetResizable(True); sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        cont=QWidget(); lay=QVBoxLayout(cont); lay.setContentsMargins(8,8,8,8); lay.setSpacing(8)

        grp=QGroupBox("SERVIDOR"); gl=QGridLayout(grp); gl.setSpacing(8); gl.setContentsMargins(8,12,8,8)
        gl.addWidget(QLabel("Tipo:"),0,0)
        self.ctype=QComboBox(); self.ctype.addItems(["Icecast2","Shoutcast v1","Shoutcast v2"]); self.ctype.currentIndexChanged.connect(self._on_stype); gl.addWidget(self.ctype,0,1)
        gl.addWidget(QLabel("Servidor:"),1,0); self.ehost=QLineEdit(); self.ehost.setPlaceholderText("radio.servidor.com"); gl.addWidget(self.ehost,1,1)
        gl.addWidget(QLabel("Puerto:"),2,0); self.eport=QLineEdit("8000"); gl.addWidget(self.eport,2,1)
        gl.addWidget(QLabel("Contraseña:"),3,0); self.epass=QLineEdit(); self.epass.setEchoMode(QLineEdit.EchoMode.Password); gl.addWidget(self.epass,3,1)
        self.lbl_mount=QLabel("Montaje/SID:"); gl.addWidget(self.lbl_mount,4,0)
        self.emount=QLineEdit("1"); gl.addWidget(self.emount,4,1)
        lay.addWidget(grp)

        grp2=QGroupBox("CALIDAD"); gl2=QGridLayout(grp2); gl2.setSpacing(8); gl2.setContentsMargins(8,12,8,8)
        gl2.addWidget(QLabel("Bitrate:"),0,0); self.cbr=QComboBox(); self.cbr.addItems(["64k","128k","192k","320k"]); self.cbr.setCurrentIndex(1); gl2.addWidget(self.cbr,0,1)
        gl2.addWidget(QLabel("Formato:"),1,0); self.cfmt=QComboBox(); self.cfmt.addItems(["MP3","OGG"]); gl2.addWidget(self.cfmt,1,1)
        lay.addWidget(grp2)

        grp3=QGroupBox("OYENTES EN VIVO"); g3=QHBoxLayout(grp3); g3.setContentsMargins(8,12,8,8)
        self.lbl_list=QLabel("0"); self.lbl_list.setStyleSheet("color:#00cc66;font-size:26px;font-weight:700;font-family:'Courier New';")
        u=QLabel("oyentes\nactivos"); u.setStyleSheet("color:#444;font-size:9px;")
        g3.addWidget(self.lbl_list); g3.addWidget(u); g3.addStretch()
        self.lbl_peak=QLabel("Pico: 0"); self.lbl_peak.setStyleSheet("color:#ff6600;font-size:10px;"); g3.addWidget(self.lbl_peak)
        lay.addWidget(grp3)

        self.btn_conn=QPushButton("Conectar streaming")
        self.btn_conn.setStyleSheet("QPushButton{background:#ff6600;color:#fff;border:none;border-radius:4px;padding:8px;font-weight:700;}QPushButton:hover{background:#ff7722;}QPushButton:pressed{background:#cc4400;}")
        self.btn_conn.clicked.connect(self._toggle_stream_right); lay.addWidget(self.btn_conn)

        self.lbl_stest=QLabel(""); self.lbl_stest.setWordWrap(True); self.lbl_stest.setStyleSheet("font-size:10px;")
        btn_test=QPushButton("🔍 Probar conexión"); btn_test.clicked.connect(self._test_conn); lay.addWidget(btn_test); lay.addWidget(self.lbl_stest)
        lay.addStretch(); sa.setWidget(cont); return sa

    def _right_aux(self):
        w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(4,4,4,4); lay.setSpacing(4)
        lbl=QLabel("PLAYLIST AUXILIAR"); lbl.setStyleSheet("color:#444;font-size:9px;letter-spacing:1px;"); lay.addWidget(lbl)
        self.aux_tbl=self._make_pltbl(); lay.addWidget(self.aux_tbl,1)
        bb=QHBoxLayout()
        for txt,slot in [("+ Añadir",self._add_files),("Limpiar",lambda: None)]:
            b=QPushButton(txt); b.setFixedHeight(22); bb.addWidget(b)
        bb.addStretch(); lay.addLayout(bb)
        return w

    # ── STATUSBAR ─────────────────────────
    def _statusbar(self):
        sb=self.statusBar()
        self.st_play=QLabel("⬤ Detenido"); self.st_stream=QLabel("⬤ Sin conexión")
        self.st_pl=QLabel("Playlist: 0 pistas"); self.st_list=QLabel("Oyentes: 0")
        sb.addWidget(self.st_play); sb.addWidget(QLabel(" | "))
        sb.addWidget(self.st_stream); sb.addWidget(QLabel(" | "))
        sb.addWidget(self.st_pl); sb.addWidget(QLabel(" | "))
        sb.addWidget(self.st_list)
        sb.addPermanentWidget(QLabel(f"{APP_BRAND} · {APP_NAME} v{APP_VERSION} · {APP_MEMORY}"))

    # ══════════════════════════════════════
    #  MENUBAR
    # ══════════════════════════════════════
    def _menubar(self):
        mb=self.menuBar()
        def a(text,slot=None,sc=None):
            act=QAction(text,self)
            if slot: act.triggered.connect(slot)
            if sc: act.setShortcut(QKeySequence(sc))
            return act

        fm=mb.addMenu("Archivo")
        fm.addAction(a("Nueva playlist",self._new_pl,"Ctrl+N"))
        fm.addAction(a("Abrir playlist",self._open_pl,"Ctrl+O"))
        fm.addAction(a("Guardar playlist",self._save_pl,"Ctrl+S"))
        fm.addSeparator(); fm.addAction(a("Salir",self.close,"Ctrl+Q"))

        vm=mb.addMenu("Ver")
        vm.addAction(a("Explorador","F1")); vm.addAction(a("Programador","F3"))
        vm.addSeparator()
        areas=vm.addMenu("Áreas de trabajo")
        areas.addAction(a("Área 1",None,"Ctrl+1")); areas.addAction(a("Área 2",None,"Ctrl+2"))
        areas.addAction(a("Área 3",None,"Ctrl+3")); areas.addAction(a("Área adicional",None,"Ctrl+4"))
        vm.addAction(a("Pantalla completa",self.showFullScreen,"F11"))
        vm.addSeparator()
        tm=vm.addMenu("Tema")
        self.act_dark=QAction("🌙 Oscuro",self); self.act_dark.setCheckable(True); self.act_dark.setChecked(True); self.act_dark.triggered.connect(lambda: self.apply_theme("dark")); tm.addAction(self.act_dark)
        self.act_light=QAction("☀ Claro",self); self.act_light.setCheckable(True); self.act_light.triggered.connect(lambda: self.apply_theme("light")); tm.addAction(self.act_light)

        cm=mb.addMenu("Cuñas")
        self.cacts=[]
        for i in range(9):
            act=QAction(f"{i+1}. {self.jnames[i]}",self); act.triggered.connect(lambda _,idx=i: self._play_jingle(idx)); cm.addAction(act); self.cacts.append(act)
        cm.addSeparator(); cm.addAction(a("Locución de hora",self._play_hour,"H")); cm.addSeparator(); cm.addAction(a("Editar Cuñas...",self._edit_cunas))

        lm=mb.addMenu("Lista")
        lm.addAction(a("Añadir pistas...",self._add_files,"Ctrl+A"))
        lm.addAction(a("Añadir locución de hora",self._play_hour,"Ctrl+H"))
        lm.addSeparator(); lm.addAction(a("Añadir radio de internet...",self._add_radio))
        lm.addSeparator(); lm.addAction(a("Barajar",self._shuffle,"Ctrl+K"))
        lm.addSeparator(); lm.addAction("Actualizar todas las duraciones")

        mm=mb.addMenu("Media")
        mm.addAction(a("Reproducir",self._toggle_play,"P")); mm.addAction(a("Parar",self._stop,"S"))
        mm.addAction(a("Siguiente",self._skip,"N")); mm.addAction(a("Parar tras la actual",None,"B"))

        hm=mb.addMenu("Herramienta")
        hm.addAction("Mezclador..."); hm.addAction("Explorador del registro..."); hm.addSeparator(); hm.addAction("Opciones...")

        sm=mb.addMenu("Streaming")
        sm.addAction(a("Configurar streaming...",self._show_stream_dlg))
        sm.addSeparator(); sm.addAction(a("Conectar / Desconectar",self._toggle_stream))
        sm.addSeparator(); sm.addAction("Ver estadísticas")

        am=mb.addMenu("Ayuda")
        am.addAction(a(f"En memoria de Polechita — 10 de Mayo 2026",lambda: QMessageBox.information(self,"♥ Polechita",f"<b>{APP_NAME} v{APP_VERSION}</b><br><i>{APP_BRAND}</i><br><br><b>Proyecto hecho en memoria de Polechita</b><br><i>10 de Mayo 2026</i><br><br>Con amor y dedicación. 🐾")))
        am.addSeparator(); am.addAction(a(f"Acerca de {APP_NAME}",lambda: QMessageBox.about(self,APP_NAME,f"<b>{APP_NAME} v{APP_VERSION}</b><br><i>{APP_BRAND}</i><br><br>{APP_MEMORY}<br><br>Radio Automation Suite")))

    # ══════════════════════════════════════
    #  TEMA
    # ══════════════════════════════════════
    def apply_theme(self,theme):
        self._theme=theme; app=QApplication.instance()
        app.setStyleSheet(DARK if theme=="dark" else LIGHT)
        pal=app.palette()
        if theme=="dark":
            pal.setColor(QPalette.ColorRole.Window,QColor("#111"))
            pal.setColor(QPalette.ColorRole.WindowText,QColor("#ddd"))
            pal.setColor(QPalette.ColorRole.Base,QColor("#0a0a0a"))
            pal.setColor(QPalette.ColorRole.AlternateBase,QColor("#141414"))
            pal.setColor(QPalette.ColorRole.Text,QColor("#ccc"))
            pal.setColor(QPalette.ColorRole.Button,QColor("#1a1a1a"))
            pal.setColor(QPalette.ColorRole.ButtonText,QColor("#bbb"))
            self.btn_theme.setText("☀  Tema claro")
            if hasattr(self,'act_dark'): self.act_dark.setChecked(True); self.act_light.setChecked(False)
            hdr="#080808"; bar="#080808"; clk="#ffffff"; ti="#ffffff"
        else:
            pal.setColor(QPalette.ColorRole.Window,QColor("#f0f0f0"))
            pal.setColor(QPalette.ColorRole.WindowText,QColor("#1a1a1a"))
            pal.setColor(QPalette.ColorRole.Base,QColor("#fff"))
            pal.setColor(QPalette.ColorRole.AlternateBase,QColor("#fafafa"))
            pal.setColor(QPalette.ColorRole.Text,QColor("#222"))
            pal.setColor(QPalette.ColorRole.Button,QColor("#fff"))
            pal.setColor(QPalette.ColorRole.ButtonText,QColor("#333"))
            self.btn_theme.setText("🌙  Tema oscuro")
            if hasattr(self,'act_light'): self.act_light.setChecked(True); self.act_dark.setChecked(False)
            hdr="#ffffff"; bar="#f0f0f0"; clk="#111111"; ti="#111111"
        app.setPalette(pal)
        bd="1px solid #ddd" if theme=="light" else "1px solid #1a1a1a"
        for name,bg in [("HDR",hdr),("TINF",bar),("MICBAR",bar),("TRANS",hdr if theme=="dark" else "#fff"),("EQBOX","#0a0a0a")]:
            for ch in self.findChildren(QWidget,name):
                ch.setStyleSheet(f"#{name}{{background:{bg};border-bottom:{bd};}}")
        if hasattr(self,'lbl_clk'): self.lbl_clk.setStyleSheet(f"color:{clk};font-family:'Courier New';font-size:20px;font-weight:700;")
        if hasattr(self,'lbl_title'): self.lbl_title.setStyleSheet(f"color:{ti};font-size:13px;font-weight:700;")
        if hasattr(self,'lbl_rem'): self.lbl_rem.setStyleSheet(f"color:{clk};font-family:'Courier New';font-size:13px;font-weight:700;")
        if hasattr(self,'eq'): self.eq.set_dark(theme=="dark")

    def _toggle_theme(self): self.apply_theme("light" if self._theme=="dark" else "dark")

    # ══════════════════════════════════════
    #  SIGNALS
    # ══════════════════════════════════════
    def _signals(self):
        self.audio.songFinished.connect(self._song_done)
        self.audio.posUpdate.connect(self._pos_upd)
        self.stream.statusChanged.connect(self._on_stream_status)
        self.stream.listenersUpdate.connect(self._on_listeners)

    # ══════════════════════════════════════
    #  PLAYBACK
    # ══════════════════════════════════════
    def _toggle_play(self):
        if self.playing:
            self.audio.pause(); self.playing=False; self.btn_play.setText("▶")
            self.eq.set_playing(False); self.lbl_eqst.setText("PAUSADO")
            self.st_play.setText("⬤ Pausado")
        else:
            if self.ci<0 and self.playlist: self._play_idx(0); return
            self.audio.pause(); self.playing=True; self.btn_play.setText("⏸")
            self.eq.set_playing(True); self._playing_st()

    def _stop(self):
        self.audio.stop(); self.playing=False; self.btn_play.setText("▶")
        self.prog.setValue(0); self.lbl_pos.setText("00:00 / 00:00")
        self.lbl_rem.setText("--:--"); self.eq.set_playing(False)
        self.lbl_eqst.setText("SILENCIO"); self.lbl_eqst.setStyleSheet("color:#333;font-size:10px;font-weight:700;")
        self.st_play.setText("⬤ Detenido"); self.st_play.setStyleSheet("color:#444;")

    def _play_idx(self,idx):
        if idx<0 or idx>=len(self.playlist): return
        it=self.playlist[idx]
        path=it.url if it.typ==PLItem.R else it.path
        if not path: return
        if it.typ!=PLItem.R and not os.path.exists(path):
            QMessageBox.warning(self,"No encontrado",path); return
        self.ci=idx; self.audio.play(path); self.playing=True; self.btn_play.setText("⏸")
        if it.typ==PLItem.R: self._stream_idx=idx; it._sdur=0
        self.lbl_title.setText(it.title); self.lbl_artist.setText(it.artist or "—")
        self.eq.set_playing(True); self.lbl_eqst.setText("EN VIVO")
        self.lbl_eqst.setStyleSheet("color:#ff6600;font-size:10px;font-weight:700;")
        self._playing_st(); self._upd_next(); self._hi_row(idx)

    def _playing_st(self):
        self.st_play.setText("⬤ Reproduciendo"); self.st_play.setStyleSheet("color:#00cc66;")

    def _play_prev(self):
        if self.ci>0: self._play_idx(self.ci-1)

    def _skip(self):
        if self._rnd and self.playlist: self._play_idx(random.randint(0,len(self.playlist)-1)); return
        ni=self.ci+1
        if ni<len(self.playlist): self._play_idx(ni)
        elif self._repl and self.playlist: self._play_idx(0)
        else: self._stop()

    def _song_done(self):
        if self._stopafer: self._stop(); self.btn_sa.setChecked(False); self._stopafer=False; return
        if self._rep: self._play_idx(self.ci); return
        self._skip()

    def _pos_upd(self,pos,dur):
        if dur>0:
            self.prog.setValue(int(pos/dur*1000))
            self.lbl_pos.setText(f"{int(pos//60):02d}:{int(pos%60):02d} / {int(dur//60):02d}:{int(dur%60):02d}")
            rem=dur-pos; self.lbl_rem.setText(f"{int(rem//60):02d}:{int(rem%60):02d}")

    def _update_sdur(self):
        if self.playing and self._stream_idx>=0 and self._stream_idx<len(self.playlist):
            it=self.playlist[self._stream_idx]
            if it.typ==PLItem.R:
                it._sdur+=1
                cell=self.pltbl.item(self._stream_idx,4)
                if cell: cell.setText(it.dur_str())

    # ══════════════════════════════════════
    #  HORA
    # ══════════════════════════════════════
    def _sel_tf(self):
        f=QFileDialog.getExistingDirectory(self,"Carpeta de locuciones de hora")
        if f: self._time_folder=f; self.edit_tf.setText(f)

    def _play_hour(self):
        now=datetime.now(); hour=now.hour
        folder=self.edit_tf.text().strip() if hasattr(self,"edit_tf") else self._time_folder
        if not folder or not os.path.exists(folder):
            QMessageBox.information(self,"Carpeta de hora","Configura la carpeta en la pestaña 'Eventos'.\nArchivos: 00.mp3, 01.mp3 ... 23.mp3"); return
        for name in [f"{hour:02d}.mp3",f"{hour}.mp3",f"hora_{hour:02d}.mp3",f"{hour:02d}.wav",f"{hour:02d}.ogg"]:
            full=os.path.join(folder,name)
            if os.path.exists(full):
                self.audio.play(full); self.lbl_title.setText(f"🕐 Hora {hour:02d}:00"); self.lbl_artist.setText("Locución automática")
                self.eq.set_playing(True); return
        QMessageBox.warning(self,"No encontrado",f"Sin archivo para {hour:02d}:00 en:\n{folder}")

    # ══════════════════════════════════════
    #  PLAYLIST
    # ══════════════════════════════════════
    def _add_files(self):
        files,_=QFileDialog.getOpenFileNames(self,"Añadir pistas","","Audio (*.mp3 *.wav *.ogg *.flac *.aac *.m4a *.wma)")
        for f in files: self.playlist.append(PLItem(f))
        self._refresh_pl()

    def _add_folder(self):
        f=QFileDialog.getExistingDirectory(self,"Seleccionar carpeta")
        if f: self._add_folder_path(f)

    def _add_folder_path(self,folder):
        exts={".mp3",".wav",".ogg",".flac",".aac",".m4a",".wma"}
        for fn in sorted(os.listdir(folder)):
            if os.path.splitext(fn)[1].lower() in exts:
                self.playlist.append(PLItem(os.path.join(folder,fn)))
        self._refresh_pl()

    def _add_radio(self):
        dlg=RadioDlg(self)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            it=dlg.get_item()
            if it: self.playlist.append(it); self._refresh_pl()

    def _files_dropped(self,paths):
        for p in paths: self.playlist.append(PLItem(p))
        self._refresh_pl()

    def _rem_sel(self):
        rows=sorted({i.row() for i in self.pltbl.selectedIndexes()},reverse=True)
        for r in rows: self.playlist.pop(r)
        self._refresh_pl()

    def _mv_up(self):
        for r in sorted({i.row() for i in self.pltbl.selectedIndexes()}):
            if r>0: self.playlist[r],self.playlist[r-1]=self.playlist[r-1],self.playlist[r]
        self._refresh_pl()

    def _mv_dn(self):
        for r in sorted({i.row() for i in self.pltbl.selectedIndexes()},reverse=True):
            if r<len(self.playlist)-1: self.playlist[r],self.playlist[r+1]=self.playlist[r+1],self.playlist[r]
        self._refresh_pl()

    def _clr_pl(self):
        if QMessageBox.question(self,"Limpiar","¿Limpiar toda la playlist?")==QMessageBox.StandardButton.Yes:
            self.playlist.clear(); self.ci=-1; self._stream_idx=-1; self._refresh_pl()

    def _shuffle(self): random.shuffle(self.playlist); self._refresh_pl()

    def _refresh_pl(self):
        t=self.pltbl; t.setRowCount(len(self.playlist))
        TC={PLItem.M:"#44aaaa",PLItem.J:"#ff8833",PLItem.S:"#aa44ff",PLItem.R:"#44aaff",PLItem.P:"#888"}
        for i,it in enumerate(self.playlist):
            t.setRowHeight(i,24); t.setItem(i,0,QTableWidgetItem(str(i+1)))
            t.setItem(i,1,QTableWidgetItem(it.title)); t.setItem(i,2,QTableWidgetItem(it.artist))
            ti=QTableWidgetItem(it.typ); ti.setForeground(QColor(TC.get(it.typ,"#888"))); t.setItem(i,3,ti)
            t.setItem(i,4,QTableWidgetItem(it.dur_str()))
        td=sum(p.dur for p in self.playlist if p.typ!=PLItem.R)
        h,r=divmod(int(td),3600); m,s=divmod(r,60)
        self.lbl_tot.setText(f"{len(self.playlist)} pistas — {h:02d}:{m:02d}:{s:02d}" if h else f"{len(self.playlist)} pistas — {m:02d}:{s:02d}")
        self.st_pl.setText(f"Playlist: {len(self.playlist)} pistas"); self._upd_next()

    def _hi_row(self,idx):
        for r in range(self.pltbl.rowCount()):
            for c in range(self.pltbl.columnCount()):
                it=self.pltbl.item(r,c)
                if it:
                    it.setBackground(QColor("#ff660022" if r==idx else "transparent"))
                    it.setForeground(QColor("#ff9944" if r==idx else "#cccccc"))

    def _upd_next(self):
        ni=self.ci+1
        if ni<len(self.playlist):
            self.lbl_next.setText(self.playlist[ni].title)
            self.lbl_nextd.setText(f"{self.playlist[ni].artist} — {self.playlist[ni].dur_str()}")
        else: self.lbl_next.setText("— Fin —"); self.lbl_nextd.setText("")

    # ══════════════════════════════════════
    #  CUÑAS
    # ══════════════════════════════════════
    def _play_jingle(self,idx):
        p=self.jingles[idx]
        if p and os.path.exists(p): self.audio.play(p)
        else: QMessageBox.information(self,f"Cuña {idx+1}","Sin archivo. Clic derecho para asignar.")

    def _assign_jingle(self,idx):
        p,_=QFileDialog.getOpenFileName(self,f"Cuña {idx+1}","","Audio (*.mp3 *.wav *.ogg *.flac)")
        if p:
            self.jingles[idx]=p; n=os.path.splitext(os.path.basename(p))[0][:10]
            self.jbns[idx].setText(f"F{idx+1}\n{n}"); self.jnames[idx]=n
            if hasattr(self,'cacts'): self.cacts[idx].setText(f"{idx+1}. {n}")

    def _edit_cunas(self):
        dlg=QDialog(self); dlg.setWindowTitle("Editar Cuñas"); dlg.setFixedSize(520,400)
        lay=QVBoxLayout(dlg); g=QGridLayout(); g.setSpacing(6)
        edits=[]
        for i in range(9):
            l=QLabel(f"Cuña {i+1}:"); l.setStyleSheet("color:#888;")
            ne=QLineEdit(self.jnames[i]); ne.setFixedWidth(120)
            pe=QLineEdit(self.jingles[i]); pe.setPlaceholderText("(sin archivo)")
            btn=QPushButton("..."); btn.setFixedWidth(28)
            btn.clicked.connect(lambda _,p=pe: p.setText(QFileDialog.getOpenFileName(dlg,"","","Audio (*.mp3 *.wav *.ogg)")[0]))
            g.addWidget(l,i,0); g.addWidget(ne,i,1); g.addWidget(pe,i,2); g.addWidget(btn,i,3); edits.append((ne,pe))
        lay.addLayout(g)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject); lay.addWidget(bb)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            for i,(ne,pe) in enumerate(edits):
                self.jnames[i]=ne.text(); self.jingles[i]=pe.text()
                self.jbns[i].setText(f"F{i+1}\n{self.jnames[i]}")
                if hasattr(self,'cacts'): self.cacts[i].setText(f"{i+1}. {self.jnames[i]}")

    # ══════════════════════════════════════
    #  SCHEDULER
    # ══════════════════════════════════════
    def _add_event(self):
        dlg=QDialog(self); dlg.setWindowTitle("Planificar evento"); dlg.setFixedSize(440,400)
        lay=QVBoxLayout(dlg); lay.setSpacing(8)
        g=QGridLayout(); g.setSpacing(8)
        g.addWidget(QLabel("Hora:"),0,0); te=QTimeEdit(); te.setDisplayFormat("HH:mm"); g.addWidget(te,0,1)
        g.addWidget(QLabel("Tipo:"),1,0); tc=QComboBox(); tc.addItems(SchEvent.TYPES); g.addWidget(tc,1,1)
        g.addWidget(QLabel("Descripción:"),2,0); ae=QLineEdit("Cuña horaria"); g.addWidget(ae,2,1)
        g.addWidget(QLabel("Fichero:"),3,0)
        fr=QHBoxLayout(); fe=QLineEdit()
        fb=QPushButton("..."); fb.setFixedWidth(28)
        fb.clicked.connect(lambda: fe.setText(QFileDialog.getOpenFileName(dlg,"","","Audio (*.mp3 *.wav *.ogg *.flac)")[0]))
        fr.addWidget(fe); fr.addWidget(fb); g.addLayout(fr,3,1); lay.addLayout(g)
        lay.addWidget(QLabel("Días activos:"))
        dr=QHBoxLayout(); dcs=[QCheckBox(d) for d in DAYS_ES]
        for d in dcs: d.setChecked(True); dr.addWidget(d)
        lay.addLayout(dr)
        opt=QHBoxLayout()
        rc=QCheckBox("Repetir"); rc.setChecked(True)
        ic=QCheckBox("Interrumpir canción actual"); ic.setChecked(True)
        opt.addWidget(rc); opt.addWidget(ic); lay.addLayout(opt)
        bb=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        bb.button(QDialogButtonBox.StandardButton.Ok).setText("Aceptar")
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject); lay.addWidget(bb)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            ev=SchEvent(te.time().toString("HH:mm"),ae.text(),fe.text(),rc.isChecked(),[d.isChecked() for d in dcs],tc.currentText(),ic.isChecked())
            self.sched.append(ev); self._refresh_sched()

    def _del_event(self):
        rows=sorted({i.row() for i in self.sched_tbl.selectedIndexes()},reverse=True)
        for r in rows:
            if r<len(self.sched): self.sched.pop(r)
        self._refresh_sched()

    def _clr_events(self):
        if QMessageBox.question(self,"Limpiar","¿Eliminar todos?")==QMessageBox.StandardButton.Yes:
            self.sched.clear(); self._refresh_sched()

    def _refresh_sched(self):
        t=self.sched_tbl; t.setRowCount(len(self.sched))
        TC={"Cuña":"#ff8833","Spot":"#aa44ff","Silencio":"#888","Archivo":"#44cc66","Locución hora":"#ffcc00"}
        for i,ev in enumerate(self.sched):
            t.setRowHeight(i,24); t.setItem(i,0,QTableWidgetItem(ev.ts))
            ti=QTableWidgetItem(ev.etype); ti.setForeground(QColor(TC.get(ev.etype,"#888"))); t.setItem(i,1,ti)
            t.setItem(i,2,QTableWidgetItem(os.path.basename(ev.fp) if ev.fp else ev.action))
            t.setItem(i,3,QTableWidgetItem("--:--"))
            t.setItem(i,4,QTableWidgetItem("".join(d for d,v in zip(DAYS_ES,ev.days) if v)))

    def _check_sched(self):
        now=datetime.now().strftime("%H:%M")
        for ev in self.sched:
            if ev.ts==now and not ev.done and ev.runs_today():
                ev.done=True
                if ev.etype=="Silencio": self._stop()
                elif ev.etype=="Locución hora": self._play_hour()
                elif ev.fp and os.path.exists(ev.fp):
                    if ev.interrupt: self.audio.stop()
                    self.audio.play(ev.fp); self.lbl_title.setText(f"[{ev.etype}] {ev.action}")
                self._refresh_sched()

    # ══════════════════════════════════════
    #  STREAMING
    # ══════════════════════════════════════
    def _on_stype(self,idx):
        ls=["Montaje:","Contraseña fuente:","Station ID (ej: 1):"]; phs=["/stream","","1"]
        if hasattr(self,'lbl_mount'): self.lbl_mount.setText(ls[idx]); self.emount.setPlaceholderText(phs[idx])

    def _show_stream_dlg(self):
        dlg=StreamDlg(self,self._scfg)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            self._scfg=dlg.get_cfg(); self.stream.configure(self._scfg)
            if hasattr(self,'lbl_rname'): self.lbl_rname.setText(self._scfg.get("radio_name","Mi Radio Online"))
            self._sync_stream_panel(); self._save_cfg()

    def _sync_stream_panel(self):
        """Sincroniza el panel derecho de streaming con la config guardada"""
        if not hasattr(self,'ehost'): return
        c=self._scfg
        self.ehost.setText(c.get("host","")); self.eport.setText(c.get("port","8000"))
        self.epass.setText(c.get("password","")); self.emount.setText(c.get("mountpoint","1"))
        t=c.get("type","icecast2")
        if "v1" in t: self.ctype.setCurrentIndex(1)
        elif "v2" in t: self.ctype.setCurrentIndex(2)
        else: self.ctype.setCurrentIndex(0)

    def _get_stream_cfg_from_panel(self):
        """Lee config del panel derecho"""
        if not hasattr(self,'ehost'): return self._scfg
        stype=["icecast2","shoutcast_v1","shoutcast_v2"][self.ctype.currentIndex()]
        br=int(self.cbr.currentText().replace("k",""))
        return {"host":self.ehost.text().strip(),"port":self.eport.text().strip(),
                "password":self.epass.text(),"mountpoint":self.emount.text().strip(),
                "type":stype,"bitrate":br,"format":self.cfmt.currentText().lower(),
                "reconnect":True}

    def _toggle_stream(self):
        if self.stream.is_connected():
            self.stream.disconnect()
        else:
            cfg=self._get_stream_cfg_from_panel()
            if not cfg.get("host"): self._show_stream_dlg(); cfg=self._get_stream_cfg_from_panel()
            if not cfg.get("host"): return
            self._scfg=cfg; self.stream.configure(cfg)
            self.btn_stream.setEnabled(False); self.btn_stream.setText("⬤  Conectando...")
            self.stream.connect_bg()

    def _toggle_stream_right(self):
        """Botón conectar del panel derecho"""
        self._toggle_stream()

    def _test_conn(self):
        if not hasattr(self,'ehost'): return
        try:
            s=socket.socket(); s.settimeout(5)
            r=s.connect_ex((self.ehost.text().strip(),int(self.eport.text())))
            s.close()
            if r==0: self.lbl_stest.setText("✅ Servidor accesible"); self.lbl_stest.setStyleSheet("color:#00cc66;")
            else: self.lbl_stest.setText("❌ Sin respuesta en ese puerto"); self.lbl_stest.setStyleSheet("color:#cc3333;")
        except Exception as ex: self.lbl_stest.setText(f"❌ {ex}"); self.lbl_stest.setStyleSheet("color:#cc3333;")

    def _on_stream_status(self,connected,msg):
        self.btn_stream.setEnabled(True)
        if connected:
            self._upd_stream_btn(True)
            self.lbl_sdot.setStyleSheet("color:#00cc66;font-size:12px;")
            self.lbl_smin.setText(msg); self.lbl_smin.setStyleSheet("color:#00cc66;font-size:10px;")
            self.st_stream.setText("⬤ Streaming activo"); self.st_stream.setStyleSheet("color:#00cc66;")
            if hasattr(self,'btn_conn'): self.btn_conn.setText("Desconectar streaming"); self.btn_conn.setStyleSheet("QPushButton{background:#8b0000;color:#fff;border:none;border-radius:4px;padding:8px;font-weight:700;}QPushButton:hover{background:#aa0000;}")
            if hasattr(self,'lbl_stest'): self.lbl_stest.setText(msg); self.lbl_stest.setStyleSheet("color:#00cc66;font-size:10px;")
        else:
            self._upd_stream_btn(False)
            self.lbl_sdot.setStyleSheet("color:#220000;font-size:12px;")
            self.lbl_smin.setText("Sin stream"); self.lbl_smin.setStyleSheet("color:#444;font-size:10px;")
            self.st_stream.setText("⬤ Sin conexión"); self.st_stream.setStyleSheet("color:#444;")
            if hasattr(self,'btn_conn'): self.btn_conn.setText("Conectar streaming"); self.btn_conn.setStyleSheet("QPushButton{background:#ff6600;color:#fff;border:none;border-radius:4px;padding:8px;font-weight:700;}QPushButton:hover{background:#ff7722;}")
            if msg and "❌" in msg:
                QMessageBox.warning(self,"Error de Streaming",msg)
            if hasattr(self,'lbl_stest'): self.lbl_stest.setText(msg or ""); self.lbl_stest.setStyleSheet("color:#cc4444;font-size:10px;")

    def _on_listeners(self,count):
        if count>self._peak: self._peak=count
        if hasattr(self,'lbl_list'): self.lbl_list.setText(str(count))
        if hasattr(self,'lbl_peak'): self.lbl_peak.setText(f"Pico: {self._peak}")
        self.st_list.setText(f"Oyentes: {count}")

    # ══════════════════════════════════════
    #  FILES
    # ══════════════════════════════════════
    def _new_pl(self): self._clr_pl()

    def _open_pl(self):
        p,_=QFileDialog.getOpenFileName(self,"Abrir playlist","","PoleCaster Playlist (*.pcp)")
        if not p: return
        try:
            with open(p,"r",encoding="utf-8") as f: data=json.load(f)
            self.playlist=[PLItem.from_dict(d) for d in data.get("playlist",[])]
            self.sched=[SchEvent.from_dict(d) for d in data.get("sched",[])]
            self._refresh_pl(); self._refresh_sched()
        except Exception as ex: QMessageBox.critical(self,"Error",str(ex))

    def _save_pl(self):
        p,_=QFileDialog.getSaveFileName(self,"Guardar playlist","","PoleCaster Playlist (*.pcp)")
        if not p: return
        try:
            with open(p,"w",encoding="utf-8") as f:
                json.dump({"playlist":[i.to_dict() for i in self.playlist],"sched":[e.to_dict() for e in self.sched]},f,indent=2)
        except Exception as ex: QMessageBox.critical(self,"Error",str(ex))

    # ══════════════════════════════════════
    #  CONFIG
    # ══════════════════════════════════════
    def _load_cfg(self):
        if not os.path.exists(CONFIG_FILE): return
        try:
            with open(CONFIG_FILE) as f: cfg=json.load(f)
            self._scfg=cfg.get("scfg",{}); self.stream.configure(self._scfg)
            if self._scfg.get("radio_name"): self.lbl_rname.setText(self._scfg["radio_name"])
            self.jingles=cfg.get("jingles",[""]*9); self.jnames=cfg.get("jnames",["Cuña "+str(i+1) for i in range(9)])
            self._time_folder=cfg.get("tf","")
            if hasattr(self,"edit_tf") and self._time_folder: self.edit_tf.setText(self._time_folder)
            for i,p in enumerate(self.jingles):
                if p: self.jbns[i].setText(f"F{i+1}\n{self.jnames[i]}")
            if hasattr(self,'cacts'):
                for i,a in enumerate(self.cacts): a.setText(f"{i+1}. {self.jnames[i]}")
            self._sync_stream_panel()
            self.apply_theme(cfg.get("theme","dark"))
            for d in cfg.get("sched",[]): self.sched.append(SchEvent.from_dict(d))
            self._refresh_sched()
        except: pass

    def _save_cfg(self):
        tf=self._time_folder
        if hasattr(self,"edit_tf"): tf=self.edit_tf.text().strip() or tf
        cfg={"scfg":self._scfg,"jingles":self.jingles,"jnames":self.jnames,"tf":tf,
             "theme":self._theme,"sched":[e.to_dict() for e in self.sched]}
        try:
            with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,indent=2)
        except: pass

    # ══════════════════════════════════════
    #  CLOCK
    # ══════════════════════════════════════
    def _tick(self):
        now=datetime.now()
        self.lbl_clk.setText(now.strftime("%H:%M:%S"))
        self.lbl_date.setText(now.strftime("%A %d de %B de %Y"))
        if now.hour==0 and now.minute==0 and now.second<2:
            for ev in self.sched: ev.done=False
        # Countdown
        ns=now.strftime("%H:%M"); pend=[(ev.ts,ev) for ev in self.sched if not ev.done and ev.ts>ns and ev.runs_today()]
        pend.sort(key=lambda x:x[0])
        if pend:
            ts,ev=pend[0]; h,m=map(int,ts.split(":")); then=now.replace(hour=h,minute=m,second=0)
            mins=int((then-now).total_seconds()//60)
            self.lbl_next_ev.setText(f"[{ev.etype}] {ev.action} — {mins} min")
            self.lbl_cd.setText(f"En {mins} min")
        else: self.lbl_next_ev.setText("Sin eventos pendientes"); self.lbl_cd.setText("")

    def closeEvent(self,event):
        self._save_cfg(); self.audio.stop()
        if self.stream.is_connected(): self.stream.disconnect()
        event.accept()

# ══════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════
def main():
    app=QApplication(sys.argv)
    app.setApplicationName(APP_NAME); app.setApplicationVersion(APP_VERSION)
    if os.path.exists(LOGO_PATH): app.setWindowIcon(QIcon(LOGO_PATH))
    win=PoleCaster(); win.show(); sys.exit(app.exec())

if __name__=="__main__":
    main()
