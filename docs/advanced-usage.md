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

Check below for details to create your own filter search.

<details>

<summary>Properties</summary>

* `name` Name of the site being checked.
* `cat` Category of the site.
* `uri_check` The URL used to check for the existence of an account.
* `e_code` Expected HTTP status code when an account exists.
* `e_string` A string expected in the response when an account exists.
* `m_string` A string expected in the response when an account does not exist.
* `m_code` Expected HTTP status code when an account does not exist.

</details>

<details>

<summary>Operators</summary>

* `=` Equal to
* `~` Contains
* `>` Greater than
* `<` Less than
* `>=` Greater than or equal to
* `<=` Less than or equal to
* `!=` Not equal to

</details>

<details>

<summary>Examples</summary>

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

### Enhanced Instagram Account Metadata Extraction

The tool is able to extract additional, such as **obfuscated email and phone number information**. To take advantage of the enhanced Instagram account metadata extraction functionality, you need to set the `INSTAGRAM_SESSION_ID` in your `.env` file.

<details>

<summary>Steps to Acquire <code>INSTAGRAM_SESSION_ID</code>:</summary>

* **Log in to Instagram:**
  * Use your preferred web browser to log in to your Instagram account.
* **Open Developer Tools:**
  * Open the browser's developer tools. This is usually accessible by pressing `F12` or right-clicking on the page and selecting "Inspect".
* **Navigate to Cookies:**
  * In the developer tools, navigate to the "Application" tab.
  * Under "Storage," click on "Cookies" and then select the Instagram domain (e.g., `instagram.com`).
* **Find the `sessionid` Cookie:**
  * Locate the cookie named `sessionid` in the list of cookies.
* **Copy the `sessionid` Value:**
  * Copy the value of the `sessionid` cookie. This value is your `INSTAGRAM_SESSION_ID`.
*   **Set the `INSTAGRAM_SESSION_ID` in `.env`:**

    * Open your `.env` file (create one if it doesn't exist) in the root directory of your project.
    * Add the following line, replacing `your_session_id_here` with the value you copied:

    ```env
    INSTAGRAM_SESSION_ID=your_session_id_here
    ```

</details>

### Permute

If you\`re stuck in your investigation, you can use `--permute` to generate variations of a given username.&#x20;

```bash
python blackbird.py --username balestek 86 --permute
```

This will generate a list of 12 combinations:

<details>

<summary><code>--permute</code> Combinations</summary>

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



</details>

You can go even further and use `--permuteall` to generate more variations.

<details>

<summary><code>--permuteall</code> Combinations</summary>

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



</details>

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
