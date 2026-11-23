# Controllo di gestione e export studio

## Anti-double-counting (R3.x)

### Ciclo passivo (R3.1)

```
C_effettivo = C_fatture_passive + C_DDT_non_fatturati
I_residuo = max(0, Valore_Ordine − Valore_DDT_e_Fatture)
```

Non sommare `C_effettivo` e `I_residuo`.

### Ciclo attivo (R3.2)

- Preventivi accettati → solo budget/portafoglio.
- Produzione consuntiva = fatture emesse (netto TD04/storni) + SAL maturati non fatturati.

## Margini

| Concetto | Formula |
|----------|---------|
| **Margine %** (su prezzo) | `Prezzo = Costo / (1 − m)` |
| **Markup %** (su costo) | `Prezzo = Costo × (1 + k)` |
| Esempio | m=25% → prezzo 133,33 da costo 100; k=25% → 125 (margine reale 20%) |

Bloccare `m ≥ 1` (prezzo infinito o negativo). `m < 0` (vendita sottocosto) è lecito: avviso, non blocco.

Nel progetto, le definizioni del prodotto (KPI, categorie di costo, decisioni E-ID) prevalgono su queste formule generiche: una differenza va in [DIVERGENZA DA DECIDERE].

## EBITDA e BEP (R3.3)

- MdC = Ricavi − costi diretti.
- EBITDA = MdC − overhead operativi (no ammortamenti/finanza/imposte).
- BEP: se `(R − CV) ≤ 0` → soglia irraggiungibile.

## Manodopera edile (R3.5)

`Incidenza% = Costo_Manodopera / Valore_Opera_Netto_IVA × 100` vs indici CNCE per categoria (OG1, OS6, restauro 30%, …).

## Export commercialista (flussi)

1. **Prima nota** — dare/avere, commessa, partite, ritenute garanzia, **11% bonifici parlanti**. Ogni registrazione deve quadrare anche con ritenuta e bollo: fornitore = costo + IVA − ritenuta (Avere «Erario c/ritenute da versare»); cliente = ricavo + IVA − ritenuta subita (Dare «Erario c/ritenute subite»). Se il totale salvato è già al netto, la ritenuta va ricavata e registrata, altrimenti la fattura esce dai registri.
2. **Registri IVA** — TD16–TD19 in vendite **e** acquisti; **escludere TD29**.
3. **CU** — per **DataPagamento** (ritenute a cassa).
4. **F24** — Erario periodo competenza.

### Codici tributo F24 (azienda)

| Codice | Sezione | Uso |
|--------|---------|-----|
| **6001–6012** | Erario | IVA mensile (gennaio–dicembre); periodo = anno |
| **6031–6033** | Erario | IVA trimestrale, 1°–3° trimestre. Per opzione: +1% di interessi sul debito |
| **6034** | Erario | 4° trimestre **solo** per i trimestrali speciali (autotrasporto, carburanti…), senza l'1% |
| **6099** | Erario | Saldo IVA annuale; i trimestrali per opzione ci versano il 4° trimestre, con l'1% |
| **6035** | Erario | **Solo** acconto IVA (dicembre), mai il versamento di un mese |
| **1001** | Erario | Ritenute su retribuzioni dipendenti (non sezione INPS) |
| **1040** | Erario | Ritenute lavoro autonomo (CU/770 ST), per data di pagamento |
| **1038** | Erario | Ritenute su provvigioni, agenzia, mediazione |
| **1039** | — | **Solo** riconciliazione incassi: ritenuta 11% su bonifici versata da banche/Poste, **non** F24 impresa |
| **1041** | — | **Non** usare come ritenute appalti edilizia |

La periodicità (mensile, trimestrale per opzione, trimestrale speciale, esonerato/forfettario) deve stare nelle impostazioni fiscali: se manca, non dedurla, segnala la riga IVA «da completare».

Contributi INPS (sezione INPS, causali DM10 ecc.) separati dall'IRPEF: non sommare tutto sotto un solo codice. Per codici diversi da questi verifica sulla tabella ufficiale dei codici tributo AdE prima di proporli.

Appalti >200k €: codice delega **09** (Committente).

## Ritenute a cassa (R5.6)

F24 e CU alla **data quietanza**; pagamenti parziali ripartiti pro-quota tra anni d’imposta.

## Conservazione a norma

- Standard **UNI 11386:2020** (SInCRO): RdV, IPdA, hash, firma, marca temporale.
- Termine: **3 mesi** dalla presentazione dichiarazione redditi.
- Date operative: fatture **2025** → prudente **01/02/2027**; **2026** → **31/01/2028**.
- Durata minima **10 anni** (art. 2220 c.c.).

## Anti-pattern audit (A4.x)

| Codice | Rischio |
|--------|---------|
| A4.1 | float/double su importi fiscali |
| A4.2 | IVA su totale unico |
| A4.3 | Ritenuta sul ricavo di competenza |
| A4.4 | Double-counting documenti |
| A4.5 | Storico non immutabile |
| A4.6 | TD16–TD20 / TD29 ruoli invertiti |
| A4.7 | Bonifico parlante non scorporato |
| A4.8 | IVA del riepilogo come somma delle IVA di riga |
| A4.9 | Natura derivata dall'aliquota (0% = N2.2 sempre) |
| A4.10 | Partita doppia che non quadra con ritenuta o bollo |
| A4.11 | Codice tributo IVA del mese = 6035 |
| A4.12 | Esigibilità D (IVA per cassa) detratta subito |