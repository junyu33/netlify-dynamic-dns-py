# netlify-dynamic-dns-py

Since oscartbeaumont's [netlify-dynamic-dns](https://github.com/oscartbeaumont/netlify-dynamic-dns/) seems to be abandoned, I decided to create a Python version of it.

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

Fill your `ACCESSTOKEN`, `ZONE` (root domain) and `RECORD` (subdomain) in `config.sh` and run it.

```bash
bash ddns.sh
```

## License

MIT


