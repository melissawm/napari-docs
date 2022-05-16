"""ALL pre-rendering and pre-preparation of docs should occur in this file.

Note: make no assumptions about the working directory
from which this script will be called.
"""
import sys
from pathlib import Path

DOCS = Path(__file__).parent.parent.absolute()


def prep_napari():
    from subprocess import check_call

    check_call("python -m pip install git+https://github.com/napari/napari.git#egg=napari[all]".split())


def prep_npe2():
    #   some plugin docs live in npe2 for testing purposes
    from subprocess import check_call

    check_call("rm -rf npe2".split())
    check_call("git clone https://github.com/napari/npe2".split())
    check_call([sys.executable, "npe2/_docs/render.py", DOCS / 'plugins'])
    check_call("rm -rf npe2".split())


def main():
    prep_napari()
    prep_npe2()
    __import__('update_preference_docs').main()
    __import__('update_event_docs').main()


if __name__ == "__main__":
    main()
