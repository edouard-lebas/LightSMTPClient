from tkinter import *
import yaml

class LightSMTPClient(Frame):

    def __init__(self,window):
        Frame.__init__(self, window)
        self.window = window
        self.config = yaml.safe_load(open("config.yml"))
        self.initUI()

    def initUI(self):
        config_frame = LabelFrame(window, text="Configuration", padx=20, pady=20)
        config_frame.grid(column=0, row=0, padx=20, pady=20)

        message_frame = LabelFrame(window, text="Message", padx=20, pady=20)
        message_frame.grid(column=0, row=2,padx=20, pady=20)

        #SERVER
        server_label = Label(config_frame, text="Server")
        server_label.grid(column=0, row=1)
        server_data = StringVar()
        if self.config["config"]["server"] != None:
            server_data.set(self.config["config"]["server"])
        server_input = Entry(config_frame, textvariable=server_data, width=30)
        server_input.grid(column=1, row=1,padx=5, pady=5)

        #PORT
        port_label = Label(config_frame, text="Port")
        port_label.grid(column=0, row=2)
        port_data = StringVar()
        if self.config["config"]["port"] != None:
            port_data.set(self.config["config"]["port"])
        port_input = Entry(config_frame, textvariable=port_data, width=30)
        port_input.grid(column=1, row=2,padx=5, pady=5)

        #FROM
        from_label = Label(message_frame, text="From")
        from_label.grid(column=0, row=3)
        from_data = StringVar()
        if self.config["message"]["from"] != None:
            from_data.set(self.config["message"]["from"])
        from_input = Entry(message_frame, textvariable=from_data, width=30)
        from_input.grid(column=1, row=3,padx=5, pady=5)

        #TO
        to_label = Label(message_frame, text="To")
        to_label.grid(column=0, row=4)
        to_data = StringVar()
        if self.config["message"]["to"] != None:
            to_data.set(self.config["message"]["to"])
        to_input = Entry(message_frame, textvariable=to_data, width=30)
        to_input.grid(column=1, row=4,padx=5, pady=5)

        #SUBJECT
        subject_label = Label(message_frame, text="Subject")
        subject_label.grid(column=0, row=5)
        subject_data = StringVar()
        if self.config["message"]["subject"] != None:
            subject_data.set(self.config["message"]["subject"])
        subject_input = Entry(message_frame, textvariable=subject_data, width=30)
        subject_input.grid(column=1, row=5,padx=5, pady=5)

        #MESSAGE
        message_label = Label(message_frame, text="Message")
        message_label.grid(column=0, row=6)
        body_input = Text(message_frame, height=10, width=30)
        if self.config["message"]["content"] != None:
            body_input.insert(1.0,self.config["message"]["content"])
        body_input.grid(column=1, row=6,padx=5, pady=5)

        send_button=Button(window, text="Send")
        send_button.grid(column=0, row=10, padx=20, pady=20)

if __name__ == "__main__":
    window = Tk()
    LightSMTPClient(window)
    window.title('LightSMTPClient')
    window.geometry('')

    window.mainloop()