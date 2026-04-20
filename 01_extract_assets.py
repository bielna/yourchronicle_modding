import UnityPy

ASSETS_PATH = 'inputs/resources.assets'
OUTPUT_FILE = 'processed/{}_original.txt'

ASSETS_OBJECT_NAMES = ['[Translation]Upgrade_Action_Name',
                       '[Translation]Dungeon_DungeonName']


def extract_original_text(assets_path):
    env = UnityPy.load(assets_path)

    text_to_patch = []

    for obj in env.objects:
        if obj.type.name != 'TextAsset':
            continue

        if obj.peek_name() not in ASSETS_OBJECT_NAMES:
            continue

        instance = obj.parse_as_object()
        text_to_patch.append((instance.m_Name, instance.m_Script))

    return text_to_patch


if __name__ == '__main__':
    text_to_patch = extract_original_text(ASSETS_PATH)

    for object_name, text_original in text_to_patch:
        output_file = OUTPUT_FILE.format(object_name)
        with open(output_file, 'w', encoding='utf-8') as _f:
            _f.write(text_original)
            _f.write('\n')
