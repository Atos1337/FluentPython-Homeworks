import asyncio

import aiohttp
import aiofiles


async def download_site(url, session, index, output_folder):
    async with session.get(url) as response:
        async with aiofiles.open(f"{output_folder}/picture{index}.jpg", mode="wb") as f:
            await f.write(await response.read())
            print(f"Read {response.content.total_bytes} from {index}")


async def download_all_sites(sites, output_folder):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(sites):
            task = asyncio.create_task(download_site(url, session, i, output_folder))
            tasks.append(task)

        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            print(repr(ex))


if __name__ == "__main__":
    """ Parameteres
    """
    output_folder = "artifacts/easy"
    picture_count = 30

    sites = ["https://picsum.photos/200/300"] * picture_count

    loop = asyncio.get_event_loop()

    try:
        task = loop.create_task(download_all_sites(sites, output_folder))
        loop.run_until_complete(task)
    finally:
        loop.close()
