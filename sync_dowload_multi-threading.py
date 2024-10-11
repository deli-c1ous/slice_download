import time
import signal
from pathlib import Path
from threading import Event
from concurrent.futures import ThreadPoolExecutor

import requests
from rich.progress import Progress, BarColumn, TaskProgressColumn, TimeRemainingColumn, TextColumn, DownloadColumn, \
    TransferSpeedColumn

from utils import slice_by_count
from config import URL, FILENAME, CHUNK_COUNT, ITER_CHUNK_SIZE


def download_slice(cnt, start, end):
    headers = {'Range': f'bytes={start}-{end}'}
    task = p.add_task(f"{my_filename} 分片{cnt}", total=end - start + 1, start=False)
    r = s.get(URL, headers=headers, stream=True)
    with open(my_filename, 'rb+') as f:
        f.seek(start)
        p.start_task(task)
        for chunk in r.iter_content(chunk_size=ITER_CHUNK_SIZE):
            f.write(chunk)
            p.update(task, advance=len(chunk))
            p.update(main_task, advance=len(chunk))
            if keyboard_interrupt_event.is_set():
                return


def signal_handler(signal, frame):
    keyboard_interrupt_event.set()
    raise KeyboardInterrupt()


keyboard_interrupt_event = Event()
signal.signal(signal.SIGINT, signal_handler)

my_filename = 'TEST2-' + FILENAME
Path(my_filename).touch()
max_workers = CHUNK_COUNT

with (
    Progress(
        TextColumn('{task.description}'),
        BarColumn(),
        TaskProgressColumn('{task.percentage:>5.1f}%'),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(compact=True, elapsed_when_finished=True),
    ) as p,
    requests.Session() as s,
    ThreadPoolExecutor(max_workers=max_workers) as pool,
):
    r = s.head(URL)
    content_length = int(r.headers.get('Content-Length'))
    main_task = p.add_task(f"[color(204)]{my_filename}", total=content_length)
    for cnt, start, end in slice_by_count(content_length, CHUNK_COUNT):
        pool.submit(download_slice, cnt, start, end)
    while not p.finished:
        time.sleep(1)
