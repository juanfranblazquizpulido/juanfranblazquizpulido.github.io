# Imagen de Teaching: cambio y restauración

El usuario aprobó probar `teaching-limit-original-darker.png` en la web.
La imagen anterior se conserva intacta en `public/assets/pizarra.png`.

Para volver a la anterior desde PyCharm:

1. Abre `content/images.json` y cambia el valor de `teaching` por
   `assets/pizarra.png`.
2. En `custom.css`, busca `.hero-teaching{isolation:isolate;` y cambia su
   fondo de `#3b3d3d` a `#595a57`, el color anterior de los laterales.
3. Ejecuta `build.py` y `verify.py`, revisa la web y haz Commit and Push.

La nueva imagen usa `object-fit:contain` para mostrarla completa también en
móvil. La zona de cabecera sobrante se rellena con el color de la pizarra.

Los roles se generan en el bucle de cursos de `build.py`: Course Instructor
para Introduction to microeconomics y Teaching Assistant para los demás.
Course Instructor expresa la responsabilidad docente de la asignatura, sin
implicar una categoría contractual como titular o catedrático.
