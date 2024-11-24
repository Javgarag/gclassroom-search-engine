from managers import ScrapeManager, AnnouncementManager, APIManager

async def search(a: 2):
    """Searches on Google. Can search on Images, Videos and normal search, provided with the first argument."""
    if a[0] == "images":
        page = await ScrapeManager.new_page("https://www.google.com/search?tbm=isch&q=" + a[1])
    elif a[0] == "videos":
        page = await ScrapeManager.new_page("https://www.google.com/search?tbm=vid&q=" + a[1])
    else:
        page = await ScrapeManager.new_page("https://www.google.com/search?q=" + a[0] + (" " + a[1] if len(a) > 1 else ""))

    try: # Before continuing popup
        await page.waitForXPath("//input[@class='basebutton button searchButton']", timeout=3000)
        button = await page.xpath("//input[@class='basebutton button searchButton']")
        await button[0].click()
        await page.waitForNavigation()
    except:
        pass

    page_name = await page.title()
    capture_path = await ScrapeManager.take_capture(page, page_name)
    await ScrapeManager.close_page(page)

    drive_file = APIManager.upload(capture_path, page_name, "pdf", "application/pdf")
    AnnouncementManager.send_announcement("Results for '" + (a[1] if len(a) > 1 else a[0]) + "':", drive_file, page_name, "pdf")