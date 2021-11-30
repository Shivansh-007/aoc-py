"""Useful functions for AoC. Note deferred imports."""

__all__ = (
    "extract_ints",
    "chinese_remainder_theorem",
)


def extract_ints(raw: str):
    """
    Extract integers from a string.
    """
    import re

    for match in re.findall(r"(\d+)", raw):
        yield int(match)


def chinese_remainder_theorem(moduli, residues):
    from math import prod

    N = prod(moduli)

    X = sum(
        (div := (N // modulus)) * pow(div, -1, modulus) * residue
        for modulus, residue in zip(moduli, residues)
    )

    return X % N
