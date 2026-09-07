# Novedades y estadísticas

## Editar News & updates

Edita `content/news.json`. Cada entrada tiene `date`, `title`, `text` y un `url` opcional. Se muestran en el orden del archivo: coloca primero las novedades más recientes. Ejemplo de formato (sustituye los textos antes de publicarlo):

```json
[
  {
    "date": "October 2026",
    "title": "Título de la novedad",
    "text": "Descripción breve en inglés para la web.",
    "url": "research.html#publications"
  }
]
```

Con `[]` se muestra una frase informativa, sin anuncios inventados. La sección aparece solo en Home, encima de Explore my research y Contact me.

## Activar las estadísticas

La integración está preparada, pero NO está activa mientras `cloudflare_token` esté vacío en `content/analytics.json`.

1. En tu cuenta de Cloudflare, abre Web Analytics y elige Add a site.
2. Introduce `juanfranblazquizpulido.github.io` (o el dominio definitivo).
3. En Manage site, copia el token del fragmento JavaScript: el valor de `token` dentro de `data-cf-beacon`. Es un identificador público del sitio, no una contraseña ni una clave API privada.
4. Pega ese valor en `cloudflare_token` en `content/analytics.json`. Si cambia el dominio, actualiza también `hostname`.
5. Ejecuta `python build.py` y publica la web. El flujo de GitHub Pages también ejecuta la compilación al publicar los cambios.
6. Consulta las estadísticas en tu panel privado de Cloudflare Web Analytics. Pueden tardar unos minutos en aparecer.

Solo se carga el contador en el hostname configurado: las visitas a localhost y las previsualizaciones no se cuentan. No hay estadísticas retroactivas. Bloqueadores o JavaScript desactivado pueden impedir registrar visitas.

El panel ofrece visitas, páginas vistas, país y enlaces de procedencia cuando están disponibles. No revela nombres, emails ni identidades de visitantes. Una visita no equivale necesariamente a una persona distinta.

Documentación oficial: https://developers.cloudflare.com/web-analytics/get-started/
Dimensiones disponibles: https://developers.cloudflare.com/web-analytics/data-metrics/dimensions/
