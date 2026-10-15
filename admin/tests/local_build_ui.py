"""Build through the admin UI without saving pages or contacting deployment APIs."""
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from new_services_ui import BASE, login, build


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        try:
            context = browser.new_context(viewport={'width': 1600, 'height': 1000})
            login(context)

            def guard(route):
                request = route.request
                url = urlparse(request.url)
                if url.hostname not in {'127.0.0.1', 'localhost'}:
                    route.abort()
                elif url.path in {'/api/server/pause', '/api/deploy/status'}:
                    route.fulfill(json={'ok': True, 'pause': {'configured': False}, 'deploy': {}})
                elif request.method != 'GET' and url.path != '/api/build':
                    route.abort()
                    raise AssertionError('Unexpected write: ' + url.path)
                else:
                    route.continue_()

            context.route('**/*', guard)
            page = context.new_page()
            page.goto(BASE)
            page.wait_for_function('typeof state !== "undefined" && state.pages.length > 0')
            build(page)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
