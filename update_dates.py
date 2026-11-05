"""Persist change dates, independent of build time, checkout time and locale."""
from datetime import date
import hashlib
import json

MONTHS = ('January February March April May June July August September October November December').split()


def english_date(iso):
    value = date.fromisoformat(iso)
    return f'{value.day} {MONTHS[value.month - 1]} {value.year}'


def fingerprint(parts):
    digest = hashlib.sha256()
    for part in parts:
        # Text line endings must not change between Windows and GitHub's Linux runner.
        if isinstance(part, str):
            part = part.replace('\r\n', '\n').encode('utf-8')
        digest.update(len(part).to_bytes(8, 'big'))
        digest.update(part)
    return digest.hexdigest()


def changed_record(previous, digest, today=None):
    if previous and previous.get('hash') == digest:
        return previous
    return {'hash': digest, 'date': (today or date.today()).isoformat()}


def read_records(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def write_records(path, records):
    text = json.dumps(records, indent=2, ensure_ascii=False) + '\n'
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')
