from tkinter import *
import yaml
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

class LightSMTPClient(Frame):

    def __init__(self,window):
        Frame.__init__(self, window)
        self.window = window
        self.config = yaml.safe_load(open("config.yml"))
        self.server = ""
        self.port = ""
        self.sender = ""
        self.recipient = ""
        self.subject = ""
        self.message = ""
        self.initUI()

    def initUI(self):
        def retrieve_data():
            self.server = server_input.get()
            self.port = port_input.get()
            self.sender = from_input.get()
            self.recipient = to_input.get()
            self.subject = subject_input.get()
            self.message = body_input.get("1.0",END)
            print("Trying to send from server {server} with port {port} from {sender} to {recipient} with subject {subject} with body {message}".format(server=self.server, port=self.port, sender=self.sender, recipient=self.recipient, subject=self.subject, message=self.message))
            if self.server and self.port and self.sender and self.recipient and self.subject and self.message:
                self.send_email()
            else:
                print("ERROR > ALL fields are required")

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
        if self.config["message"]["body"] != None:
            body_input.insert(1.0,self.config["message"]["body"])
        body_input.grid(column=1, row=6,padx=5, pady=5)

        send_button=Button(window, text="Send", command=retrieve_data)
        send_button.grid(column=0, row=10, padx=20, pady=20)



    def send_email(self):
        s = smtplib.SMTP(host=self.server, port=self.port)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg["Date"] = formatdate(localtime=True)
        part = MIMEText(self.message, 'html')
        msg.attach(part)
        try:
            s.sendmail(from_addr=self.sender, to_addrs=self.recipient, msg=msg.as_string())
            print("MAIL SENT")
        except Exception as e:
            print("ERROR > " +str(e))
        s.quit()

if __name__ == "__main__":
    window = Tk()
    LightSMTPClient(window)
    window.title('LightSMTPClient')
    window.iconbitmap('icon.ico')
    window.resizable(False, False)
    window.geometry('')
    window.mainloop()