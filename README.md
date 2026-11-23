# italian-accounting-qa

Skill per agenti di coding: audit QA fiscale-contabile del SaaS gestionale B2B italiano (FatturaPA/SDI, commesse/SAL, edilizia, transizione Testo Unico IVA 2026–2027).

Pensata per **Pratico for Building** (`building-core`), ma utilizzabile su qualsiasi codebase con motore fiscale italiano.

## Installazione

Node.js 22.20+.

```bash
npx skills add raffaele-cpu/italian-accounting-qa --agent cursor -y
```

```bash
# Globale (tutti i progetti)
npx skills add raffaele-cpu/italian-accounting-qa -g --agent cursor -y

# Altri agenti: claude-code, codex, opencode, ...
npx skills add raffaele-cpu/italian-accounting-qa --agent '*' -y
```

Verifica: `npx skills list -a cursor`

## Contenuto

| Path | Ruolo |
|------|--------|
| `SKILL.md` | Workflow audit e regole bloccanti |
| `references/` | Specifica tematica 01–05 |
| `scripts/validate_fiscal_ids.py` | Checksum P.IVA/CF e mini tabelle di verità |

```bash
python scripts/validate_fiscal_ids.py --self-test
```

## Licenza

MIT — Pratico Applications.