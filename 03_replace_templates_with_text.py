import os
import csv

INPUT_FILE = 'processed/text_with_templates.txt'
OUTPUT_FILE = 'processed/text_{}.txt'
LOG_FILE = 'processed/log_new_lines_{}.txt'
TARGETS = ['feminine', 'masculine', 'neutral']

LINE_ID_INDEX = 0
TEXT_EN_INDEX = 3

VERBOSE = False

templates = {
    '__MC_CHILD_TERM__': {
        'masculine': 'son',
        'feminine': 'daughter',
        'neutral': 'child'
    },
    '__MC_CHILD_TERM_CAPITAL__': {
        'masculine': 'Son',
        'feminine': 'Daughter',
        'neutral': 'Child'
    },
    '__MC_KID_TERM__': {
        'masculine': 'boy',
        'feminine': 'girl',
        'neutral': 'kid'
    },
    '__MC_KID_TERM_CAPITAL__': {
        'masculine': 'Boy',
        'feminine': 'Girl',
        'neutral': 'Kid'
    },
    '__MC_SIB_TERM__': {
        'masculine': 'bro',
        'feminine': 'sis',
        'neutral': 'pal'
    },
    '__MC_SIBLING_TERM__': {
        'masculine': 'brother',
        'feminine': 'sister',
        'neutral': 'friend'
    },
    '__MC_PERSON_TERM__': {
        'masculine': 'man',
        'feminine': 'woman',
        'neutral': 'person'
    },
    '__MC_SOMEONE_TERM__': {
        'masculine': 'guy',
        'feminine': 'gal',
        'neutral': 'one'
    },
    '__MC_A_SOMEONE_TERM__': {
        'masculine': 'a guy',
        'feminine': 'a gal',
        'neutral': 'someone'
    },
    '__MC_PRONOUN_SUBJECT_DO__': {
        'masculine': 'he does',
        'feminine': 'she does',
        'neutral': 'they do'
    },
    '__MC_PRONOUN_SUBJECT_BE__': {
        'masculine': 'he is',
        'feminine': 'she is',
        'neutral': 'they are'
    },
    '__MC_PRONOUN_SUBJECT_HAVE_BEEN__': {
        'masculine': "he's been",
        'feminine': "she's been",
        'neutral': "they've been"
    },
    '__MC_PRONOUN_SUBJECT_DID_HAVE_TO__': {
        'masculine': 'did he have to',
        'feminine': 'did she have to',
        'neutral': 'did they have to'
    },
    '__MC_PRONOUN_SUBJECT_HAVE__': {
        'masculine': 'he has',
        'feminine': 'she has',
        'neutral': 'they have'
    },
    '__MC_PRONOUN_SUBJECT_HAVE_CAPITAL__': {
        'masculine': 'He has',
        'feminine': 'She has',
        'neutral': 'They have'
    },
    '__MC_PRONOUN_SUBJECT_WANT__': {
        'masculine': 'he wants',
        'feminine': 'she wants',
        'neutral': 'they want'
    },
    '__MC_PRONOUN_SUBJECT__': {
        'masculine': 'he',
        'feminine': 'she',
        'neutral': 'they'
    },
    '__MC_PRONOUN_SUBJECT_CAPITAL__': {
        'masculine': 'He',
        'feminine': 'She',
        'neutral': 'They'
    },
    '__MC_PRONOUN_OBJECT__': {
        'masculine': 'him',
        'feminine': 'her',
        'neutral': 'them'
    },
    '__MC_PRONOUN_POSSESSIVE__': {
        'masculine': 'his',
        'feminine': 'her',
        'neutral': 'their'
    },
    '__SWORD_USER_TERM__': {
        'masculine': 'swordsman',
        'feminine': 'swordswoman',
        'neutral': 'swordfighter'
    },
    '__STRONG_TERM__': {
        'masculine': 'ladykiller',
        'feminine': 'muscle lady',
        'neutral': 'powerhouse'
    },
    '__SANDWICH_TERM__': {
        'masculine': 'Sandwich Man',
        'feminine': 'Sandwich Lady',
        'neutral': 'Sandwich Friend'
    },
    '__MC_TITLE_TERM__': {
        'masculine': 'mister',
        'feminine': 'miss',
        'neutral': 'friend'
    },
    '__MC_TITLE_TERM_CAPITAL__': {
        'masculine': 'Mister',
        'feminine': 'Miss',
        'neutral': 'Friend'
    },
}


def process_file(input_file, target, log_file):
    processed_rows = []

    with open(input_file, encoding='utf-8') as _f:
        reader = csv.reader(_f)

        for row in reader:
            line_id = row[LINE_ID_INDEX]
            text_en = row[TEXT_EN_INDEX]

            new_text = replace_placeholders_with_text(text_en, target)

            if new_text != text_en:
                log_change(line_id, text_en, new_text, log_file)
                row[TEXT_EN_INDEX] = new_text

            processed_rows.append(row)

    return processed_rows


def replace_placeholders_with_text(text, target):
    for token, values in templates.items():
        text = text.replace(token, values[target])

    return text

def log_change(line_id, text_en, new_text, log_file):
    if VERBOSE: print(f'[{line_id}] {text_en} -> {new_text}')
    log_file.write(f'[{line_id}] {text_en} -> {new_text}\n')

def write_file_with_substitutions(output_file, rows):
    with open(output_file, 'w', encoding='utf-8', newline='') as _f:
        writer = csv.writer(_f, lineterminator='\n')

        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f'File with template text not found: {INPUT_FILE}')

    print(f'Applying {len(templates)} substitution rules')

    for target in TARGETS:
        log_file = LOG_FILE.format(target)
        output_file = OUTPUT_FILE.format(target)

        with open(log_file, 'w', encoding='utf-8') as _f:
            rows = process_file(INPUT_FILE, target, _f)
        write_file_with_substitutions(output_file, rows)

        print(f'All substitutions applied for target \'{target}\'')
