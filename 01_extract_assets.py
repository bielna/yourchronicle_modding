import UnityPy

ASSETS_PATH = 'inputs/resources.assets'
OUTPUT_FILE = 'processed/text_original.txt'

ASSETS_OBJECT_NAME = '[Translation]Upgrade_Action_Name'


def extract_original_text(assets_path):
    env = UnityPy.load(assets_path)

    for obj in env.objects:
        if obj.type.name != 'TextAsset':
            continue

        if obj.peek_name() != ASSETS_OBJECT_NAME:
            continue

        instance = obj.parse_as_object()
        return instance.m_Script

    raise ValueError(f'Target TextAsset {ASSETS_OBJECT_NAME} not found in {assets_path}')


if __name__ == '__main__':
    text_original = extract_original_text(ASSETS_PATH)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as _f:
        _f.write(text_original)
        _f.write('\n')
