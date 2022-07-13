from tkinter import *

window = Tk()
window.title('LightSMTPClient')
window.geometry('400x600')

config_frame = LabelFrame(window, text="Configuration", padx=20, pady=20)
config_frame.pack(fill="both", expand="yes", padx=20, pady=20)

message_frame = LabelFrame(window, text="Message", padx=20, pady=20)
message_frame.pack(fill="both", expand="yes",padx=20, pady=20)

#SERVER
server_label = Label(config_frame, text="SMTP server")
server_label.pack()
server_data = StringVar()
server_input = Entry(config_frame, textvariable=server_data, width=30)
server_input.pack()

#PORT
port_label = Label(config_frame, text="Port")
port_label.pack()
port_data = StringVar()
port_input = Entry(config_frame, textvariable=port_data, width=10)
port_input.pack()

#FROM
from_label = Label(message_frame, text="From")
from_label.pack()
from_data = StringVar()
from_input = Entry(message_frame, textvariable=from_data, width=30)
from_input.pack()

#TO
to_label = Label(message_frame, text="To")
to_label.pack()
to_data = StringVar()
to_input = Entry(message_frame, textvariable=to_data, width=30)
to_input.pack()

#SUBJECT
subject_label = Label(message_frame, text="Subject")
subject_label.pack()
subject_data = StringVar()
subject_input = Entry(message_frame, textvariable=subject_data, width=30)
subject_input.pack()

#SUBJECT
message_label = Label(message_frame, text="Message")
message_label.pack()
body_data = StringVar()
body_input = Entry(message_frame, textvariable=body_data, width=30)
body_input.pack()

send_button=Button(window, text="Send")
send_button.pack(padx=20, pady=20)

window.mainloop()