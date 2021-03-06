__all__ = (
    "AoCInput",
    "chinese_remainder_theorem",
    "erange",
    "dot_print",
)


from pathlib import Path


class AoCInput:
    @staticmethod
    def get_ints(raw, use_regexp=False, regexp=r"-?\d+", as_tuple=False):
        """
        Parse self.path containing whitespace delimited integers into a list of integers.

        If use_regexp=True, parse the entire file using regexp to extract integers.
        Returns a list of list by default, or a tuple of tuple if as_tuple=True.
        """
        kind = tuple if as_tuple else list

        if use_regexp:
            import re

            exp = re.compile(regexp)
            return kind(map(int, exp.findall(raw)))

        return kind(map(int, raw.split()))

    @staticmethod
    def get_lines(raw, rstrip=True, lstrip=True, as_tuple=False):
        """
        Read file into a list (or tuple) of lines.

        Strips lines on both ends by default unless rstrip=False or lstrip=False.
        Returns a list of strings by default, or a tuple if as_tuple=True.
        """
        kind = tuple if as_tuple else list
        lines = map(lambda l: l.rstrip("\n"), raw.split("\n"))
        lines = [line for line in lines if line != ""]

        if rstrip and lstrip:
            return kind(map(str.strip, lines))
        elif rstrip:
            return kind(map(str.rstrip, lines))
        elif lstrip:
            return kind(map(str.lstrip, lines))
        else:
            return kind(lines)

    @staticmethod
    def get_raw(path: str) -> str:
        return Path(path).read_text()


def chinese_remainder_theorem(moduli, residues):
    from math import prod

    N = prod(moduli)

    X = sum(
        (div := (N // modulus)) * pow(div, -1, modulus) * residue
        for modulus, residue in zip(moduli, residues)
    )

    return X % N


def erange(start, end, step=1):
    """Range from start to end (included) in steps of +/- step regardless if start > end or end > start."""
    if start > end:
        yield from range(start, end - 1, -step)
    yield from range(start, end + 1, step)


def dot_print(array):
    """
    Pretty print a binary or boolean array.
    """
    for row in array:
        print("".join(" #"[i] for i in row))
