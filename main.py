# AURA IA - MARK 10 - MARKMETA LABS (Android Ready)
import os, json, datetime, threading, requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

# --- RUTAS SEGURAS PARA ANDROID Y PC ---
def get_file_path(filename):
    try:
        app = App.get_running_app()
        if app and app.user_data_dir:
            return os.path.join(app.user_data_dir, filename)
    except:
        pass
    return filename

# --- MEMORIA POR USUARIO ---
def load_users():
    path = get_file_path("users.json")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_user(name, memory):
    path = get_file_path("users.json")
    users = load_users()
    users[name] = memory
    with open(path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

# --- GEMINI VÍA REST API (EVITA ERRORES EN ANDROID) ---
def ask_gemini(prompt, user_memory):
    try:
        key = ""
        gemini_path = get_file_path("gemini_key.txt")
        
        if os.path.exists(gemini_path):
            with open(gemini_path, "r", encoding="utf-8") as f:
                key = f.read().strip()
        else:
            key = os.getenv("GEMINI_API_KEY", "")

        if not key:
            return "Jefe, pon tu API Key de Gemini en Ajustes para responder de todo."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        
        historial_reciente = user_memory.get("historial", [])[-10:]
        contexto = f"Eres AURA IA de MarkMeta Labs. Usuario: {user_memory.get('nombre')}. Historial reciente: {json.dumps(historial_reciente, ensure_ascii=False)}. Responde natural, mexicana, no robótica. Pregunta: {prompt}"
        
        payload = {
            "contents": [{
                "parts": [{"text": contexto}]
            }]
        }
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error en la API de Gemini: {response.status_code}"
            
    except Exception as e:
        return f"Soy AURA local, Jefe {user_memory.get('nombre', '')}. Sin internet por ahora, pero recuerdo que te interesa {user_memory.get('interes', 'aprender')}. Error: {str(e)}"

# --- VOZ NATIVA PARA ANDROID ---
def speak(text):
    text = text[:350]
    print(f"[AURA]: {text}")
    def run_voice():
        try:
            from plyer import tts
            tts.speak(text)
        except Exception as e:
            print(f"Error en TTS: {e}")
    threading.Thread(target=run_voice, daemon=True).start()

# --- INTERFAZ GRÁFICA (KIVY) ---

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[b]AURA IA - MARKMETA LABS[/b]", markup=True, font_size='22sp'))
        layout.add_widget(Label(text="Ingresa tu nombre de usuario:"))
        
        self.user_input = TextInput(multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.user_input)
        
        btn_login = Button(text="Iniciar Sesión", size_hint_y=None, height=55)
        btn_login.bind(on_release=self.login)
        layout.add_widget(btn_login)
        self.add_widget(layout)

    def login(self, instance):
        username = self.user_input.text.strip()
        if username:
            app = App.get_running_app()
            app.current_user = username
            users = load_users()
            if username not in users:
                users[username] = {"nombre": username, "interes": "aprender", "historial": []}
                save_user(username, users[username])
            app.user_memory = users[username]
            
            chat_screen = self.manager.get_screen('chat')
            chat_screen.update_header(username)
            self.manager.current = 'chat'
            speak(f"Hola Jefe {username}, lista para ayudarte.")

class ChatScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.header = Label(text="AURA IA", size_hint_y=None, height=35, font_size='18sp')
        layout.add_widget(self.header)
        
        self.scroll = ScrollView()
        self.chat_log = Label(text="", size_hint_y=None, markup=True, halign='left', valign='top')
        self.chat_log.bind(texture_size=self._update_log_height)
        self.scroll.add_widget(self.chat_log)
        layout.add_widget(self.scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.text_input = TextInput(multiline=False)
        btn_send = Button(text="Enviar", size_hint_x=0.25)
        btn_send.bind(on_release=self.send_message)
        
        btn_settings = Button(text="Ajustes", size_hint_x=0.2)
        btn_settings.bind(on_release=self.open_settings)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(btn_send)
        input_layout.add_widget(btn_settings)
        layout.add_widget(input_layout)
        
        self.add_widget(layout)

    def _update_log_height(self, instance, value):
        self.chat_log.height = value[1]
        self.chat_log.text_size = (self.chat_log.width, None)
        self.scroll.scroll_y = 0

    def update_header(self, username):
        self.header.text = f"Usuario: [b]{username}[/b] | MarkMeta Labs"

    def open_settings(self, instance):
        self.manager.current = 'settings'

    def send_message(self, instance):
        prompt = self.text_input.text.strip()
        if not prompt:
            return
        
        self.text_input.text = ""
        self.append_text(f"[b]Tú:[/b] {prompt}")
        
        app = App.get_running_app()
        
        def process_response():
            response = ask_gemini(prompt, app.user_memory)
            Clock.schedule_once(lambda dt: self.finish_response(response, prompt))
            
        threading.Thread(target=process_response, daemon=True).start()

    def finish_response(self, response, prompt):
        self.append_text(f"[b]AURA:[/b] {response}")
        speak(response)
        
        app = App.get_running_app()
        if "historial" not in app.user_memory:
            app.user_memory["historial"] = []
            
        app.user_memory["historial"].append({
            "q": prompt, 
            "a": response, 
            "time": str(datetime.datetime.now())
        })
        
        if len(app.user_memory["historial"]) > 50:
            app.user_memory["historial"] = app.user_memory["historial"][-50:]
            
        save_user(app.current_user, app.user_memory)

    def append_text(self, text):
        self.chat_log.text += f"\n{text}\n"
        self.scroll.scroll_y = 0

class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text="[b]Configuración de Gemini[/b]", markup=True, font_size='18sp'))
        layout.add_widget(Label(text="Clave API de Gemini:"))
        
        self.key_input = TextInput(multiline=False, size_hint_y=None, height=45)
        
        gemini_path = get_file_path("gemini_key.txt")
        if os.path.exists(gemini_path):
            with open(gemini_path, "r", encoding="utf-8") as f:
                self.key_input.text = f.read().strip()
                
        layout.add_widget(self.key_input)
        
        btn_save = Button(text="Guardar y Volver", size_hint_y=None, height=50)
        btn_save.bind(on_release=self.save_key)
        layout.add_widget(btn_save)
        
        self.add_widget(layout)

    def save_key(self, instance):
        key = self.key_input.text.strip()
        gemini_path = get_file_path("gemini_key.txt")
        with open(gemini_path, "w", encoding="utf-8") as f:
            f.write(key)
        self.manager.current = 'chat'

class AuraApp(App):
    def build(self):
        self.title = "AURA IA - MarkMeta Labs"
        self.current_user = None
        self.user_memory = {}
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    AuraApp().run()
