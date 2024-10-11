# slice_download
large file silce download using python (with progress bar)
## files
**config.py**: configure the download url and settings.

**async_download.py**: async download with asyncio, aiohttp. (fast and simple, proposed)

**sync_download_multi-threading.py**: sync download using requests, ThreadPoolExecutor. (also fast but not that simple)

**sync_download.py**: sync download using requests with single thread. (slow, only for contrast)

**utils.py**: 2 slice method implementation.
