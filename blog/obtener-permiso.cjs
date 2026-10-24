/**
 * Pide UNA vez el permiso de Blogger (OAuth) y guarda el token FUERA del repositorio.
 * Uso: node blog/obtener-permiso.cjs D:/secretos-uninexo/blogger-cliente.json
 * El token NO se muestra en pantalla: queda en D:/secretos-uninexo/blogger-token.txt
 */
const fs = require('fs');
const http = require('http');
const { execFile } = require('child_process');

const archivoCliente = process.argv[2] || 'D:/secretos-uninexo/blogger-cliente.json';
const salida = 'D:/secretos-uninexo/blogger-token.txt';
const c = JSON.parse(fs.readFileSync(archivoCliente, 'utf8'));
const { client_id, client_secret } = c.installed || c.web;
const PUERTO = 53682;
const redirect = `http://127.0.0.1:${PUERTO}`;
const url = 'https://accounts.google.com/o/oauth2/v2/auth?' + new URLSearchParams({
  client_id, redirect_uri: redirect, response_type: 'code',
  scope: 'https://www.googleapis.com/auth/blogger', access_type: 'offline', prompt: 'consent',
});

http.createServer(async (req, res) => {
  const code = new URL(req.url, redirect).searchParams.get('code');
  if (!code) { res.end('Sin codigo'); return; }
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ code, client_id, client_secret, redirect_uri: redirect, grant_type: 'authorization_code' }),
  }).then((x) => x.json());
  if (!r.refresh_token) { res.end('Google no dio el permiso. Vuelve a intentarlo.'); console.log('Error:', r.error || 'sin refresh_token'); process.exit(1); }
  // Comprueba el permiso buscando el blog
  const blog = await fetch('https://www.googleapis.com/blogger/v3/blogs/byurl?url=' + encodeURIComponent('https://blog.uninexo.link/'), {
    headers: { authorization: 'Bearer ' + r.access_token },
  }).then((x) => x.json());
  fs.mkdirSync('D:/secretos-uninexo', { recursive: true });
  fs.writeFileSync(salida, `BLOGGER_REFRESH_TOKEN=${r.refresh_token}\nBLOGGER_CLIENT_ID=${client_id}\nBLOGGER_CLIENT_SECRET=${client_secret}\nBLOGGER_BLOG_ID=${blog.id || ''}\n`);
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end('<h2>✅ Listo. Ya puedes cerrar esta pestaña.</h2>');
  console.log(`✅ Permiso guardado en ${salida}`);
  console.log(blog.id ? `Blog encontrado: «${blog.name}» (${blog.posts?.totalItems ?? '?'} entradas)` : 'Ojo: no encontré el blog, revisa que la cuenta sea la dueña del blog.');
  process.exit(0);
}).listen(PUERTO, '127.0.0.1', () => {
  console.log('Abriendo el navegador para dar el permiso…');
  execFile('cmd', ['/c', 'start', '', url.replace(/&/g, '^&')]);
});
