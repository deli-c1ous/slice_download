import asyncio
from pathlib import Path

import aiohttp
from rich.progress import Progress, BarColumn, TaskProgressColumn, TimeRemainingColumn, TextColumn, DownloadColumn, \
    TransferSpeedColumn

from utils import slice_by_count
from config import URL, FILENAME, CHUNK_COUNT, ITER_CHUNK_SIZE


async def fetch(s, cnt, start, end, p, main_task):
    headers = {"Range": f"bytes={start}-{end}"}
    task = p.add_task(f"{my_filename} 分片{cnt}", total=end - start + 1, start=False)
    with open(my_filename, 'rb+') as f:
        f.seek(start)
        async with s.get(URL, headers=headers) as r:
            p.start_task(task)
            async for chunk in r.content.iter_chunked(ITER_CHUNK_SIZE):
                f.write(chunk)
                p.update(task, advance=len(chunk))
                p.update(main_task, advance=len(chunk))


my_filename = 'TEST3-' + FILENAME
Path(my_filename).touch()


async def main():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=None)) as s:
        async with s.head(URL) as r:
            content_length = int(r.headers.get('Content-Length'))
        with Progress(
                TextColumn('{task.description}'),
                BarColumn(),
                TaskProgressColumn('{task.percentage:>5.1f}%'),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(compact=True, elapsed_when_finished=True),
        ) as p:
            main_task = p.add_task(f"[color(204)]{my_filename}", total=content_length, start=False)
            tasks = (fetch(s, cnt, start, end, p, main_task) for cnt, start, end in
                     slice_by_count(content_length, CHUNK_COUNT))
            p.start_task(main_task)
            await asyncio.gather(*tasks)


asyncio.run(main())
