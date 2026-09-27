# DEPLOYMENT

## Local

- Windows
- Python 3.11.9
- Django 5.0.14
- MariaDB 10.4.32 qua XAMPP
- `config/settings_local.py`

Local là source development chính.

## iNET

- Passenger
- Python 3.11
- Django 5.0.14
- MariaDB 10.4.32

Application root:
`/home/vorsnlkqhosting/dongtien`

Virtualenv Python:
`/home/vorsnlkqhosting/virtualenv/dongtien/3.11/bin/python`

## Quy trình

1. Test local.
2. Commit Git.
3. Upload/deploy source.
4. Nếu đổi model:
   `manage.py migrate`
5. Nếu đổi static:
   `manage.py collectstatic --clear --noinput`
6. Restart Python App.
7. Smoke test domain.

## Permission

- Directory: 755
- File: 644
- Không dùng 777.

## Không deploy

- `venv/`
- `__pycache__/`
- `*.pyc`
- `.git/`
- `config/settings_local.py`
- local secrets
- `public/static/` build cũ từ local

## Security

Không ghi credential thật vào tài liệu/repository.
