# 🧐 Use Cases

Here you can find several use cases for Blackbird, demonstrating how it can be applied in real-world scenarios.

### Reverse search multiple emails and usernames

```bash
python blackbird.py --username username1 username2 username3 --email email@email email1@email email2@email
```

### Reverse search multiple emails and usernames and export to PDF and CSV

```bash
python blackbird.py --pdf --csv --username username1 username2 username3 --email email@email.com email1@email.com email2@email.com
```

### Reverse search a username on Instagram to obtain obfuscated email and phone number

```bash
python blackbird.py --username username1 --filter "name=Instagram"
```

### Reverse search email and save HTTP response data for later analysis

```bash
python blackbird.py --email john@gmail.com --dump
```

### Reverse search username in social anime sites

```bash
python blackbird.py --username username1 --filter "uri_check~anime and cat=social"
```

### Reverse search list of usernames in TikTok

```bash
python blackbird.py --username username1 --filter "name=TikTok"
```
