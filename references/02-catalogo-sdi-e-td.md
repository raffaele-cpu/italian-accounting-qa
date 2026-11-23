# Catalogo SDI, tolleranze e TipoDocumento

## Tolleranze pre-validazione (chiuse)

| Controllo | Codice | Tolleranza |
|-----------|--------|------------|
| Imposta riepilogo | 00421 | **±0,01 €** (HALF_UP 2 decimali) |
| ImponibileImporto | 00422 | **±1,00 €** |
| PrezzoTotale riga | 00423 | **quadratura esatta** (prezzo unitario, sconti, quantità) |

## Fascia 00200–00330 (anagrafica e formato)

Integrare in pre-validazione oltre a 00100 e 004xx:

- Validazione struttura anagrafica, FormatoTrasmissione, IdFiscale.
- **00313**: uso errato di `XXXXXXX` per soggetti non residenti.
- **00330**: caselle PEC di sistema SdI nel destinatario.
- **`0000000`**: privati senza canale accreditato (con PEC o consumatore finale).
- Verifica su Elenco Controlli integrale: dettaglio **00448**, **00460** (testo v. 1.10).

## Catalogo 004xx documentato (estratto)

| Codice | Condizione | Azione preventiva |
|--------|------------|-------------------|
| 00100 | Certificato firma non valido | Check CA pre-invio |
| 00400/00413 | Aliquota 0 senza Natura | Blocco |
| 00404/00409 | Duplicati | Univocità DB / lotto |
| 00411 | Ritenuta=SI senza DatiRitenuta | Blocco |
| 00414/00430 | Natura con aliquota > 0 | Blocco |
| 00419 | Riepiloghi < distinte aliquote | Blocco |
| 00420 | N6 + EsigibilitaIVA S | Blocco |
| 00421–00423 | Calcoli | Ricalcolo + tolleranze sopra |
| 00424 | Aliquota non percentuale (22.00 non 0.22) | Blocco |
| 00425 | Numero senza cifre | RegEx |
| 00426 | PECDestinatario mancante | Con regole CodiceDestinatario |
| 00428 | FormatoTrasmissione / versione | Coerenza FPA12/FPR12 |
| 00437 | Sconto senza % né importo | Blocco |
| 00445 | N2, N3, N6 generici | Solo sottocodici |
| 00471/00473/00476 | TD vs identificativi | Matrice TD |
| TD29 | Cedente paese ≠ IT | Blocco |

## TipoDocumento (serie reale)

**Non esistono TD10–TD15.**

| Range | Esempi |
|-------|--------|
| TD01–TD06 | TD01 fattura, TD04 nota credito, TD06 parcella |
| TD07–TD09 | Semplificata / NC / ND semplificata |
| TD16–TD20 | Integrazioni / autofatture (RC, estero, intra, regolarizzazioni) |
| TD22–TD29 | Estrazioni deposito, differite, triangolari, TD26 ammortizzabili, TD28 San Marino, **TD29** omessa/irregolare fattura |

TD29: comunicazione denuncia; **non** autofattura RC (usare TD20+TD16).

## Checksum anagrafica

### Partita IVA (11 cifre)

- Luhn **modificato** (posizioni pari raddoppiate, somma modulo 10).
- **Bloccare esplicitamente `00000000000`** (può superare il test formale in implementazioni deboli).

### Codice fiscale (16 caratteri)

- Modulo 26 con tabelle valori posizioni dispari/pari.
- **Omocodia**: sostituzione cifre con lettere LMNPQRSTUV (fino a 127 varianti).
- Società: 11 cifre = stessa P.IVA.

### CodiceDestinatario

| Destinatario | Codice |
|--------------|--------|
| PA | 6 caratteri IPA |
| B2B con canale | 7 caratteri |
| Senza canale IT | `0000000` + PEC se disponibile |
| Estero | `XXXXXXX` (non per residenti IT — 00313) |
| Consumatore finale | `0000000`, solo CF |

Script: `scripts/validate_fiscal_ids.py`.