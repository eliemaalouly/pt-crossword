from playwright.sync_api import sync_playwright

URL = "https://www.linguno.com/crosswords/?lang=por&dialect=1"
SECTION_TITLE = "Level"  # Level, Monolingual, Theme
BUTTON_INDEX = 0   # 0 = A1, 1 = A2, 2 = B1, 3 = B2, etc.

section_title_selector = f'div.section_title_container div.small_section_title:has-text("{SECTION_TITLE} crosswords")'
button_selector = 'a.crossword_list_box[href*="/crossword/"]'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")

    section_title = page.locator(section_title_selector).first
    if section_title.count() == 0:
        print("Could not find crosswords title")
        browser.close()
        raise SystemExit(1)

    section_block = section_title.locator(
        "xpath=./parent::div/following-sibling::div[1]").first

    buttons = section_block.locator(button_selector)
    target = buttons.nth(BUTTON_INDEX)

    if target.count() == 0:
        print("Could not find crossword button in {} section".format(SECTION_TITLE))
        browser.close()
        raise SystemExit(1)

    target.click()
    page.wait_for_url("**/crossword/**")

    printable_url = page.url + "?printable&black"
    print(printable_url)

    page.goto(printable_url, wait_until="networkidle")
    page.pdf(
        path="daily_crossword.pdf",
        width="6.21in",
        height="8.28in",
        print_background=True,
        margin={"top": "0.5in", "right": "0in", "bottom": "0in", "left": "0in"}
    )

    browser.close()
