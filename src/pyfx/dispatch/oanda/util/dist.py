## dist.py

from importlib_metadata import distribution, Distribution, PackageNotFoundError


def find_distribution(pkg: str) -> Distribution:
    """Return the Distribution for a provided package name"""
    try:
        return distribution(pkg)
    except PackageNotFoundError:
        basepkg = pkg.rsplit(".", maxsplit=1)[0]
        if basepkg == pkg:
            raise
        else:
            return find_distribution(basepkg)


__all__ = ("find_distribution",)
