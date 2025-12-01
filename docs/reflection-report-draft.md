# Refleksjonsrapport - Programmering med KI

## 1. Gruppeinformasjon

**Gruppenavn:** [Navn på gruppen]

**Gruppemedlemmer:**
- [Navn 1] - [Student-ID/E-post]
- [Navn 2] - [Student-ID/E-post]
- [Navn 3] - [Student-ID/E-post]

**Dato:** 01.12.2025

---

## 2. Utviklingsprosessen

### 2.1 Oversikt over prosjektet
Vi har utviklet "HMSREG Documentation Chatbot", en AI-drevet assistent designet for å hjelpe brukere av HMSREG-systemet med å finne informasjon i omfattende dokumentasjon. Hovedmålet med applikasjonen er å redusere antall supporthenvendelser og gjøre det enklere for brukere (spesielt underentreprenører) å finne svar på spørsmål om mannskapslister, HMS-kort og dokumentkrav uten å måtte lete manuelt i store tekstmengder. Løsningen bruker RAG (Retrieval-Augmented Generation) for å hente relevant informasjon fra `docs.hmsreg.com` og generere presise svar.

### 2.2 Arbeidsmetodikk
Vi har organisert arbeidet ved hjelp av en strukturert, AI-assistert metodikk.
- **Oppgavefordeling:** Vi har jobbet iterativt med ulike "AI-personaer" (f.eks. UX Designer, Product Manager) for å definere krav, design og teknisk arkitektur.
- **Verktøy:** Vi har brukt Git for versjonskontroll, og kommunisert via en "Bmad" agent-basert arbeidsflyt hvor vi har simulert ulike roller.
- **KI-verktøy:** KI har vært sentral i hele prosessen. Vi har brukt verktøy som Claude Code og Gemini CLI for å generere dokumentasjon, kode, og analysere problemer. Vi har også brukt "Five Whys" og "Question Storming" i brainstorming-sesjoner fasilitert av KI.

### 2.3 Teknologi og verktøy
**Frontend:**
- React 18 med TypeScript
- Vite (byggverktøy)
- Tailwind CSS og shadcn/ui (styling og komponenter)

**Backend:**
- Python 3.11+
- FastAPI (API-rammeverk)
- LangChain (RAG-rammeverk)

**Database:**
- ChromaDB (vektordatabase for dokument-embeddings)
- PostgreSQL (relasjonsdatabase for samtalelogg og feedback)

**KI-verktøy:**
- OpenAI GPT-4o-mini (hovedmodell for tekstgenerering, valgt for god norsk-støtte og pris)
- text-embedding-3-small (for embeddings)
- Claude Code & Gemini CLI (utviklingsassistenter)

### 2.4 Utviklingsfaser

**Fase 1: Planlegging og Spesifikasjon (Oktober 2025)**
- Vi startet med å utarbeide en detaljert "Case Description". Her brukte vi KI (Claude Code) til å utvide en enkel skisse til en fullverdig teknisk spesifikasjon på over 1000 linjer.
- Vi definerte teknisk arkitektur, tidslinje (6 uker), og teststrategi.
- Vi utarbeidet en "Product Brief" for å definere MVP (Minimum Viable Product) og suksesskriterier.
- *KI-bruk:* KI ble brukt til å estimere tidsbruk, identifisere risikoer (f.eks. scraping-problemer), og foreslå en kostnadseffektiv arkitektur for et studentprosjekt.

**Fase 2: Design og Brukerforståelse (November 2025)**
- Vi gjennomførte en brainstorming-sesjon (12. november) fokusert på brukerproblemet "Vanskelig å finne riktig artikkel". Vi brukte metoder som "Five Whys" og tankekartlegging.
- Vi gjennomførte en UX Design-sesjon (17. november) hvor vi validerte designspesifikasjoner mot brukerreiser. Her oppdaget vi mangler i brukerreisene som vi rettet opp i samarbeid med en "UX Designer"-agent.
- *KI-bruk:* KI fungerte som fasilitator for brainstorming og som en kritisk partner for å validere UX-dokumentasjon.

**Fase 3: Utvikling (Pågående)**
- Implementering av frontend og backend basert på spesifikasjonene.
- *KI-bruk:* Generering av boilerplate-kode, oppsett av database-skjemaer, og implementering av RAG-pipeline.

---

## 3. Utfordringer og løsninger

### 3.1 Tekniske utfordringer

**Utfordring 1: Datainnsamling og Scraping**
- **Problem:** Risiko for at `docs.hmsreg.com` er vanskelig å scrape pga. JavaScript-rendering eller blokkeringer.
- **Løsning:** Vi planla en lagdelt strategi: Først `Beautiful Soup` (enkel HTML), deretter `Playwright` (hvis JS er nødvendig), og manuell innsamling som siste utvei.
- **KI sin rolle:** KI hjalp oss å identifisere denne risikoen tidlig og foreslå konkrete biblioteker og fallback-strategier.

**Utfordring 2: Presisjon i svar (RAG Accuracy)**
- **Problem:** Risiko for at chatboten hallusinerer eller gir irrelevante svar (under 80% nøyaktighet).
- **Løsning:** Vi la inn en spesifikk testfase i uke 4 for "Iterative refinement", hvor vi justerer "chunk size" og "overlap" i embeddings. Vi valgte også å bruke en "confidence threshold" på 0.7 for å filtrere ut dårlige treff.
- **KI sin rolle:** KI foreslo de spesifikke parameterne for RAG-pipelinen og testmetodikken.

### 3.2 Samarbeidsutfordringer
- **Kommunikasjon med AI-agenter:** Under UX-sesjonen (17. november) oppsto det en situasjon hvor AI-agenten (UX Designer) feilaktig trodde vi manglet visuelle artefakter (`ux-showcase.html`) og ga oss en lav valideringsscore (32%).
- **Løsning:** Vi måtte eksplisitt peke agenten til riktig fil. Etter dette økte scoren til 76%.
- **Læring:** Dette lærte oss at AI-agenter kan ha "blinde soner" og krever tydelig kontekststyring.

### 3.3 KI-spesifikke utfordringer
- **Språkkvalitet (Norsk):** En bekymring har vært om engelskspråklige modeller kan generere naturlig norsk, spesielt med fagterminologi fra byggebransjen (f.eks. "seriøsitetskontroll").
- **Løsning:** Vi valgte GPT-4o-mini som har god støtte for norsk, og la inn krav om norske system-prompts og en ordliste for faguttrykk.

---

## 4. Kritisk vurdering av KI sin påvirkning

### 4.1 Fordeler med KI-assistanse

**Effektivitet og produktivitet:**
- KI har vært ekstremt effektivt for å produsere dokumentasjon. I arbeidet med "Case Description" økte vi dokumentet fra 73 linjer til 1040 linjer på bare 2-3 timer. Dette er en økning på over 1300%, noe som ville tatt dager å skrive manuelt.
- Oppsett av prosjektstruktur og boilerplate-kode gikk mye raskere enn ved tradisjonell koding.

**Kvalitet på koden og planlegging:**
- KI hjalp oss å tenke på ting vi kanskje ville glemt, som en detaljert "Risk Management"-plan og en spesifikk teststrategi med 8 evalueringsmetrikker. Dette hevet kvaliteten på prosjektplanen fra et "C-nivå" til et estimert "A/B-nivå".

### 4.2 Begrensninger og ulemper

**Kvalitet og pålitelighet:**
- Som nevnt i UX-sesjonen, kan KI gjøre feilvurderinger basert på manglende kontekst. Den kan være "skråsikker" selv når den tar feil.
- Vi må hele tiden verifisere at koden som genereres faktisk fungerer og følger "beste praksis", og ikke bare ser riktig ut.

**Avhengighet:**
- Det er en risiko for at vi lener oss for mye på KI for å strukturere tankene våre. Når KI genererer 1000 linjer med tekst, kan det være fristende å bare "godkjenne" det uten å lese nøye gjennom alt.

### 4.3 Sammenligning: Med og uten KI
- **Uten KI:** Vi ville brukt mesteparten av tiden på å skrive dokumentasjon og sette opp grunnleggende kode. Vi ville sannsynligvis hatt en mindre detaljert risikoanalyse og testplan.
- **Med KI:** Vi har kunnet fokusere mer på *hva* vi skal lage (produktverdi, brukerreiser) og *hvordan* det skal henge sammen (arkitektur), mens KI har tatt seg av "grovarbeidet" med å skrive teksten og koden. Sluttresultatet er mer profesjonelt og gjennomtenkt.

### 4.4 Samlet vurdering
KI har vært en netto positiv faktor. Den har fungert som en "seniorutvikler" og "prosjektleder" som har guidet oss gjennom prosessen, men vi har måttet være aktive "reviewers" for å sikre kvaliteten.

---

## 5. Etiske implikasjoner

### 5.1 Ansvar og eierskap
- Selv om KI har skrevet store deler av koden og dokumentasjonen, er det vi som gruppe som er ansvarlige for sluttproduktet. Hvis chatboten gir feil svar om HMS-regler, er det vårt ansvar, ikke OpenAI sitt.
- Vi må kvalitetssikre alt KI genererer.

### 5.2 Transparens
- Vi mener det bør være transparent at KI er brukt. I denne rapporten dokumenterer vi åpent hvordan vi har brukt verktøy som Claude og Gemini.
- For sluttbrukeren av chatboten er det også viktig at det kommer tydelig frem at de snakker med en AI, og at svarene kan inneholde feil.

### 5.3 Påvirkning på læring
- Ved å bruke KI slipper vi å skrive mye "boilerplate"-kode, noe som kan gjøre at vi mister trening i grunnleggende syntaks.
- Samtidig lærer vi mer om arkitektur, systemdesign og prompt engineering, som er ferdigheter som blir viktigere fremover.

---

## 6. Teknologiske implikasjoner

### 6.1 Kodekvalitet og vedlikehold
- KI-generert kode er ofte godt dokumentert og følger standarder, men den kan bli kompleks.
- En utfordring er at hvis vi ikke forstår koden 100% selv, blir det vanskelig å debugge den senere.

### 6.2 Fremtidig utvikling
- Vi tror utviklere fremover vil bruke mer tid på å være "arkitekter" og "reviewers" enn å skrive hver enkelt linje med kode.
- Evnen til å formulere presise instruksjoner (prompts) til KI blir en nøkkelkompetanse.

---

## 7. Konklusjon og læring

### 7.1 Viktigste lærdommer
1. **Kontekst er konge:** KI trenger presis og fullstendig kontekst for å gi gode svar. Manglende kontekst fører til hallusinasjoner eller feilvurderinger.
2. **Iterasjon er nødvendig:** Det første svaret fra KI er sjelden det beste. Man må iterere, be om forbedringer, og utfordre svarene.
3. **Planlegging lønner seg:** Å bruke tid på å lage en god "Case Description" og "Product Brief" med KI i starten sparte oss for mye tid senere i prosessen.

### 7.2 Hva ville dere gjort annerledes?
- Vi ville kanskje startet med en enda enklere MVP for å komme raskere i gang med testing.
- Vi kunne vært enda nøyere med å dokumentere *hvilke* prompts vi brukte underveis for å lære mer systematisk av det.

### 7.3 Anbefalinger
- **Bruk KI til planlegging:** Ikke bare bruk KI til å skrive kode, men bruk den til å kritisere planene dine og finne hull i logikken.
- **Vær kritisk:** Aldri kopier kode eller tekst fra KI uten å lese og forstå det først.

### 7.4 Personlig refleksjon (individuelt)

**[Navn på gruppemedlem 1]:**
[Fyll inn personlig refleksjon her...]

**[Navn på gruppemedlem 2]:**
[Fyll inn personlig refleksjon her...]

**[Navn på gruppemedlem 3]:**
[Fyll inn personlig refleksjon her...]

---

## 8. Vedlegg (valgfritt)
- Skjermbilder av applikasjonen (se egen mappe)
- Lenke til GitHub repository: [Sett inn lenke]

---

**Ordantall:** Ca. 1200 ord (foreløpig utkast)
**Forventet lengde:** 3000-5000 ord
