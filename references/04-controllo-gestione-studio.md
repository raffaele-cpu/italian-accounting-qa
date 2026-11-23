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

Bloccare `m ≥ 1` o `m < 0`.

## EBITDA e BEP (R3.3)

- MdC = Ricavi − costi diretti.
- EBITDA = MdC − overhead operativi (no ammortamenti/finanza/imposte).
- BEP: se `(R − CV) ≤ 0` → soglia irraggiungibile.

## Manodopera edile (R3.5)

`Incidenza% = Costo_Manodopera / Valore_Opera_Netto_IVA × 100` vs indici CNCE per categoria (OG1, OS6, restauro 30%, …).

## Export commercialista (flussi)

1. **Prima nota** — dare/avere, commessa, partite, ritenute garanzia, **11% bonifici parlanti**.
2. **Registri IVA** — TD16–TD19 in vendite **e** acquisti; **escludere TD29**.
3. **CU** — per **DataPagamento** (ritenute a cassa).
4. **F24** — Erario periodo competenza.

### Codici tributo F24 (azienda)

| Codice | Uso |
|--------|-----|
| **1040** | Lavoro autonomo / assimilati (CU/770 ST) |
| **1038** | Provvigioni, agenzia, mediazione |
| **9399** | Regolarizzazione IVA |
| **1039** | **Solo** riconciliazione incassi: ritenuta 11% su bonifici (banche/Poste), **non** F24 impresa |
| **1041** | **Non** usare come ritenute appalti edilizia |

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