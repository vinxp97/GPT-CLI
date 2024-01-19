import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
from openai import OpenAI

class ChatInterface:
    def __init__(self, master):
        self.master = master
        master.title("AI Chat Interface")

        # Initialize OpenAI client
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        self.history = [
            {"role": "system", "content": "You are an intelligent assistant..."}
        ]

        # Create a scrolled text area for chat history
        self.chat_history = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_history.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Create an entry box for user input
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=0, sticky="ew")

        # Create a Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)

        # Configure grid
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

    def send_message(self):
        user_message = self.entry.get()
        if user_message:
            self.update_chat_history(f"User: {user_message}")
            self.entry.delete(0, tk.END)
            Thread(target=self.fetch_response, args=(user_message,)).start()

    def fetch_response(self, message):
        self.history.append({"role": "user", "content": message})
        completion = self.client.chat.completions.create(
            model="local-model",
            messages=self.history,
            temperature=0.7,
            stream=True,
        )

        assistant_message = ''
        for chunk in completion:
            if chunk.choices[0].delta.content:
                assistant_message += chunk.choices[0].delta.content

        self.history.append({"role": "assistant", "content": assistant_message})
        self.update_chat_history(f"AI: {assistant_message}")

    def update_chat_history(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

def main():
    root = tk.Tk()
    chat_interface = ChatInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
