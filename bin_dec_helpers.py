# Autor: Markus Ineichen, 2025
from dataclasses import dataclass
from typing import List, Tuple
import ipywidgets as widgets
import math

@dataclass(frozen=True)
class BitSystem:
    weights: Tuple[int, ...]

# Default: 6-bit system with weights for 2^5..2^0
DEFAULT_SYSTEM = BitSystem(weights=(32, 16, 8, 4, 2, 1))

def bits_to_decimal(bits: List[int], weights: Tuple[int, ...]) -> int:
    return sum(b*w for b, w in zip(bits, weights))

def decimal_to_bits(n: int, weights: Tuple[int, ...]) -> List[int]:
    remaining = n
    bits = []
    for w in weights:
        bit = 1 if remaining >= w else 0
        bits.append(bit)
        if bit == 1:
            remaining -= w
    return bits

def format_equation(bits: List[int], weights: Tuple[int, ...], show_zeros: bool=True) -> str:
    terms = []
    for b, w in zip(bits, weights):
        if b == 1:
            terms.append(str(w))
        elif show_zeros:
            terms.append("0")
    if not terms:
        terms = ["0"]
    total = bits_to_decimal(bits, weights)
    return " + ".join(terms) + f" = {total}"

def greedy_steps(n: int, weights: Tuple[int, ...]) -> str:
    remaining = n
    lines = []
    for w in weights:
        fits = remaining >= w
        if fits:
            lines.append(f"Passt {w} in {remaining}? Ja → 1, Rest: {remaining - w}")
            remaining -= w
        else:
            lines.append(f"Passt {w} in {remaining}? Nein → 0")
    return "<br>".join(lines)

def sanitize_binary_string(s: str) -> str:
    return "".join(ch for ch in s if ch in "01")

def bits_from_string(s: str, width: int) -> List[int]:
    s = sanitize_binary_string(s)
    if not s:
        s = "0"
    s = s[-width:].rjust(width, "0")
    return [int(ch) for ch in s]

def bits_to_string(bits: List[int]) -> str:
    return "".join(str(b) for b in bits)

def bit_columns(weights: Tuple[int, ...], checkboxes: List[widgets.Checkbox]) -> widgets.HBox:
    cols = []
    for w, chk in zip(weights, checkboxes):
        power = int(math.log2(w)) if w>0 and (w & (w-1)) == 0 else None
        label = f"2<sup>{power}</sup> = {w}" if power is not None else str(w)
        cols.append(
            widgets.VBox(
                [
                    widgets.HTML(f"<div style='text-align:center; font-size:14px'>{label}</div>"),
                    chk
                ],
                layout=widgets.Layout(align_items='center', width='80px')
            )
        )
    return widgets.HBox(cols, layout=widgets.Layout(justify_content='center', gap='10px', flex_flow='row wrap'))
