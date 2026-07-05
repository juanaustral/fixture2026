# Dashboard AkiraOS — Plan de Desarrollo

> **Para Hermes:** Usar subagent-driven-development para implementar este plan task por task.

**Goal:** Construir un dashboard personal todo-en-uno que funcione como centro de control de Juan: notas, finanzas, listas, calendario, conexiones MCP, servicios y archivos.

**Arquitectura:** Single-page application full-stack con backend en Python/FastAPI + frontend React con Refine + shadcn/ui. SQLite como base de datos principal. Desplegado en VPS Contabo via Caddy.

**Tech Stack:**
- Backend: FastAPI + SQLAlchemy/Database ORM + SQLite
- Frontend: React 19 + TypeScript + Vite
- Framework UI: Refine (35.2k stars, admin panel code-first) + shadcn/ui (118k stars)
- Base de Datos: SQLite (suficiente para uso personal, compatible con nuestro stack)
- Despliegue: Caddy reverse proxy en el VPS (:8586 o similar)

---

## Resumen de Investigacion

### Repos evaluados (los que paso Juan)
| Repo | Stars | Stack | Verdict |
|---|---|---|---|
| **Gentelella** | 21.4k | Bootstrap 5 | Template UI bonito, solo frontend. Inspiracion visual |
| **Glance** | 35.6k | Go/YAML | Dashboard de feeds minimalista. No apto para datos propios |
| **Dashbrd** | 43 | Bootstrap | Muy pequeño, descartado |

### Dashboard Templates (inspiracion visual)
| Proyecto | Stars | Por que importa |
|---|---|---|
| **AdminLTE** | 45.5k | Layout probado: sidebar + navbar + widgets + grids. Bootstrap 5 |
| **Volt Bootstrap 5** | 2.7k | Alternativa mas moderna |
| **Mazer** | 3k | Diseno limpio, sidebar compacta |

### Alternativas Notion-like (evaluadas y descartadas como base)
| Proyecto | Stars | Por que NO lo usamos como base |
|---|---|---|
| **AppFlowy** | 73.3k | Flutter+Rust, app nativa. No es web-first. Pesado de integrar |
| **NocoDB** | 63.7k | Airtable alternative. Buen backend de datos pero agrega complejidad |
| **Focalboard** | 26.3k | Trello-like. No reemplaza un dashboard general |

### Frameworks para construir el dashboard CUSTOM
| Framework | Stars | Verdict |
|---|---|---|
| **Refine** | 35.2k | **GANADOR**. React code-first. CRUD generado, auth, theming, real-time. MIT license |
| **shadcn/ui** | 118k | UI components copy-paste con Tailwind. Moderno, accesible, facil de modificar |
| **react-admin** | 26.8k | Similar a Refine pero UI fija (MUI). Menos flexible |
| Appsmith/Budibase | 28-40k | Low-code visual. No apto para personalizar a este nivel |

### Modulos externos que podemos INTEGRAR (via API/Bridge)
| Modulo | Proyecto | Stars | Stack | Como se integra |
|---|---|---|---|---|
| **Finanzas/Suscripciones** | Wallos | 8.2k | PHP+SQLite | Docker aparte, API REST. O construir modulo propio mas liviano |
| **Finanzas completo** | Actual Budget | 27.4k | JS+SQLite | Sync server con API. Pesado pero completo |
| **Finanzas completo** | Firefly III | 23.9k | PHP+MySQL | REST API madura. Muy completo pero PHP |
| **Listas Media** | Ryot | 3.4k | Rust+React+PostgreSQL | GraphQL API. Docker. Rastrea peliculas, series, juegos, libros |
| **Listas Media** | Watcharr | 1.4k | Go+SvelteKit | Docker. UI limpia. Solo media |
| **Notas** | SilverBullet | Ya instalado | Node.js | Ya lo tenemos en /var/notas/. API via Space Lua |
| **Calendario** | Custom | - | React | Componente propio con FullCalendar o similar |

**Decision:** Construir modulos de finanzas y listas PROPIOS (livianos, SQLite, integrados) en lugar de depender de servicios externos. Esto evita tener que mantener multiples servicios Docker.

---

## Modulos del Dashboard

1. **Home** — Resumen general, widgets personalizables, estadisticas rapidas
2. **Notas** — Integracion con SilverBullet (lectura de notas via API/filesystem)
3. **Finanzas** — Suscripciones, servicios mensuales, gastos, dashboard financiero
4. **Listas** — Peliculas, series, lugares, comidas. Base de datos editable tipo planilla
5. **Calendario** — Eventos, recordatorios, fechas de pago
6. **Conexiones MCP** — Servicios activos, status endpoints, configuracion
7. **Archivos** — Acceso a documentos BPS y recursos
8. **Servicios** — Health checks del VPS, cron jobs, estado de servicios

---

## Plan de Implementacion

### Fase 0: Setup del Proyecto
**Objetivo:** Inicializar la estructura base del proyecto

Archivos:
- Crear: `/root/dashboard/backend/`
- Crear: `/root/dashboard/frontend/`
- Crear: `/root/dashboard/.env`

Pasos:
1. Inicializar backend FastAPI con estructura de carpetas (routers/, models/, services/, db/)
2. Inicializar frontend Vite + React + TypeScript
3. Configurar Tailwind CSS + shadcn/ui
4. Configurar Refine con layout basico (sidebar + header + content)
5. Agregar a Caddy en puerto :8586

### Fase 1: Core — Layout Base + Autenticacion
**Objetivo:** Tener el layout funcional con navegacion lateral y autenticacion basica

Tareas:
1. Layout Refine con sidebar colapsable (iconos + labels)
2. Tema claro/oscuro (persistir en localStorage)
3. Sistema de autenticacion simple (usuario unico, password hasheado, JWT)
4. Pagina de login con diseno moderno
5. Dashboard Home con cards de resumen

### Fase 2: Modulo Base de Datos — Configuracion SQLite
**Objetivo:** Toda la data persistente en SQLite con migrations

Tareas:
1. Setup SQLAlchemy + SQLite en `/root/dashboard/backend/database/`
2. Migrations con Alembic
3. Modelos base: User, Service, Subscription, Movie, Series, Place, Note, Event
4. CRUD API generico con FastAPI (list, create, update, delete)

### Fase 3: Modulo Finanzas
**Objetivo:** Gestion de servicios, suscripciones y gastos mensuales

Tareas:
1. CRUD de servicios/subscripciones (nombre, monto, fecha vencimiento, categoria)
2. Dashboard financiero con graficos de gastos mensuales
3. Recordatorio de pagos proximos (badge "pago en 3 dias")
4. Historial de pagos
5. Total gasto mensual / anual

### Fase 4: Modulo Listas (Media + Lugares)
**Objetivo:** Base de datos de peliculas, series, lugares, comidas

Tareas:
1. CRUD de listas con campos customizables (tipo: movie/series/place/food)
2. Busqueda y filtros por tipo, estado, rating
3. Vista de tarjetas con poster/thumbnail (via TMDB API para media)
4. Vista de tabla para lugares/comidas
5. Importacion CSV basica

### Fase 5: Modulo Notas
**Objetivo:** Integracion con SilverBullet o notas en DB propia

Tareas:
1. Opcion A: Integracion via filesystem con /var/notas/ (lectura de archivos .md)
2. Opcion B: Editor de markdown propio con almacenamiento en SQLite
3. Listado de notas con busqueda
4. Vista de nota individual con renderizado markdown

### Fase 6: Modulo Calendario
**Objetivo:** Vista mensual con eventos y recordatorios

Tareas:
1. Integracion con FullCalendar React
2. CRUD de eventos
3. Marcadores automaticos: fechas de pago de servicios
4. Vista mensual, semanal, diaria

### Fase 7: Modulo Conexiones MCP + Servicios
**Objetivo:** Panel de monitoreo de servicios y conexiones

Tareas:
1. Listado de conexiones MCP activas (SuperMemory, Mattermost, etc.)
2. Health checks de servicios del VPS (Parda&Panda, SilverBullet, etc.)
3. Estado de cron jobs
4. Logs recientes de cada servicio

### Fase 8: Home Dashboard — Widgets Personalizables
**Objetivo:** Pagina principal con widgets configurables

Tareas:
1. Widgets: Resumen financiero, Proximos pagos, Notas recientes, Calendario mini
2. Layout drag-and-drop para reordenar widgets
3. Persistencia de configuracion de widgets por usuario

### Fase 9: Polish Final
**Objetivo:** Animaciones, transiciones, responsive, QA

Tareas:
1. Transiciones suaves entre paginas (Framer Motion)
2. Animaciones de carga (skeleton loaders)
3. Responsive design (mobile-friendly basico)
4. Modo offline parcial (PWA basics)
5. Prueba de integracion completa

---

## Archivos Clave

```
/root/dashboard/
├── backend/
│   ├── main.py                 # FastAPI app entry
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   └── migrations/         # Alembic
│   ├── routers/
│   │   ├── auth.py
│   │   ├── services.py         # Finanzas/services CRUD
│   │   ├── lists.py            # Listas CRUD
│   │   ├── notes.py
│   │   ├── calendar.py
│   │   └── mcp.py              # Conexiones MCP
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Refine app provider
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx   # Home con widgets
│   │   │   ├── Finance/
│   │   │   ├── Lists/
│   │   │   ├── Notes/
│   │   │   ├── Calendar/
│   │   │   └── Connections/
│   │   └── components/         # shadcn/ui components
│   ├── package.json
│   └── vite.config.ts
├── Caddyfile                    # Proxy :8586
└── docker-compose.yml           # Opcional
```

---

## Riesgos y Tradeoffs

1. **Refine lock-in:** Si Refine se vuelve demasiado opinado, podemos migrar a React puro + React Router. El uso de shadcn/ui hace que los componentes sean portables.
2. **SQLite concurrencia:** Para uso single-user no hay problema. Si en futuro quiere multi-usuario, migrar a PostgreSQL.
3. **Tiempo de desarrollo:** ~2-3 semanas trabajando intermitentemente. Priorizar modulos en orden de importancia.
4. **SilverBullet integracion:** Depende de que SilverBullet tenga API accesible. Alternativa: guardar notas en SQLite directamente.

---

## Lista de Tareas (para ejecucion)

### Setup Inicial
- [ ] F0.1: Inicializar backend FastAPI con estructura de carpetas
- [ ] F0.2: Inicializar frontend Vite + React + TypeScript + Tailwind
- [ ] F0.3: Instalar y configurar shadcn/ui
- [ ] F0.4: Configurar Refine con layout basico
- [ ] F0.5: Agregar Caddy reverse proxy para :8586

### Core
- [ ] F1.1: Layout Refine con sidebar y header
- [ ] F1.2: Toggle tema claro/oscuro
- [ ] F1.3: Autenticacion JWT (backend + frontend)
- [ ] F1.4: Pagina de login
- [ ] F1.5: Setup SQLite + SQLAlchemy + Alembic
- [ ] F1.6: Modelos base y CRUD API generico

### Finanzas
- [ ] F2.1: CRUD servicios/subscripciones
- [ ] F2.2: Dashboard financiero con graficos
- [ ] F2.3: Recordatorio pagos proximos
- [ ] F2.4: Historial de pagos

### Listas
- [ ] F3.1: CRUD de listas multi-tipo
- [ ] F3.2: Busqueda y filtros
- [ ] F3.3: Vista tarjetas con posters (TMDB)
- [ ] F3.4: Vista tabla para lugares/comidas

### Notas
- [ ] F4.1: Integracion con /var/notas/ o notas en SQLite
- [ ] F4.2: Editor markdown + renderizado
- [ ] F4.3: Busqueda de notas

### Calendario
- [ ] F5.1: FullCalendar React integrado
- [ ] F5.2: CRUD eventos
- [ ] F5.3: Marcadores automaticos de pagos

### Conexiones y Servicios
- [ ] F6.1: Listado conexiones MCP activas
- [ ] F6.2: Health checks servicios VPS
- [ ] F6.3: Estado cron jobs

### Home y Polish
- [ ] F7.1: Widgets personalizables en Home
- [ ] F7.2: Layout drag-and-drop
- [ ] F7.3: Animaciones (Framer Motion)
- [ ] F7.4: Skeleton loaders
- [ ] F7.5: Responsive design
- [ ] F7.6: QA final y deploy

---

**Verificacion final:** Acceder via https://juanmartinezgarcia.com:8586 (o el subdominio que elijamos), login, verificar que todos los modulos cargan, datos CRUD funcionan, y el dashboard Home muestra informacion correcta.
