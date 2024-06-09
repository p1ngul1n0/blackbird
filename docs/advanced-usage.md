# 🕵️ Advanced Usage

### Verbose

Verbose mode provides more detailed information during the tool's execution.

```bash
python blackbird.py --username username1 --verbose
```

### Filter

The `filter` command allows you to filter the sites to be searched based on various conditions. You can use a variety of operators and logical connectors to create complex filter expressions.

```bash
python blackbird.py --filter "name~Mastodon and cat=social or e_code<=200" --username crash 
```

#### Supported Operators

* `=` Equal to
* `~` Contains (substring match)
* `>` Greater than
* `<` Less than
* `>=` Greater than or equal to
* `<=` Less than or equal to
* `!=` Not equal to

<details>

<summary>More Examples</summary>

**Filter by Name Contains "Mastodon"**

```bash
python blackbird.py --filter "name~Mastodon" --username crash 
```

**Filter by Existent Code Greater Than 200**

```bash
python blackbird.py --filter "e_code>200" --username crash 
```

**Filter by Category Equals "social" and URI Contains "101010"**

```bash
python blackbird.py --filter "cat=social and uri_check~101010" --username crash 
```

**Filter by Error String Equals "@101010.pl" or Innexistent Code Less Than or Equal to 404**

```bash
python blackbird.py --filter "e_string=@101010.pl or m_code<=404" --username crash 
```

</details>

### Permute

If you\`re stuck in your investigation, you can use `--permute` to generate variations of a given username.&#x20;

```bash
python blackbird.py --username balestek 86 --permute
```

This will generate a list of 12 combinations:

```
balestek86
_balestek86
balestek86_
balestek_86
balestek-86
balestek.86
86balestek
_86balestek
86balestek_
86_balestek
86-balestek
86.balestek
```

You can go even further and use `--permuteall` to generate more variations

```
balestek
_balestek
balestek_ 
86
_86
86_
balestek86
_balestek86
balestek86_
balestek_86
balestek-86
balestek.86
86balestek
_86balestek
86balestek_
86_balestek
86-balestek
86.balestek
```

### No NSFW

If you wish to exclude NSFW sites from the search, simply use the `--no-nsfw` argument.

```bash
python blackbird.py --username username1 --no-nsfw
```

### Proxy

Use the `--proxy` argument to route all HTTP requests through a proxy.

```bash
python blackbird.py --username username1 --proxy "http://myproxy:9090"
```

### Timeout

To modify the server response timeout, use the `--timeout` argument followed by the desired timeout duration in seconds.

```bash
python blackbird.py --username username1 --timeout 30
```

### No Update

Use the `--no-update` argument to instruct the tool not to check for updates in the WhatsMyName list.

```bash
python blackbird.py --username username1 --no-update
```
