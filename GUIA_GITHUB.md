# Tu web: editar, copiar y guardar versiones

La carpeta `site` contiene el proyecto completo. Es una web estática: Python genera páginas HTML a partir de textos, imágenes y estilos. No necesita base de datos ni instalar paquetes de Python. Necesita Python 3 para compilar y Git para guardar versiones.

## Qué significa cada copia

- La carpeta local es tu copia de trabajo: puedes modificarla sin cambiar lo guardado en GitHub.
- Un **commit** es una versión guardada con un mensaje que describe los cambios. Solo incluye lo que hayas añadido a Git.
- **Push** envía tus commits a GitHub. **Pull** trae los cambios desde GitHub.
- El repositorio privado guarda código e historial. No publica una web visible por otras personas. GitHub Pages no se ejecuta mientras este repositorio sea privado.
- El historial empieza con la versión actual. Los ajustes anteriores a la creación del repositorio no se convierten automáticamente en commits antiguos.

## Dónde modificar cada cosa

| Qué quieres cambiar | Archivo o carpeta |
| --- | --- |
| Biografía y formación de Home | `content/inicio.json` (el generador utiliza los bloques 3, 4 y 5; conserva el orden) |
| Novedades de Home | `content/news.json` |
| Abstracts, conferencias y seminarios | `content/research.json` (conserva el orden de los bloques, usado por el generador) |
| Nombres, títulos, estados y estructura de los papers | `build.py`, sección Research |
| Asignaturas de Teaching | Lista `courses` en `build.py` |
| Textos de CV y Contact, emails, dirección, cabeceras y pie | `build.py` |
| Redes sociales: nombre, URL e icono | `content/socials.json` |
| Webs de los coautores | `content/coauthors.json` |
| Imagen asignada a cada página | `content/images.json` |
| Fotos, iconos y PDF | `public/assets/` |
| Colores, tamaños, posiciones y diseño responsive | `custom.css`; estilos base en `styles.css` |
| Modo claro/oscuro | `public/theme.js` y `custom.css` |
| Estadísticas (todavía sin activar) | `content/analytics.json` |

No edites `dist`: es el resultado generado y se sobrescribe al compilar. No se guarda en Git, porque se puede reconstruir. Edita los originales descritos arriba. Los archivos JSON requieren comillas dobles y no admiten comentarios ni una coma después del último elemento. Los textos con `html` permiten etiquetas como `<a href="...">texto</a>` y `<em>cursiva</em>`.

Para las novedades, cada entrada admite `label` (columna izquierda), `prefix` (texto antes del enlace), `title` (nombre enlazado), `url` y un `text` opcional. Se muestran en el orden del archivo. Puedes añadir más entradas o quitar las antiguas.

Para sustituir una foto, copia el nuevo archivo a `public/assets/` y cambia su ruta en `content/images.json`, por ejemplo `assets/nueva-foto.jpg`. Respeta mayúsculas y extensiones: GitHub distingue entre ellas. Conserva los originales si quieres reutilizarlos. Para cambiar el encuadre, busca la clase de esa foto en `custom.css`; en `object-position`, aumentar el porcentaje vertical muestra una zona más baja de la foto cuando se usa `cover`.

## Flujo de trabajo local

Abre una terminal dentro de `site` (en el Explorador puedes escribir `powershell` en la barra de dirección). Ejecuta:

```powershell
git pull
# Edita los archivos y guarda los cambios.
python build.py
python verify.py
python -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Abre http://127.0.0.1:8765/index.html. La terminal del servidor debe seguir abierta; Ctrl+C lo detiene. Si el puerto está ocupado por otro servidor, utiliza 8766 y cambia también el número en el enlace. La dirección 127.0.0.1 solo sirve en tu ordenador. Si `python` no existe en otro PC, instala Python desde python.org, o usa `py` si está disponible.

Cuando estés satisfecho, en otra terminal dentro de `site`:

```powershell
git status
git diff
git add .
git commit -m "Actualiza novedades y docencia"
git push
```

Revisa `git status` antes de `git add .` para no incluir archivos personales ajenos a la web. Guardar un archivo no crea un commit y hacer commit no lo sube: hace falta push. No subas contraseñas ni claves API privadas.

## GitHub sin terminal

En el repositorio puedes abrir un archivo y pulsar el lápiz para editarlo. `Commit changes` guarda una nueva versión. `Add file > Upload files` permite subir imágenes a su carpeta. Después ejecuta `git pull` en tu ordenador antes de seguir editando localmente.

En un archivo, `History` muestra sus cambios. En la página principal del repositorio, el historial de commits permite revisar versiones completas. GitHub Desktop es otra opción: abre esta carpeta con `Add local repository`, revisa los cambios, escribe un resumen, pulsa `Commit to main` y después `Push origin`. Para recibir cambios, usa `Fetch origin` / `Pull origin`.

Para experimentar sin afectar a `main`, crea una rama como `prueba-diseno`; al terminar puedes abrir una pull request y combinarla. Una rama es una línea de trabajo dentro del mismo repositorio, no una copia de seguridad externa.

## Recuperar una versión

```powershell
git log --oneline
git revert IDENTIFICADOR_DEL_COMMIT
git push
```

`revert` crea un nuevo commit que deshace el elegido y conserva el historial. Si hay conflictos, resuélvelos antes de continuar. Para una única foto o un archivo también puedes abrir su versión antigua en GitHub y volver a guardar ese contenido en una nueva versión. Evita `reset --hard` y `push --force` para este flujo habitual: pueden descartar trabajo o reescribir el historial.

## Copiar o mover la web a otra carpeta

Copia **toda la carpeta `site`**, incluida la carpeta oculta `.git`: contiene el historial local y la conexión con GitHub. Puedes renombrar la carpeta local sin cambiar el nombre del repositorio ni la futura dirección de la web. Abre una terminal en la nueva ubicación y ejecuta `python build.py`; todas las rutas del proyecto son relativas.

No mezcles la carpeta con otro repositorio existente ni copies solo `dist` si quieres seguir editando: `dist` es únicamente la web generada. Tras copiar, el servidor que estuviera abierto continúa sirviendo la carpeta antigua hasta que lo detengas y lo inicies desde la nueva.

Para otro ordenador, lo recomendable es **clonar**:

```powershell
git clone https://github.com/juanfranblazquizpulido/juanfranblazquizpulido.github.io.git
cd juanfranblazquizpulido.github.io
python build.py
```

Necesitarás iniciar sesión con una cuenta con acceso al repositorio privado. `Code > Download ZIP` descarga los archivos pero NO el historial `.git`. Conserva una única carpeta de trabajo habitual o sincroniza con pull/push si trabajas con varias.

## Cuando quieras publicar

En GitHub Free, este sitio de organización necesita un repositorio público para utilizar GitHub Pages. No cambies la visibilidad hasta decidir publicarlo: el código y el historial también quedarían visibles. Revisa antes los archivos e historial. Después configura `Settings > Pages > Source: GitHub Actions` y ejecuta el flujo de Pages. El flujo está preparado para saltarse el despliegue mientras el repositorio sea privado.

La dirección prevista es https://juanfranblazquizpulido.github.io/ . Guardar ahora un repositorio privado no activa esa dirección. Tener un repositorio privado tampoco implica que una futura web publicada sea privada. Las estadísticas son independientes y siguen pendientes de vincular Cloudflare.
