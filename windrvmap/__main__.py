from .cli_drives import main 


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter; Reason: @click.command decorator edits the function parameters, but pylint does not know this since it does not run the code.
