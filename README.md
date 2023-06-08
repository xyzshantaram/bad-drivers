# bad-drivers

quick and dirty python app to track bad drivers in Indian cities.

## Usage

Clone this repo.

```sh
git clone https://github.com/xyzshantaram/bad-drivers
```

Set up a venv.

```sh
python3 -m venv .venv
```

Install dependencies

```sh
pip install -r requirements.txt
```

Run app.

```sh
gunicorn -w 4 'main:create_app()' -b 127.0.0.1:3010
```

## todo

- [ ] group by license plate
- [ ] paginate queries
