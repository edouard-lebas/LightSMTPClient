import smtplib
import dns.resolver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
from tkinter import *
from tkinter import filedialog
import yaml

class LightSMTPClient(Frame):
    def __init__(self, window):
        """
        Initialise l'interface graphique et charge la configuration.

        :param window: Fenêtre principale de l'application.
        """
        super().__init__(window)
        self.window = window
        self.config = yaml.safe_load(open("config.yml"))
        self.attachment_paths = []  # Liste pour stocker les chemins des fichiers joints
        self.initUI()

    def initUI(self):
        """
        Initialise l'interface utilisateur avec les widgets nécessaires.
        """
        def retrieve_data():
            """
            Récupère les données saisies par l'utilisateur et envoie l'email.
            """
            try:
                self.server = server_input.get()
                self.port = int(port_input.get()) if port_input.get().isdigit() else None
                self.starttls = starttls_var.get()
                self.username = username_input.get()
                self.password = password_input.get()
                self.sender = from_input.get()
                self.recipient = to_input.get()
                self.subject = subject_input.get()
                self.message = body_input.get("1.0", END).strip()

                if not all([self.server, self.port, self.sender, self.recipient, self.subject, self.message]):
                    log_input.insert(1.0, "[ERROR] All fields are required.\n")
                    return

                self.send_email()
                log_input.insert(1.0, "[SUCCESS] Email sent successfully.\n")
            except Exception as e:
                log_input.insert(1.0, f"[ERROR] {str(e)}\n")

        def select_attachment():
            """
            Permet à l'utilisateur de sélectionner un fichier à joindre à l'email.
            """
            file_path = filedialog.askopenfilename()
            if file_path:
                self.attachment_paths.append(file_path)
                attachment_label.config(text="\n".join(self.attachment_paths) if self.attachment_paths else "No file selected")

        def clear_logs():
            """
            Efface les logs affichés dans l'interface.
            """
            log_input.delete("1.0", END)

        # Configuration des frames pour organiser les widgets
        config_frame = LabelFrame(window, text="Configuration", padx=20, pady=20)
        config_frame.grid(column=0, row=0, padx=20, pady=20, sticky='n')

        message_frame = LabelFrame(window, text="Message", padx=20, pady=20)
        message_frame.grid(column=0, row=1, padx=20, pady=20, sticky='n')

        log_frame = LabelFrame(window, text="Logs", padx=20, pady=20)
        log_frame.grid(column=1, row=0, rowspan=2, padx=20, pady=20, sticky='ns')

        # Widgets pour la configuration du serveur SMTP
        Label(config_frame, text="Server").grid(column=0, row=1)
        server_input = Entry(config_frame, width=30)
        server_input.grid(column=1, row=1, padx=5, pady=5)

        Label(config_frame, text="Port").grid(column=0, row=2)
        port_input = Entry(config_frame, width=30)
        port_input.grid(column=1, row=2, padx=5, pady=5)

        starttls_var = IntVar()
        Checkbutton(config_frame, text="STARTTLS", variable=starttls_var).grid(column=0, row=3, columnspan=2, padx=5, pady=5)

        Label(config_frame, text="Username").grid(column=0, row=4)
        username_input = Entry(config_frame, width=30)
        username_input.grid(column=1, row=4, padx=5, pady=5)

        Label(config_frame, text="Password").grid(column=0, row=5)
        password_input = Entry(config_frame, width=30, show="*")
        password_input.grid(column=1, row=5, padx=5, pady=5)

        # Widgets pour la composition du message
        Label(message_frame, text="From").grid(column=0, row=0)
        from_input = Entry(message_frame, width=30)
        from_input.grid(column=1, row=0, padx=5, pady=5)

        Label(message_frame, text="To").grid(column=0, row=1)
        to_input = Entry(message_frame, width=30)
        to_input.grid(column=1, row=1, padx=5, pady=5)

        Label(message_frame, text="Subject").grid(column=0, row=2)
        subject_input = Entry(message_frame, width=30)
        subject_input.grid(column=1, row=2, padx=5, pady=5)

        Label(message_frame, text="Message").grid(column=0, row=3)
        body_input = Text(message_frame, height=10, width=30)
        body_input.grid(column=1, row=3, padx=5, pady=5)

        # Widgets pour la gestion des pièces jointes
        Label(message_frame, text="Attachments:").grid(column=0, row=4, padx=5, pady=5)
        Button(message_frame, text="Select File", command=select_attachment).grid(column=1, row=4, padx=5, pady=5, sticky='w')
        attachment_label = Label(message_frame, text="No file selected")
        attachment_label.grid(column=1, row=5, padx=5, pady=5, sticky='w')

        # Bouton pour envoyer l'email
        Button(window, text="Send", command=retrieve_data, bg="red", width=75).grid(column=0, row=2, padx=20, pady=5, sticky='n')

        # Zone d'affichage des logs
        log_input = Text(log_frame, height=20, width=40)
        log_input.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # Bouton pour effacer les logs
        Button(window, text="Clear Logs", command=clear_logs, bg="blue", width=75).grid(column=1, row=2, padx=20, pady=5, sticky='s')

    def send_email(self):
        """
        Envoie un email avec les informations fournies par l'utilisateur.
        """
        s = smtplib.SMTP(host=self.server, port=self.port)
        if self.starttls:
            s.starttls()
        if self.username and self.password:
            s.login(self.username, self.password)

        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Date'] = formatdate(localtime=True)

        msg.attach(MIMEText(self.message, 'plain'))

        for attachment_path in self.attachment_paths:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={attachment_path.split('/')[-1]}")
                msg.attach(part)

        s.sendmail(from_addr=self.sender, to_addrs=self.recipient, msg=msg.as_string())
        s.quit()

if __name__ == "__main__":
    window = Tk()
    LightSMTPClient(window)
    window.title('LightSMTPClient')
    window.iconbitmap('icon.ico')
    window.resizable(False, False)
    window.mainloop()
