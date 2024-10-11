from pathlib import Path

import requests
from rich.progress import Progress, BarColumn, TaskProgressColumn, TimeRemainingColumn, TextColumn, DownloadColumn, \
    TransferSpeedColumn

from config import URL, FILENAME, ITER_CHUNK_SIZE

my_filename = 'TEST1-' + FILENAME
Path(my_filename).touch()

with (
    Progress(
        TextColumn('{task.description}'),
        BarColumn(),
        TaskProgressColumn('{task.percentage:>5.1f}%'),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(compact=True, elapsed_when_finished=True)
    ) as p,
    requests.Session() as s,
    open(my_filename, 'wb') as f
):
    r = s.get(URL, stream=True)
    content_length = int(r.headers.get('Content-Length'))
    main_task = p.add_task(f"[color(204)]{my_filename}", total=content_length)
    for chunk in r.iter_content(chunk_size=ITER_CHUNK_SIZE):
        f.write(chunk)
        p.update(main_task, advance=len(chunk))
