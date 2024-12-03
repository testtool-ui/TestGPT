from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests

class ChatBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Scrollable chat window
        self.scrollview = ScrollView(size_hint=(1, 0.8))
        self.chat_log = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_log.bind(minimum_height=self.chat_log.setter('height'))
        self.scrollview.add_widget(self.chat_log)
        
        # Input and button layout
        self.input_layout = BoxLayout(size_hint=(1, 0.2))
        self.user_input = TextInput(hint_text="Type your message...", multiline=False)
        self.send_button = Button(text="Send")
        self.send_button.bind(on_press=self.send_message)
        
        self.input_layout.add_widget(self.user_input)
        self.input_layout.add_widget(self.send_button)
        
        self.add_widget(self.scrollview)
        self.add_widget(self.input_layout)
    
    def send_message(self, instance):
        user_message = self.user_input.text.strip()
        if user_message:
            self.add_message(f"You: {user_message}", bot=False)
            self.user_input.text = ""
            # Simulate bot response (replace this with your API logic)
            self.fetch_bot_response(user_message)
    
    def add_message(self, message, bot=True):
        label = Label(text=message, size_hint_y=None, halign="left" if bot else "right", valign="middle")
        label.text_size = (self.scrollview.width - 20, None)
        label.bind(texture_size=label.setter('size'))
        self.chat_log.add_widget(label)
        self.scrollview.scroll_to(label)
    
    def fetch_bot_response(self, user_message):
        try:
            # Replace this with your API endpoint or chatbot logic
            response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                headers={"Authorization": "Bearer YOUR_HUGGINGFACE_TOKEN"},
                json={"inputs": user_message}
            )
            bot_reply = response.json().get("generated_text", "I'm sorry, I couldn't process that.")
            self.add_message(f"Bot: {bot_reply}")
        except Exception as e:
            self.add_message(f"Error: {str(e)}")

class TestGPTApp(App):
    def build(self):
        return ChatBox()

if __name__ == "__main__":
    TestGPTApp().run()
