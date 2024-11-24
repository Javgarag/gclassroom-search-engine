import wget
from managers import ScrapeManager, AnnouncementManager, APIManager
from urllib.parse import urlparse, parse_qs
from pyppeteer.errors import NetworkError, PageError

async def format_google_redirect(url):
    """Convert Google redirect URL to normal usable URL."""
    if "https://www.google.com/url?esrc=s&q=&rct=j&sa=U&url=" in url:
        query = urlparse(url).query
        params = parse_qs(query)
        url = params['url'][0] if 'url' in params else url
    return url


async def get(a):
    """Gets the content of a URL and sends it as an announcement."""
    a[0] = await format_google_redirect(a[0])

    try:
        page = await ScrapeManager.new_page(a[0])
        page_name = await page.title()
        capture_path = await ScrapeManager.take_capture(page, page_name)
        await ScrapeManager.close_page(page)

    except (NetworkError, PageError) as e:
        if a[0].endswith(".pdf") and PageError: # PDF page!
            page_name = (await ScrapeManager.format_file_name(a[0])).strip(".pdf")
            wget.download(a[0], out=".temp/" + page_name + ".pdf")
            capture_path = ".temp/" + page_name + ".pdf"
            print("\n")
        else:
            AnnouncementManager.send_announcement("ERROR: " + str(e))
            return

    drive_file = APIManager.upload(capture_path, page_name, "pdf", "application/pdf")
    AnnouncementManager.send_announcement("URL '" + a[0] + "':", drive_file, page_name, "pdf")
