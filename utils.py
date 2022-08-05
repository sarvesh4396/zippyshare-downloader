import math
import re
from os.path import basename

# Taken from https://github.com/mansuf/zippyshare-downloader.git
REGEXS_ZIPPYSHARE_URL = [
    # View zippyshare url
    r"https:\/\/www[0-9]{1,3}\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html",
    r"https:\/\/www\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html",
    # Download Zippyshare url
    r"https:\/\/www[0-9]{1,3}\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/",
    r"https:\/\/www\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/",
]


ALLOWED_NAMES = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

# Taken from https://github.com/mansuf/zippyshare-downloader.git
# Credit for the evaluate() method: Leodanis Pozo Ramos  https://realpython.com/python-eval-function/
def evaluate(expression):
    """Evaluate a math expression."""

    # Compile the expression
    code = compile(expression, "<string>", "eval")

    # Validate allowed names
    for name in code.co_names:
        if name not in ALLOWED_NAMES:
            raise NameError(
                "The use of '%s' is not allowed. Expression used: %s"
                % (name, expression)
            )

    return eval(code, {"__builtins__": {}}, ALLOWED_NAMES)


def check_valid_zippyshare_url(url):
    """Check if given url is valid Zippyshare url"""
    for regex in REGEXS_ZIPPYSHARE_URL:
        if re.match(regex, url) is not None:
            return True
    return False


def get_urls(urls):
    urls = [u.strip() for u in urls.split("\n") if u.strip() != ""]
    valid_urls = []
    for u in urls:
        if check_valid_zippyshare_url(u):
            valid_urls.append(u)

    return valid_urls


# Taken from https://github.com/mansuf/zippyshare-downloader.git
def getStartandEndvalue(value: str, sub: str, second_sub=None):
    v = value[value.find(sub) + 1 :]
    if second_sub is not None:
        return v[: v.find(second_sub)]
    else:
        return v[: v.find(sub)]


# Taken from https://github.com/mansuf/zippyshare-downloader.git
def get_download_url(url, soup):
    for script in soup.find_all("script"):
        if "document.getElementById('dlbutton').href" in script.decode_contents():
            scrapped_script = script.decode_contents()
            break

    startpos_init = scrapped_script.find("document.getElementById('dlbutton').href")
    scrapped_init = scrapped_script[startpos_init:]
    endpos_init = scrapped_init.find(";")
    scrapped = scrapped_init[:endpos_init]
    element_value = scrapped.replace("document.getElementById('dlbutton').href = ", "")
    url_download_init = getStartandEndvalue(element_value, '"')
    random_number = getStartandEndvalue(element_value, "(", ")")
    # Now using self.evaluate() to safely do math calculations
    url_number = str(evaluate(random_number))
    continuation_download_url_init = getStartandEndvalue(element_value, "(")
    continuation_download_url = continuation_download_url_init[
        continuation_download_url_init.find('"') + 1 :
    ]
    return (
        url[: url.find(".")]
        + ".zippyshare.com"
        + url_download_init
        + url_number
        + continuation_download_url
    )


def get_download_links_button(url):
    name = basename(url)
    template = """<a href="{}" target="_blank" rel="noopener noreferrer" class="text-blue-500 underline hover:text-rose-500 duration-300">
          {} 
          <i class="fa-solid fa-file-arrow-down ml-2"></i>
      </a>
      """

    return template.format(url, name)
