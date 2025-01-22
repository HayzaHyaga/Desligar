import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import threading

# Variáveis globais para controlar o agendamento
shutdown_scheduled = False
shutdown_thread = None
scheduled_time_label = None  # Para exibir o horário agendado

def schedule_shutdown():
    global shutdown_scheduled, shutdown_thread, scheduled_time_label

    if shutdown_scheduled:
        messagebox.showerror("Erro", "Já existe um desligamento agendado. Cancele antes de agendar outro.")
        return

    try:
        selected_time = entry_time.get()
        shutdown_time = datetime.strptime(selected_time, "%H:%M").time()
        now = datetime.now()
        shutdown_datetime = datetime.combine(now.date(), shutdown_time)
        if shutdown_datetime < now:
            shutdown_datetime += timedelta(days=1)

        time_difference = (shutdown_datetime - now).total_seconds()

        shutdown_scheduled = True
        shutdown_thread = threading.Thread(target=shutdown_after_delay, args=(time_difference,))
        shutdown_thread.start()

        # Atualiza o rótulo com o horário agendado
        scheduled_time_label.config(text=f"Desligamento agendado para: {shutdown_datetime.strftime('%H:%M')}")

        messagebox.showinfo("Agendamento", f"O computador será desligado às {shutdown_time}.\nTodos os programas abertos serão fechados.")
    except ValueError:
        messagebox.showerror("Erro", "Insira o horário no formato HH:MM.")

def shutdown_after_delay(delay):
    global shutdown_scheduled
    time.sleep(delay)
    if shutdown_scheduled:  # Verifica se o agendamento não foi cancelado
        os.system("shutdown /s /f /t 1")

def cancel_shutdown():
    global shutdown_scheduled

    if not shutdown_scheduled:
        messagebox.showinfo("Cancelar", "Nenhum desligamento agendado para cancelar.")
        return

    os.system("shutdown /a")  # Comando para abortar o desligamento
    shutdown_scheduled = False

    # Limpa o rótulo do horário agendado
    scheduled_time_label.config(text="Nenhum desligamento agendado.")

    messagebox.showinfo("Cancelar", "O desligamento agendado foi cancelado.")

# Interface gráfica
app = tk.Tk()
app.title("Agendar Desligamento")

label_instruction = tk.Label(app, text="Digite o horário para desligar (HH:MM):")
label_instruction.pack(pady=10)

entry_time = tk.Entry(app, font=("Arial", 14))
entry_time.pack(pady=10)

button_schedule = tk.Button(app, text="Agendar", command=schedule_shutdown)
button_schedule.pack(pady=10)

button_cancel = tk.Button(app, text="Cancelar", command=cancel_shutdown, bg="red", fg="white")
button_cancel.pack(pady=10)

# Rótulo para exibir o horário agendado
scheduled_time_label = tk.Label(app, text="Nenhum desligamento agendado.", fg="blue", font=("Arial", 12))
scheduled_time_label.pack(pady=20)

app.geometry("350x300")
app.mainloop()
