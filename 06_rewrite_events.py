import csv
import io
import os
import UnityPy

from encoding_utils import decode_translation, encode_translation

ASSETS_FOLDER = 'outputs/assets_{}'
INPUT_ASSETS_FILE = 'resources.assets'
OUTPUT_ASSETS_FILE = 'resources_with_rewritten_events.assets'
TARGETS = ['feminine', 'masculine', 'neutral']

ASSETS_OBJECT_NAME = '[Translation]Upgrade_Action_Name'

# Format:
# (event_id, original_us_name, new_us_name, new_us_description)
REPLACEMENTS = [
    # Replacement: Valley Village, epilogue
    # Makes Bestla the new Chief while making Gilling talk about proposing to her.
    # Acknowledges the children offered as sacrifice may not be willing to come back.
    (
        'A9EventR1',
        'Talk with Bestla 1/3',
        'Talk with Gilling 1/3',
        "Oh, you! Thank you for everything you've done. Bestla is already working as chief. She hasn't rested for a moment."
    ),
    (
        'A9EventR2',
        'Talk with Bestla 2/3',
        'Talk with Gilling 2/3',
        "I'll support her however I can. Bestla is the one who brought change to this village."
    ),
    (
        'A9EventR3',
        'Talk with Bestla 3/3',
        'Talk with Gilling 3/3',
        "And... well, I still intend to marry her someday. For now, I'll help her and her mother however I can."
    ),
    (
        'A9EventS1',
        'Talk with Gilling 1/3',
        'Talk with Bestla 1/3',
        "Thank you very much. Thanks to you, I was able to return to my mother...and now I have to protect this village as its chief."
    ),
    (
        'A9EventS2',
        'Talk with Gilling 2/3',
        'Talk with Bestla 2/3',
        "So the Divine Beast carried the offered children to towns outside the valley...? Then they may still be alive, living lives of their own."
    ),
    (
        'A9EventS3',
        'Talk with Gilling 3/3',
        'Talk with Bestla 3/3',
        "I want to contact them, if I can. They may not return, but I would like them to know that the village has changed."
    ),
    # Replacements : Dragon Village, epilogue
    # Improves Dragon Princess' leadership by giving her lines after her recovery
    # and having her thank the protagonist.
    # Keep the Elder's joke, make princess call her out.
    (
        'A12TalkElder2',
        'Talk with Elder 1/6',
        'Talk with Elder 1/2',
        "...oh, thank you so much! The black bruises disappeared, and the princess has finally awakened from her peaceful sleep."
    ),
    (
        'A12TalkElder2',
        'Talk with Elder 2/6',
        'Talk with Dragon Priestess 1/4',
        "I am sorry to greet you from my sickbed again. But this time, I can thank you properly as the Dragon Priestess."
    ),
    (
        'A12TalkElder2',
        'Talk with Elder 3/6',
        'Talk with Dragon Priestess 2/4',
        "You saved me from the curse, and you freed The Dragon from the evil that had taken hold of him. I will not forget this."
    ),
    (
        'A12TalkElder2',
        'Talk with Elder 4/6',
        'Talk with Dragon Priestess 3/4',
        "I will inform the guild that you fulfilled our request. From now on, Dragon Village will gladly lend you its strength."
    ),
    (
        'A12TalkElder2',
        'Talk with Elder 5/6',
        'Talk with Elder 2/2',
        "If I were a little younger, I would have offered this body of mine as thanks...time truly is a cruel thing."
    ),
    (
        'A12TalkElder2',
        'Talk with Elder 6/6',
        'Talk with Dragon Priestess 4/4',
        "...please ignore her. You have already done more than enough for us. I hope we meet again under calmer skies."
    ),
    # Replacement : Academic City, Norn events
    # Changes the comments and reasoning for Norn leaving the dorm to be focused
    # on her own story, instead of the MC.
    (
        'A3EventAPBoys',
        'Boys passing by',
        'Students passing by',
        "Whoa, who's that pretty girl? She came here right after school started? Lucky..."
    ),
    (
        'A3EventAPTalkNorn2',
        'Talk with Norn 1/2',
        'Talk with Norn 1/2',
        "Hmm...if I stay here all the time, I won't get to know anyone in my own dorm."
    ),
    (
        'A3EventAPTalkNorn2',
        'Talk with Norn 2/2',
        'Talk with Norn 2/2',
        "I think I'll go back to my room for today. I'll be okay by myself! Bye-bye!"
    ),
    # Replacement : Akashic Records, upgrade action
    # Ensures consistency between Fili 'Duel with her' and Ottar 'Duel with Him'
    (
        'A15_addOttarBattleAfterGraduationAR',
        'Duel with Him',
        'Duel with him',
        "You know you are already stronger than him.\nIf you 'graduate' before completing the 'Tournament - Round 7', add an action to duel him in the Academy City.",
    ),
]


def parse_csv(script):
    return list(csv.reader(io.StringIO(script)))


def write_csv(rows):
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(rows)
    return output.getvalue()


def patch_action_name(assets_path):
    env = UnityPy.load(assets_path)

    for obj in env.objects:
        if obj.type.name != 'TextAsset':
            continue

        if obj.peek_name() != ASSETS_OBJECT_NAME:
            continue

        instance = obj.parse_as_object()
        script = decode_translation(instance.m_Script)

        rows = parse_csv(script)

        found_pairs = set()

        replacements_by_pair = {
            (event_id, original_us_name): (new_us_name, new_us_description)
            for event_id, original_us_name, new_us_name, new_us_description in REPLACEMENTS
        }

        for row in rows:
            if len(row) < 4:
                continue

            event_id = row[0]
            us_name = row[1]

            pair = (event_id, us_name)

            if pair not in replacements_by_pair:
                continue

            new_us_name, new_us_description = replacements_by_pair[pair]

            row[1] = new_us_name
            row[3] = new_us_description

            found_pairs.add(pair)

            print(f'Patched ({event_id}, {us_name}) -> ({event_id}, {new_us_name})')

        for event_id, original_us_name, _, _ in REPLACEMENTS:
            pair = (event_id, original_us_name)

            if pair not in found_pairs:
                print(f'Warning: pair not found: ({event_id}, {original_us_name})')

        instance.m_Script = encode_translation(write_csv(rows))
        obj.patch(instance)

        print(f'Patched {ASSETS_OBJECT_NAME} in {assets_path}')
        return env.file.save()

    raise ValueError(f'Target TextAsset {ASSETS_OBJECT_NAME} not found in {assets_path}')


if __name__ == '__main__':
    for target in TARGETS:
        assets_folder = ASSETS_FOLDER.format(target)
        input_assets_path = os.path.join(assets_folder, INPUT_ASSETS_FILE)
        output_assets_path = os.path.join(assets_folder, OUTPUT_ASSETS_FILE)

        if not os.path.exists(input_assets_path):
            raise FileNotFoundError(f'Assets file not found: {input_assets_path}')

        patched_assets = patch_action_name(input_assets_path)

        # write to temp file because writing to an open assets file can cause issues in UnityPy
        tmp = output_assets_path + '.tmp'
        with open(tmp, 'wb') as _f:
            _f.write(patched_assets)

        os.replace(tmp, output_assets_path)
        print(f'Updated assets written to {output_assets_path}')
