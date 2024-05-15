# 🔍 Basic Usage

{% hint style="info" %}
Blackbird can make mistakes. Consider checking the information.
{% endhint %}

### 👤 Username Reverse Search

```bash
python blackbird.py --username username1 username2 username3
```

### 📧 Email Reverse Search

```bash
python blackbird.py --email email1@email email2@email email3@email
```

### 📁 Export

#### PDF

```bash
python blackbird.py --username username1 --pdf
```

<figure><img src=".gitbook/assets/blackbird_report_pdf_results.png" alt=""><figcaption></figcaption></figure>

#### CSV

```
python blackbird.py --username username1 --csv
```

#### DUMP

Dump all found account HTTP responses.

```
python blackbird.py --username username1 --dump
```
