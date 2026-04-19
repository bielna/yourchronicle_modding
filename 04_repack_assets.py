import os
import UnityPy

INPUT_ASSETS_PATH = 'inputs/resources.assets'
INPUT_TEXT_FILE = 'processed/text_{}.txt'
OUTPUT_ASSETS_FOLDER = 'outputs/assets_{}'
OUTPUT_ASSETS_FILE = 'resources.assets'

TARGETS = ['feminine', 'masculine', 'neutral']

ASSETS_OBJECT_NAME = '[Translation]Upgrade_Action_Name'


def repack_text_into_assets(assets_path, text_file):
    env = UnityPy.load(assets_path)

    with open(text_file, 'r', encoding='utf-8') as _f:
        new_text = _f.read()

    for obj in env.objects:
        if obj.type.name != 'TextAsset':
            continue

        if obj.peek_name() != ASSETS_OBJECT_NAME:
            continue

        instance = obj.parse_as_object()
        instance.m_Script = new_text
        obj.patch(instance)

        print(f'Updated {ASSETS_OBJECT_NAME} in {assets_path} using text {text_file}')
        return env.file.save()

    raise ValueError(f'Target TextAsset {ASSETS_OBJECT_NAME} not found in {assets_path}')


if __name__ == '__main__':
    for target in TARGETS:
        input_text_file = INPUT_TEXT_FILE.format(target)
        output_assets_folder = OUTPUT_ASSETS_FOLDER.format(target)
        output_assets_file = os.path.join(output_assets_folder, OUTPUT_ASSETS_FILE)

        modified_assets = repack_text_into_assets(INPUT_ASSETS_PATH, input_text_file)

        os.makedirs(output_assets_folder, exist_ok=True)
        with open(output_assets_file, 'wb') as _f:
            _f.write(modified_assets)
            print(f'Updated assets written to {output_assets_file}')
