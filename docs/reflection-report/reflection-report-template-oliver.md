# Refleksjonsrapport - Programmering med KI

## 1. Gruppeinformasjon

**Gruppenavn:** [Navn på gruppen]

**Gruppemedlemmer:**
- [Navn 1] - [Student-ID/E-post]
- [Navn 2] - [Student-ID/E-post]
- [Navn 3] - [Student-ID/E-post]

**Dato:** [DD.MM.ÅÅÅÅ]

---

## 2. Utviklingsprosessen

### 2.1 Oversikt over prosjektet
[Kort beskrivelse av hva dere har utviklet. Hva var hovedmålet med applikasjonen?]

### 2.2 Arbeidsmetodikk
[Beskriv hvordan dere organiserte arbeidet]
- Hvordan fordelte dere oppgaver?
- Hvilke verktøy brukte dere for samarbeid og hvordan det fungerte? (f.eks. Git, og Teams)
- Hvordan brukte dere KI-verktøy i prosessen?

### 2.3 Teknologi og verktøy

**Frontend:**
- Next.js 14 (App Router) med TypeScript
- Tailwind CSS
- shadcn/ui (UI-komponenter)
- React Context API (state management)
- Lucide React (ikoner)

**Backend:**
- Python 3.11+
- FastAPI (web framework)
- Pydantic AI (RAG framework med type-sikkerhet)
- Beautiful Soup 4 (web scraping)
- langchain_text_splitters (document chunking)
- uvicorn (ASGI server)
- slowapi (rate limiting)
- instructor (for strukturert LLM output)

**Database:**
- Supabase (PostgreSQL - for samtaler, feedback, analytics)
- ChromaDB (vektordatabase - for dokumentembeddings)

**KI-verktøy:**
- Google Gemini 2.5 Pro (produksjon - chat responses)
- text-embedding-004 (embeddings/søk)
- Gemini CLI (utvikling)
- Claude Pro (AI-assistert koding)

**Andre verktøy:**
- VS Code (editor)
- Git/GitHub (versjonskontroll)
- Microsoft Teams (ukentlige møter og fortløpende chat)
- Vercel (planlagt frontend hosting)
- Railway (planlagt backend hosting)

### 2.4 Utviklingsfaser

Prosjektet har fulgt BMAD (Business-driven Modular Agile Development) metodikken med følgende faser:

**Fase 0: Analyse og Ideeutvikling (Oktober 2025)**
- Gjennomførte strukturerte brainstorming-sesjoner med KI-fasiliterte metoder:
  - "Five Whys" for å identifisere rotårsaker til brukerproblemer
  - "Question Storming" for å utforske problemområdet
  - "Mind Mapping" for å visualisere og organisere innsikter
- Utførte teknisk research for å velge AI-biblioteker og teknologistack
- Utviklet Product Brief for å definere produktvisjon og kjerneverdier
- **KI-bruk:** KI fungerte som fasilitator for brainstorming-sesjoner og hjalp med å analysere teknologivalg. Eksempel på prompt: "Which AI library should we use for orchestrating LLM interactions?"

**Fase 1: Planlegging (November 2025)**
- Utviklet detaljert Product Requirements Document (PRD) med funksjonelle og ikke-funksjonelle krav
- Validerte PRD mot beste praksis og prosjektmål
- Designet UX-spesifikasjon med brukerreiser, UI-komponenter og responsive layouts
- Validerte UX-design mot PRD og identifiserte gaps
- Oppdaterte epics og user stories basert på UX-design (f.eks. splittet Story 2.2 i tre mer granulære stories)
- **KI-bruk:** KI ble brukt til mer eller mindre alt i denne fasen - fra å generere PRD-dokumentasjon til å fungere som en "UX Designer"-agent som validerte design mot krav. UX-agenten ga først en score på 32% på grunn av manglende kontekst, men etter korreksjon økte scoren til 76%.

**Fase 2: Solutioning (November 2025 - Delvis gjennomført)**
- Startet på arkitekturdefinisjon og teknisk design
- Påbegynt epics og stories for implementering
- **Status:** Ikke fullført enda
- **KI-bruk:** Brukt til å utarbeide tekniske spesifikasjoner og arkitekturbeslutninger

**Fase 3: Implementering (Pågående)**
- Planlagt implementering av frontend og backend basert på spesifikasjonene
- **Status:** Ikke startet for fullt enda
- **KI-bruk:** Planlagt bruk til generering av boilerplate-kode, oppsett av database-skjemaer, og implementering av RAG-pipeline

**Viktige erfaringer fra prosessen:**
- KI har vært sentralt i hele prosessen, fra idéutvikling til teknisk planlegging
- Vi har opplevd at kvaliteten på KI-output er sterkt avhengig av hvor god kontekst vi gir
- Iterativ validering og forbedring har vært nødvendig - det første resultatet fra KI er sjelden det beste

---

## 3. Utfordringer og løsninger

### 3.1 Tekniske utfordringer

**Utfordring 1: BMAD Konfigurasjonsoppdatering (.md til .yaml)**
- **Problem:** BMAD-rammeverket gjennomgikk en oppdatering hvor konfigurasjonsfiler ble endret fra Markdown (.md) til YAML (.yaml) format. Dette krevde migrering av eksisterende konfigurasjon og kunne potensielt bryte eksisterende workflows.
- **Løsning:** Vi måtte manuelt oppdatere konfigurasjonsfilene til det nye formatet og verifisere at alle workflows fortsatt fungerte korrekt etter migreringen. Dette krevde grundig testing av agent-baserte kommandoer.
- **KI sin rolle:** KI var begrenset hjelpsom i denne situasjonen da problemet var relatert til et eksternt verktøy som gjennomgikk breaking changes. Dette illustrerer en viktig begrensning: KI kan ikke alltid håndtere verktøyspesifikke oppdateringer som ikke er godt dokumentert i treningsdata.

**Utfordring 2: Gemini's Kompatibilitet med BMAD Slash-Commands**
- **Problem:** Etter en oppdatering av Gemini mistet AI-modellen evnen til å korrekt lese og tolke BMAD slash-commands. Dette påvirket hele vår agent-baserte workflow, da kommandoer som `/run-agent-task` ikke lenger ble gjenkjent eller utført korrekt.
- **Løsning:** Vi måtte eksperimentere med alternative formuleringer og være mer eksplisitte i hvordan vi instruerte KI om å bruke slash-commands. I noen tilfeller måtte vi bytte til manuelle workflows inntil kompatibiliteten ble gjenopprettet eller omgått.
- **KI sin rolle:** Paradoksalt nok var det KI selv som skapte problemet, noe som viser at oppdateringer av AI-modeller kan introdusere regresjoner i funksjonalitet. Dette lærte oss viktigheten av å ha fallback-strategier når man er avhengig av tredjepartsverktøy.

**Utfordring 3: Forventede Utfordringer i Implementeringsfasen**
Selv om vi ikke har nådd full implementering enda, har vi identifisert flere tekniske utfordringer vi forventer å møte:

- **Datainnsamling og Web Scraping:** Risiko for at docs.hmsreg.com er vanskelig å scrape på grunn av JavaScript-rendering eller anti-scraping-mekanismer. Løsningsstrategi: Lagdelt tilnærming med Beautiful Soup først, deretter Playwright for JavaScript-tunge sider, og manuell innsamling som siste utvei.

- **RAG Accuracy (< 80% nøyaktighet):** Risiko for at chatboten hallusinerer eller gir irrelevante svar. Løsningsstrategi: Omfattende testfase med iterativ justering av chunk size, overlap og confidence threshold (0.7).

- **Norsk Språkkvalitet:** Bekymring om engelskspråklige modeller kan håndtere norsk fagterminologi fra byggebransjen (f.eks. "seriøsitetskontroll", "HMS-kort"). Løsningsstrategi: Valg av Gemini 2.5 Pro med god norsk-støtte, norske system-prompts og fagterminologi-ordliste.

**KI sin rolle i disse forventede utfordringene:** KI har hjulpet oss å identifisere disse risikoene tidlig i prosjektet og foreslått konkrete mitigerings-strategier, noe som forhåpentligvis vil spare oss for mye feilsøking senere.

### 3.2 Samarbeidsutfordringer
[Utfordringer knyttet til teamarbeid og kommunikasjon]
- [Beskriv utfordringer og hvordan dere løste dem]

### 3.3 KI-spesifikke utfordringer
[Problemer spesifikt knyttet til bruk av KI]
- [f.eks. Feil kode fra KI, misforståelser, inkonsistent kvalitet]
- [Hvordan håndterte dere disse?]

---

## 4. Kritisk vurdering av KI sin påvirkning

### 4.1 Fordeler med KI-assistanse
[Reflekter over de positive aspektene]

**Effektivitet og produktivitet:**
- [Hvordan påvirket KI arbeidshastigheten?]
- [Eksempler på oppgaver som gikk raskere]

**Læring og forståelse:**
- [Hva lærte dere ved å bruke KI?]
- [Bidro KI til bedre forståelse av konsepter?]

**Kvalitet på koden:**
- [Hvordan påvirket KI kodekvaliteten?]
- [Eksempler på forbedringer KI foreslo]

### 4.2 Begrensninger og ulemper
[Reflekter over de negative aspektene]

**Kvalitet og pålitelighet:**
- [Eksempler på feil eller dårlige løsninger fra KI]
- [Hvordan oppdaget og håndterte dere disse?]

**Avhengighet og forståelse:**
- [Ble dere for avhengige av KI?]
- [Var det tilfeller hvor KI hindret læring?]

**Kreativitet og problemløsning:**
- [Påvirket KI deres egen kreativitet?]
- [Eksempler på situasjoner hvor KI begrenset kreativ tenkning]

### 4.3 Sammenligning: Med og uten KI
[Reflekter over hvordan prosjektet ville vært uten KI]
- Hva ville vært annerledes?
- Hvilke deler av prosjektet ville vært vanskeligere/lettere?
- Ville sluttresultatet vært bedre eller dårligere?

### 4.4 Samlet vurdering
[Konklusjon: Hvordan påvirket KI sluttresultatet totalt sett?]
- Var KI en netto positiv eller negativ faktor?
- Hva var den viktigste lærdommen om å bruke KI i utviklingsprosessen?

---

## 5. Etiske implikasjoner

### 5.1 Ansvar og eierskap
- Hvem er ansvarlig for koden når KI har bidratt?
- Hvordan sikrer man kvalitet når KI genererer kode?
- Diskuter spørsmål om opphavsrett og intellektuell eiendom

### 5.2 Transparens
- Bør det være transparent at KI er brukt?
- Hvordan dokumenterer man KI sin bidrag?
- Hva er konsekvensene av å ikke være åpen om KI-bruk?

### 5.3 Påvirkning på læring og kompetanse
- Hvordan påvirker KI-avhengighet fremtidig kompetanse?
- Hvilke ferdigheter risikerer man å ikke utvikle?
- Balanse mellom effektivitet og læring

### 5.4 Arbeidsmarkedet
- Hvordan kan utbredt KI-bruk påvirke fremtidige jobber i IT?
- Hvilke roller vil bli viktigere/mindre viktige?
- Deres refleksjoner om fremtidig karriere i en KI-drevet verden

### 5.5 Datasikkerhet og personvern
- Hvilke data delte dere med KI-verktøy?
- Potensielle risikoer ved å dele kode og data med KI
- Hvordan skal man tenke på sikkerhet når man bruker KI?

---

## 6. Teknologiske implikasjoner

### 6.1 Kodekvalitet og vedlikehold

**Forståelighet og struktur:**
KI-generert kode kan variere betydelig i forståelighet. Vi har opplevd at KI ikke alltid følger dokumentmaler eller etablerte strukturer ved første forsøk. I flere tilfeller har KI funnet på sin egen måte å skrive dokumentasjon eller viktige konfigurasjonsfiler, noe som har ført til merarbeid. Vanligvis klarer KI å følge malene korrekt på andre eller tredje forsøk når vi er mer spesifikke om å følge malen nøyaktig.

**Debugging-utfordringer:**
Når KI genererer kode som ikke fungerer som forventet, kan det være utfordrende å debugge. Et konkret eksempel er HTML-mockupen vi fikk generert - den fulgte definitivt ikke beste praksis i de første forsøkene og måtte gå gjennom flere iterasjoner før resultatet ble tilfredsstillende. Problemet er at KI-generert kode ofte ser riktig ut på overflaten, men kan inneholde subtile feil eller suboptimale løsninger som krever erfaring å oppdage.

**Langsiktig vedlikehold:**
Vi har bekymringer om langsiktig vedlikehold av KI-generert kode. Hvis vi ikke fullt ut forstår koden KI har produsert, kan det bli vanskelig å vedlikeholde og utvide den senere. Dette skaper en avhengighet hvor man må enten:
1. Bruke KI igjen for å gjøre endringer (med risiko for at nye versjoner av KI kan ha andre tilnærminger)
2. Bruke betydelig tid på å forstå koden grundig før man kan modifisere den manuelt

**Dokumentasjon:**
KI er generelt god på å dokumentere kode når den blir bedt om det, men kvaliteten varierer. Noen ganger er dokumentasjonen overfladisk eller unødvendig verbose. Vi har lært at vi må være eksplisitte om dokumentasjonsstil og -nivå vi ønsker.

**Praktisk erfaring:**
I vårt prosjekt har vi ikke generert mye faktisk kjørbar kode enda (utenom HTML mockups), men erfaringene med BMAD-konfigurasjon og dokumentgenerering har lært oss at KI-generert innhold krever grundig review og ofte flere iterasjoner før det er produksjonsklart.

### 6.2 Standarder og beste praksis

**KI's overholdelse av standarder:**
Vår erfaring er at KI ikke konsekvent følger beste praksis og industristandarder uten eksplisitt instruksjon. Vi har observert flere tilfeller hvor KI:
- Ikke følger dokumentmaler selv når de er tilgjengelige i konteksten
- Genererer HTML-kode som ikke følger moderne beste praksis (f.eks. tilgjengelighet, semantisk HTML, responsiv design)
- Velger suboptimale løsninger fordi den ikke har full kontekst på prosjektets spesifikke krav

Et konkret eksempel er HTML mockup-generering, hvor de første forsøkene manglet:
- Proper semantisk struktur
- Tilgjengelighetsstandarder (ARIA-labels, keyboard navigation)
- Moderne CSS-praksis (flexbox/grid over legacy layouts)

**Viktigheten av validering:**
Vi har alltid gått gjennom AI-output grundig og har i de fleste tilfeller måttet korrigere noe før resultatet ble helt som forventet. Dette er en kritisk læring: **Aldri stole blindt på KI-generert kode eller dokumentasjon.**

Vår valideringsprosess inkluderer:
1. **Manuell gjennomgang:** Vi leser gjennom alt arbeid for å se etter umiddelbare feil eller avvik fra krav
2. **Self-evaluation:** Vi ber KI om å evaluere sitt eget arbeid med en score fra 1-100 og foreslå konkrete forbedringer
3. **Iterativ forbedring:** Basert på evalueringen utføres en ny runde med forbedringer
4. **Cross-validation:** Vi sammenligner KI-output med etablerte maler og standarder i prosjektet

**Eksempler på korreksjoner:**
- **UX-valideringsscore:** UX Designer-agenten ga først prosjektet 32% fordi den ikke fant visse filer. Etter å eksplisitt peke agenten til riktig fil økte scoren til 76%.
- **Dokumentasjonsstruktur:** KI måtte instrueres flere ganger om å følge spesifikke dokumentmaler (f.eks. PRD-mal, UX-spesifikasjonsmaler)
- **HTML mockups:** Krevde 3-4 iterasjoner for å oppnå akseptabel kvalitet med moderne beste praksis

**Lærdom:**
Den viktigste lærdommen er at KI er et kraftig verktøy for å **akselerere** arbeidet, men det er ikke en erstatning for menneskelig ekspertise og kvalitetskontroll. Man må ha kunnskap om beste praksis selv for å kunne evaluere om KI følger dem. Dette skaper et paradoks: De som trenger KI mest (nybegynnere) er også de som har minst forutsetninger for å validere kvaliteten på output.

**Anbefalinger:**
- Bruk KI til å generere første utkast, men anta alltid at det krever forbedring
- Vær svært spesifikk i prompts om hvilke standarder og beste praksis som skal følges
- Implementer self-evaluation som standard arbeidsflyt
- Ha alltid en menneskelig review-prosess før KI-generert arbeid godkjennes

### 6.3 Fremtidig utvikling
- Hvordan tror dere KI vil påvirke programvareutvikling fremover?
- Hvilke ferdigheter blir viktigere for utviklere?
- Deres anbefalinger for hvordan man bør bruke KI i utviklingsprosesser

---

## 7. Konklusjon og læring

### 7.1 Viktigste lærdommer
[Liste de 3-5 viktigste tingene dere lærte gjennom prosjektet]
1. [Lærdom 1]
2. [Lærdom 2]
3. [Lærdom 3]

### 7.2 Hva ville dere gjort annerledes?
[Reflekter over hva dere ville endret hvis dere skulle startet på nytt]
- [Tekniske valg]
- [Bruk av KI]
- [Samarbeid og organisering]

### 7.3 Anbefalinger
[Deres anbefalinger til andre studenter som skal bruke KI i utvikling]
- [Råd om effektiv bruk av KI]
- [Fallgruver å unngå]
- [Beste praksis dere oppdaget]

### 7.4 Personlig refleksjon (individuelt)

**[Navn på gruppemedlem 1]:**
[Personlig refleksjon over egen læring og utvikling]

**[Navn på gruppemedlem 2]:**
[Personlig refleksjon over egen læring og utvikling]

**[Navn på gruppemedlem 3]:**
[Personlig refleksjon over egen læring og utvikling]

---

## 8. Vedlegg (valgfritt)

- Skjermbilder av applikasjonen
- Lenke til GitHub repository
- Annen relevant dokumentasjon

---

**Ordantall:** [Ca. antall ord]

**Forventet lengde:** 3000-5000 ord (avhengig av gruppestørrelse og prosjektets kompleksitet)