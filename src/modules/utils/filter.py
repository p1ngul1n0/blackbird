import re
import config
import sys


def filterFoundAccounts(site):
    if site["status"] == "FOUND":
        return True
    else:
        return False


def filterAccounts(filter, site):
    match = re.match(r"^([^=]+)=(.+)", filter)

    if match:
        prop = match.group(1)
        value = match.group(2)
        if str(site[prop]) == value:
            return True
        else:
            return False
    else:
        config.console.print(
            '⭕ Filter is not in correct format. Format should be --filter "property=value"'
        )
        sys.exit()


def filterNSFW(site):
    if site["cat"] == "xx NSFW xx":
        return False
    else:
        return True


def applyFilters(sitesToSearch):
    if config.filter:
        sitesToSearch = list(
            filter(lambda x: filterAccounts(config.filter, x), sitesToSearch)
        )
        if (len(sitesToSearch)) <= 0:
            config.console.print(
                f"⭕ No sites found for the given filter {config.filter}"
            )
            sys.exit()
        else:
            config.console.print(
                f':page_with_curl: Applied "{config.filter}" filter to sites [{len(sitesToSearch)}]'
            )

    if config.no_nsfw:
        sitesToSearch = list(filter(lambda x: filterNSFW(x), sitesToSearch))
        if (len(sitesToSearch)) <= 0:
            config.console.print(
                f"⭕ No remaining sites to be searched after NSFW filtering"
            )
            sys.exit()
        else:
            config.console.print(
                f":page_with_curl: Filtered NSFW sites [{len(sitesToSearch)}]"
            )

    return sitesToSearch
