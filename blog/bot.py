"""Bot del blog (24/10/2026): una entrada por universidad en blog.uninexo.link, con tu ✅ en Telegram.

Cada vuelta (GitHub Actions, cada 2 horas):
  1. Lee tus toques ✅/❌ (solo valen los de TU chat).
  2. Publica lo aprobado en Blogger (API oficial). Si la universidad ya tenía entrada, la ACTUALIZA (nunca duplica).
  3. Desde las 9:00 de Perú, si no hay nada esperando y hoy aún no propuso, te manda UNA propuesta:
     una universidad nueva o una ya publicada cuyos datos cambiaron.
Las entradas las arma ../publicador/blog-entradas-bot.mjs con los datos en vivo de uninexo.link (solo las que califican).
Telegram: su propio bot (TELEGRAM_* en blog/.env) o, si falta, el de empleos. Blogger: blog/.env (BLOGGER_*).
Memoria: estado.json.
"""
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import telegram

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADO = os.path.join(AQUI, 'estado.json')
PERU = timezone(timedelta(hours=-5))
HORA_PROPUESTA = 9
DIAS_VIGENCIA = 7


def ahora():
    return datetime.now(PERU)


def cargar_json(ruta, defecto):
    try:
        with open(ruta, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return defecto


def guardar_estado(estado):
    with open(ESTADO, 'w', encoding='utf-8') as fh:
        json.dump(estado, fh, ensure_ascii=False, indent=1)


def estado_inicial():
    return {'offset': 0, 'publicadas': {}, 'descartadas': {}, 'pendiente': None, 'ultima_propuesta': ''}


# ---------------------------------------------------------------- entradas

def armar_entradas():
    """Corre el armador (Node) y devuelve {uniId: entrada}."""
    pub = os.environ.get('UNINEXO_PUBLICADOR_DIR') or os.path.join(AQUI, '..', 'publicador')
    with tempfile.TemporaryDirectory() as tmp:
        salida = os.path.join(tmp, 'entradas.json')
        r = subprocess.run(['node', os.path.join(pub, 'blog-entradas-bot.mjs'), salida],
                           capture_output=True, text=True, encoding='utf-8', timeout=600)
        if r.returncode != 0:
            raise RuntimeError(f'el armador falló: {(r.stderr or r.stdout)[-300:]}')
        return {e['uniId']: e for e in cargar_json(salida, [])}


def elegir(entradas, estado):
    """Siguiente universidad: primero las nuevas (en el orden del catálogo), luego las publicadas con datos nuevos."""
    pub, des = estado['publicadas'], estado['descartadas']
    nuevas = [u for u, e in entradas.items() if u not in pub and des.get(u) != e['huella']]
    cambiadas = [u for u, e in entradas.items() if u in pub and pub[u].get('huella') != e['huella'] and des.get(u) != e['huella']]
    return (nuevas or cambiadas or [None])[0]


def texto_propuesta(e, estado):
    pub = estado['publicadas'].get(e['uniId'])
    accion = f'🔄 <b>Actualizar</b> la entrada (cambiaron los datos)\n{pub["url"]}' if pub else '🆕 <b>Entrada nueva</b>'
    return (f'📝 <b>Blog de UniNexo</b> · {accion}\n\n<b>{telegram.esc(e["titulo"])}</b>\n{telegram.esc(e["descripcion"])}\n\n'
            f'🏷️ {telegram.esc(", ".join(e["etiquetas"]))}\n'
            f'👀 Los mismos datos en la web: https://uninexo.link/universidad/{e["uniId"]}')


# ---------------------------------------------------------------- Blogger

class Blogger:
    API = 'https://www.googleapis.com/blogger/v3/blogs/'

    def __init__(self, env):
        faltan = [k for k in ('BLOGGER_REFRESH_TOKEN', 'BLOGGER_CLIENT_ID', 'BLOGGER_CLIENT_SECRET', 'BLOGGER_BLOG_ID') if not env.get(k)]
        if faltan:
            raise RuntimeError('faltan en blog/.env: ' + ', '.join(faltan))
        self.env, self.token = env, None

    def _pedir(self, metodo, url, datos=None):
        if not self.token:
            cuerpo = urllib.parse.urlencode({
                'grant_type': 'refresh_token', 'refresh_token': self.env['BLOGGER_REFRESH_TOKEN'],
                'client_id': self.env['BLOGGER_CLIENT_ID'], 'client_secret': self.env['BLOGGER_CLIENT_SECRET'],
            }).encode()
            self.token = json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', cuerpo, timeout=30))['access_token']
        req = urllib.request.Request(url, method=metodo, data=json.dumps(datos).encode() if datos is not None else None,
                                     headers={'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json'})
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as err:
            raise RuntimeError(f'Blogger respondió {err.code}: {err.read().decode("utf-8", "ignore")[:200]}')

    def publicar(self, e, post_id=None):
        """Crea la entrada o, si ya existe, la actualiza. Devuelve (id, url)."""
        cuerpo = {'title': e['titulo'], 'content': e['html'], 'labels': e['etiquetas']}
        base = self.API + self.env['BLOGGER_BLOG_ID'] + '/posts/'
        r = self._pedir('PATCH', base + post_id, cuerpo) if post_id else self._pedir('POST', base, cuerpo)
        return r['id'], r['url']


# ---------------------------------------------------------------- vuelta

def leer_toques(tg, estado):
    p = estado.get('pendiente')
    for u in tg.actualizaciones(estado.get('offset', 0)):
        estado['offset'] = max(estado.get('offset', 0), u['update_id'] + 1)
        cq = u.get('callback_query')
        if not cq:
            continue
        de = str((cq.get('from') or {}).get('id', ''))
        chat = str(((cq.get('message') or {}).get('chat') or {}).get('id', ''))
        if de != tg.chat_id or chat != tg.chat_id:
            tg.responder_toque(cq['id'], 'Solo el administrador de UniNexo puede aprobar.')
            continue
        accion, _, uni = (cq.get('data') or '').partition(':')
        if not p or p['uni'] != uni or p['estado'] != 'pendiente' or accion not in ('blgpub', 'blgdes'):
            tg.responder_toque(cq['id'], 'Esto ya se revisó.')
            continue
        if accion == 'blgpub':
            p['estado'] = 'aprobada'
            tg.responder_toque(cq['id'], '✅ Aprobado: lo publico en la próxima vuelta.')
        else:
            p['estado'] = 'descartada'
            estado['descartadas'][uni] = p['huella']
            tg.responder_toque(cq['id'], '❌ Saltada.')
            tg.editar(p['mensaje'], p['texto'] + '\n\n❌ <b>Saltada</b>. No la vuelvo a proponer hasta que cambien sus datos.')
    if p and p['estado'] == 'pendiente' and p['enviado'] < (ahora() - timedelta(days=DIAS_VIGENCIA)).date().isoformat():
        p['estado'] = 'vencida'
        tg.editar(p['mensaje'], p['texto'] + '\n\n⌛ <b>Venció</b> sin respuesta: te la vuelvo a proponer otro día.')


def vuelta(tg, blogger, estado, entradas_fn=armar_entradas, hora_minima=HORA_PROPUESTA):
    leer_toques(tg, estado)
    guardar_estado(estado)
    p, entradas, hecho = estado.get('pendiente'), None, []
    hoy = ahora().date().isoformat()
    if p and p['estado'] == 'aprobada':
        entradas = entradas_fn()
        e = entradas.get(p['uni'])
        if not e:
            p['estado'] = 'invalida'
            tg.editar(p['mensaje'], p['texto'] + '\n\n⚠️ <b>No se publicó</b>: esta universidad ya no tiene datos suficientes.')
        else:
            previa = estado['publicadas'].get(p['uni'])
            try:
                post_id, url = blogger.publicar(e, previa and previa['post_id'])
            except Exception as err:  # se reintenta en la próxima vuelta; avisa una vez al día
                if estado.get('aviso_error') != hoy:
                    tg.enviar(f'⚠️ <b>No pude publicar en el blog</b>: {telegram.esc(str(err)[:300])}\nLo reintento en la próxima vuelta.')
                    estado['aviso_error'] = hoy
                guardar_estado(estado)
                return f'error al publicar {p["uni"]}: {err}'
            estado['publicadas'][p['uni']] = {'post_id': post_id, 'url': url, 'huella': e['huella'], 'fecha': hoy}
            p['estado'] = 'publicada'
            tg.editar(p['mensaje'], p['texto'] + f'\n\n✅ <b>{"Actualizada" if previa else "Publicada"}</b>: {url}')
            hecho.append(f'{"actualizada" if previa else "publicada"} {p["uni"]}')
        guardar_estado(estado)
    p = estado.get('pendiente')
    if (not p or p['estado'] != 'pendiente') and estado.get('ultima_propuesta') != hoy and ahora().hour >= hora_minima:
        entradas = entradas if entradas is not None else entradas_fn()
        uni = elegir(entradas, estado)
        estado['ultima_propuesta'] = hoy
        if uni:
            e = entradas[uni]
            texto = texto_propuesta(e, estado)
            mensaje = tg.enviar_con_botones(texto, [[('✅ Publicar', f'blgpub:{uni}'), ('❌ Saltar', f'blgdes:{uni}')]])
            estado['pendiente'] = {'uni': uni, 'huella': e['huella'], 'mensaje': mensaje, 'texto': texto, 'enviado': hoy, 'estado': 'pendiente'}
            hecho.append(f'propuesta {uni}')
        else:
            hecho.append('no hay universidades nuevas ni con datos nuevos')
        guardar_estado(estado)
    return ' · '.join(hecho) or 'nada que hacer'


def main(argv):
    env_blog = telegram.cargar_env(os.path.join(AQUI, '.env'))
    # Su propio bot de Telegram si blog/.env lo trae (nadie más lee sus toques); si no, el de empleos
    env_tg = env_blog if env_blog.get('TELEGRAM_BOT_TOKEN') else telegram.cargar_env(os.path.join(AQUI, '..', 'empleos', '.env'))
    tg = telegram.Telegram(env_tg.get('TELEGRAM_BOT_TOKEN'), env_tg.get('TELEGRAM_CHAT_ID'))
    blogger = Blogger(env_blog)
    estado = cargar_json(ESTADO, None) or estado_inicial()
    for k, v in estado_inicial().items():
        estado.setdefault(k, v)
    hora = HORA_PROPUESTA
    if '--forzar' in argv:  # para probar a mano: propone aunque hoy ya haya propuesto o sea temprano
        estado['ultima_propuesta'] = ''
        hora = 0
    resultado = vuelta(tg, blogger, estado, hora_minima=hora)
    linea = f'{ahora():%Y-%m-%d %H:%M} blog: {resultado}'
    os.makedirs(os.path.join(AQUI, 'logs'), exist_ok=True)
    with open(os.path.join(AQUI, 'logs', 'bot.log'), 'a', encoding='utf-8') as fh:
        fh.write(linea + '\n')
    print(linea)


if __name__ == '__main__':
    main(sys.argv[1:])
