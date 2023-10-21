"""arg parser support"""

import argparse as ap
import re
from contextlib import contextmanager
from typing import Any, Callable, Iterator, TypeAlias


OptionsFunc: TypeAlias = Callable[[ap.Namespace], Any]

@contextmanager
def argparser(
    prog,
    formatter_class: type[ap.HelpFormatter] = ap.HelpFormatter,
    **kwargs,
) -> Iterator[ap.ArgumentParser]:
    parser = ap.ArgumentParser(prog=prog, formatter_class=formatter_class, **kwargs)
    yield parser


@contextmanager
def subparsers(
    root_parser: ap.ArgumentParser,
    title="commands",
    help="Available commands. See <command> -h",
    **kwargs,
) -> Iterator[ap._SubParsersAction]:
    yield root_parser.add_subparsers(title=title, help=help, **kwargs)


@contextmanager
def command_parser(
    subparser: ap._SubParsersAction,
    name: str,
    func: OptionsFunc,
    description: str,
    formatter_class: type[ap.HelpFormatter] = ap.HelpFormatter,
    **parser_args,
) -> Iterator[ap.ArgumentParser]:
    helper_args = {}
    if "help" not in parser_args:
        ## include the first line from the command desciption as the help text
        ## for the command when listed under `project.py -h`
        helper_args["help"] = re.split("[\n\r]", description, maxsplit=1)[0]

    cmd_parser = subparser.add_parser(
        name,
        formatter_class=formatter_class,
        description=description,
        **helper_args,  # type: ignore
        **parser_args,
    )
    cmd_parser.set_defaults(func=func)
    yield cmd_parser


__all__ = ("argparser", "subparsers", "command_parser", "OptionsFunc")
