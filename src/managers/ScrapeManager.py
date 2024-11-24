import os, asyncio
from pyppeteer import launch

browser = None
async def init_browser():
    global browser
    if not browser:
        browser = await launch(
            ignoreHTTPSErrors = True,
            headless = True, 
            autoClose = False,
            handleSIGINT = False,
            handleSIGTERM = False,
            handleSIGHUP = False,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-software-rasterizer', '--disable-setuid-sandbox'])
        
    return browser

async def format_file_name(string):
    string = string.replace("/", "")
    if os.name == "nt":
        string = string.replace("<", " ")
        string = string.replace(">", " ")
        string = string.replace(":", " ")
        string = string.replace('"', " ")
        string = string.replace("\\", " ")
        string = string.replace("|", " ")
        string = string.replace("?", " ")
        string = string.replace("*", " ")

    return string

async def new_page(url):
    global browser
    browser = await init_browser()
    page = await browser.newPage()

    navigation_promise = page.waitForNavigation()
    await asyncio.gather(
        navigation_promise,
        page.goto(url, waitUntil='networkidle2')
    )
    return page

async def close_page(page):
    await page.close()

async def take_capture(page, page_name):
    page_name = await format_file_name(page_name)
    if not os.path.exists(".temp"):
        os.mkdir(".temp")

    try: # scrollHeight may not be available
        page_height = await page.evaluate("document.body.scrollHeight")
    except:
        page_height = 10000
            
    pdf_options = {
        "path": ".temp/" + page_name + ".pdf",
        "width": f"{page_height + 200}px",
        "printBackground": True,
        "landscape": True
    }
    await page.pdf(pdf_options)
    return pdf_options["path"]