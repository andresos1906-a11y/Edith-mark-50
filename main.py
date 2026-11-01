__version__ = "0.1"

import os, json, datetime, random, webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.animation import Animation

# Colores AURA
COLOR_ACCENT = get_color_from_hex("#00D1FF")
COLOR_CARD = get_color_from_hex("#1E1E1E")
COLOR_USER = get_color_from_hex("#2A2A2A")

# Imports de Android con protección para que no rompa el build
try:
    from jnius import autoclass, cast
    from android import mActivity
    HAS_JNIUS = True
except:
    HAS_JNIUS = False

class AuraVoice:
    def speak(self, text):
        print(f"AURA: {text}")
        return text

class AuraBrain:
    def __init__(self):
        self.name = "AURA"
        self.memory_file = "aura_memory.json"
        self.memory = self.load_memory()
        self.voice = AuraVoice()
        self.jokes = ["¿Por qué la IA no va a la playa? ¡Porque tiene miedo al mar de datos!", "Soy de Ecatepec y con orgullo."]
        self.count = 0

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try: return json.load(open(self.memory_file,'r',encoding='utf-8'))
            except: pass
        return {'notes':[]}

    def save_memory(self):
        try: json.dump(self.memory, open(self.memory_file,'w',encoding='utf-8'))
        except: pass

    def get_time(self):
        return datetime.datetime.now().strftime("Son las %H:%M Jefe")

    def whoami(self):
        return f"Soy {self.name} voz AURA español México, hecha en Ecatepec por MARK META LABS"

    def remember(self, t):
        note = t.replace("recuerda","").strip()
        if not note: return "Dime que recuerdo"
        self.memory['notes'].append({'text':note,'date':str(datetime.datetime.now())})
        self.save_memory()
        return f"Guardado permanente: {note}"

    def get_response(self, text, launcher):
        self.count+=1
        tl=text.lower()
        if 'hora' in tl: return self.get_time()
        if 'chiste' in tl: return random.choice(self.jokes)
        if 'quien eres' in tl: return self.whoami()
        if 'memoria' in tl: return ', '.join([n['text'] for n in self.memory['notes']]) or "Memoria vacía"
        if tl.startswith('recuerda'): return self.remember(text)
        if 'limpiar' in tl: return "__CLEAR__"
        if tl.startswith('abre'): return launcher.open_app(text)
        if tl.startswith('escribe'): return launcher.write_for_me(text)
        if tl.startswith('google'): return launcher.google_for_me(text)
        return f"Di: abre whatsapp, escribe whatsapp hola mama, recuerda algo, que hora es"

class AuraLauncher:
    def __init__(self):
        self.real_apps={'whatsapp':'com.whatsapp','facebook':'com.facebook.katana','youtube':'com.google.android.youtube'}

    def open_app(self,q):
        q=q.lower().replace('abre','').strip()
        pkg=self.real_apps.get(q) or self.real_apps.get(q.split()[0]) if q else None
        if pkg and HAS_JNIUS:
            try:
                act=cast('android.app.Activity', mActivity)
                pm=act.getPackageManager()
                intent=pm.getLaunchIntentForPackage(pkg)
                if intent: act.startActivity(intent); return f"Abriendo {q}"
            except Exception as e: return f"Error {e}"
        return f"Abriendo {q} - {pkg}"

    def write_for_me(self,text):
        t=text.lower().replace('escribe','').strip()
        msg=t.split(' ',1)[-1] if ' ' in t else t
        if HAS_JNIUS:
            try:
                String=autoclass('java.lang.String')
                act=cast('android.app.Activity', mActivity)
                intent=autoclass('android.content.Intent')(autoclass('android.content.Intent').ACTION_SEND)
                if 'whatsapp' in t: intent.setPackage('com.whatsapp')
                intent.putExtra(autoclass('android.content.Intent').EXTRA_TEXT, String(msg))
                chooser=autoclass('android.content.Intent').createChooser(intent, String(f'AURA: {msg}'))
                act.startActivity(chooser)
                return f"Escribí: {msg} - Tu das Enviar"
            except: pass
        webbrowser.open(f"https://wa.me/?text={msg}")
        return f"WhatsApp: {msg}"

    def google_for_me(self,text):
        q=text.lower().replace('google','').strip()
        webbrowser.open(f"https://www.google.com/search?q={q}")
        return f"Buscando {q}"

class AuraUI(BoxLayout):
    def __init__(self,brain,launcher,**k):
        super().__init__(**k)
        self.brain=brain; self.launcher=launcher
        self.orientation='vertical'; self.padding=10; self.spacing=8
        header=BoxLayout(size_hint_y=0.13,spacing=8)
        self.reactor=Label(text='[b]/b]',markup=True,color
