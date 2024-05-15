# 🕵️ Advanced Usage

### Verbose

Verbose mode provides more detailed information during the tool's execution.

```bash
python blackbird.py --username username1 --verbose
```

### Filter

{% hint style="info" %}
This feature is expected to be enhanced soon to support a more dynamic approach.
{% endhint %}

You can filter the sites to be searched using the `--filter` argument by specifying a property name and the desired filter value. The available properties for filtering can be found in the JSON files used during the search.

```bash
python blackbird.py --username username1 --filter "name=Twitter"
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
