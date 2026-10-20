"""Envío de mensajes y archivos por Telegram (solo a TU chat). El token y el chat salen del archivo .env, nunca del código."""
import html
import json
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

LIMITE = 3800  # Telegram admite 4096 caracteres por mensaje; se deja margen


class ErrorTelegram(Exception):
    pass


def cargar_env(ruta):
    datos = {}
    if os.path.exists(ruta):
        with open(ruta, encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith('#') and '=' in linea:
                    k, v = linea.split('=', 1)
                    datos[k.strip()] = v.strip().strip('"').strip("'")
    return datos


def esc(texto):
    """Escapa el texto para el modo HTML de Telegram."""
    return html.escape(str(texto or ''), quote=False)


def partir(bloques, limite=LIMITE):
    """Junta bloques de texto en mensajes que no pasen el límite (un bloque nunca se parte por la mitad, salvo que él solo lo supere)."""
    mensajes, actual = [], ''
    for b in bloques:
        while len(b) > limite:  # bloque gigante: se corta por líneas
            corte = b.rfind('\n', 0, limite)
            corte = corte if corte > 0 else limite
            if actual:
                mensajes.append(actual)
                actual = ''
            mensajes.append(b[:corte])
            b = b[corte:].lstrip('\n')
        if len(actual) + len(b) + 2 > limite and actual:
            mensajes.append(actual)
            actual = b
        else:
            actual = (actual + '\n\n' + b) if actual else b
    if actual:
        mensajes.append(actual)
    return mensajes


class Telegram:
    def __init__(self, token, chat_id):
        if not token or not chat_id:
            raise ErrorTelegram('Falta TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en el archivo .env')
        self.token, self.chat_id = token, str(chat_id)

    def _llamar(self, metodo, datos=None, cuerpo=None, cabeceras=None):
        url = f'https://api.telegram.org/bot{self.token}/{metodo}'
        req = urllib.request.Request(url, data=cuerpo if cuerpo is not None else (urllib.parse.urlencode(datos).encode() if datos else None), headers=cabeceras or {})
        for intento in range(3):
            try:
                return json.load(urllib.request.urlopen(req, timeout=60))
            except urllib.error.HTTPError as e:
                detalle = e.read().decode('utf-8', 'ignore')
                if e.code == 429:  # demasiados mensajes: Telegram dice cuánto esperar
                    try:
                        espera = json.loads(detalle).get('parameters', {}).get('retry_after', 5)
                    except Exception:
                        espera = 5
                    time.sleep(min(int(espera) + 1, 60))
                    continue
                raise ErrorTelegram(f'Telegram respondió {e.code}: {detalle[:200]}')
            except Exception as e:
                if intento == 2:
                    raise ErrorTelegram(f'no se pudo conectar con Telegram ({repr(e)[:80]})')
                time.sleep(3)
        raise ErrorTelegram('Telegram no respondió')

    def enviar(self, texto):
        """Manda un mensaje en HTML (sin vista previa de enlaces)."""
        r = self._llamar('sendMessage', {'chat_id': self.chat_id, 'text': texto, 'parse_mode': 'HTML', 'disable_web_page_preview': 'true'})
        if not r.get('ok'):
            raise ErrorTelegram(str(r)[:200])
        time.sleep(1.1)  # Telegram pide no pasar de ~1 mensaje por segundo en un mismo chat
        return r

    def enviar_varios(self, bloques):
        for m in partir(bloques):
            self.enviar(m)

    def enviar_archivo(self, ruta, leyenda=''):
        limite = uuid.uuid4().hex
        nombre = os.path.basename(ruta)
        tipo = mimetypes.guess_type(nombre)[0] or 'application/octet-stream'
        partes = []
        for k, v in (('chat_id', self.chat_id), ('caption', leyenda), ('parse_mode', 'HTML')):
            partes.append(f'--{limite}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode('utf-8'))
        partes.append(f'--{limite}\r\nContent-Disposition: form-data; name="document"; filename="{nombre}"\r\nContent-Type: {tipo}\r\n\r\n'.encode('utf-8'))
        with open(ruta, 'rb') as f:
            partes.append(f.read())
        partes.append(f'\r\n--{limite}--\r\n'.encode('utf-8'))
        r = self._llamar('sendDocument', cuerpo=b''.join(partes), cabeceras={'Content-Type': f'multipart/form-data; boundary={limite}'})
        if not r.get('ok'):
            raise ErrorTelegram(str(r)[:200])
        return r
