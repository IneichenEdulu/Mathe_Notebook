# Author: Markus Ineichen, 2025
from typing import List, Tuple

HEX_DIGITS = "0123456789ABCDEF"

def _clean_bin(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip().replace(" ", "").replace("_", "")
    s = s[2:] if s.lower().startswith("0b") else s
    if s == "":
        return ""
    if not all(c in "01" for c in s):
        raise ValueError("Binärzahl darf nur 0 und 1 (plus optionale Leerzeichen/Unterstriche) enthalten.")
    return s

def _clean_hex(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip().replace(" ", "").replace("_", "").upper()
    s = s[2:] if s.startswith("0X") else s
    if s == "":
        return ""
    if not all(c in HEX_DIGITS for c in s):
        raise ValueError("Hexadezimalzahl darf nur 0–9 und A–F enthalten.")
    return s

def binary_to_hex(bin_str: str) -> str:
    b = _clean_bin(bin_str)
    if b == "":
        return ""
    pad = (-len(b)) % 4
    b = "0"*pad + b
    hx_chars = []
    for i in range(0, len(b), 4):
        nibble = b[i:i+4]
        hx_chars.append(format(int(nibble, 2), "X"))
    # Entferne führende Nullen (aber nicht, wenn Ergebnis leer wäre)
    hx = "".join(hx_chars).lstrip("0")
    return hx if hx != "" else "0"

def hex_to_binary(hx: str, group_nibbles: bool = True) -> str:
    h = _clean_hex(hx)
    if h == "":
        return ""
    bits = "".join(format(int(c, 16), "04b") for c in h)
    if not group_nibbles:
        return bits.lstrip("0") or "0"
    # gruppiert in 4er-Gruppen
    grouped = " ".join(bits[i:i+4] for i in range(0, len(bits), 4))
    # führende 0000 Gruppen optional reduzieren
    groups = grouped.split()
    while len(groups) > 1 and groups[0] == "0000":
        groups.pop(0)
    return " ".join(groups)

def binary_to_decimal(bin_str: str) -> int:
    b = _clean_bin(bin_str)
    return int(b, 2) if b != "" else 0

def hex_to_decimal(hx: str) -> int:
    h = _clean_hex(hx)
    return int(h, 16) if h != "" else 0

def decimal_to_binary_steps(n: int) -> Tuple[str, List[Tuple[int, int, int]]]:
    if not isinstance(n, int) or n < 0:
        raise ValueError("Bitte eine nichtnegative ganze Zahl verwenden.")
    if n == 0:
        return "0", [(0, 0, 0)]
    steps = []
    digits = []
    x = n
    while x > 0:
        q, r = divmod(x, 2)
        steps.append((x, q, r))  # (aktuelles n, n//2, Rest)
        digits.append(str(r))
        x = q
    digits.reverse()
    return "".join(digits), steps

def decimal_to_hex_steps(n: int) -> Tuple[str, List[Tuple[int, int, int]]]:
    if not isinstance(n, int) or n < 0:
        raise ValueError("Bitte eine nichtnegative ganze Zahl verwenden.")
    if n == 0:
        return "0", [(0, 0, 0)]
    steps = []
    digits = []
    x = n
    while x > 0:
        q, r = divmod(x, 16)
        steps.append((x, q, r))  # (aktuelles n, n//16, Rest)
        digits.append(HEX_DIGITS[r])
        x = q
    digits.reverse()
    return "".join(digits), steps

def pretty_print_div2_steps(steps: List[Tuple[int, int, int]]) -> None:
    print("n   n//2  Rest")
    print("------------")
    for n, q, r in steps:
        print(f"{n:<3} {q:<5} {r}")
    print("(Reste von unten nach oben lesen)")

def pretty_print_div16_steps(steps: List[Tuple[int, int, int]]) -> None:
    print("n    n//16  Rest  Hex-Rest")
    print("---------------------------")
    for n, q, r in steps:
        print(f"{n:<4} {q:<6} {r:<4} {HEX_DIGITS[r]}")
    print("(Hex-Ziffern von unten nach oben lesen)")
