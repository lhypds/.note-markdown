import sys

from commands import create as create_command
from commands import format as format_command
from commands import markdown as markdown_command


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv:
        format_command.main([])
        return

    command = argv[0]
    command_args = argv[1:]

    if command == "create":
        create_command.main(command_args)
        return

    if command == "format":
        format_command.main(command_args)
        return

    if command == "markdown":
        markdown_command.main(command_args)
        return

    format_command.main(argv)


if __name__ == "__main__":
    main()
