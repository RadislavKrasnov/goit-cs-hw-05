import argparse
import asyncio
from aiopath import AsyncPath
from aioshutil import copy
import logging


async def copy_file(file_path, output_folder):
    """Copies files asyncronously

    Args:
        file_path: AsyncPath object with source file path
        output_folder: String with outout folder
    """
    try:
        output_folder = AsyncPath(output_folder)
        extension = file_path.suffix.lstrip('.').lower() or 'misc'
        destination = output_folder / extension

        if not await destination.exists():
            await destination.mkdir(parents=True)

        await copy(file_path, destination / file_path.name)
        logging.info(f"Copied {file_path} to {destination / file_path.name}")
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")


async def read_folder(source_folder, output_folder):
    """Reads folder content and copies it into output folder
    
    Args:
        source_folder: String with source folder to read.
        output_folder: String with destination where to copy files.
    """
    try:
        folder = AsyncPath(source_folder)

        if not await folder.exists():
            raise ValueError(f'{source_folder} doesn\'t exist')

        if not await folder.is_dir():
            raise ValueError(f'{source_folder} is not a directory')

        async for path in folder.rglob('*'):
            if await path.is_file():
                await copy_file(path, output_folder)
    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")


def run():
    """Entrypoint"""
    logging.basicConfig(
        filename='logs/logs.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder', help="source folder", type=str)
    parser.add_argument("output_folder", help="output folder", type=str)
    args = parser.parse_args()
    source_folder = args.source_folder
    output_folder = args.output_folder
    asyncio.run(read_folder(source_folder, output_folder))


if __name__ == '__main__':
    run()
