# Diapositivas del taller

Presentación en reveal.js 5.1.0, vendorizado en `vendor/`. Funciona sin conexión: basta con abrir `index.html` en el navegador (Chrome o Firefox) con doble clic.

## Estructura

- `index.html`: todas las diapositivas, en orden.
- `tema.css`: el único fichero de estilo. Colores, fuentes y tamaños están como variables al principio (`--acento`, `--tam-cuerpo`…).
- `img/`: imágenes (`cartel-j2-informatica.jpg`: cartel de las Jornadas por Palestina, en sRGB y reducido).
- Los vídeos no se incluyen (derechos de terceros): la diapositiva enlaza a youtube.com/shorts/akcSX81KOv4 e instagram.com/reel/DdUvJkjy8xk.
- `img/qr-repo.svg`, `img/qr-substack.svg`: códigos QR generados con `segno`.
- `fonts/`: Source Serif 4 y Source Sans 3 (woff2, licencia OFL).
- `capturas/`: capturas de cada diapositiva con todos los fragmentos visibles.

## Editar el texto

Casi todas las diapositivas son Markdown:

```html
<section data-markdown data-separator-notes="^Note:">
<textarea data-template>
## Título de la diapositiva

- Un punto
- Otro punto que aparece al pulsar <!-- .element: class="fragment" -->

Note:
Lo que dirá el ponente. Solo se ve en la vista del ponente.
</textarea>
</section>
```

- Escribe el Markdown pegado al margen izquierdo, sin sangría.
- La virgulilla `~` dos veces en la misma línea se convierte en tachado: escríbela como `\~`.
- Las diapositivas con diagrama o animación compleja son HTML/SVG: «Qué es un LLM», «El contexto decide la palabra», «La zona estúpida», «Buscando una solución token a token», «Agente = LLM + arnés + herramientas», «Ejemplo de llamada a una herramienta» y «La fábrica de software». Busca los comentarios `<!-- EDITA AQUÍ -->`.
- En las barras de probabilidad, el ancho de cada barra se pone a mano en `style="width:…%"` (está explicado en el comentario de cada una).

## Añadir una diapositiva

Copia un bloque `<section data-markdown …> … </section>` completo, pégalo donde quieras que aparezca y cambia el texto. Para un título grande centrado verticalmente (portada), añade `class="portada"` al `<section>` y usa `#` en vez de `##`.

## Presentar

- Flechas o espacio para avanzar; `F` pantalla completa; `Esc` vista general.
- `S` abre la vista del ponente en otra ventana (reloj y siguiente diapositiva; esta copia pública no incluye las notas del ponente). Si el navegador bloquea la ventana emergente, permítela para este fichero.

## Exportar a PDF

Atajo: `./capturar.sh "$PWD"` desde `diapositivas/` regenera el PDF y las capturas `capturas/sNN.png`.

A mano:


1. Abre `index.html?print-pdf` en Chrome (añade `?print-pdf` antes de `#` en la barra de direcciones).
2. Imprimir → Guardar como PDF, orientación horizontal, márgenes «Ninguno», con «Gráficos de fondo» activado.

El PDF muestra cada diapositiva en su estado final (todos los fragmentos visibles). Para una página por fragmento, cambia `pdfSeparateFragments: false` a `true` en `index.html`.

Con decktape instalado (`npm i -g decktape`) también funciona: `decktape reveal index.html diapositivas.pdf --size 1280x720`.
