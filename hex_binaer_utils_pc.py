# Author: Markus Ineichen, 2025
from typing import List, Tuple

HEX_DIGITS = "0123456789ABCDEF"

def clean_binary(s: str) -> str:
    '''Leerzeichen/Unterstriche entfernen und Binärzeichen validieren.'''
    s = s.replace(" ", "").replace("_", "")
    if s.lower().startswith("0b"):
        s = s[2:]
    if s == "":
        return s
    if not all(c in "01" for c in s):
        raise ValueError("Binärzahl darf nur aus 0 und 1 bestehen (plus optionalen Leerzeichen/Unterstrichen).")
    return s

def clean_hex(s: str) -> str:
    '''Hex-String normalisieren (in Grossbuchstaben umwandeln, 0x entfernen, Leerzeichen und Unterstriche löschen).'''
    s = s.strip().replace(" ", "").replace("_", "")
    if s.lower().startswith("0x"):
        s = s[2:]
    s = s.upper()
    if s == "":
        return s
    if not all(c in HEX_DIGITS for c in s):
        raise ValueError("Hexadezimalzahl darf nur die Zeichen 0-9 und A-F enthalten.")
    return s

def group_bits(s: str, group: int = 4) -> str:
    '''Eine Bitfolge von links in Gruppen der Länge 'group' mit Leerzeichen unterteilen. 
    Von links mit Nullen auffüllen, bis die Länge ein Vielfaches von 'group' ist.'''
    s = clean_binary(s)
    if s == "":
        return s
    pad = (-len(s)) % group
    s = "0"*pad + s
    return " ".join(s[i:i+group] for i in range(0, len(s), group))

def hex_to_binary(hex_str: str, group_nibbles: bool = True) -> str:
    '''Hexadezimal in Binär umwandeln (optional in Nibbles gruppiert).'''
    hx = clean_hex(hex_str)
    if hx == "":
        return ""
    bits = "".join(format(int(c, 16), "04b") for c in hx)
    return " ".join(bits[i:i+4] for i in range(0, len(bits), 4)) if group_nibbles else bits

def binary_to_hex(bin_str: str) -> str:
    '''Binär in Hexadezimal umwandeln (in Nibbles gruppieren).'''
    b = clean_binary(bin_str)
    if b == "":
        return ""
    pad = (-len(b)) % 4
    b = "0"*pad + b
    hx = ""
    for i in range(0, len(b), 4):
        nibble = b[i:i+4]
        hx += format(int(nibble, 2), "X")
    return hx

def decimal_to_binary_steps(n: int) -> Tuple[str, List[Tuple[int, int, int]]]:
    '''Gibt (binary_string, steps) für wiederholte Division durch 2 zurück.
    Jeder Schritt: (current_n, next_n, remainder) mit next_n = current_n // 2.'''
    if n < 0:
        raise ValueError("Nur nichtnegative ganze Zahlen für dieses Notebook.")
    if n == 0:
        return "0", [(0, 0, 0)]
    digits = []
    steps = []
    current = n
    while current > 0:
        q, r = divmod(current, 2)
        steps.append((current, q, r))
        digits.append(str(r))
        current = q
    digits.reverse()
    return "".join(digits), steps

def decimal_to_hex_steps(n: int) -> Tuple[str, List[Tuple[int, int, int]]]:
    '''Gibt (hex_string, steps) für wiederholte Division durch 16 zurück.
    Jeder Schritt: (current_n, next_n, remainder) mit next_n = current_n // 16.'''
    if n < 0:
        raise ValueError("Nur nichtnegative ganze Zahlen für dieses Notebook.")
    if n == 0:
        return "0", [(0, 0, 0)]
    digits = []
    steps = []
    current = n
    while current > 0:
        q, r = divmod(current, 16)
        steps.append((current, q, r))
        digits.append(HEX_DIGITS[r])
        current = q
    digits.reverse()
    return "".join(digits), steps

def binary_to_decimal(bin_str: str) -> int:
    b = clean_binary(bin_str)
    return int(b, 2) if b != "" else 0

def hex_to_decimal(hex_str: str) -> int:
    hx = clean_hex(hex_str)
    return int(hx, 16) if hx != "" else 0

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
