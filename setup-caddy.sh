#!/bin/sh
# Añadir ruta al Caddyfile existente
CADDYFILE="/etc/caddy/Caddyfile"
LINE="localhost:8587"
if grep -q "$LINE" "$CADDYFILE" 2>/dev/null; then
  echo "Ya existe una entrada para :8587"
else
  # Insertar antes del último bloque cerrando }
  sed -i '$i\
\
localhost:8587 {\
\troot * /root/dashboard\
\tfile_server\
}\
' "$CADDYFILE"
  echo "Entrada añadida a Caddyfile"
fi

# Recargar Caddy
caddy reload --config /etc/caddy/Caddyfile 2>/dev/null || caddy fmt /etc/caddy/Caddyfile --overwrite && systemctl reload caddy 2>/dev/null
echo "Hecho"
