---
name: agenda-pessoal-qa
description: Contexto de QA do PWA "Minha Agenda Pessoal" (~/agenda-deploy/index.html) — single-file, Firebase, repo público
metadata:
  type: project
---

PWA single-file `~/agenda-deploy/index.html` (HTML+CSS+JS inline ~940 linhas) da Maiara. Stack: vanilla + Firebase compat 10.12.2 (Auth e-mail/senha + Firestore `users/{uid}`). Publicado no GitHub Pages (repo público `maiarafraga/minha-agenda`).

**Why:** App pessoal de usuária não-técnica (agenda/rotina/compras/gratidão/metas/hábitos). Dados sincronizam em tempo real via onSnapshot; salvam com `docRef.set(...,{merge:true})`. Seeds (SEED_EVENTS, SEED_SHOPPING) com upsert + lista `seedRemoved`. Proteção real dos dados = regras do Firestore no console (uid==userId), NÃO o repo.

**How to apply:** Em QA deste app, focar em: (1) XSS — todo texto via `esc()`, mas IDs interpolados em `onclick='...${id}'` são gerados internamente (uid()/seed-), baixo risco; (2) bug de exclusão de seed: ao reaparecer item após excluir, checar `seedRemoved` no upsert; (3) `merge:true` nunca apaga arrays no servidor — exclusões dependem de reescrever o array inteiro (risco de ressurreição se save concorrente); (4) tudo é client-side, sem testes/lint. Backup versionado: ver [[backup_versionado_agenda]] (convenção de outro app, confirmar antes de aplicar aqui).
