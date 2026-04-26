import os
import UnityPy

ASSETS_PATH = 'outputs/assets_{}/resources.assets'
TARGETS = ['feminine', 'masculine', 'neutral']

ASSETS_OBJECT_NAME = '[Translation]Title_Name'

REPLACEMENTS = [{
        'original': 'Lord of the Cave',
        'new': {
            'masculine': 'Lord of the Cave',
            'feminine': 'Lady of the Cave',
            'neutral': 'Ruler of the Cave'
        }
    },
    {
        'original': 'Lord of the Mountain',
        'new': {
            'masculine': 'Lord of the Mountain',
            'feminine': 'Lady of the Mountain',
            'neutral': 'Ruler of the Mountain'
        }
    },
    {
        'original': 'Beast King',
        'new': {
            'masculine': 'Beast King',
            'feminine': 'Beast Queen',
            'neutral': 'Beast Sovereign'
        }
    }]


def patch_routine_name(assets_path, target):
    env = UnityPy.load(assets_path)

    for obj in env.objects:
        if obj.type.name != 'TextAsset':
            continue

        if obj.peek_name() != ASSETS_OBJECT_NAME:
            continue

        instance = obj.parse_as_object()

        text_to_patch = instance.m_Script

        for replacement in REPLACEMENTS:
            original_text = replacement['original']
            new_text = replacement['new'][target]

            if original_text not in instance.m_Script:
                raise ValueError(
                    f'Expected text {original_text} not found in {ASSETS_OBJECT_NAME} for target {target}'
                )

            text_to_patch = text_to_patch.replace(original_text, new_text)

        instance.m_Script = text_to_patch
        obj.patch(instance)


        print(f'Patched {ASSETS_OBJECT_NAME} in {assets_path}')
        return env.file.save()

    raise ValueError(f'Target TextAsset {ASSETS_OBJECT_NAME} not found in {assets_path}')


if __name__ == '__main__':
    for target in TARGETS:
        assets_path = ASSETS_PATH.format(target)

        if not os.path.exists(assets_path):
            raise FileNotFoundError(f'Assets file not found: {assets_path}')

        patched_assets = patch_routine_name(assets_path, target)

        # write to temp file because writing to open assets file can cause issues in UnityPy
        tmp = assets_path + ".tmp"
        with open(tmp, 'wb') as _f:
            _f.write(patched_assets)

        os.replace(tmp, assets_path)
