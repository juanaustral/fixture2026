# AkiraOS Dashboard

Backend FastAPI + Frontend React (Refine + shadcn + Tailwind v4).

## Directorio
- Backend: `/root/dashboard/backend/`
- Frontend: `/root/dashboard/frontend/`

## Puertos
- API: 127.0.0.1:8585
- Caddy: 144.91.81.173:8586 (sin auth en /api/*, con basic auth en frontend)

## Base de Datos
- SQLite: `/root/dashboard/data/dashboard.db`
- 7 modulos: Home, Notas, Finanzas, Listas, Calendario, Servicios, Akira

## Comandos
- Build frontend: `cd /root/dashboard/frontend && npm run build`
- Iniciar backend: `cd /root/dashboard && python3 -m backend.main`

## Variables
- CORS permite todos los origenes
- Basic auth en frontend: admin + bcrypt hash
- API sin auth
