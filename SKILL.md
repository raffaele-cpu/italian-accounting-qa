---
name: italian-accounting-qa
description: >-
  Audit tecnico del motore fiscale, contabile e di controllo gestione per SaaS B2B
  italiano (PMI, edilizia, servizi) nel biennio 2026–2027: FatturaPA/SDI, cascata
  IVA, commesse/SAL, anti-double-counting, edilizia, export studio, transizione
  Testo Unico IVA. Usa SEMPRE questa skill quando l'utente chiede QA fiscale,
  audit contabile, controlli SDI, verifica FatturaPA, beni significativi, split
  payment, TD01–TD29, DURC/DURF, bonifici parlanti, F24/CU, conservazione SInCRO
  o conformità normativa 2026/2027 su building-core o sibling gestionali.
---

# Italian Accounting QA (2026–2027)

Specifica operativa per agenti che verificano **Pratico for Building** (`building-core`) e moduli collegati. La normativa sta nei file `references/`.

## Installazione (`npx skills`)

Questo repository **è** la skill (root = `SKILL.md` + `references/` + `scripts/`).

```bash
npx skills add raffaele-cpu/italian-accounting-qa --agent cursor -y
```

Opzioni: `-g` (globale), `--agent '*'` (tutti gli agenti). Vedi `README.md`.

## Quando attivare

- Audit o code review su fatturazione elettronica, IVA, ritenute, SAL, margini commessa, export commercialista.
- Implementazione o fix su SDI, anagrafiche fiscali, regime forfetario, edilizia agevolata, TD29.
- Verifica transizione DPR 633/72 → D.Lgs. 10/2026 e Specifiche Tecniche SDI v. 1.10 (operative dall’11/01/2027).

## Workflow di audit

1. **Ambito** — chiedi o inferisci: emissione FE, ricezione SDI, preventivi/commesse, contabilità/export, solo anagrafica.
2. **Carica contesto** — leggi i `references/` pertinenti (non tutto il corpus se il task è circoscritto).
3. **Script deterministici** — per P.IVA/CF e sanity check numerici, dalla root della skill installata (`~/.claude/skills/italian-accounting-qa/`, `.cursor/skills/italian-accounting-qa/` o il clone del repo). Su Windows l'interprete è spesso `python`, non `python3`:
   ```bash
   python scripts/validate_fiscal_ids.py --self-test
   python scripts/validate_fiscal_ids.py --piva 12345678903 --cf RSSMRA80A01H501U
   python scripts/validate_fiscal_ids.py --vat-groups 9393,25969,24883,40583,63397 --rate 22
   ```
4. **Mappatura codice** — in `building-core`:

   | Area | Dove |
   |------|------|
   | XML emesso (TD01/TD04), riepiloghi, Natura, bollo, ritenuta | `server/lib/services/fatturapa-xml-build.ts`, `fatturapa-xml.service.ts`, `fatturapa-xml-credit-note.service.ts` |
   | Totali fattura e IVA di riga | `shared/schemas/accounting.schema.ts` (`calculateInvoiceTotals`), `shared/lib/invoice-line-net.ts`, `server/routes/invoices/issued-items.prepare.ts` |
   | Destinatario SDI, P.IVA/CF | `shared/lib/sdi-recipient.ts`, `shared/lib/italian-vat.ts`, `shared/lib/vat-tax-code.ts` |
   | Ricezione SDI | `server/lib/sdi/`, `server/lib/services/sdi-inbound-*.ts`, `fatturapa-xml-parser.service.ts` |
   | Prima nota, registri, F24 | `shared/lib/ledger-*.ts`, `server/lib/services/ledger/`, `server/lib/services/iva-*.ts` |
   | Commesse, SAL, KPI | `shared/lib/contabilita/`, `shared/lib/costs/kpi/`, `shared/lib/finance-report/` |
   | UI fatture (modulo «Billing», non è Stripe) | `client/src/modules/Billing/` |

   Altri repo: cerca gli equivalenti con grep su `DatiRiepilogo`, `ImponibileImporto`, `TipoDocumento`, `codiceTributo`.
5. **Tassonomia del progetto** — prima di giudicare costi, margini e KPI leggi le definizioni del prodotto: in `building-core` `Docs/product/systems/cost-classification.md` (10 categorie + Movimenti non economici, Fisso/Variabile, registro `cost_allocations`, KPI in `shared/lib/costs/kpi/`) e le decisioni numerate **E-ID** nei piani `tasks/costi/`. Una regola di questa skill che diverge da una decisione E-ID documentata non è un bug: va in **[DIVERGENZA DA DECIDERE]** citando l'E-ID. Usa il vocabolario del manuale (MdC, «Da classificare», produzione, cassetto), non sinonimi.
6. **Report** — classifica ogni rilievo:
   - **[BLOCCANTE]** — rischio scarto SDI, errore fiscale, double-counting ricavi/costi, float su importi fiscali, violazione immutabilità storica, partita doppia che non quadra.
   - **[ALTO]** — gap su controlli 00200–00330, tolleranze SDI, routing 2027, TD/RegimeFiscale, export F24 errato.
   - **[MIGLIORAMENTO]** — copertura test, documentazione, allineamento a v. 1.10 prima della data switch.
   - **[DIVERGENZA DA DECIDERE]** — scelta di prodotto documentata (E-ID, manuale) diversa dalla regola generica: si decide con l'utente, non si corregge d'ufficio.
   Ricontrolla sul codice ogni [BLOCCANTE] riportato da un sottoagente prima di metterlo nel report.
7. **Patch** — proponi diff mirati (file + righe); non applicare fix fiscalmente sensibili senza conferma utente.

## Regole [BLOCCANTI] (sempre verificare)

| ID | Regola | Riferimento |
|----|--------|-------------|
| B1 | **No float** su prezzi, IVA, riepiloghi, partita doppia: `NUMERIC`/centesimi + HALF_UP a 2 decimali sui riepilogo SDI | `references/01-*`, audit A4.1 |
| B2 | **Cascata fiscale** nell’ordine R1.1: riga → sconto testata → cassa → DatiRiepilogo per gruppo → imposta → bollo → totale → ritenuta → netto | `references/01-cascata-fiscale-fatturapa.md` |
| B3 | **Un DatiRiepilogo per distinta** (AliquotaIVA, Natura, EsigibilitaIVA); mai IVA sul totale documento unico | R1.5, 00419 |
| B4 | **Anti-double-counting** preventivo/ordine/DDT/fattura/SAL acconti | `references/04-controllo-gestione-studio.md` R3.1–R3.2 |
| B5 | **Routing normativo** diciture e riferimenti legge per **DataEffettuazione** (≤31/12/2026 DPR 633/72; ≥01/01/2027 D.Lgs. 10/2026) | `references/05-raccordo-2026-2027.md` |
| B6 | **Immutabilità storica** — documenti emessi: snapshot di aliquote, regimi, diciture; no overwrite in-place | A4.5 |
| B7 | **Tolleranze pre-validazione SDI**: Imposta ±0,01 € (00421); ImponibileImporto ±1,00 € (00422); PrezzoTotale esatto (00423) | `references/02-catalogo-sdi-e-td.md` |
| B8 | **TD29** — nessuna registrazione in registro IVA acquisti né detrazione; fornitore in CedentePrestatore, paese IT | R5.5 |
| B9 | **F24 azienda**: IVA mensile **6001–6012**, trimestrale **6031–6033** (+1% per opzione), 4° trimestre **6099** per opzione o **6034** solo trimestrali speciali, **6035 solo acconto**; ritenute 1040 / 1038, dipendenti **1001** in sezione Erario; **1039** solo riconciliazione incassi bonifici parlanti (banche/Poste), non F24 impresa; **non usare 1041** per ritenute appalti; appalti >200k € senza DURF → delega codice identificativo **09** | `references/04-controllo-gestione-studio.md` |
| B10 | **Imposta per gruppo, non per riga**: `Imposta` = HALF_UP(Σ imponibili del gruppo × aliquota). La somma delle IVA arrotondate riga per riga sfora ±0,01 € (00421) già con 5+ righe | `references/01-*` |
| B11 | **Natura da operazione, non da aliquota**: aliquota 0 non implica N2.2; reverse charge → N6.x, esenti → N4, non imponibili → N3.x | R1.5, 00445 |
| B12 | **ImportoTotaleDocumento al lordo della ritenuta**; ritenuta in `DatiRitenuta`, bollo in `DatiBollo`; la partita doppia deve quadrare con ritenuta e bollo | R1.1, R1.4 |
| B13 | **Ricezione SDI per TipoDocumento**: solo TD01–TD03, TD05, TD06, TD24–TD27 diventano costo del fornitore; TD16–TD20, TD28 sono documenti dell'azienda stessa (integrazione: IVA a debito **e** a credito); TD29 fuori registri | `references/02-*`, B8 |

## Puntatori ai references

| File | Contenuto |
|------|-----------|
| `references/01-cascata-fiscale-fatturapa.md` | Cascata, casse TC01–TC22, RT01/RT02, bollo, split payment (proroga al 30/06/2029), semplificata TD07–TD09 |
| `references/02-catalogo-sdi-e-td.md` | Scarti 00100, 00200–00330, 00400–00476, tolleranze, TD01–TD29, P.IVA/CF, CodiceDestinatario |
| `references/03-edilizia-e-commesse-sal.md` | IVA 4%/10%, beni significativi, N6.3/N6.7, bonifici 11%, DURC 70k €, DURF 200k €, SAL, TD04 |
| `references/04-controllo-gestione-studio.md` | Anti-double-counting, margini, EBITDA, BEP, prima nota, F24/CU, conservazione UNI 11386:2020 |
| `references/05-raccordo-2026-2027.md` | Tabella raccordo normativo, DataEffettuazione, SDI v. 1.10, RF21/RF13/RF19, storicizzazione |

## Chiusure operative (delta rispetto al documento base)

- Pulizia artefatti di estrazione: niente marker di citazione numerici nel testo skill.
- Controlli anagrafici **00200–00330** in pre-validazione (es. **00313** XXXXXXX per non residenti errato; **00330** PEC di sistema SdI; **0000000** per privati senza canale).
- **TD10–TD15 non esistono** in FatturaPA: serie TD01–TD06, TD07–TD09, TD16–TD29.
- Fattura semplificata: limite **400 € IVA inclusa** solo regime ordinario; **eliminato** forfetari e RF20 dal 01/01/2025.
- Beni significativi: art. 7 L. 488/1999 → art. 35 c. 4 + Tab. A IV n. 121 D.Lgs. 10/2026 (nn. 116–117 beni finiti/recupero).
- Conservazione: **UNI 11386:2020** (SInCRO); chiusura entro 3 mesi dalla dichiarazione redditi (prudente **01/02/2027** fatture 2025; **31/01/2028** per 2026); decennale.
- Codici **00448** e **00460**: verificare testo integrale Elenco Controlli v. 1.10 prima del freeze.
- Fonti da confermare prima di citarle come certe: proroga split payment (decisione UE 2026/1728, 30/06/2029) e data di pubblicazione delle Specifiche v. 1.10. Il codice tributo **9399** è stato tolto da B9: non verificato.

## Anti-pattern trovati sul campo (audit building-core 23/11/2026)

- IVA di riga arrotondata e poi sommata nel riepilogo → scarti 00421 (B10).
- `Natura = "N2.2"` fissa per ogni riga allo 0%: il reverse charge edile esce come «non soggetta» (B11).
- `total_cents` salvato al netto della ritenuta e scritto come `ImportoTotaleDocumento`; nessun `DatiRitenuta` / `DatiBollo` (B12).
- Bollo calcolato su «IVA totale = 0», quindi applicato anche al reverse charge (N6 è operazione soggetta, niente bollo).
- Prima nota con costo + IVA = totale netto ritenuta → sbilancio, fattura esclusa dai registri.
- F24 IVA mensile con 6035.
- Ricezione: ogni TD diverso da TD04 registrato come costo con IVA detraibile (B13); reverse charge ricevuto con IVA 0.
- Prefisso `IT` lasciato in `IdCodice`; P.IVA estera validata col checksum italiano; validatore P.IVA che accetta `00000000000`.
- `Quantita` scritta con meno decimali di quelli usati per `PrezzoTotale` (00423).
- Detrazione IVA per data fattura invece che per ricezione a cavallo d'anno.

## Output atteso dell’audit

```markdown
# Audit QA Fiscale-Contabile — <modulo> — <data>

## Executive summary
## [BLOCCANTE]
- File: `path` Lnn–mm — descrizione — patch proposta

## [ALTO]
...

## [MIGLIORAMENTO]
...

## [DIVERGENZA DA DECIDERE]
- Decisione / E-ID — regola generica — opzioni

## Verificato e corretto
...

## Copertura skill
- References consultati: ...
- Script eseguiti: ...
```

## Non fare

- Non sostituire parere professionale o deposito ufficiale.
- Non inventare codici TD o scarti SDI non presenti in `references/02` o nell’Elenco Controlli ufficiale.
- Non applicare modifiche schema DB/migrazioni come parte dell’audit senza task esplicito.