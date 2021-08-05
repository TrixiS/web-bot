import os
import traceback
import logging
import asyncio
import argparse

from scripts import install
from bot import root_path


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-app", action="store_true")
    parser.add_argument("--no-deps", action="store_true")

    args = parser.parse_args()

    if not args.no_deps:
        install.deps()

    from scripts import run

    if not args.no_app:
        return await run.app()

    logging.basicConfig(
        filename=root_path / "logs.log",
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
    )

    await run.bot()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)

        if install.WINDOWS:
            os.system("pause")
