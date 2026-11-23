#!/usr/bin/env python3
"""Validazione P.IVA / CF italiani e mini tabelle di verità fiscali (skill italian-accounting-qa)."""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

ODD_DIGIT = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21]
ODD_LETTER = [
    1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23,
]
CF_BODY = (
    r"^[A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST][0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{3}[A-Z]$"
)
import re

CF_RE = re.compile(CF_BODY)


def normalize_piva(raw: str | None) -> str | None:
    if not raw:
        return None
    compact = raw.replace(" ", "").replace(".", "").replace("-", "").upper()
    if compact.startswith("IT"):
        compact = compact[2:]
    return compact if len(compact) == 11 and compact.isdigit() else None


def is_valid_piva(raw: str | None) -> bool:
    piva = normalize_piva(raw)
    if not piva or piva == "0" * 11:
        return False
    total = 0
    for i, ch in enumerate(piva[:10]):
        d = int(ch)
        if i % 2 == 0:
            total += d
        else:
            doubled = d * 2
            total += doubled - 9 if doubled > 9 else doubled
    check = (10 - (total % 10)) % 10
    return check == int(piva[10])


def _cf_char_value(ch: str, odd: bool) -> int:
    o = ord(ch)
    if "0" <= ch <= "9":
        idx = o - 48
        return ODD_DIGIT[idx] if odd else idx
    idx = o - 65
    return ODD_LETTER[idx] if odd else idx


def normalize_cf(raw: str | None) -> str | None:
    if not raw:
        return None
    compact = raw.replace(" ", "").upper()
    return compact or None


def is_valid_cf(raw: str | None) -> bool:
    cf = normalize_cf(raw)
    if not cf:
        return False
    if len(cf) == 11 and cf.isdigit():
        return is_valid_piva(cf)
    if not CF_RE.match(cf):
        return False
    total = sum(_cf_char_value(cf[i], i % 2 == 0) for i in range(15))
    return chr(65 + (total % 26)) == cf[15]


def half_up_eur(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def simulate_iva_riepilogo(imponibile: Decimal, aliquota_pct: Decimal) -> Decimal:
    return half_up_eur(imponibile * aliquota_pct / Decimal(100))


def simulate_beni_significativi(totale: Decimal, bene: Decimal) -> tuple[Decimal, Decimal]:
    """Resto lavori P = T - B; se B > P applica cap R5.1 manutenzioni abitative."""
    resto = totale - bene
    if bene <= resto or resto < 0:
        return totale, Decimal(0)
    base_10 = resto * 2
    base_22 = bene - resto
    return base_10, base_22


def simulate_bonifico_parlante(total_cents: int, rate_pct: int = 11) -> int:
    """Allineato a `shared/lib/invoices/bank-withholding.ts`: round(total_cents × rate / 122)."""
    return round(total_cents * rate_pct / 122)


def simulate_sdi_tolerances(
    imponibile: Decimal, aliquota: Decimal, imposta_attesa: Decimal, imponibile_dichiarato: Decimal
) -> dict[str, bool]:
    calc = simulate_iva_riepilogo(imponibile, aliquota)
    ok_421 = abs(calc - imposta_attesa) <= Decimal("0.01")
    ok_422 = abs(imponibile - imponibile_dichiarato) <= Decimal("1.00")
    return {"00421_within_0_01": ok_421, "00422_within_1_00": ok_422, "imposta_calcolata": calc}


def run_self_test() -> None:
    asserts: list[tuple[str, bool]] = [
        ("piva_zeros_blocked", not is_valid_piva("00000000000")),
        ("piva_example", is_valid_piva("IT07643520567") or is_valid_piva("07643520567")),
        ("cf_checksum", is_valid_cf("RSSMRA80A01H501U")),
        ("iva_22", simulate_iva_riepilogo(Decimal("100"), Decimal("22")) == Decimal("22.00")),
        ("beni_B_gt_P", simulate_beni_significativi(Decimal("10000"), Decimal("6000")) == (Decimal("8000"), Decimal("2000"))),
        ("bonifico_11", simulate_bonifico_parlante(1_100_000, 11) == 99_180),
    ]
    failed = [name for name, ok in asserts if not ok]
    if failed:
        print("SELF-TEST FAILED:", ", ".join(failed), file=sys.stderr)
        sys.exit(1)
    print("SELF-TEST OK (", len(asserts), "checks)")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Italian fiscal IDs and run fiscal sanity checks")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--piva", action="append", default=[])
    parser.add_argument("--cf", action="append", default=[])
    parser.add_argument("--simulate-sdi", action="store_true", help="Run SDI tolerance demo on 1000 at 22 percent")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.self_test:
        run_self_test()

    for raw in args.piva:
        print(f"PIVA {raw!r}: {'OK' if is_valid_piva(raw) else 'INVALID'}")
    for raw in args.cf:
        print(f"CF {raw!r}: {'OK' if is_valid_cf(raw) else 'INVALID'}")

    if args.simulate_sdi:
        print(simulate_sdi_tolerances(Decimal("1000"), Decimal("22"), Decimal("220.00"), Decimal("1000.5")))

    if not args.self_test and not args.piva and not args.cf and not args.simulate_sdi:
        parser.print_help()
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())