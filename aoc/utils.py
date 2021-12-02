__all__ = (
    "extract_ints",
    "chinese_remainder_theorem",
)


class AoCInput:
    def __init__(self, fname: str, mode: str = 'r') -> None:
        self.path = open(fname, mode)

    def get_ints(self, use_regexp=False, regexp=r"-?\d+", as_tuple=False):
        """
        Parse self.path containing whitespace delimited integers into a list of integers.

        If use_regexp=True, parse the entire file using regexp to extract integers.
        Returns a list of list by default, or a tuple of tuple if as_tuple=True.
        """
        kind = tuple if as_tuple else list

        if use_regexp:
            import re

            exp = re.compile(regexp)
            return kind(map(int, exp.findall(self.path.read())))

        return kind(map(int, self.path.read().split()))

    def get_lines(self, rstrip=True, lstrip=True, as_tuple=False):
        """
        Read file into a list (or tuple) of lines.

        Strips lines on both ends by default unless rstrip=False or lstrip=False.
        Returns a list of strings by default, or a tuple if as_tuple=True.
        """
        kind = tuple if as_tuple else list
        lines = map(lambda l: l.rstrip("\n"), self.path)

        if rstrip and lstrip:
            return kind(map(str.strip, lines))
        elif rstrip:
            return kind(map(str.rstrip, lines))
        elif lstrip:
            return kind(map(str.lstrip, lines))
        else:
            return kind(lines)


def chinese_remainder_theorem(moduli, residues):
    from math import prod

    N = prod(moduli)

    X = sum(
        (div := (N // modulus)) * pow(div, -1, modulus) * residue
        for modulus, residue in zip(moduli, residues)
    )

    return X % N
