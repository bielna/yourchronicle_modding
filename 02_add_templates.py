import csv
import re

INPUT_FILE = 'processed/{}_original.txt'
OUTPUT_FILE = 'processed/{}_with_templates.txt'
LOG_FILE = 'processed/log_changes.txt'

ASSETS_OBJECT_NAMES = ['[Translation]Upgrade_Action_Name',
                       '[Translation]Dungeon_DungeonName']

LINE_ID_INDEX = 0
TEXT_EN_INDEX = 3

VERBOSE = False

rules = [
    {
        'find': r'\bson\b',
        'replace': '__MC_CHILD_TERM__',
        'exclude': ['A13HatBoy2',
                    'A13HatBoy3',
                    'A13_FiliArcanaForum2',
                    'A11EventR1']
    },
    {
        'find': r'\bSon\b',
        'replace': '__MC_CHILD_TERM_CAPITAL__'
    },
    {
        'find': r'\bboy\b',
        'replace': '__MC_KID_TERM__',
        'exclude': ['bishopEventB4',
                    'bishopEventB6',
                    'A5EventH7']
    },
    {
        'find': r'\bBoy\b',
        'replace': '__MC_KID_TERM_CAPITAL__'
    },
    {
        'find': r'\bbro\b',
        'replace': '__MC_SIB_TERM__',
        'exclude': ['A11EventCommonH2']
    },
    {
        'find': r'\bbrother\b',
        'replace': '__MC_SIBLING_TERM__',
        'include': ['A3EventD3']
    },
    {
        'find': r'\bman\b',
        'replace': '__MC_PERSON_TERM__',
        'include': ['talkMuscleman1',
                    'A4EventH2',
                    'A4EventB3',
                    'C5EventB2',
                    'A10EventL_Normal1',
                    'A10EventR_SavingBoss3',
                    'talkInnkeeper',
                    'talkLorem']
    },
    {
        'find': r'\ba guy\b',
        'replace': '__MC_A_SOMEONE_TERM__',
        'include': ['A11EventCommonA1']
    },
    {
        'find': r'\bguy\b',
        'replace': '__MC_SOMEONE_TERM__',
        'include': ['A2EventF4',
                    'A3EventB5',
                    'C6AskrsSoliloquy',
                    'A12TalkCheerfulMerchant',
                    'A3EventAPBoys']
    },
    {
        'find': r'\bhe does\b',
        'replace': '__MC_PRONOUN_SUBJECT_DO__',
        'include': ['C6SigurdsSoliloquyDestiny']
    },
    {
        'find': r'\bhe is\b',
        'replace': '__MC_PRONOUN_SUBJECT_BE__',
        'include': ['C6SigurdsSoliloquyFather']
    },
    {
        'find': r"\bhe's been\b",
        'replace': '__MC_PRONOUN_SUBJECT_HAVE_BEEN__',
        'include': ['C6SigurdsSoliloquyDestiny']
    },
    {
        'find': r'\bdid he have to\b',
        'replace': '__MC_PRONOUN_SUBJECT_DID_HAVE_TO__',
        'include': ['C6EmblasSoliloquy']
    },
    {
        'find': r'\bhe has\b',
        'replace': '__MC_PRONOUN_SUBJECT_HAVE__',
        'include': ['C6SigurdsSoliloquyFather']
    },
    {
        'find': r'\bHe has\b',
        'replace': '__MC_PRONOUN_SUBJECT_HAVE_CAPITAL__',
        'include': ['C6SigurdsSoliloquyFather',
                    'C6SigurdsSoliloquyDestiny']
    },
    {
        'find': r'\bhe wants\b',
        'replace': '__MC_PRONOUN_SUBJECT_WANT__',
        'include': ['A4EventB3']
    },
    {
        'find': r'\bhe\b',
        'replace': '__MC_PRONOUN_SUBJECT__',
        'include': ['A4EventB3',
                    'C6SigurdsSoliloquyFather',
                    'C6SigurdsSoliloquyDestiny']
    },
    {
        'find': r'\bHe\b',
        'replace': '__MC_PRONOUN_SUBJECT_CAPITAL__',
        'include': ['C6SigurdsSoliloquyFather',
                    'C6SigurdsSoliloquyDestiny']
    },
    {
        'find': r'\bhim\b',
        'replace': '__MC_PRONOUN_OBJECT__',
        'include': ['talkVillagerE',
                    'C6SigurdsSoliloquyFather',
                    'C6SigurdsSoliloquyDestiny']
    },
    {
        'find': r'\bhis\b',
        'replace': '__MC_PRONOUN_POSSESSIVE__',
        'include': ['C6SigurdsSoliloquyFather',
                    'C6SigurdsSoliloquyDestiny']
    },
    {
        'find': r'\bswordsman\b',
        'replace': '__SWORD_USER_TERM__',
        'include': ['talkSpearsmithA',
                    'training_roomG',
                    'swordClassAdvanced']
    },
    {
        'find': r'\bladykiller\b',
        'replace': '__STRONG_TERM__'
    },
    {
        'find': r'\bSandwich Man\b',
        'replace': '__SANDWICH_TERM__'
    },
    {
        'find': r'\bmister\b',
        'replace': '__MC_TITLE_TERM__'
    },
    {
        'find': r'\bMister\b',
        'replace': '__MC_TITLE_TERM_CAPITAL__'
    }
]


def process_file(input_file, log_file):
    processed_rows = []

    with open(input_file, encoding='utf-8') as _f:
        reader = csv.reader(_f)

        for row in reader:
            line_id = row[LINE_ID_INDEX]
            text_en = row[TEXT_EN_INDEX]

            new_text = add_placeholders(line_id, text_en)

            if new_text != text_en:
                log_change(line_id, text_en, new_text, log_file)
                row[TEXT_EN_INDEX] = new_text

            processed_rows.append(row)

    return processed_rows


def add_placeholders(line_id, text):
    for rule in rules:
        include = rule.get('include')
        exclude = rule.get('exclude')

        include_ok = (
            not include
            or line_id in include
        )

        exclude_ok = (
            not exclude
            or line_id not in exclude
        )

        if include_ok and exclude_ok:
            text = re.sub(rule['find'], rule['replace'], text)

    return text

def log_change(line_id, text_en, new_text, log_file):
    if VERBOSE: print(f'[{line_id}] {text_en} -> {new_text}')
    log_file.write(f'[{line_id}] {text_en} -> {new_text}\n')

def write_file_with_templates(output_file, rows):
    with open(output_file, 'w', encoding='utf-8', newline='') as _f:
        writer = csv.writer(_f, lineterminator='\n')

        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    print(f'Applying {len(rules)} placeholder rules')

    for asset_object_name in ASSETS_OBJECT_NAMES:
        input_file = INPUT_FILE.format(asset_object_name)
        output_file = OUTPUT_FILE.format(asset_object_name)

        with open(LOG_FILE, 'a', encoding='utf-8') as _f:
            rows = process_file(input_file, _f)
        write_file_with_templates(output_file, rows)

        print(f'All placeholders applied to {asset_object_name}')
