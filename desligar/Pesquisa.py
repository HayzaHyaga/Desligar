import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import threading

def schedule_shutdown():
    try:
        selected_time = entry_time.get()
        shutdown_time = datetime.strptime(selected_time, "%H:%M").time()
        now = datetime.now()
        shutdown_datetime = datetime.combine(now.date(), shutdown_time)
        if shutdown_datetime < now:
            shutdown_datetime += timedelta(days=1)

        time_difference = (shutdown_datetime - now).total_seconds()

        messagebox.showinfo("Agendamento", f"O computador será desligado às {shutdown_time}.\nTodos os programas abertos serão fechados.")
        threading.Thread(target=shutdown_after_delay, args=(time_difference,)).start()
    except ValueError:
        messagebox.showerror("Erro", "Insira o horário no formato HH:MM.")

def shutdown_after_delay(delay):
    time.sleep(delay)
    os.system("shutdown /s /f /t 1")  # /s: desliga, /f: força o fechamento de aplicativos

# Interface gráfica
app = tk.Tk()
app.title("Agendar Desligamento")

label_instruction = tk.Label(app, text="Digite o horário para desligar (HH:MM):")
label_instruction.pack(pady=10)

entry_time = tk.Entry(app, font=("Arial", 14))
entry_time.pack(pady=10)

button_schedule = tk.Button(app, text="Agendar", command=schedule_shutdown)
button_schedule.pack(pady=10)

app.geometry("300x200")
app.mainloop()
