import os
import UnityPy

INPUT_ASSETS_PATH = 'inputs/resources.assets'
INPUT_TEXT_FILE = 'processed/{}_{}.txt'
OUTPUT_ASSETS_FOLDER = 'outputs/assets_{}'
OUTPUT_ASSETS_FILE = 'resources.assets'

ASSETS_OBJECT_NAMES = ['[Translation]Upgrade_Action_Name',
                       '[Translation]Dungeon_DungeonName',
                       '[Translation]Title_Name',
                       '[Translation]Routine_Name']

TARGETS = ['feminine', 'masculine', 'neutral']


def repack_text_into_assets(assets_path, target):
    env = UnityPy.load(assets_path)

    for obj in env.objects:
        if obj.type.name != 'TextAsset':
            continue

        if obj.peek_name() not in ASSETS_OBJECT_NAMES:
            continue

        instance = obj.parse_as_object()

        text_file = INPUT_TEXT_FILE.format(instance.m_Name, target)
        with open(text_file, 'r', encoding='utf-8') as _f:
            new_text = _f.read()

        instance.m_Script = new_text
        obj.patch(instance)

        print(f'Updated {assets_path} using text {text_file}')

    return env.file.save()


if __name__ == '__main__':
    for target in TARGETS:
        output_assets_folder = OUTPUT_ASSETS_FOLDER.format(target)
        output_assets_file = os.path.join(output_assets_folder, OUTPUT_ASSETS_FILE)

        modified_assets = repack_text_into_assets(INPUT_ASSETS_PATH, target)

        os.makedirs(output_assets_folder, exist_ok=True)
        with open(output_assets_file, 'wb') as _f:
            _f.write(modified_assets)
            print(f'Updated assets written to {output_assets_file}')
