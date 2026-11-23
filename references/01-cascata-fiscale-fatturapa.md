# Cascata fiscale FatturaPA

## Ordine di calcolo (R1.1)

1. `PrezzoTotale` riga: `HALF_UP((PrezzoUnitario ± sconti riga) × Quantità, 2)`
2. `ScontoMaggiorazione` testata (00437: Tipo + almeno Percentuale o Importo)
3. `DatiCassaPrevidenziale` (TC01–TC22): flag `concorre_base_iva`, `soggetta_ritenuta` storicizzati
4. Raggruppamento **DatiRiepilogo** per (AliquotaIVA, Natura, EsigibilitaIVA)
5. `Imposta` = `HALF_UP(ImponibileImporto × AliquotaIVA / 100, 2)` — tolleranza SDI **±0,01 €**. Calcolata sul **gruppo**, non come somma delle IVA di riga: con n righe l'errore della somma arriva a n × 0,005 € (simulazione: 10 righe al 22% → ~10% delle fatture fuori tolleranza). Se serve un'IVA per riga, il resto si scarica sull'ultima riga del gruppo.
6. `ImportoBollo` (2,00 € se la somma degli importi **senza IVA** del documento > 77,47 €: vedi R1.4)
7. `ImportoTotaleDocumento` = imponibili + imposte (+ bollo addebitato), **al lordo della ritenuta**
8. `DatiRitenuta` (RT01/RT02) se almeno una riga `Ritenuta = SI` (00411)
9. `NettoAPagare` = totale documento − ritenuta (è `ImportoPagamento`); **ricavo di competenza** resta lordo imponibile

Anti-pattern: salvare il totale netto ritenuta e scriverlo come `ImportoTotaleDocumento`; usare un solo campo «totale» per XML, Cassa e prima nota.

## R1.2 Ritenuta

- Base: imponibile netto IVA + casse soggette a ritenuta (es. rivalsa INPS 4% GS); esclusa cassa previdenziale “pura”.
- Parametri: `quota_base_ritenuta` (100% / 50% / 20%), aliquota (20% / 23%).
- Forfetari: non subiscono ritenuta d'acconto; subiscono invece la ritenuta 11% della banca sul bonifico parlante.

## R1.3 Split payment

- Proroga al **30/06/2029** indicata come decisione UE 2026/1728 (escluse FTSE MIB dal 01/07/2025): **fonte da confermare** prima di citarla in un report.
- `EsigibilitaIVA = S`: IVA in totale documento; incasso e `ImportoPagamento` = solo imponibile.
- **00420**: N6.x + EsigibilitaIVA `S` vietato.

## R1.4 Bollo virtuale

- 2,00 € se la somma degli importi senza IVA > 77,47 €. Conta: N1 (escluse art. 15), N2.x (es. N2.2 forfetari), N4 (esenti), N3.x salvo le non imponibili per esportazione e assimilate (verificare l'esenzione caso per caso; le N3.5 da lettera d'intento pagano il bollo).
- **Mai su N6.x** (reverse charge): è un'operazione soggetta a IVA. Anti-pattern: decidere il bollo con «IVA totale = 0».
- `DatiBollo/BolloVirtuale = SI` sempre quando il bollo è dovuto: senza, l'AdE non lo conteggia nel bollo virtuale da versare.
- Rivalsa cliente: riga di dettaglio; a carico emittente: `DatiBollo` senza variare netto a pagare.

## R1.5 Aliquota vs Natura

| AliquotaIVA | Natura |
|-------------|--------|
| 0,00 | obbligatoria; no N2, N3, N6 generici (00445) |
| > 0 | assente (00414 / 00430) |

La Natura dipende dall'**operazione**, non dall'aliquota: serve un campo per riga (o per codice IVA interno). Edilizia: subappalto e servizi del comparto → N6.3 / N6.7; forfetario → N2.2; esenti → N4. Il riepilogo raggruppa per (aliquota, natura, esigibilità), quindi due righe allo 0% con nature diverse fanno due `DatiRiepilogo`.

## Tabella di verità (estratto)

| Caso | Input | Output atteso |
|------|--------|----------------|
| Riga | Pu=100, Q=1, IVA 22% | PrezzoTotale 100; Imposta gruppo 22,00 |
| Cassa + riga stessa aliquota | Ik=1000, Ck=40, a=22% | ImponibileImporto 1040; Imposta 228,80 |
| Split PA | Imponibile 1000, IVA 220 | Totale 1220; incasso 1000 |
| Bollo | S_nb=77,48 € senza IVA | ImportoBollo 2,00 |
| Bollo RC | Subappalto N6.7 da 5.000 € | nessun bollo |
| Ritenuta | Imponibile 1000, IVA 220, RT 20% | ImportoTotaleDocumento 1220; ImportoRitenuta 200; ImportoPagamento 1020 |
| Arrotondamento | Righe 93,93 / 259,69 / 248,83 / 405,83 / 633,97 al 22% | Imposta 361,30 (la somma per riga darebbe 361,28 → 00421) |

## Fattura semplificata (TD07–TD09)

- Schema dedicato; TD07 fattura, TD08 NC, TD09 ND semplificata.
- **400 € IVA inclusa**: solo regime **ordinario** (note rettificative escluse dal tetto).
- Dal **01/01/2025**: nessun limite per **forfetari** e **RF20**.
- Esclusi: intra-UE, reverse charge, operazioni con IVA nello Stato destinatario (salvo esenti).
- Dal 11/01/2027: regime **RF21** forfetari (Specifiche v. 1.10).

## Mappatura aliquote principali (2026 vs 2027)

Aliquote percentuali invariate; rinumerazione Tabella A e Nature (N2.1, N2.2, N3.x, N4, N6.x) con riferimenti DPR 633/72 → D.Lgs. 10/2026 — dettaglio in `05-raccordo-2026-2027.md`.