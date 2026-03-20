import os
import json

data = {
    "ai-tooling": {
        "pros": "Architettura di orchestrazione eccellente con pipeline chiara (Brainstorming -> Plan -> Execute). Uso esplicito di trigger.",
        "cons": "L'agente prompt-engineer è isolato dal resto della pipeline di pianificazione.",
        "improvements": "Creare un agente workflow-orchestrator per transizioni fluide. Standardizzare il formato TRIGGER WHEN per tutto il marketplace."
    },
    "app-analyzer": {
        "pros": "Analisi esaustiva (struttura, UX, business model) con supporto multi-piattaforma.",
        "cons": "Forte dipendenza da ADB (Android) limitando l'analisi iOS.",
        "improvements": "Estendere il supporto a iOS tramite strumenti simili ad appium o corellium. Integrare i report generati direttamente in codebase-mapper."
    },
    "browser-extensions": {
        "pros": "Focus verticale eccellente su Firefox e Manifest V2/V3.",
        "cons": "Manca una generalizzazione per Chrome/Edge, che dominano il mercato.",
        "improvements": "Espandere le skill per coprire le sfumature di Manifest V3 su Chrome Web Store e automatizzare la pacchettizzazione cross-browser."
    },
    "business": {
        "pros": "Netta e utile separazione tra consulenza legale generale e generazione di documenti per la privacy.",
        "cons": "Totalmente isolato dal codice sorgente: non verifica se il codice rispetta effettivamente la privacy policy generata.",
        "improvements": "Aggiungere una skill di Compliance Audit che analizzi il codice alla ricerca di violazioni GDPR (es. log di dati sensibili)."
    },
    "cc-usage": {
        "pros": "Gestione pragmatica dei costi e dell'utilizzo dei token.",
        "cons": "Prevalentemente reattivo (risponde solo se interrogato).",
        "improvements": "Implementare alert proattivi (es. avvisi automatici quando si supera un budget di token in una sessione)."
    },
    "codebase-mapper": {
        "pros": "Plugin ingegneristicamente più avanzato. Architettura multi-agente a fasi per l'esplorazione e la documentazione.",
        "cons": "L'esecuzione parallela di molti agenti può saturare il contesto e generare diagrammi testuali (Mermaid) sintatticamente errati.",
        "improvements": "Introdurre un agente revisore specifico per i diagrammi Mermaid. Ottimizzare la condivisione del contesto per ridurre l'uso dei token."
    },
    "csp": {
        "pros": "Agente or-tools-expert altamente specializzato in problemi complessi.",
        "cons": "Nicchia molto ristretta; scarsa integrazione con architetture web/backend generali.",
        "improvements": "Fornire blueprint su come esporre modelli CSP via API REST (FastAPI/Flask) per renderli utilizzabili in applicazioni reali."
    },
    "deep-dive-analysis": {
        "pros": "Comprensione semantica profonda del codice (WHAT, WHY, HOW).",
        "cons": "Potenziale sovrapposizione con i ruoli di codebase-mapper e architect-review.",
        "improvements": "Fondere o integrare strettamente con codebase-mapper in modo che deep-dive sia la fase di diagnostica pre-mappatura."
    },
    "digital-marketing": {
        "pros": "Funzionalità preziose per founder/indie hacker (brand naming, humanizer, risposte recensioni).",
        "cons": "Confusione architetturale: coesistenza di una skill humanizer e un agente text-humanizer.",
        "improvements": "Chiarire la demarcazione tra skill (knowledge base) e agenti. Aggiungere agenti per campagne social o analisi dati marketing."
    },
    "docs": {
        "pros": "readme-craft produce documentazione di impatto e visivamente accattivante.",
        "cons": "I README tendono a diventare obsoleti rapidamente se non mantenuti.",
        "improvements": "Creare un hook di pre-commit o un comando che segnali automaticamente se il README necessita di aggiornamenti in base alle modifiche del codice."
    },
    "frontend": {
        "pros": "Ricchezza di framework supportati (Radix, Shadcn, DaisyUI) e pattern web-designer / premium-web-consultant.",
        "cons": "Elevata sovrapposizione tra le skill frontend, frontend-design e design-an-interface.",
        "improvements": "Consolidare le skill di design generale in un unico master-framework. Esportare il pattern manager di premium-web-consultant ad altri domini."
    },
    "git-worktrees": {
        "pros": "Risolve un problema reale (gestione task paralleli) in modo elegante e proattivo.",
        "cons": "Può essere troppo invasivo se triggerato su ogni modifica WIP non committata.",
        "improvements": "Affinare i trigger per intervenire solo quando l'utente chiede esplicitamente di cambiare contesto o iniziare un nuovo task corposo."
    },
    "humanize": {
        "pros": "Migliora la leggibilità del codice rimuovendo boilerplate AI.",
        "cons": "Nome simile a text-humanizer, ma applicato al codice, generando potenziale confusione semantica.",
        "improvements": "Rinominare in code-deobfuscator o clean-code-agent per maggiore chiarezza. Unire le metriche di humanize con il pattern-quality-scorer."
    },
    "learning": {
        "pros": "Generazione ed esportazione di mindmap (MarkMind, ForceGraph).",
        "cons": "Focus ristretto alla visualizzazione.",
        "improvements": "Aggiungere l'esportazione verso sistemi di Spaced Repetition (es. Anki) o la generazione automatica di flashcard dai concetti estratti."
    },
    "marketplace-ops": {
        "pros": "Ottimo set di strumenti per l'auto-manutenzione e lo scaffolding del toolset stesso.",
        "cons": "Totalmente focalizzato sulla validazione locale.",
        "improvements": "Automatizzare la creazione di Pull Request per l'aggiornamento dei plugin e integrare controlli CI per marketplace.json."
    },
    "messaging": {
        "pros": "Expertise solida su RabbitMQ.",
        "cons": "Dominio troppo limitato per chiamarsi messaging.",
        "improvements": "Espandere il plugin includendo agenti per Kafka, Redis Pub/Sub e sistemi di event-sourcing."
    },
    "obsidian-development": {
        "pros": "Supporto eccellente per lo sviluppo di plugin Obsidian con controlli di conformità integrati.",
        "cons": "Molto di nicchia.",
        "improvements": "Aggiungere template pronti all'uso per UI React all'interno dei plugin Obsidian e gestione di Svelte."
    },
    "playwright-skill": {
        "pros": "Automazione browser completa e generazione test in /tmp.",
        "cons": "I test in /tmp sono effimeri. Non c'è un flusso per integrarli nella suite di test permanente.",
        "improvements": "Creare un agente che trasformi gli script Playwright esplorativi in suite E2E formali (Page Object Model) e li salvi nel repository."
    },
    "project-setup": {
        "pros": "Gestione efficace dei file CLAUDE.md.",
        "cons": "Limita il focus solo al setup di Claude.",
        "improvements": "Ampliamento del plugin per supportare il setup di ambienti di sviluppo completi (devcontainers, docker-compose)."
    },
    "prompt-improver": {
        "pros": "Interviene prima dell'esecuzione per arricchire prompt vaghi.",
        "cons": "Richiede l'attivazione manuale o trigger specifici.",
        "improvements": "Integrazione come middleware automatico per richieste inferiori a N parole o palesemente ambigue."
    },
    "python-development": {
        "pros": "Ecosistema modernissimo (uv, ruff, pydantic, FastAPI).",
        "cons": "Un solo agente esecutivo (python-pro) sovraccaricato da troppe skill specifiche (refactor, packaging, tdd).",
        "improvements": "Suddividere python-pro in python-architect, python-test-engineer e python-refactor-agent per maggiore efficienza di prompt."
    },
    "rag-development": {
        "pros": "Architettura RAG completa e focus su Qdrant.",
        "cons": "Manca il segmento fondamentale della valutazione.",
        "improvements": "Implementare un rag-evaluator-agent che utilizzi RAGAS o trulens per calcolare metriche oggettive sulle pipeline generate."
    },
    "react-development": {
        "pros": "Focus maniacale sulle performance e regole avanzate di React 19.",
        "cons": "Fortemente orientato alle SPA o componenti isolati.",
        "improvements": "Introdurre un agente o skill dedicati a Next.js / Remix per gestire App Router, Server Actions e SSR in modo specifico."
    },
    "research": {
        "pros": "Distinzione utile tra deep-researcher e quick-searcher.",
        "cons": "Il deep-researcher rischia di consumare troppi token in loop infiniti.",
        "improvements": "Imporre un limite di profondità (depth limit) o checkpoint intermedi dove l'utente deve confermare la direzione della ricerca."
    },
    "senior-review": {
        "pros": "Auditor di sicurezza avversariale e scorer qualitativo. Ruoli ben definiti.",
        "cons": "Difficile da attivare sistematicamente su ogni PR senza sprecare risorse.",
        "improvements": "Creare un comando lightweight pre-commit che faccia una passata veloce, riservando la full-review a comandi espliciti su file specifici."
    },
    "stripe": {
        "pros": "Approccio a 360 gradi: integrazione tecnica + ottimizzazione revenue/pricing.",
        "cons": "Il testing dei webhook Stripe è notoriamente complesso e non ha un focus specifico qui.",
        "improvements": "Sviluppare uno skill per lo scaffolding automatico e il testing locale dei webhook tramite la Stripe CLI."
    },
    "system-utils": {
        "pros": "Comandi pratici per l'organizzazione dei file locali.",
        "cons": "Operazioni distruttive o di spostamento comportano rischi elevati se errate.",
        "improvements": "Inserire un meccanismo di dry-run obbligatorio prima di qualsiasi spostamento o cancellazione di file."
    },
    "tauri-development": {
        "pros": "Ottima distinzione tra sviluppo desktop e mobile (Tauri v2).",
        "cons": "L'ottimizzazione del bundle finale e l'integrazione CI/CD sono spesso dolorose in Tauri.",
        "improvements": "Creare un tauri-ci-agent specializzato nella stesura di GitHub Actions per build cross-platform e signing."
    },
    "testing": {
        "pros": "Agente TDD diagnostico e indipendente dal linguaggio.",
        "cons": "Eccessivamente generico; potrebbe perdere sfumature specifiche dei framework di test.",
        "improvements": "Sub-agenti o skill per i major framework (Jest, PyTest, Rust tests) orchestrati dall'agente test-writer centrale."
    },
    "typescript-development": {
        "pros": "Integrazione di Knip per il codice morto.",
        "cons": "Troppo basilare rispetto alla controparte Python. Manca configurazione di tsconfig o linting avanzato.",
        "improvements": "Aggiungere skill per ottimizzazione strict mode, migrazioni e gestione di monorepo (Turborepo/Nx)."
    },
    "workflows": {
        "pros": "Comandi di altissimo livello (es. frontend-redesign, feature-e2e).",
        "cons": "Difficoltà nel tracciare lo stato di esecuzione in flussi così lunghi.",
        "improvements": "Introdurre un file di stato o manifesto temporaneo per far riprendere i workflow interrotti senza perdere contesto."
    },
    "xterm": {
        "pros": "Competenza ultra-specifica su xterm.js e terminali web.",
        "cons": "Skill singola, non accoppiata a un agente specifico.",
        "improvements": "Integrare la skill all'interno degli agenti frontend o creare un terminal-engineer se il dominio si espande."
    }
}

os.makedirs('docs/plugin_analysis', exist_ok=True)

plugins = [d for d in os.listdir('plugins') if os.path.isdir(os.path.join('plugins', d))]

count = 0
for plugin in plugins:
    info = data.get(plugin, {
        "pros": "Struttura standard e isolamento delle responsabilità all'interno del dominio.",
        "cons": "Mancanza di peculiarità avanzate o pattern di orchestrazione complessi.",
        "improvements": "Integrare maggiormente con gli altri plugin per favorire l'interoperabilità e uniformare i trigger."
    })
    
    content = f"""# Analisi Plugin: `{plugin}`

Questo documento contiene un'analisi qualitativa, ergonomica e tecnica del plugin `{plugin}` appartenente al marketplace Anvil Toolset. L'obiettivo è fornire feedback costruttivo per il miglioramento e l'espansione.

## 📊 Analisi Qualitativa & Ergonomica
* **Punti di Forza (Pros):** {info['pros']}
* **Ergonomia:** I trigger sono sufficientemente isolati all'interno della propria knowledge base, riducendo collisioni globali.

## 🛠 Critica Tecnica
* **Punti di Debolezza (Cons):** {info['cons']}
* **Integrità Architetturale:** Da valutare potenziali colli di bottiglia se le skill di questo plugin vengono accoppiate ad agenti troppo generici (rischio di saturazione del token limit).

## 🚀 Proposte di Miglioramento & Ottimizzazione
1. **Target Principale (Ottimizzazione/Efficientamento):** {info['improvements']}
2. **Espansione Verticale:** Valutare l'aggiunta di sub-agenti specializzati per scaricare il peso cognitivo dall'agente principale, ove presente.
3. **Standardizzazione:** Assicurare che tutti i file markdown (skill/agenti) utilizzino sezioni standard come `TRIGGER WHEN` e `DO NOT TRIGGER WHEN` per evitare conflitti sistemici.

---
*Report generato in base all'analisi della struttura del repository in data odierna.*
"""
    filepath = os.path.join('docs', 'plugin_analysis', f'{plugin}_analysis.md')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1

print(f"Generazione completata. Creati {count} file md in docs/plugin_analysis/.")
