import os
import UnityPy

ASSETS_PATH = 'outputs/assets_{}/resources.assets'
TARGETS = ['feminine', 'masculine', 'neutral']

ASSETS_OBJECT_NAME = '[Translation]Routine_Name'
ORIGINAL_TEXT = '"Hey hey hey, is he insane to eat as it is? He\'ll die for sure."'

REPLACEMENTS = {
    'masculine': ORIGINAL_TEXT,
    'feminine': '"Hey hey hey, is she insane to eat as it is? She\'ll die for sure."',
    'neutral': '"Hey hey hey, are they insane to eat as it is? They\'ll die for sure."',
}


def patch_routine_name(assets_path, target):
    env = UnityPy.load(assets_path)
    replacement_text = REPLACEMENTS[target]

    for obj in env.objects:
        if obj.type.name != 'TextAsset':
            continue

        if obj.peek_name() != ASSETS_OBJECT_NAME:
            continue

        instance = obj.parse_as_object()

        if ORIGINAL_TEXT not in instance.m_Script:
            raise ValueError(
                f'Expected text not found in {ASSETS_OBJECT_NAME} for target {target}'
            )

        original_text = instance.m_Script
        new_text = original_text.replace(ORIGINAL_TEXT, replacement_text)

        instance.m_Script = new_text
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
