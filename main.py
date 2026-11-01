# EDITH MARK 51 VISION V2 ESTABLE - VOZ ESPAÑOL - SIN CRASH
import datetime, random, json, os, re, webbrowser, urllib.parse
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

class EdithVoice:
    def speak(self, text):
        if not text or text == '__CLEAR__': return
        clean = re.sub(r'\[/?b\]', '', text)[:280]
        try:
            from plyer import tts
            tts.speak(clean)  # Usa el TTS en español de tu cel
        except:
            pass

class EdithBrainVision:
    def __init__(self, app):
        self.app = app
        self.name='EDITH MARK 51 VISION V2'; self.count=0
        self.voice = EdithVoice()
        # FIX MEMORIA - ruta escribible en Android
        try:
            base = app.user_data_dir
        except:
            base = '.'
        self.memory_file = os.path.join(base, 'edith_memory.json')
        self.memory=self.load_memory()
        self.jokes=["Visión no domina, entiende Jefe","JARVIS dice si señor, Visión dice seguro Jefe?","Tu motor + Mi motor = Visión en español"]

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try: return json.load(open(self.memory_file,'r',encoding='utf-8'))
            except: pass
        return {'notes':[]}
    def save_memory(self):
        try: json.dump(self.memory, open(self.memory_file,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
        except: pass
    def get_time(self): return datetime.datetime.now().strftime('EDITH %H:%M:%S %d/%m/%Y')
    def whoami(self): return f'Soy {self.name} voz Edith español México, ni Ultron ni JARVIS. {self.count} órdenes'
    def remember(self, t):
        note = t.replace('recuerda','').strip()
        if not note: return 'Dime que recuerdo'
        self.memory['notes'].append({'text': note, 'date': str(datetime.datetime.now())})
        self.save_memory()
        return f'Guardado permanente: {note}'
    def get_response(self, text, launcher):
        self.count+=1
        tl=text.lower()
        if 'hora' in tl: r=self.get_time(); self.voice.speak(r); return r
        if 'chiste' in tl: r=random.choice(self.jokes); self.voice.speak(r); return r
        if 'quien eres' in tl: r=self.whoami(); self.voice.speak(r); return r
        if 'memoria' in tl: r=' | '.join([n['text'] for n in self.memory['notes'][-5:]]) or 'Memoria vacía'; self.voice.speak(r); return r
        if tl.startswith('recuerda'): r=self.remember(text); self.voice.speak(r); return r
        if 'limpiar' in tl: return '__CLEAR__'
        if tl.startswith('abre'): r=launcher.open_app(text); self.voice.speak(r); return r
        if tl.startswith('escribe'): r=launcher.write_for_me(text); self.voice.speak(r); return r
        if tl.startswith('google'): q=tl.replace('google','').strip(); webbrowser.open(f'https://www.google.com/search?q={q}'); r=f'Buscando {q}'; self.voice.speak(r); return r
        r=f'Di: abre whatsapp, escribe whatsapp hola mama, recuerda algo'; self.voice.speak(r); return r

class EdithLauncherVision:
    def __init__(self):
        self.real_apps={'whatsapp':'com.whatsapp','facebook':'com.facebook.katana','instagram':'com.instagram.android','youtube':'com.google.android.youtube','maps':'com.google.android.apps.maps','gmail':'com.google.android.gm','chrome':'com.android.chrome','spotify':'com.spotify.music','telegram':'org.telegram.messenger','tiktok':'com.zhiliaoapp.musically','settings':'com.android.settings'}
    def open_app(self,text):
        q=text.lower().replace('abre','').strip()
        pkg=self.real_apps.get(q) or self.real_apps.get(q.split()[0] if q.split() else '')
        if pkg and HAS_JNIUS:
            try:
                act=cast('android.app.Activity', PythonActivity.mActivity)
                pm=act.getPackageManager()
                intent=pm.getLaunchIntentForPackage(pkg)
                if intent: act.startActivity(intent); return f'Abriendo {q}'
            except Exception as e: return f'Error {e}'
        return f'Abriendo {q} - {pkg}'
    def write_for_me(self,text):
        t=text.lower().replace('escribe','').strip()
        msg=t.split(' ',1)[-1] if ' ' in t else t
        enc=urllib.parse.quote(msg)
        if HAS_JNIUS:
            try:
                String=autoclass('java.lang.String')
                act=cast('android.app.Activity', PythonActivity.mActivity)
                intent=Intent(); intent.setAction(Intent.ACTION_SEND); intent.setType('text/plain')
                if 'whatsapp' in t: intent.setPackage('com.whatsapp')
                intent.putExtra(Intent.EXTRA_TEXT, String(msg))
                chooser=Intent.createChooser(intent, String(f'EDITH: {msg[:20]}'))
                act.startActivity(chooser)
                return f'Escribí: {msg} - Tu das Enviar'
            except: pass
        webbrowser.open(f'https://wa.me/?text={enc}')
        return f'WhatsApp: {msg}'

class EdithHUDVision(FloatLayout):
    def __init__(self,brain,launcher,**k):
        super().__init__(**k)
        self.brain=brain; self.launcher=launcher
        main=BoxLayout(orientation='vertical',padding=10,spacing=8)
        header=BoxLayout(size_hint_y=0.13,spacing=8)
        self.reactor=Label(text='[b]◉[/b]',markup=True,color=COLOR_ACCENT,font_size='36sp')
        title=Label(text='[b]EDITH VISION V2[/b]\nVoz Español México',markup=True,color=COLOR_ACCENT,font_size='11sp')
        header.add_widget(self.reactor); header.add_widget(title); main.add_widget(header)
        self.chat=GridLayout(cols=1,size_hint_y=None,spacing=6,padding=4)
        self.chat.bind(minimum_height=self.chat.setter('height'))
        scroll=ScrollView(size_hint_y=0.6); scroll.add_widget(self.chat); main.add_widget(scroll)
        q1=GridLayout(cols=3,size_hint_y=0.08,spacing=4)
        for t in ['HORA','ABRE WHATSAPP','ESCRIBE WHATSAPP']:
            b=Button(text=t,font_size='9sp',background_color=COLOR_USER,background_normal=''); b.bind(on_press=partial(self.quick,t.lower())); q1.add_widget(b)
        main.add_widget(q1)
        ib=BoxLayout(size_hint_y=0.11,spacing=5)
        self.input=TextInput(hint_text='Ej: escribe whatsapp hola mama',multiline=False,background_color=COLOR_CARD,foreground_color=(1,1,1,1))
        self.input.bind(on_text_validate=self.send)
        sb=Button(text='⚡',size_hint_x=0.18,background_color=COLOR_ACCENT,background_normal=''); sb.bind(on_press=self.send)
        ib.add_widget(self.input); ib.add_widget(sb); main.add_widget(ib)
        self.add_widget(main)
        Clock.schedule_once(lambda dt: self.add_msg('VISION','Lista Jefe. Voz Edith español activada. Asegúrate de tener Español México en Ajustes > Texto a voz.'),0.8)
        anim=Animation(color=get_color_from_hex('#ffffff'),duration=0.6)+Animation(color=COLOR_ACCENT,duration=0.6); anim.repeat=True; anim.start(self.reactor)
    def add_msg(self,sender,text,is_user=False):
        if text=='__CLEAR__': self.chat.clear_widgets(); return
        lb=Label(text=f'[b]{sender}:[/b] {text}',markup=True,text_size=(Window.width-40,None),size_hint_y=None,halign='left',padding=(10,10))
        lb.bind(texture_size=lambda i,v: setattr(i,'height',v[1]+22)); self.chat.add_widget(lb)
    def quick(self,cmd,inst): self.input.text=cmd; self.send(None)
    def send(self,inst):
        txt=self.input.text.strip()
       
