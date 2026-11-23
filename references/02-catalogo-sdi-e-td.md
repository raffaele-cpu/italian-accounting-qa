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

TD29: comunicazione all'AdE della fattura omessa o irregolare del fornitore (dal 01/04/2025; per questo caso sostituisce il TD20). **Non** è un documento di integrazione del reverse charge: quello è TD16 (RC interno, es. subappalto edile) o TD17–TD19 (acquisti da estero).

### Ricezione: cosa diventa costo

| TipoDocumento in arrivo | Trattamento |
|-------------------------|-------------|
| TD01, TD02, TD03, TD05, TD06, TD24, TD25, TD26, TD27 | Fattura del fornitore: costo + IVA secondo detraibilità |
| TD04 | Nota di credito: storna costo e IVA della fattura d'origine |
| TD16–TD19 | Integrazione/autofattura dell'azienda stessa: IVA a debito **e** a credito, collegata alla fattura d'origine; **non** un secondo costo |
| TD20, TD28 | Documenti dell'azienda (regolarizzazione, San Marino): stessa logica, non un costo nuovo |
| TD29 | Fuori registri IVA e detrazione (B8) |
| Sconosciuto | In coda con motivo, mai costo automatico |

Riepilogo con Natura N6.x in arrivo = reverse charge: l'IVA è 0 nel documento, ma va integrata dal cessionario (aliquota da proporre). Detrazione IVA: nel periodo di **ricezione** (a cavallo d'anno una fattura di dicembre ricevuta a gennaio va nell'anno nuovo).

### Identificativi nell'XML

- `IdPaese` + `IdCodice` separati: `IdCodice` **senza** prefisso `IT` (anche nel nome file `IT<piva>_<progr>.xml`).
- P.IVA estera: niente checksum italiano; `IdPaese` dal prefisso, non da un default «IT».
- `PECDestinatario`: formato email valido e mai una casella `@pec.fatturapa.it` (00330).
- `Quantita` e `PrezzoUnitario` con gli stessi decimali usati per calcolare `PrezzoTotale` (fino a 8), altrimenti 00423.

## Checksum anagrafica

### Partita IVA (11 cifre)

- Luhn **modificato** (posizioni pari raddoppiate, somma modulo 10).
- **Bloccare esplicitamente `00000000000`** (supera il checksum: somma 0, cifra di controllo 0). Se nel codice ci sono più validatori, devono dare lo stesso esito: cercali tutti.

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