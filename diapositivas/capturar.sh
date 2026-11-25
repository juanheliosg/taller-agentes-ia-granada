#!/bin/bash
# Regenera capturas/diapositivas.pdf y capturas/sNN.png con Chrome headless.
# Uso: ./capturar.sh "$PWD" [número de diapositivas, por defecto 24]
# Chrome falla a veces al paginar; por eso reintenta hasta obtener ese número de páginas.
set -e
D="$1"; cd "$D"
for t in 1 2 3 4 5 6 7 8; do
  /usr/bin/google-chrome --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=10000 \
    --print-to-pdf=capturas/diapositivas.pdf "file://$PWD/index.html?print-pdf" 2>/dev/null
  n=$(pdfinfo capturas/diapositivas.pdf | awk '/Pages/{print $2}')
  [ "$n" -eq "${2:-24}" ] && break
done
echo "Páginas: $n"
rm -f capturas/s*.png
pdftoppm -png -scale-to-x 1280 -scale-to-y 720 capturas/diapositivas.pdf capturas/tmp
i=0; for f in $(ls capturas/tmp-*.png | sort -V); do mv "$f" "capturas/s$(printf %02d $i).png"; i=$((i+1)); done
