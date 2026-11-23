# Cascata fiscale FatturaPA

## Ordine di calcolo (R1.1)

1. `PrezzoTotale` riga: `HALF_UP((PrezzoUnitario ± sconti riga) × Quantità, 2)`
2. `ScontoMaggiorazione` testata (00437: Tipo + almeno Percentuale o Importo)
3. `DatiCassaPrevidenziale` (TC01–TC22): flag `concorre_base_iva`, `soggetta_ritenuta` storicizzati
4. Raggruppamento **DatiRiepilogo** per (AliquotaIVA, Natura, EsigibilitaIVA)
5. `Imposta` = `HALF_UP(ImponibileImporto × AliquotaIVA / 100, 2)` — tolleranza SDI **±0,01 €**
6. `ImportoBollo` (2,00 € se operazioni senza IVA > 77,47 €, regole N1/N2/N4)
7. `ImportoTotaleDocumento`
8. `DatiRitenuta` (RT01/RT02) se almeno una riga `Ritenuta = SI` (00411)
9. `NettoAPagare` = totale documento − ritenuta; **ricavo di competenza** resta lordo imponibile

## R1.2 Ritenuta

- Base: imponibile netto IVA + casse soggette a ritenuta (es. rivalsa INPS 4% GS); esclusa cassa previdenziale “pura”.
- Parametri: `quota_base_ritenuta` (100% / 50% / 20%), aliquota (20% / 23%).
- Forfetari: né applicano né subiscono ritenuta.

## R1.3 Split payment

- Decisione UE 2026/1728: proroga al **30/06/2029** (escluse FTSE MIB dal 01/07/2025).
- `EsigibilitaIVA = S`: IVA in totale documento; incasso = solo imponibile.
- **00420**: N6.x + EsigibilitaIVA `S` vietato.

## R1.4 Bollo virtuale

- 2,00 € se somma importi senza IVA > 77,47 € (es. N4, N2.2 forfetari).
- Rivalsa cliente: riga di dettaglio; a carico emittente: `DatiBollo` senza variare netto a pagare.

## R1.5 Aliquota vs Natura

| AliquotaIVA | Natura |
|-------------|--------|
| 0,00 | obbligatoria; no N2, N3, N6 generici (00445) |
| > 0 | assente (00414 / 00430) |

## Tabella di verità (estratto)

| Caso | Input | Output atteso |
|------|--------|----------------|
| Riga | Pu=100, Q=1, IVA 22% | PrezzoTotale 100; Imposta gruppo 22,00 |
| Cassa + riga stessa aliquota | Ik=1000, Ck=40, a=22% | ImponibileImporto 1040; Imposta 228,80 |
| Split PA | Imponibile 1000, IVA 220 | Totale 1220; incasso 1000 |
| Bollo | S_nb=77,48 € senza IVA | ImportoBollo 2,00 |

## Fattura semplificata (TD07–TD09)

- Schema dedicato; TD07 fattura, TD08 NC, TD09 ND semplificata.
- **400 € IVA inclusa**: solo regime **ordinario** (note rettificative escluse dal tetto).
- Dal **01/01/2025**: nessun limite per **forfetari** e **RF20**.
- Esclusi: intra-UE, reverse charge, operazioni con IVA nello Stato destinatario (salvo esenti).
- Dal 11/01/2027: regime **RF21** forfetari (Specifiche v. 1.10).

## Mappatura aliquote principali (2026 vs 2027)

Aliquote percentuali invariate; rinumerazione Tabella A e Nature (N2.1, N2.2, N3.x, N4, N6.x) con riferimenti DPR 633/72 → D.Lgs. 10/2026 — dettaglio in `05-raccordo-2026-2027.md`.