# Blackbird

<figure><img src=".gitbook/assets/blackbird_printscreen.png" alt=""><figcaption></figcaption></figure>

> Blackbird is a robust OSINT tool that facilitates rapid searches for user accounts by username or email across a wide array of platforms, enhancing digital investigations. It features WhatsMyName integration, export options in PDF, CSV, and HTTP response formats, and customizable search filters.

***

### Setup

**Clone the repository**

```
git clone https://github.com/p1ngul1n0/blackbird
cd blackbird
```

**Install requirements**

```
pip install -r requirements.txt
```

### Usage

**Search by username**

```
python blackbird.py --username username1 username2 username3
```

**Search by email**

```
python blackbird.py --email email1@email email2@email email3@email
```

**Other arguments**

```
usage: blackbird [-h] [-u [USERNAME ...]] [-e [EMAIL ...]] [--csv | --no-csv] [--pdf | --no-pdf] [-v | --verbose | --no-verbose] [--filter FILTER] [--no-nsfw] [--dump]
                 [--proxy PROXY] [--timeout TIMEOUT] [--no-update] [--about]

An OSINT tool to search for accounts by username in social networks.

options:
  -h, --help            show this help message and exit
  -u [USERNAME ...], --username [USERNAME ...]
                        One or more usernames to search.
  -e [EMAIL ...], --email [EMAIL ...]
                        One or more email to search.
  --csv, --no-csv       Generate a CSV with the results.
  --pdf, --no-pdf       Generate a PDF with the results.
  -v, --verbose, --no-verbose
                        Show verbose output.
  --filter FILTER       Filter sites to be searched by list property value.E.g --filter "cat=social"
  --no-nsfw             Removes NSFW sites from the search.
  --dump                Dump HTML content for found accounts.
  --proxy PROXY         Proxy to send HTTP requests through.
  --timeout TIMEOUT     Timeout in seconds for each HTTP request (Default is 30).
  --no-update           Don't update sites lists.
  --about               Show about information and exit.
```

### WhatsMyName Integration

Blackbird is fully integrated with [WhatsMyName](https://github.com/WebBreacher/WhatsMyName) project, witch has 600+ sites to perform accurate reverse username search.

### Sponsors

This project is proudly sponsored by:

[![Cyber Hunter Lab Logo](https://raw.githubusercontent.com/p1ngul1n0/src/master/logo\_chl.jpg)](https://site.cyberhunteracademy.com/)

### Disclaimer

```
This or previous program is for Educational purpose ONLY. Do not use it without permission. 
The usual disclaimer applies, especially the fact that me (P1ngul1n0) is not liable for any 
damages caused by direct or indirect use of the information or functionality provided by these 
programs. The author or any Internet provider bears NO responsibility for content or misuse 
of these programs or any derivatives thereof. By using these programs you accept the fact 
that any damage (dataloss, system crash, system compromise, etc.) caused by the use of these 
programs is not P1ngul1n0's responsibility.
```

### Contact

Feel free to contact me at [X](https://x.com/p1ngul1n0)\
