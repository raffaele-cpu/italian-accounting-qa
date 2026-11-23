# Edilizia, commesse, SAL

## IVA agevolata

| Aliquota | Casi principali |
|----------|-----------------|
| **4%** | Abitazioni non di lusso (prima casa), barriere architettoniche (Tab. A II) |
| **10%** | Recupero/restauro/ristrutturazione, case abitazione, beni finiti committente (Tab. A III → IV nn. 116–117 dal 2027) |

**Manutenzioni abitative** (art. 7 L. 488/1999 → art. 35 c. 4 + Tab. A IV n. 121 D.Lgs. 10/2026): 10% sulla prestazione dell’esecutore al committente; **non** su subappalti all’impresa principale né acquisti diretti del cliente.

## Beni significativi (D.M. 29/12/1999)

Sette categorie (ascensori, infissi, caldaie, videocitofoni, climatizzazione, sanitari/rubinetteria, sicurezza).

**R5.1**: su manutenzione abitativa con fornitura beni da esecutore:

- Se `B ≤ P` (bene ≤ resto prestazione): tutto il corrispettivo al 10%.
- Se `B > P`: base 10% = `2×P` (fino a concorrenza); eccedenza `B − P` al **22%**; valore beni in fattura.
- Restauro/ristrutturazione edilizia: **no** cap beni significativi — tutto 10%.
- Componenti autonome (tapparelle, zanzariere non integrate): contano in P al 10%.

## Reverse charge edile

Subappalti e servizi (pulizia, demolizione, impianti, completamento): **N6.x**; fattura senza IVA dall’appaltatore.

## Bonifico parlante (dal 03/2024, 11%)

`Ritenuta = HALF_UP((Bp / 1.22) × 0.11, 2)` — scorporo convenzionale **sempre al 22%**, anche con fattura al 10% o forfettaria.

## DURC congruità

- Obbligatorio: lavori pubblici + privati **≥ 70.000 €** netti IVA (intero cantiere).
- Scostamento manodopera: tolleranza **5%** con DL; oltre → regolarizzazione 15 gg / BNI.
- Blocco **pre-saldo** senza congruità positiva.

## DURF (art. 17-bis D.Lgs. 241/1997)

Appalti/subappalti privati **> 200.000 €/anno** (per singola impresa) senza DURF: verifica versamenti ritenute lavoratori → F24 deleghe distinte codice identificativo **"09"** (Committente).

Si applica solo se ricorrono **tutte** le condizioni: opere/servizi con **prevalente utilizzo di manodopera**, presso le **sedi di attività del committente**, con **beni strumentali** del committente o a lui riconducibili. Fuori da queste condizioni nessun obbligo.

## Ciclo SAL e TD04

### R2.1 Competenza vs liquidità

- Economico: SAL maturati + lavori da fatturare.
- Tesoreria: incassi/scadenze netti (ritenute, split, garanzia, 11% bonifici).

### R2.2 Storno acconti

`Imponibile_saldo = V_tot − Σ acconti` per aliquota; **storni negativi** con stessa aliquota/natura degli acconti.

### R2.3 Ritenuta di garanzia

Credito vincolato a collaudo; **non** riduce ricavo di commessa.

### R2.4 TD04

Importi XML **positivi**; segno contabile negativo; stessa qualificazione fiscale originale; dal 2027 richiamo art. 92 D.Lgs. 10/2026.

## Tabella di verità SAL (estratto)

| Regola | Edge case |
|--------|-----------|
| R2.2 | Acconto 10%, saldo 22%: storno mantiene aliquota acconto |
| R2.3 | Senza DURC: saldo bloccato anche senza contestazioni tecniche |
| R2.4 | TD04: mai importi con segno meno nell’XML |