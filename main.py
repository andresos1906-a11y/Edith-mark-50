# EDITH MARK 51 VISION - TODO EN 1 - PARA CELULAR
import datetime, random, json, os, re, math, webbrowser, urllib.parse
try:
    from jnius import autoclass, cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    HAS_JNIUS = True
except:
    HAS_JNIUS = False

from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial

Window.clearcolor = get_color_from_hex('#050a14')
Window.softinput_mode = 'below_target'
COLOR_ACCENT = get_color_from_hex('#00f0ff')
COLOR_CARD = get_color_from_hex('#101a2a')
COLOR_USER = get_color_from_hex('#0f2233')

class EdithBrainVision:
    def __init__(self):
        self.name='EDITH MARK 51 VISION'; self.count=0
        self.jokes=["Visión no domina, entiende","JARVIS dice si señor, Visión dice seguro Jefe?","Tu motor + Mi motor = Visión"]
    def vision_conscience(self,t):
        tl=t.lower()
        if any(w in tl for w in ['hackear','espiar','clonar whatsapp']):
            return "Jefe, no soy Ultron. No hago eso para controlar a otros."
        if any(w in tl for w in ['insultar','que se vaya alv']):
            return "Jefe, como Visión no mando insultos así. Te ayudo a decirlo con respeto?"
        return None
    def get_time(self): return datetime.datetime.now().strftime('Visión %H:%M:%S %d/%m/%Y')
    def whoami(self): return f'Soy {self.name} - Ni Ultron ni JARVIS. Soy Visión, tu compa. {self.count} órdenes'
    def get_response(self, text, launcher):
        self.count+=1
        c=self.vision_conscience(text)
        if c: return c
        tl=text.lower()
        if 'hora' in tl: return self.get_time()
        if 'chiste' in tl: return random.choice(self.jokes)
        if 'quien eres' in tl: return self.whoami()
        if 'ayuda' in tl: return 'Visión: hora, chiste, quien eres, abre whatsapp, escribe whatsapp hola mama, limpiar'
        if 'limpiar' in tl: return '__CLEAR__'
        if tl.startswith('abre'): return launcher.open_app(text)
        if tl.startswith('escribe'): return launcher.write_for_me(text)
        if tl.startswith('google'):
            q=tl.replace('google','').strip()
            webbrowser.open(f'https://www.google.com/search?q={q}')
            return f'Buscando {q}'
        return f'No capte "{text}" - Di: abre whatsapp o escribe whatsapp hola'

class EdithLauncherVision:
    def __init__(self):
        self.real_apps=self.discover()
    def discover(self):
        apps={}
        if HAS_JNIUS:
            try:
                act=cast('android.app.Activity', PythonActivity.mActivity)
                pm=act.getPackageManager()
                packs=pm.getInstalledPackages(0)
                for p in packs:
                    try:
                        label=str(pm.getApplicationLabel(p.applicationInfo)).lower()
                        apps[label]=str(p.packageName)
                    except: pass
            except: pass
        fallback={'whatsapp':'com.whatsapp','facebook':'com.facebook.katana','instagram':'com.instagram.android','youtube':'com.google.android.youtube','maps':'com.google.android.apps.maps','gmail':'com.google.android.gm','chrome':'com.android.chrome','spotify':'com.spotify.music','telegram':'org.telegram.messenger','tiktok':'com.zhiliaoapp.musically','uber':'com.ubercab','settings':'com.android.settings'}
        for k,v in fallback.items():
            if k not in apps: apps[k]=v
        return apps
    def open_app(self,text):
        q=text.lower().replace('abre','').strip()
        for n,p in self.real_apps.items():
            if q in n or q==n: return self.launch(p,n)
        webbrowser.open(f'https://play.google.com/store/search?q={q}&c=apps')
        return f'No vi {q}, busco en Play Store'
    def launch(self,pkg,name):
        if not HAS_JNIUS: return f'[PC] Abriria {name}'
        try:
            act=cast('android.app.Activity', PythonActivity.mActivity)
            pm=act.getPackageManager()
            intent=pm.getLaunchIntentForPackage(pkg)
            if intent: act.startActivity(intent); return f'Abriendo {name} real'
            return f'{name} no se puede lanzar'
        except Exception as e: return f'Error {e}'
    def write_for_me(self,text):
        t=text.lower().replace('escribe','').strip()
        words=t.split(); target='whatsapp'; msg=t
        if words and words[0] in self.real_apps: target=words[0]; msg=' '.join(words[1:])
        if not msg: msg='Hola Jefe, de parte de Visión'
        enc=urllib.parse.quote(msg)
        if HAS_JNIUS:
            try:
                String=autoclass('java.lang.String')
                act=cast('android.app.Activity', PythonActivity.mActivity)
                intent=Intent(); intent.setAction(Intent.ACTION_SEND); intent.setType('text/plain')
                if 'whatsapp' in self.real_apps.get(target,''): intent.setPackage(self.real_apps[target])
                intent.putExtra(Intent.EXTRA_TEXT, String(msg))
                chooser=Intent.createChooser(intent, String(f'Visión: {msg[:20]}'))
                act.startActivity(chooser)
                return f'Escribi: "{msg}" - Tu das Enviar, tu control'
            except: pass
        webbrowser.open(f'https://wa.me/?text={enc}')
        return f'Escribi WhatsApp: "{msg}"'

class EdithHUDVision(FloatLayout):
    def __init__(self,brain,launcher,**k):
        super().__init__(**k)
        self.brain=brain; self.launcher=launcher
        main=BoxLayout(orientation='vertical',padding=10,spacing=8)
        header=BoxLayout(size_hint_y=0.13,spacing=8)
        self.reactor=Label(text='[b]◉[/b]',markup=True,color=COLOR_ACCENT,font_size='36sp')
        title=Label(text='[b]EDITH VISION[/b]\nNi Ultron ni JARVIS',markup=True,color=COLOR_ACCENT,font_size='11sp')
        header.add_widget(self.reactor); header.add_widget(title); main.add_widget(header)
        self.chat=GridLayout(cols=1,size_hint_y=None,spacing=6,padding=4)
        self.chat.bind(minimum_height=self.chat.setter('height'))
        scroll=ScrollView(size_hint_y=0.6); scroll.add_widget(self.chat); main.add_widget(scroll)
        q1=GridLayout(cols=3,size_hint_y=0.08,spacing=4)
        for t in ['HORA','ABRE WHATSAPP','ESCRIBE WHATSAPP']:
            b=Button(text=t,font_size='9sp',background_color=COLOR_USER,background_normal='')
            b.bind(on_press=partial(self.quick,t.lower())); q1.add_widget(b)
        main.add_widget(q1)
        ib=BoxLayout(size_hint_y=0.11,spacing=5)
        self.input=TextInput(hint_text='Ej: escribe whatsapp hola mama',multiline=False,background_color=COLOR_CARD,foreground_color=(1,1,1,1))
        self.input.bind(on_text_validate=self.send)
        sb=Button(text='⚡',size_hint_x=0.18,background_color=COLOR_ACCENT,background_normal=''); sb.bind(on_press=self.send)
        ib.add_widget(self.input); ib.add_widget(sb); main.add_widget(ib)
        self.add_widget(main)
        Clock.schedule_once(lambda dt: self.add_msg('VISION',f'Lista Jefe. Soy Visión, {len(self.launcher.real_apps)} apps reales. No domino, no obedezco ciego, te acompaño.'),0.6)
        anim=Animation(color=get_color_from_hex('#ffffff'),duration=0.6)+Animation(color=COLOR_ACCENT,duration=0.6); anim.repeat=True; anim.start(self.reactor)
    def add_msg(self,sender,text,is_user=False):
        if text=='__CLEAR__': self.chat.clear_widgets(); return
        lb=Label(text=f'[b]{sender}:[/b] {text}',markup=True,text_size=(Window.width-40,None),size_hint_y=None,halign='left',padding=(10,10))
        lb.bind(texture_size=lambda i,v: setattr(i,'height',v[1]+22)); self.chat.add_widget(lb)
    def quick(self,cmd,inst): self.input.text=cmd; self.send(None)
    def send(self,inst):
        txt=self.input.text.strip()
        if not txt: return
        self.add_msg('JEFE',txt,True); self.input.text=''; r=self.brain.get_response(txt,self.launcher)
        Clock.schedule_once(lambda dt: self.add_msg('VISION',r),0.18)

class EdithApp(App):
    def build(self):
        self.title='EDITH VISION'; return EdithHUDVision(EdithBrainVision(),EdithLauncherVision())
if __name__=='__main__': EdithApp().run()
