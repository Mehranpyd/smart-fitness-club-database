from pathlib import Path
import py_compile

root = Path(__file__).parent
for p in root.joinpath('app').glob('*.py'):
    py_compile.compile(str(p), doraise=True)

required = [
    'docker-compose.yml', 'README.md',
    'sql/01_schema.sql', 'sql/02_seed.sql', 'sql/03_indexes.sql', 'sql/04_queries.sql',
    'nosql/seed_mongo.py', 'nosql/queries.js',
    'app/Dockerfile', 'app/requirements.txt', 'app/main.py',
    'docs/ER-diagram.md', 'docs/DESIGN_NOTES.md'
]
missing = [x for x in required if not root.joinpath(x).exists()]
if missing:
    raise SystemExit('Missing: ' + ', '.join(missing))
print('Structure and Python syntax verified.')
