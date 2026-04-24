import os
import csv

INPUT_FILE = 'processed/{}_with_templates.txt'
OUTPUT_FILE = 'processed/{}_{}.txt'
LOG_FILE = 'processed/log_new_lines_{}.txt'
TARGETS = ['feminine', 'masculine', 'neutral']

ASSETS_OBJECT_NAMES = ['[Translation]Upgrade_Action_Name',
                       '[Translation]Dungeon_DungeonName',
                       '[Translation]Title_Name',
                       '[Translation]Routine_Name']

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
    '__MC_PRONOUN_SUBJECT_NEED__': {
        'masculine': 'he needs',
        'feminine': 'she needs',
        'neutral': 'they need'
    },
    '__MC_PRONOUN_SUBJECT_SEEM_CAPITAL__': {
        'masculine': 'He seems',
        'feminine': 'She seems',
        'neutral': 'They seem'
    },
    '__MC_PRONOUN_SUBJECT_BE_INTERROGATIVE__': {
        'masculine': 'is he',
        'feminine': 'is she',
        'neutral': 'are they'
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
    '__STRONG_TERM_CAPITAL__': {
        'masculine': 'A ladykiller',
        'feminine': 'You look pretty strong now',
        'neutral': 'You look pretty strong now'
    },
    '__SANDWICH_TERM__': {
        'masculine': 'Sandwich Man',
        'feminine': 'Sandwich Lady',
        'neutral': 'Sandwich Friend'
    },
    '__GOOD_PEOPLE__': {
        'masculine': 'good men',
        'feminine': 'good people',
        'neutral': 'good people'
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
    '__MC_DRAGONSLAYER_STRONG_TERM__': {
        'masculine': 'strong man',
        'feminine': 'strong woman',
        'neutral': 'one'
    },
    '__MC_BEAST_SOVEREIGN_TERM__': {
        'masculine': 'king',
        'feminine': 'queen',
        'neutral': 'sovereign'
    }
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

def run_process_file(asset_object_name, target, log_file):
        input_file = INPUT_FILE.format(asset_object_name)
        output_file = OUTPUT_FILE.format(asset_object_name, target)

        with open(log_file, 'a', encoding='utf-8') as _f:
            rows = process_file(input_file, target, _f)
        write_file_with_substitutions(output_file, rows)

if __name__ == '__main__':
    print(f'Applying {len(templates)} substitution rules')
    for asset_object_name in ASSETS_OBJECT_NAMES:
        for target in TARGETS:
            log_file = LOG_FILE.format(target)
            run_process_file(asset_object_name, target, log_file)

            print(f'All substitutions applied for object {asset_object_name} with target \'{target}\'')
