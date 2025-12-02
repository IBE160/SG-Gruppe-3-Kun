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
Prosjektet vårt er en chatbot utviklet for HMSREGs dokumentasjon. Hovedmålet med applikasjonen er å gi brukere av HMSREG – som leverandører, underleverandører, bygningsarbeidere, prosjektledere og administratorer – raske og presise svar på spørsmål om systembruk, krav, prosedyrer og feilsøking. Målet er å redusere belastningen på support, sikre konsistente svar, øke brukernes effektivitet og gjøre HMSREG-dokumentasjonen mer tilgjengelig.

### 2.2 Arbeidsmetodikk

Vi organiserte arbeidet gjennom jevnlige møter på Teams, i gjennomsnitt en gang i uken. Vi fulgte progresjonen i forelesningene og tok valg bassert på valgene som ble tatt og anbefalt i forelesningene. Under disse gruppemøtene var det vanlig at én person delte skjerm i VS Code, mens alle bidro med innspill og kodet sammen i sanntid.

- **Hvordan fordelte dere oppgaver?**
Oppgaver ble fordelt der det var fornuftig. I startfasen var det vanskelig å fordele oppgaver, men research og brainstorming for eksempel, ble gjort individuelt, før resultatene ble diskutert i fellesskap. Hver enkelt jobbet i sin egen Git-branch for å unngå konflikter. Når en oppgave var fullført, ble koden slått sammen i `main`-branchen etter en gjennomgang.

- **Hvilke verktøy brukte dere for samarbeid og hvordan det fungerte? (f.eks. Git, og Teams)**
  - **Git:** Vi brukte Git for versjonskontroll, med en branch-basert arbeidsflyt. Dette fungerte svært bra og ga oss god kontroll på endringer og samarbeid om kode.
  - **Teams:** Brukt for alle våre gruppemøter, skjermdeling og diskusjoner.
  - **VS Code:** Skjermdeling i VS Code ble brukt for  mob-programmering.

- **Hvordan brukte dere KI-verktøy i prosessen?**
KI-verktøy var en integrert og aktiv del av hele prosessen vår, og vi fulgte BMAD-metoden for å strukturere og gjennomføre prosjektet.

I praksis brukte vi Gemini CLI som vårt primære verktøy. Inne i CLI-et benyttet vi oss av de spesialiserte agentene fra BMAD-rammeverket som Product Manager, UX Designer og Architect for å drive prosjektet fremover i de ulike fasene.

Mer konkret brukte vi KI til å:
- **Generere dokumentasjon:** Utforme alt fra tekniske spesifikasjoner til brukerhistorier og denne refleksjonsrapporten.
- **Skrive kode:** Generere boilerplate, implementere funksjoner og foreslå løsninger på tekniske problemer.
- **Analysere problemer:** KI hjalp oss med å identifisere risikoer og foreslå mottiltak.
- **Fasilitere brainstorming:** Vi brukte KI-styrte teknikker som "Five Whys" for å komme til roten av brukerproblemer og "Question Storming" for å utforske ulike løsningsretninger.

Vi startet opprinnelig med Claude Code, men gikk raskt over til å bruke Gemini CLI ettersom alle gruppemedlemmene hadde tilgang til en sjenerøs gratisversjon (free tier), noe som gjorde det enkelt for alle å delta aktivt.

### 2.3 Teknologi og verktøy
[Liste over de viktigste teknologiene og verktøyene dere brukte]
- Frontend: [f.eks. NextJS, HTML/CSS]
- Backend: [f.eks. Python/FastAPI]
- Database: [f.eks. Supabase, MongoDB, PostgreSQL]
- KI-verktøy: [f.eks. Claude Code, Gemini CLI, GPT-5 Codex]
- Andre verktøy: [f.eks. VS Code, BMAD etc]

### 2.4 Utviklingsfaser
[Beskriv de ulike fasene i utviklingen]

**Fase 1: Planlegging**
- [Hva gjorde dere i denne fasen?]
- [Hvordan brukte dere KI her? Husk å lagre promptene deres! Inkluder ALLE stegene dere gjorde.]

**Fase 2: Utvikling**
- [Hva gjorde dere i denne fasen?]
- [Hvordan brukte dere KI her? Husk å lagre promptene deres! Inkluder ALLE stegene dere gjorde.]

---

## 3. Utfordringer og løsninger

### 3.1 Tekniske utfordringer
[Beskriv 2-3 konkrete tekniske problemer dere møtte]

**Utfordring 1: [Tittel]**
- Problem: [Beskriv problemet]
- Løsning: [Hvordan løste dere det?]
- KI sin rolle: [Hvordan hjalp eller hindret KI dere?]

**Utfordring 2: [Tittel]**
- Problem: [Beskriv problemet]
- Løsning: [Hvordan løste dere det?]
- KI sin rolle: [Hvordan hjalp eller hindret KI dere?]

### 3.2 Samarbeidsutfordringer
[Utfordringer knyttet til teamarbeid og kommunikasjon]
- [Beskriv utfordringer og hvordan dere løste dem]
  Vårt samarbeid har i hovedsak vært velfungerende og uten store konflikter. Vi var gjennomgående enige om retningen for prosjektet.

Den primære utfordringen vi møtte, var knyttet til koordinering og fordeling av oppgaver. Dette skyldtes ikke manglende samarbeidsvilje – tvert imot var alle svært engasjerte. Utfordringen lå i oppgavenes natur; mange av utviklings- og designoppgavene var såpass sammenvevde at det var vanskelig å dele dem opp i helt uavhengige deler som kunne løses hver for seg.

Løsningen vår ble å dreie arbeidsmetodikken mot mer sanntids-samarbeid. Vi satte av faste, dedikerte tider til gruppemøter på Teams hvor alle deltok aktivt. På disse møtene jobbet vi ofte med par- eller mob-programmering, der én delte skjerm og de andre bidro med innspill. Dette sikret at alle hadde lik forståelse av koden og fremdriften, og det reduserte behovet for å slå sammen store, komplekse kodeendringer.

Vi opplevde ingen nevneverdige misforståelser eller kommunikasjonsproblemer, da vi hadde en åpen dialog og alle hadde tilgang til og brukte Teams aktivt for kommunikasjon.

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
- Hvordan påvirker KI-generert kode langsiktig vedlikehold?
- Er KI-kode like forståelig som menneskeskrevet kode?
- Utfordringer med å debugge KI-generert kode

### 6.2 Standarder og beste praksis
- Følger KI alltid beste praksis og industristandarder?
- Eksempler på hvor KI foreslo utdaterte eller dårlige løsninger
- Viktigheten av å validere KI sine forslag

### 6.3 Fremtidig utvikling
- Hvordan tror dere KI vil påvirke programvareutvikling fremover?
  KI vil fundamentalt endre programvareutvikling ved å automatisere repeterende oppgaver som kodeskriving, testing og feilsøking. Dette vil føre til raskere utviklingssykluser og la utviklere fokusere mer på strategiske oppgaver som systemdesign, arkitektur og kreativ problemløsning. Vi tror KI vil bli en uunnværlig partner i utviklingsteam, der den fungerer som en "super-intelligent" assistent som kan generere kode, optimalisere ytelse og til og med forutsi potensielle feil før de oppstår. Samtidig vil KI senke terskelen for å lage programvare, slik at personer med mindre teknisk bakgrunn kan realisere ideene sine gjennom naturlig språk og høynivå-beskrivelser.

- Hvilke ferdigheter blir viktigere for utviklere?
  Ferdigheter knyttet til kritisk tenkning, problemløsning på et høyere abstraksjonsnivå og evnen til å formulere presise krav blir avgjørende. Utviklere må bli eksperter på å "prompte" og veilede KI-systemer for å få ønsket resultat. Dette innebærer en dypere forståelse av systemarkitektur og designprinsipper for å kunne vurdere og integrere KI-generert kode på en fornuftig måte. Evnen til å validere, teste og kvalitetssikre KI-genererte løsninger blir også kritisk. I tillegg vil "menneskelige" ferdigheter som kreativitet, kommunikasjon og etisk bevissthet bli viktigere, ettersom utviklerens rolle i større grad blir å styre og forme teknologien, ikke bare å produsere den.

- Deres anbefalinger for hvordan man bør bruke KI i utviklingsprosesser
  1.  **Bruk KI som en partner, ikke en erstatter:** Se på KI som et verktøy for å forsterke dine egne ferdigheter. Bruk den til å automatisere kjedelige oppgaver, generere boilerplate-kode og utforske alternative løsninger, men behold alltid den endelige kontrollen og ansvaret for koden.
  2.  **Start med små, veldefinerte oppgaver:** Ikke forvent at KI skal bygge hele applikasjonen for deg. Begynn med å bruke den til å løse mindre, isolerte problemer, som å skrive en spesifikk funksjon, lage enhetstester eller refaktorere en kodeblokk.
  3.  **Valider og test all KI-generert kode:** Aldri stol blindt på koden KI produserer. Gjennomgå den nøye, forstå hva den gjør, og skriv grundige tester for å verifisere at den fungerer som forventet og ikke introduserer nye feil eller sikkerhetshull.
  4.  **Invester i "prompt engineering":** Lær deg å skrive klare, konsise og kontekst-rike prompts. Jo bedre du er til å kommunisere dine intensjoner til KI-en, desto bedre og mer relevant blir resultatet.
  5.  **Integrer KI i hele arbeidsflyten:** Bruk KI ikke bare til koding, men også til planlegging, design, dokumentasjon og testing. Verktøy som BMAD-rammeverket viser hvordan KI kan være en verdifull ressurs i alle faser av et prosjekt.

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