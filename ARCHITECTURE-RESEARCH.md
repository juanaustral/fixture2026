# AI Workspace OS -- Investigacion Estrategica y Propuesta de Arquitectura

> Autor: Akira | Fecha: 2026-07-04
> Contexto: Diseno del sistema operativo personal para trabajar junto a agentes de IA

---

## Indice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Estado del Arte: Proyectos Analizados](#2-estado-del-arte)
   - 2.1 AI Operating Systems
   - 2.2 Plataformas de Agentes
   - 2.3 Inspiracion de UX
3. [Analisis Comparativo por Dimensiones](#3-analisis-comparativo)
4. [Matriz de Puntuacion](#4-matriz-de-puntuacion)
5. [Tendencias y Patrones Emergentes](#5-tendencias)
6. [Propuesta: Arquitectura Nova](#6-propuesta-arquitectura-nova)
7. [Roadmap de Implementacion](#7-roadmap)
8. [Integracion con Hermes](#8-integracion-con-hermes)

---

## 1. Resumen Ejecutivo

### El problema

El ecosistema actual de herramientas de IA esta fragmentado. Existen:

- **Chatbots** que no entienden de proyectos (ChatGPT, Claude web)
- **Plataformas de agentes** que no tienen UI de productividad (CrewAI, AutoGen)
- **Plataformas visuales** que no entienden de codigo (Dify, Flowise, Langflow)
- **IDEs con IA** que no gestionan vida personal (VS Code + Copilot)
- **Gestores de conocimiento** que no tienen agentes (Obsidian, Notion)
- **Dashboards tecnico** que no tienen IA (Grafana, Portainer)

Ningun proyecto resuelve el problema completo.

### La tesis

El AI Workspace OS no es un chat, ni un IDE, ni un dashboard. Es un **sistema operativo centrado en proyectos** donde los agentes de IA son un componente mas, no el centro.

La conversacion no es la unidad fundamental. **El proyecto es la unidad fundamental.**

### Hallazgos clave de la investigacion

| Proyecto | Stars | Que resuelve mejor | Que falta |
|----------|-------|-------------------|-----------|
| Dify | 147k | Workflows visuales + RAG + LLMOps | Sin agentes personales, sin integracion DevOps |
| Langflow | 151k | Componentes visuales + API/MCP servers | Sin UX de productividad, sin gestion de proyectos |
| Flowise | 54k | Agentes visuales low-code | Sin memoria persistente, sin observabilidad |
| OpenHands | 79k | Control center para coding agents | Solo dev, sin vida personal, sin conocimiento |
| CrewAI | 55k | Orquestacion multi-agente | Sin UI (solo Python), sin workspace |
| AutoGen | 59k | Framework multi-agente (en mantenimiento) | Sin producto, solo libreria |
| LangGraph | 36k | Orquestacion stateful + memoria durable | Sin UI, solo framework |
| holaOS | 5.5k | Working agent con memoria + workspace | Solo macOS, ecosistema cerrado |
| Goodable | 188 | Desktop AI workspace con skills | Muy temprano, poco adoption |
| Mem0 | 60k | Capa de memoria universal para agentes | Solo memoria, no es un OS |
| Letta | 23.6k | Agentes stateful con aprendizaje continuo | Framework, no producto |

---

## 2. Estado del Arte

### 2.1 AI Operating Systems

#### holaOS (5.5k stars) -- El mas cercano a la vision

**Filosofia:** "Your super agent for work: local-first, learn your working context in mins and never forget it."

**Arquitectura:**
- Electron desktop app (TypeScript)
- Runtime portable desacoplado del desktop
- Sistema de workspaces con archivos locales
- Memory Tree + SQLite vec embeddings + RAG
- Session Context Compression (70% contexto fresco, 30% historico)
- Agent Harness con ejecutores intercambiables
- 100+ integraciones OAuth

**Lo mejor:**
- Memoria como archivos Markdown editables -- transparente y bajo control del usuario
- Session compaction inteligente que preserva coherencia en sesiones largas
- Un solo agente visible orquesta subagentes ocultos
- Local first real -- los datos no salen de tu maquina

**Lo peor:**
- Solo macOS (Win/Linux "in progress")
- Licencia Modified Apache 2.0 (restrictiva)
- Ecosistema cerrado -- no hay plugins de terceros
- No tiene gestion de proyectos, roadmap, tareas
- Enfocado en "working agent" no en "personal OS"

#### Goodable (188 stars)

**Filosofia:** Desktop AI Workstation para "super individuos" (Chinese market).

**Arquitectura:**
- Electron + Claude Agent SDK
- Skills system (dual mode: AI-triggered + GUI app)
- Python + Node.js runtime embebido
- Desktop + browser + coding capabilities

**Lo mejor:**
- Skills en dos modos: automatico (agente) y manual (app grafica)
- Publicacion one-click a cloud (Aliyun)
- Multiples "digital employees" predefinidos

**Lo peor:**
- Muy temprano (188 stars)
- Dependencia de Claude Agent SDK
- Enfocado en mercado Chino
- Sin ecosistema de plugins

#### OpenHands Agent Canvas (79k stars, ex-OpenHands)

**Filosofia:** "The self-hosted developer control center for coding agents and automations."

**Arquitectura:**
- Frontend web + Agent Server REST API + Automation Server
- Soporta ACP (Agent-Client Protocol) para agentes externos
- Arquitectura multibackend: local, Docker, VM, cloud
- Automations con schedule + webhooks

**Lo mejor:**
- Arquitectura desacoplada frontend/backend con servidores intercambiables
- Protocolo ACP como estandar abierto para agentes
- Automations como concepto first-class (schedule + webhook)
- Docker sandbox para ejecucion segura

**Lo peor:**
- Solo coding agents -- no hay vida personal, conocimiento, finanzas
- Sin memoria persistente del usuario
- Sin workspace de productividad
- Sin integracion con herramientas no-dev

---

### 2.2 Plataformas de Agentes

#### Dify (147k stars)

**Filosofia:** "LLM app development platform" -- no-code/low-code para construir aplicaciones con AI.

**Arquitectura:**
- Frontend Next.js + Backend Python (Flask)
- Workflow engine visual con nodos
- RAG pipeline completo
- Agent builder con Function Calling / ReAct
- LLMOps: monitoreo, logs, analiticas
- Backend-as-a-Service con API REST
- Docker Compose deployment

**Modulos clave:**
1. Workflow builder visual
2. Prompt IDE con comparacion de modelos
3. RAG pipeline (ingestion + retrieval)
4. Agent builder (tools + models)
5. LLMOps (monitoreo + analiticas)
6. Model providers (100+ modelos)
7. Plugin system (50+ built-in tools)

**Lo mejor:**
- Workflow engine visual mas maduro del ecosistema open-source
- LLMOps integrado (logs, costos, rendimiento)
- RAG pipeline completo out-of-the-box
- Provider agnostic (100+ modelos)

**Lo peor:**
- Sin concepto de "proyecto" personal
- Sin memoria de agente persistente
- Sin integracion DevOps/Git
- Chat-centric (no project-centric)
- Sin plugin system extensible (solo tools predefinidas)

#### Langflow (151k stars)

**Filosofia:** "Build and deploy AI-powered agents and workflows" -- visual + Python components.

**Arquitectura:**
- Python backend con React Flow
- Componentes visuales arrastrables
- API y MCP server built-in
- Multi-agent orchestration
- Playground interactivo
- Desktop app (Electron)

**Lo mejor:**
- API Server + MCP Server built-in (cada workflow es una tool)
- Componentes accesibles via Python (codigo abierto)
- Playground con step-by-step control
- Observability integrations (LangSmith, LangFuse)

**Lo peor:**
- Sin concepto de proyecto o workspace
- Sin memoria persistente
- Sin UX de productividad (notas, tareas, calendario)
- Sin agentes autonomos (todo es triggered por usuario)

#### Flowise (54k stars)

**Filosofia:** "Build AI Agents, Visually."

**Arquitectura:**
- Node.js backend + React frontend
- Components como paquetes npm instalables
- Chatflows + Agentflows
- API endpoints automaticos

**Lo mejor:**
- Componentes como paquetes npm (extensibilidad real)
- Multi-tenant con API key
- Chatflow + Agentflow como conceptos separados

**Lo peor:**
- Sin memoria persistente
- Sin observabilidad built-in
- Sin workspace o proyectos
- UI menos pulida que Dify

#### CrewAI (55k stars)

**Filosofia:** "Framework for orchestrating role-playing, autonomous AI agents."

**Arquitectura:**
- Libreria Python con abstracciones:
  - Agent (role, goal, backstory, tools)
  - Task (description, expected_output, agent)
  - Crew (agents + tasks + process)
  - Flow (event-driven automation)
- Crew Control Plane (SaaS) para tracing + observabilidad

**Lo mejor:**
- Modelo de agente con role/goal/backstory -- narrativo, facil de entender
- Crews + Flows separan colaboracion de orquestacion
- Skills para Claude Code/Cursor (patron de externalizacion)
- AMP Suite para enterprise

**Lo peor:**
- Sin UI (solo Python library)
- Sin persistencia nativa (requiere memoria externa)
- Sin concepto de workspace o proyecto
- El "crew" no esta atado a proyectos reales

#### AutoGen / Microsoft Agent Framework (59k stars)

**Filosofia:** "A programming framework for agentic AI."

**Arquitectura:**
- AgentChat API (alta)
- Core API (baja)
- Multi-agent orchestration
- MCP integration nativa
- AutoGen Studio (no-code GUI)

**Lo mejor:**
- Soporta A2A + MCP (interoperabilidad cross-runtime)
- AgentTool para anidar agentes como tools de otros agentes
- MCP Workbench para gestion de servers MCP
- Modelo de agentes conversacionales bien definido

**Lo peor:**
- En mantenimiento -- migrando a MAF
- Sin workspace, sin proyectos
- Sin memoria de largo plazo
- Framework, no producto

#### LangGraph (36k stars)

**Filosofia:** "Low-level orchestration framework for building stateful agents."

**Arquitectura:**
- Graph-based execution engine (inspirado en Pregel + Apache Beam + NetworkX)
- State management con checkpoints
- Durable execution (persistencia ante fallos)
- Human-in-the-loop (interrupts)
- Comprehensive memory (working + long-term)
- LangSmith para debugging y observabilidad
- LangGraph Platform para deployment

**Lo mejor:**
- Graph como modelo universal de computacion para agentes
- Durable execution -- los agentes sobreviven crashes
- Checkpointing automatico del estado
- Subgraphs para composicion jerarquica
- LangSmith para tracing visual

**Lo peor:**
- Solo framework -- sin UI, sin producto
- Curva de aprendizaje alta (grafos + state machines)
- Sin conceptos de proyecto, workspace, memoria personal
- Dependencia del ecosistema LangChain

---

### 2.3 Inspiracion de UX

#### Obsidian (UX aprendido)
- **Local first real** -- archivos Markdown en tu filesystem
- **Graph view** como navegacion alternativa
- **Plugin system** masivo (1500+ plugins) con API completa
- **Obsidian Sync** como servicio premium (no bloquea funcionalidad local)
- **Canvas** para pensamiento visual

#### VS Code (UX aprendido)
- **Command Palette** (Cmd+Shift+P) como acceso universal
- **Activity Bar** como navegacion primaria (iconos + sidebar contextual)
- **Split panes** jerarquicos (editor, sidebar, panel, status bar)
- **Extensions** como ciudadanos de primera clase
- **Workspace** como unidad de contexto

#### Linear (UX aprendido)
- **Project-centric** -- todo gira alrededor de proyectos
- **Keyboard-first** -- nunca necesitas el mouse
- **Command K** como acceso universal
- **Roadmap visual** con timelines
- **Triage** como workflow para nuevos items

#### Notion (UX aprendido)
- **Blocks** como unidad universal de contenido
- **Databases** como estructuras flexibles (tabla, board, calendar, gallery, list)
- **Templates** para acelerar creacion
- **Linked databases** para relaciones entre proyectos

#### Home Assistant (UX aprendido)
- **Lovelace UI** -- dashboard completamente customizables
- **Integrations** como capa de abstraccion
- **Automations** con triggers + conditions + actions
- **History & Logs** para todo evento

#### Grafana (UX aprendido)
- **Panels** como bloques de construccion visual
- **Dashboards** como colecciones de paneles
- **Data sources** intercambiables sin cambiar visualizacion
- **Alerting** con notificaciones multi-canal
- **Explore** para queries ad-hoc

#### Portainer (UX aprendido)
- **Environments** como abstraccion de infraestructura
- **Stacks** como aplicaciones completas (Docker Compose)
- **Status badges** visibles en toda la UI
- **Quick actions** para operaciones frecuentes

#### Raycast (UX aprendido)
- **Extensions** como mini-aplicaciones
- **Quicklinks** para acciones frecuentes
- **Store** como descubrimiento de extensions
- **Floating window** para acceso instantaneo

---

## 3. Analisis Comparativo por Dimensiones

### 3.1 Filosofia

| Proyecto | Paradigma | Unidad fundamental |
|----------|-----------|-------------------|
| Dify | App development | Workflow |
| Langflow | Visual building | Componente |
| Flowise | Visual building | Chatflow |
| OpenHands | Coding control center | Conversation |
| CrewAI | Role-playing agents | Crew |
| AutoGen | Agentic programming | Agent |
| LangGraph | Stateful orchestration | Graph |
| holaOS | Working agent | Workspace |
| Goodable | Desktop AI workstation | Skill |
| Mem0 | Memory layer | Memory |
| Letta | Stateful agents | Agent |

### 3.2 Arquitectura

| Proyecto | Stack | Frontend | Backend | DB |
|----------|-------|----------|---------|-----|
| Dify | Python/TS | Next.js | Flask | PostgreSQL + Redis |
| Langflow | Python | React Flow | FastAPI | SQLite/PostgreSQL |
| Flowise | Node.js | React | Express | SQLite/PostgreSQL |
| OpenHands | Python/TS | React | FastAPI | SQLite |
| CrewAI | Python | None (CLI) | Library | None |
| AutoGen | Python | React (Studio) | Library | None |
| LangGraph | Python | None | Library | LangGraph Platform |
| holaOS | TypeScript | Electron/React | Express | SQLite + SQLite vec |
| Mem0 | Python | None | Library/FastAPI | Qdrant/Chroma/PG |
| Letta | Python | React | FastAPI | PostgreSQL |

### 3.3 Memoria

| Proyecto | Tipo de memoria | Storage | RAG | Editable |
|----------|----------------|---------|-----|----------|
| Dify | Conversation | Redis/DB | Solo RAG docs | No |
| Langflow | Conversation window | En memoria | No | No |
| Flowise | Conversation window | En memoria | No | No |
| OpenHands | Session | En memoria | No | No |
| CrewAI | Entity + Short-term | En memoria/opcional | No | No |
| AutoGen | Conversation history | En memoria | No | No |
| LangGraph | Working + Long-term | Checkpoints + Store | Si | No |
| holaOS | Memory Tree + RAG | Markdown + SQLite vec | Si | Si (Markdown) |
| Mem0 | Universal memory layer | Vector DB | Si | API |
| Letta | Core + Archival + Recall | PostgreSQL + Vector | Si | API |

### 3.4 Sistema de Plugins

| Proyecto | Plugins | Como funciona |
|----------|---------|---------------|
| Dify | Solo tools predefinidas | 50+ built-in, no extensible por terceros |
| Langflow | Componentes Python | Cada componente es codigo Python accesible |
| Flowise | Paquetes npm | Components instalables via npm |
| OpenHands | No | Agentes externos via ACP |
| CrewAI | Skills | Skills para Claude Code/Cursor |
| AutoGen | No | Extensiones via paquetes |
| LangGraph | No | Integraciones via LangChain |
| holaOS | No (integraciones OAuth) | Apps via workspace APIs |
| Obsidian | Plugin API completa | 1500+ plugins, API de comunidad |

---

## 4. Matriz de Puntuacion

> Escala: 1-10 (10 = mejor en su clase)

| Dimension | Dify | Langflow | Flowise | OpenHands | CrewAI | AutoGen | LangGraph | holaOS | Obsidian |
|-----------|------|----------|---------|-----------|--------|---------|-----------|--------|----------|
| **Arquitectura** | 8 | 7 | 6 | 8 | 7 | 7 | 9 | 7 | 7 |
| **UX** | 8 | 7 | 6 | 7 | 3 | 4 | 3 | 8 | 9 |
| **Modularidad** | 6 | 8 | 7 | 7 | 8 | 7 | 9 | 6 | 8 |
| **Plugins** | 4 | 7 | 7 | 5 | 6 | 5 | 5 | 4 | 10 |
| **Escalabilidad** | 8 | 7 | 6 | 7 | 6 | 7 | 9 | 4 | 6 |
| **Diseno** | 7 | 6 | 5 | 6 | 3 | 3 | 2 | 8 | 9 |
| **Experiencia usuario** | 7 | 7 | 6 | 6 | 4 | 4 | 3 | 7 | 9 |
| **Gestion proyectos** | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 4 | 5 |
| **Gestion conocimiento** | 7 | 5 | 4 | 3 | 2 | 2 | 2 | 6 | 9 |
| **Agentes** | 7 | 7 | 7 | 9 | 8 | 8 | 9 | 7 | 1 |
| **Memoria** | 4 | 3 | 2 | 2 | 4 | 3 | 7 | 8 | 4 |
| **Automatizacion** | 9 | 8 | 7 | 8 | 7 | 7 | 8 | 5 | 2 |
| **Observabilidad** | 8 | 6 | 4 | 5 | 5 | 4 | 8 | 3 | 1 |
| **Infraestructura** | 5 | 5 | 5 | 7 | 3 | 3 | 5 | 3 | 2 |
| **Desarrollo software** | 5 | 4 | 4 | 9 | 6 | 6 | 7 | 4 | 2 |
| **Uso personal** | 3 | 3 | 3 | 3 | 2 | 2 | 2 | 6 | 9 |
| **Uso profesional** | 8 | 7 | 6 | 8 | 7 | 7 | 8 | 5 | 6 |
| **Potencial futuro** | 7 | 8 | 6 | 8 | 8 | 5 | 9 | 7 | 6 |

---

## 5. Tendencias y Patrones Emergentes

### 5.1 Patrones que se repiten en todos los proyectos

**1. Graph-based execution como modelo universal**
LangGraph, Dify (workflow), CrewAI (Flows), Langflow (React Flow) -- todos convergen en grafos como modelo de computacion para agentes. Los agentes no son lineales, son grafos de estados y transiciones.

**2. Memory como capa separada**
Mem0 (60k stars), Letta (23.6k), holaOS Memory Tree, LangGraph Store -- la memoria se esta convirtiendo en un componente independiente, no embebido en el agente.

**3. MCP como protocolo de integracion estandar**
MCP servers estandarizados (codebase-memory-mcp 26k, fastmcp 26k, 16k+ servers en registry). MCP es el "USB-C" de las herramientas de IA.

**4. ACP como protocolo de agentes**
OpenHands con ACP, Claude Code ACP, Codex ACP -- los agentes se estandarizan en un protocolo de cliente-agente.

**5. Local-first como requisito**
holaOS, Obsidian, Goodable -- los usuarios exigen que sus datos queden en su maquina. Cloud-only es cada vez menos aceptado.

**6. Workspace como unidad de contexto**
VS Code (workspace), holaOS (workspace con archivos), OpenHands (sandbox por proyecto) -- el workspace es el limite de contexto del agente.

**7. Skills como mecanismo de extension**
CrewAI Skills, Goodable Skills, Claude Code Skills, Cursor Rules -- skills son instrucciones estructuradas que ensenan al agente a hacer algo especifico.

**8. Session compaction para sesiones largas**
holaOS con Safe Session Compaction, LangGraph con checkpoints -- mantener coherencia en sesiones de dias requiere compresion inteligente.

**9. Visual builders con codigo accesible**
Langflow (Python components), Flowise (npm packages), Dify (workflow visual) -- lo visual no reemplaza el codigo, lo complementa.

**10. Multi-backend agnostic**
OpenHands (local/Docker/VM/cloud), Dify (100+ modelos), holaOS (multi-model) -- desacoplar el frontend del backend de ejecucion.

### 5.2 Estandares emergentes

| Estandar | Proposito | Quien lo impulsa | Proyectos que lo usan |
|----------|-----------|------------------|----------------------|
| **MCP** | Tools & resources | Anthropic | Claude, Cursor, Windsurf, VS Code |
| **ACP** | Agent-client protocol | OpenHands | OpenHands, Claude Code, Codex |
| **A2A** | Agent-to-agent | Google | MAF, LangGraph |
| **OpenAI-compatible API** | Model access | OpenAI | Todos |
| **OpenTelemetry** | Observability | CNCF | Dify, Langfuse |

### 5.3 Tecnologias dominantes

- **TypeScript** para frontends (Next.js, React, Electron)
- **Python** para backends de agentes (FastAPI)
- **SQLite** como base de datos local por defecto
- **Vector DBs** (SQLite vec, Qdrant, Chroma, PGVector)
- **Docker** para aislamiento y ejecucion
- **WebSocket/SSE** para streaming de agentes

---

## 6. Propuesta: Arquitectura Nova

### 6.1 Filosofia

**Nova es un sistema operativo personal centrado en proyectos, donde los agentes de IA trabajan para vos, no con vos.**

Principios fundamentales:

1. **Project-Centric** -- la conversacion no es la unidad fundamental. El proyecto lo es. Cada proyecto tiene su propia memoria, agentes, archivos, tareas y objetivos.

2. **Local-First con sync opt-in** -- todos los datos viven en tu maquina. Sincronizar a cloud es optativo y premium.

3. **Modular por diseno** -- cada modulo es independiente. Podes tener solo el modulo de notas sin agentes, o solo el de agentes sin notas.

4. **El workspace es el sandbox** -- cada proyecto/workspace es un entorno aislado con sus propios archivos, memoria y agentes.

5. **Agent-in-the-loop, no human-in-the-loop** -- los agentes trabajan en background. El humano revisa resultados, no dirige procesos.

6. **Todo observable** -- cada accion de agente, cada cambio, cada costo queda registrado y visible.

7. **Plugins como ciudadanos de primera clase** -- el sistema se extiende via plugins con API completa.

### 6.2 Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                          │
│  Desktop App (Electron/Tauri)  │  Web UI  │  Mobile Web    │
│  Command Palette  │  Activity Bar  │  Split Panes         │
├─────────────────────────────────────────────────────────────┤
│                    WORKSPACE LAYER                          │
│  Project Manager  │  Navigator  │  Search (FTS + Vector)   │
│  Knowledge Graph  │  Timeline   │  Dashboard Builder       │
├─────────────────────────────────────────────────────────────┤
│                    MODULE LAYER                             │
│  Notes  │  Tasks  │  Calendar  │  Finance  │  Services     │
│  Git    │  Docker  │  MCP/MCP  │  DevOps  │  Monitoring    │
├─────────────────────────────────────────────────────────────┤
│                    AGENT LAYER                              │
│  Agent Manager  │  Agent Runtime  │  Subagent Orchestrator │
│  Tool Registry  │  Skill System   │  Session Compactor     │
├─────────────────────────────────────────────────────────────┤
│                    MEMORY LAYER                             │
│  Working Memory  │  Project Memory  │  Long-term Memory    │
│  Vector Store    │  Knowledge Graph DB  │  FTS Index        │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                               │
│  SQLite  │  SQLite Vec  │  Filesystem (Markdown, JSON)     │
│  Redis (opcional)  │  S3 (opcional sync)                   │
├─────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE LAYER                     │
│  Docker  │  MCP Servers  │  Git  │  Cron  │  Webhooks      │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Modelo de Datos

#### Proyecto (unidad fundamental)

```typescript
interface Project {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'paused' | 'archived';
  type: 'personal' | 'dev' | 'research' | 'work' | 'finance';
  
  // Jerarquia
  parentId?: string; // subproyectos
  children: string[]; // proyectos hijos
  
  // Objetivos
  objectives: Objective[];
  roadmap: Milestone[];
  
  // Memoria del proyecto
  memory: ProjectMemory;
  
  // Agentes asignados
  agents: AgentAssignment[];
  
  // Contexto
  workspace: WorkspaceConfig; // sandbox path, env vars
  integrations: Integration[];
  
  // Metadata
  created: Date;
  updated: Date;
  tags: string[];
  
  // Metricas
  tokenUsage: TokenUsage;
  totalCost: number;
}
```

#### Agente

```typescript
interface Agent {
  id: string;
  name: string;
  role: string; // "developer", "researcher", "assistant"
  model: ModelConfig;
  
  // Comportamiento
  instructions: string; // system prompt
  skills: string[]; // loaded skills
  tools: string[]; // available MCP tools
  
  // Memoria
  memory: AgentMemory; // working + project + long-term
  
  // Ejecucion
  mode: 'interactive' | 'background' | 'scheduled' | 'event';
  schedule?: CronSchedule;
  
  // Límites
  maxIterations: number;
  maxTokensPerRun: number;
  maxCostPerRun: number;
  
  // Observabilidad
  sessions: AgentSession[];
  totalTokens: number;
  totalCost: number;
}
```

#### Memoria

```typescript
interface MemoryStore {
  // Working Memory (sesion activa)
  working: {
    currentTask: string;
    context: ContextWindow;
    recentHistory: Message[];
    state: Record<string, any>; // checkpoint
  };
  
  // Project Memory (persistente, compartida entre sesiones)
  project: {
    knowledge: Document[]; // RAG-indexed markdown
    decisions: Decision[];
    learnings: Learning[];
    artifacts: Artifact[];
  };
  
  // Long-term Memory (cross-project)
  longTerm: {
    userProfile: UserProfile;
    patterns: Pattern[];
    preferences: Preference[];
    skills: MasteredSkill[];
  };
  
  // Archival Memory (comprimida)
  archival: {
    compressedSessions: CompressedSession[];
    embeddings: VectorStore;
  };
}
```

#### Skill

```typescript
interface Skill {
  id: string;
  name: string;
  description: string;
  version: string;
  
  // Instrucciones estructuradas
  instructions: string; // markdown con frontmatter
  triggers: string[]; // cuando se activa automaticamente
  
  // Recursos
  tools: ToolDefinition[];
  templates: Template[];
  scripts: Script[];
  
  // Dependencias
  requires: string[]; // otros skills
  conflicts: string[];
}
```

### 6.4 Modulos

#### Modulos Core (siempre presentes)

| Modulo | Funcion | Inspirado en |
|--------|---------|--------------|
| **Home** | Dashboard principal con resumen de todo | Grafana + Linear |
| **Projects** | Gestion de proyectos, roadmap, milestones | Linear |
| **Notes** | Editor markdown con graph view + backlinks | Obsidian |
| **Tasks** | Kanban + lista + calendario | Linear + Notion |
| **Chat** | Conversaciones con agentes por proyecto | Claude + ChatGPT |
| **Search** | Busqueda unificada (FTS + vector + graph) | Raycast + Obsidian |
| **Settings** | Configuracion del sistema | VS Code |

#### Modulos de Productividad

| Modulo | Funcion |
|--------|---------|
| **Calendar** | Calendario unificado (Google Calendar + local + deadlines) |
| **Finance** | Finanzas personales, costos de IA, suscripciones |
| **Contacts** | Contactos con relaciones y contexto |
| **Documents** | Documentos, PDFs, presentaciones |
| **Email** | Cliente de email integrado |

#### Modulos Tecnicos

| Modulo | Funcion |
|--------|---------|
| **Git** | Gestion de repositorios, PRs, branches, commits |
| **Docker** | Contenedores, stacks, imagenes, networks |
| **Services** | Health checks, uptime, monitoreo |
| **MCP** | Gestion de MCP servers, tools, resources |
| **DevOps** | Deployments, CI/CD, cron jobs |
| **API** | API keys, endpoints, rate limits, usage |

#### Modulos de IA

| Modulo | Funcion |
|--------|---------|
| **Agents** | Creacion, configuracion, monitoreo de agentes |
| **Skills** | Marketplace de skills, creacion propia |
| **Models** | Gestion de modelos y proveedores |
| **Costs** | Costos detallados por proyecto/agente/modelo |
| **Sessions** | Historial de sesiones de agentes |
| **Prompts** | Gestion de system prompts y templates |

#### Modulos de Sistema

| Modulo | Funcion |
|--------|---------|
| **Timeline** | Linea de tiempo global de actividad |
| **Logs** | Logs estructurados de todo el sistema |
| **Backups** | Backup y restore de workspaces |
| **Plugins** | Marketplace y gestion de plugins |
| **Automations** | Automatizaciones programadas o por evento |

### 6.5 Navegacion

```
┌─────────────┬──────────────────────────────────────────────┐
│ Activity Bar  │  Main Content Area                          │
│ (Left)       │                                              │
│              │  ┌────────────────────────────────────────┐  │
│  [Home]      │  │  Sidebar (contextual)                  │  │
│  [Projects]  │  │  - Project list                        │  │
│  [Notes]     │  │  - Current project files               │  │
│  [Tasks]     │  │  - Agent sessions                      │  │
│  [Chat]      │  │  - Related notes                       │  │
│  [Agents]    │  └────────────────────────────────────────┘  │
│  [Git]       │                                              │
│  [Docker]    │  ┌────────────────────────────────────────┐  │
│  [Services]  │  │  Content Panel                         │  │
│  [Calendar]  │  │  (active module content)               │  │
│  [Finance]   │  │                                        │  │
│  ────────    │  │                                        │  │
│  [Search]    │  │                                        │  │
│  [Settings]  │  └────────────────────────────────────────┘  │
└─────────────┴──────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────┐
│  Status Bar                                                  │
│  Project: akira-os  │  Agent: idle  │  Tokens: 1,234        │
│  Services: 7/7 up   │  Cost today: $0.42                     │
└──────────────────────────────────────────────────────────────┘
```

**Patron de navegacion:**
- Cada icono en la Activity Bar cambia la sidebar y el panel principal
- La sidebar muestra el contexto del modulo activo
- Command Palette (Cmd+Shift+P) para accion universal
- Command K (Cmd+K) para busqueda rapida
- Quick Switch (Cmd+Tab) entre proyectos recientes

### 6.6 Sistema de Plugins

#### API de plugin

```typescript
// Un plugin es un modulo con:
interface NovaPlugin {
  // Identificacion
  id: string;
  name: string;
  version: string;
  author: string;
  
  // Ciclo de vida
  onActivate(): void;
  onDeactivate(): void;
  onConfigChange(config: any): void;
  
  // Contribuciones
  contributes: {
    // Paneles en la UI
    panels?: PanelDefinition[];
    // Comandos para la palette
    commands?: CommandDefinition[];
    // Vistas en el sidebar
    views?: ViewDefinition[];
    // Proveedores de datos
    dataProviders?: DataProvider[];
    // Tools para agentes
    tools?: ToolDefinition[];
    // Skills para agentes
    skills?: SkillDefinition[];
    // Bloques de dashboard
    dashboardBlocks?: BlockDefinition[];
  };
  
  // Configuracion
  configSchema?: JSONSchema;
  defaultConfig?: Record<string, any>;
}
```

Los plugins se instalan desde:
1. **Marketplace oficial** (curado, revisado)
2. **URL de git** (instalacion directa desde repo)
3. **Path local** (desarrollo propio)
4. **npm/pip package** (compatibilidad con ecosistemas existentes)

### 6.7 Sistema de Proyectos

Cada proyecto tiene:

```
project-root/
├── .nova/                    # Configuracion del workspace
│   ├── config.yaml           # Proyecto config
│   ├── agents.yaml           # Agentes asignados
│   ├── skills/               # Skills del proyecto
│   ├── memory/               # Memoria del proyecto (Markdown)
│   │   ├── knowledge/        # Conocimiento recopilado
│   │   ├── decisions/        # Decisiones registradas
│   │   ├── learnings/        # Aprendizajes
│   │   └── index.md          # Indice de memoria
│   ├── sessions/             # Sesiones de agente comprimidas
│   └── plugins/              # Plugins del proyecto
├── docs/                     # Documentacion del proyecto
├── tasks/                    # Tareas (Markdown frontmatter)
├── notes/                    # Notas del proyecto
├── src/                      # Codigo fuente
└── README.md                 # Descripcion del proyecto
```

### 6.8 Organizacion de Agentes

```
Agents
├── Personal Agents (perfil del usuario)
│   ├── Assistant (general purpose)
│   ├── Researcher (investigacion profunda)
│   └── Scheduler (calendario + tareas)
│
├── Project Agents (por proyecto)
│   ├── Dev Agent (codigo)
│   ├── Doc Agent (documentacion)
│   └── QA Agent (testing)
│
├── Background Agents (autonomos)
│   ├── Vigia (monitoreo)
│   ├── Evolucion (mejora continua)
│   └── Housekeeper (mantenimiento)
│
└── Ad-hoc Agents (un solo uso)
    ├── Research Sprint
    └── Code Review
```

Cada agente tiene:
- **Role** (que hace)
- **Goal** (que logra)
- **Tools** (que MCP servers usa)
- **Skills** (que skills conoce)
- **Memory scope** (que memoria ve)
- **Budget** (limite de costos)
- **Schedule** (cuando trabaja)

### 6.9 Modelo de Memoria

```
MEMORY ARCHITECTURE
═══════════════════════════════════════════════════════════════

WORKING MEMORY (Agent Session)
  ├── Current task context (70% context window)
  ├── Recent messages (30% context window)
  └── State checkpoints (cada N steps)

PROJECT MEMORY (.nova/memory/)
  ├── knowledge/*.md (RAG-indexed)
  ├── decisions/*.md (structured)
  ├── learnings/*.md (from agent sessions)
  └── index.md (semantic index)

LONG-TERM MEMORY (Cross-project)
  ├── User profile (preferences, patterns)
  ├── Skill mastery (skills learned)
  └── Global knowledge (facts across projects)

ARCHIVAL MEMORY (Comprimida)
  ├── Compressed sessions (resumenes de sesiones)
  ├── Vector embeddings (semantic search)
  └── FTS index (full-text search)
```

**Flujo de memoria:**
1. Working memory se comprime a project memory al cerrar sesion
2. Project memory alimenta RAG para futuras sesiones
3. Patrones cruzados suben a long-term memory
4. Sesiones antiguas se comprimen a archival memory
5. Toda la memoria es editable por el usuario (archivos Markdown)

### 6.10 Dashboards

Cada dashboard es una coleccion de bloques:

```typescript
interface Dashboard {
  id: string;
  name: string;
  projectId?: string; // null = global
  layout: GridLayout;
  blocks: BlockInstance[];
  refreshInterval?: number; // segundos
}

interface BlockDefinition {
  type: 'metrics' | 'chart' | 'table' | 'list' | 'status' | 
         'timeline' | 'activity' | 'costs' | 'custom';
  dataSource: string; // provider ID
  config: Record<string, any>;
  size: { w: number; h: number };
}
```

**Dashboards predefinidos:**
- **Home**: Resumen del dia (proyectos activos, tareas pendientes, actividad reciente, costos del dia)
- **Project**: Estado del proyecto (roadmap, tareas, sesiones, costos, health)
- **Dev**: Repos, PRs, CI status, Docker containers
- **Finance**: Costos de IA, suscripciones, presupuesto por proyecto
- **Services**: Health checks, uptime, alertas
- **Agents**: Agentes activos, sesiones, costos por agente

### 6.11 Timeline

Timeline global de todo el sistema:

```typescript
interface TimelineEvent {
  id: string;
  timestamp: Date;
  type: 'agent_action' | 'task_done' | 'deploy' | 'note_created' |
        'git_commit' | 'cost_milestone' | 'service_event' | 
        'automation_run' | 'system_event';
  source: string; // project, agent, module
  summary: string; // "Deploy v2.3.1 to production"
  details?: string; // markdown opcional
  metadata?: Record<string, any>;
  cost?: number;
}
```

### 6.12 Observabilidad

Cada modulo expone:

```typescript
interface ObservableModule {
  // Logs estructurados
  logs(query: LogQuery): LogEntry[];
  
  // Metricas en tiempo real
  metrics(): ModuleMetrics;
  
  // Costos
  costs(from: Date, to: Date): CostBreakdown;
  
  // Estado actual
  status(): 'healthy' | 'degraded' | 'error';
  
  // Actividad reciente
  activity(limit: number): ActivityEntry[];
  
  // Reasoning traces (para agentes)
  traces(sessionId: string): Trace[];
}
```

### 6.13 Sistema de Permisos

Por diseno, Nova es un sistema **single-user**. Pero los permisos existen a nivel de:

```typescript
interface PermissionScope {
  // Que puede ver el agente
  read: ('memory' | 'files' | 'notes' | 'git' | string)[];
  
  // Que puede modificar el agente
  write: ('memory' | 'files' | 'notes' | 'git' | string)[];
  
  // Que puede ejecutar el agente
  execute: ('terminal' | 'docker' | 'deploy' | string)[];
  
  // Limites
  budget: number; // max cost per run
  maxTokens: number;
  allowedModels: string[];
  blockedTools: string[];
}

// Cada agente tiene un permission scope
// Cada proyecto tiene un permission scope por defecto
// Cada sesion puede override
```

### 6.14 Busqueda Unificada

Tres modos de busqueda combinados:

1. **Full-Text Search** (FTS5 en SQLite)
   - Notas, documentos, tareas, conversaciones
   - Rapido, offline, sin dependencias

2. **Vector Search** (SQLite Vec)
   - Busqueda semantica sobre memoria
   - Embeddings locales (modelo small embebido)

3. **Knowledge Graph** (relaciones entre entidades)
   - Conexiones entre proyectos, notas, personas, conceptos
   - Graph visualization (como Obsidian)
   - Navegacion por relaciones

### 6.15 Integracion con MCP

MCP es el mecanismo de extension primario para tools:

```typescript
interface MCPIntegration {
  // Servers locales (procesos)
  localServers: MCPServer[];
  
  // Servers remotos (HTTP/SSE)
  remoteServers: MCPServer[];
  
  // Registry de servers instalados
  registry: {
    installed: MCPServer[];
    available: MCPRegistryEntry[]; // marketplace
  };
  
  // Gestion
  install(serverId: string): Promise<void>;
  configure(serverId: string, config: any): Promise<void>;
  test(serverId: string): Promise<boolean>;
}

interface MCPServer {
  id: string;
  name: string;
  transport: 'stdio' | 'http' | 'sse' | 'websocket';
  tools: MCPTool[];
  resources: MCPResource[];
  enabled: boolean;
  config: Record<string, any>;
}
```

### 6.16 Integracion con Docker

```typescript
interface DockerIntegration {
  // Entornos de ejecucion para agentes
  sandboxes: DockerSandbox[];
  
  // Servicios gestionados
  services: DockerService[];
  
  // Stacks (Docker Compose)
  stacks: DockerStack[];
  
  // Acceso desde Nova UI
  containers(): ContainerStatus[];
  logs(containerId: string): LogEntry[];
  exec(containerId: string, command: string): ExecResult;
}
```

### 6.17 Integracion con Git

```typescript
interface GitIntegration {
  // Repositorios conocidos
  repos: GitRepo[];
  
  // Estado unificado
  status(): GitStatus[];
  
  // Acciones
  commit(repo: string, message: string): CommitResult;
  push(repo: string): PushResult;
  createPR(repo: string, title: string, description: string): PRResult;
  
  // Visualizacion
  graph(repo: string): GitGraph;
  diff(repo: string, ref: string): DiffResult;
}
```

### 6.18 Integracion con Notas

El sistema de notas es nativo (no external):

```typescript
interface NoteSystem {
  // Notas locales (default)
  local: NoteStore;
  
  // Integracion con Obsidian vault
  obsidianVault?: ObsidianVault;
  
  // Integracion con SilverBullet
  silverBullet?: SilverBulletSpace;
  
  // Busqueda unificada cross-source
  search(query: string): NoteSearchResult[];
}
```

Pero tambien soporta montar vaults externos como Obsidian o SilverBullet.

### 6.19 Integracion con Finanzas

```typescript
interface FinanceModule {
  // Costos de IA por proyecto/agente/modelo
  aiCosts: CostTracker;
  
  // Suscripciones
  subscriptions: Subscription[];
  
  // Presupuestos por proyecto
  budgets: Budget[];
  
  // Servicios (VPS, dominios, etc.)
  services: Service[];
  
  // Dashboard financiero
  dashboard(): FinanceDashboard;
}
```

---

## 7. Roadmap

### Fase 1: MVP (Mes 1-2)

**Que entrega:**
- Backend FastAPI con SQLite
- Frontend React + Tailwind + shadcn/ui
- Modulo Home con dashboard basico
- Modulo Projects (CRUD, estados)
- Modulo Notes (editor Markdown, backlinks)
- Modulo Chat (conversaciones con agente)
- Modulo Search (FTS sobre notas)
- Modulo Services (health checks)
- Graph view basico en Notes
- Status bar con servicios

**No incluye:**
- Agentes (solo chat simple)
- Memoria persistente
- Plugins
- Automatizaciones

### Fase 2: Workspace (Mes 3-4)

**Que agrega:**
- Sistema de workspaces completo
- Modulo Tasks (Kanban + lista)
- Modulo Calendar (FullCalendar + Google Calendar)
- Modulo Git (estado de repos)
- Modulo Docker (contenedores, logs)
- Timeline global
- Dashboard builder (bloques)
- Theme system (light/dark)
- Command Palette (Cmd+Shift+P)
- Keyboard shortcuts configurables

### Fase 3: Agentes (Mes 5-7)

**Que agrega:**
- Agent Manager completo
- Multiple agent types (personal, project, background)
- Agent Runtime con ejecucion local
- MCP integration (instalar, configurar, ejecutar tools)
- Project Memory (knowledge, decisions, learnings)
- Working memory con session compaction
- Sesiones de agentes con streaming
- Subagent orchestrator (delegacion)
- Agent scheduling (cron jobs)
- Cost tracking por agente
- Reasoning traces en UI
- Agent status indicator

### Fase 4: Plugins (Mes 8-9)

**Que agrega:**
- Plugin API completa
- Plugin marketplace
- Plugin installation desde git/npm/local
- Plugin lifecycle management
- Plugin sandboxing
- Module hooks system
- Custom panel definitions
- Custom command definitions
- Custom block definitions
- Plugin developer docs
- Plugin validator tool

### Fase 5: Automatizacion (Mes 10-12)

**Que agrega:**
- Automation engine (triggers + conditions + actions)
- Visual automation builder
- Webhook receiver
- Event system (every action is an event)
- Automation templates
- Integration with timeline
- Alerting system (multi-channel)
- Scheduled reports
- Auto-backup de workspaces
- Housekeeping automations

### Fase 6: Inteligencia Continua (Mes 13-15)

**Que agrega:**
- Long-term memory (cross-project patterns)
- Learning system (el sistema aprende de tu uso)
- Knowledge Graph global
- Proactive suggestions (basado en patrones)
- Auto-tagging y organizacion
- Semantic search mejorada
- Session archival con compression inteligente
- Pattern detection en actividad
- Auto-evolucion (como la evolucion nocturna)
- User profile building

### Fase 7: Ecosistema (Mes 16-18)

**Que agrega:**
- Mobile companion app
- Cloud sync (opcional, premium)
- Multi-device support
- Community plugin registry
- Public API para terceros
- Desktop apps (Linux, macOS, Windows)
- Docker deployment (server mode)
- Team/collaboration features
- Enterprise features (SSO, audit)
- Public marketplace

---

## 8. Integracion con Hermes

### Rol de Hermes en Nova

Hermes no desaparece. Se convierte en **uno de los agentes del sistema**, especificamente el Assistant Agent personal.

### Responsabilidades de Hermes

1. **Assistant personal** -- el agente conversacional que te acompania todo el dia
2. **Interfaz primaria** -- desde Nova Chat, hablas con Hermes (y otros agentes)
3. **Orquestador de subagentes** -- Hermes delega tareas complejas a agentes especializados
4. **Gateway de comandos** -- desde Nova Chat, Hermes ejecuta comandos en Nova
5. **Memoria compartida** -- Hermes accede a la memoria del proyecto actual

### Que deberia hacer el Workspace (Nova)

- Proveer la UI y la navegacion
- Gestionar proyectos y workspaces
- Almacenar y servir memoria
- Ejecutar agentes en background
- Mostrar dashboards y metricas
- Gestionar plugins y extensiones
- Integrar con servicios externos
- Proveer observabilidad

### Que deberia hacer cada modulo

| Modulo | Responsabilidad |
|--------|----------------|
| **Nova Core** | Backend, DB, plugins, workspace management |
| **Nova UI** | Frontend, navegacion, dashboards |
| **Hermes Agent** | Asistente conversacional, orquestacion |
| **Subagentes** | Tareas especificas (codigo, investigacion, etc.) |
| **MCP Servers** | Tools y recursos para agentes |
| **Docker** | Sandboxes para ejecucion de agentes |
| **Git** | Control de versiones de proyectos |
| **Cron** | Automatizaciones programadas |
| **Vigia** | Monitoreo de servicios |

### Diagrama de integracion

```
                    ┌──────────────────┐
                    │    Nova UI       │
                    │  (React/Tailwind)│
                    └────────┬─────────┘
                             │ REST + WebSocket
                    ┌────────▼─────────┐
                    │   Nova Core      │
                    │  (FastAPI/SQLite)│
                    └──┬──────┬──────┬─┘
                       │      │      │
              ┌────────▼┐ ┌──▼──┐ ┌─▼──────┐
              │ Hermes  │ │MCP  │ │Plugins │
              │ Agent   │ │Srvs │ │System  │
              └──┬──────┘ └─────┘ └────────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
    Subagent  Subagent  Subagent
    (Dev)     (Res)     (Doc)
```

### Migracion desde el dashboard actual

El dashboard Akira OS actual (React + Refine + Tailwind en :8586) es la base de Nova UI.

**Pasos de migracion:**

1. Refactorizar el frontend actual para que sea modular (cada modulo independiente)
2. Agregar backend de proyectos y workspaces
3. Migrar la estructura de datos a SQLite con el schema de Nova
4. Agregar sistema de plugins
5. Agregar motor de agentes con Hermes como agente principal

**El dashboard actual NO se descarta. Es el punto de partida de Nova.**

---

## Apendice A: Stack Tecnologico Recomendado

| Capa | Tecnologia | Justificacion |
|------|-----------|---------------|
| Frontend | React 19 + TypeScript | Ecosistema mas grande, Refine ya es base |
| UI Framework | Tailwind v4 + shadcn/ui | Ya usado, consistente |
| State Management | TanStack Query + Zustand | Query para server state, Zustand para client |
| Backend | FastAPI + Python 3.12+ | Rendimiento, type hints, async nativo |
| Database | SQLite + SQLite Vec | Local first, sin setup, embebido |
| Search | FTS5 + SQLite Vec | Sin servidores externos |
| Desktop | Tauri 2.0 | Menos peso que Electron, Rust native |
| Agent Runtime | Hermes Agent SDK | Integracion nativa con el ecosistema |
| MCP Client | FastMCP | Estandar, rapido, Pythonico |
| Auth | Local only (single user) | Por diseno, simple |
| Logs | SQLite + rotation | Sin ELK stack para un solo usuario |
| Background jobs | APScheduler | Simple, sin Redis/Celery |
| File storage | Filesystem + optional S3 | Local first |

## Apendice B: Glosario

| Termino | Definicion |
|---------|-----------|
| **Workspace** | Entorno aislado con archivos, memoria y configuracion |
| **Project** | Unidad fundamental del sistema, con objetivos y memoria |
| **Agent** | Entidad de IA con role, tools y memoria |
| **Skill** | Instrucciones estructuradas que ensenan al agente |
| **MCP** | Model Context Protocol (tools & resources) |
| **ACP** | Agent-Client Protocol (agentes externos) |
| **Memory Tree** | Memoria organizada como arbol de archivos Markdown |
| **Session Compaction** | Compresion de historial para sesiones largas |
| **Block** | Unidad visual de dashboard |
| **Plugin** | Extension del sistema con API completa |
