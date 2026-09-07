# Juan Francisco Blázquiz Pulido — academic website

Repositorio privado de la web académica, con historial de versiones. La web todavía no está publicada en Internet.

Consulta [GUIA_GITHUB.md](GUIA_GITHUB.md) para editar textos, fotos y estilos, previsualizar la web, copiar la carpeta, usar GitHub y recuperar versiones. Esta es la guía actual en castellano. [EDITING_GUIDE.md](EDITING_GUIDE.md) conserva notas de diseño anteriores; algunas quedaron sustituidas por los ajustes posteriores.

## Compilar y ver localmente

Dentro de esta carpeta, con Python 3:

```sh
python build.py
python verify.py
python -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Abre http://127.0.0.1:8765/index.html. `dist` es generado y no se guarda en Git. No lo edites directamente.

## Contenido y fotos

Cinco páginas: Home, Research, Teaching, CV y Contact. Se conservan los textos académicos, conferencias, seminarios, docencia, CV, los dos emails y la dirección española. Las siete redes sociales están en `content/socials.json`.

- Home: Explanada y retrato BlazquizJ.
- Research: defensa, versión sin fecha; se conserva el original.
- Teaching: pizarra con laterales del mismo color.
- CV: campus de IMT.
- Contact: castillo de Alicante en cabecera y foto de la UA a la derecha.

Las asignaciones están en `content/images.json`. Las fotos usadas y las reservadas se guardan en `public/assets/`.

## GitHub y publicación

El repositorio `juanfranblazquizpulido/juanfranblazquizpulido.github.io` es privado. El historial comienza con el estado actual; no reconstruye las ediciones anteriores.

El flujo de Pages omite el despliegue mientras el repositorio sea privado. Publicar en GitHub Pages con el plan gratuito requerirá decidir hacer público el repositorio, revisar los archivos y configurar Settings > Pages > GitHub Actions. La dirección prevista es https://juanfranblazquizpulido.github.io/ .

Cloudflare Web Analytics está preparado pero desactivado: falta el token del sitio. Consulta [NEWS_AND_ANALYTICS.md](NEWS_AND_ANALYTICS.md). No se muestra ningún contador público.