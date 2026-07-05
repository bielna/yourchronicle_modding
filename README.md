# Your Chronicle Patch

## Setup

By default, the Makefile assumes the game is installed through Steam on Windows and is run from WSL:

```makefile
GAME_FOLDER := /mnt/c/Program Files (x86)/Steam/steamapps/common/YourChronicle/YourChronicle_Data
```

If your game is installed elsewhere, update `GAME_FOLDER` in the Makefile.

When updating to a new game version, update:

```makefile
GAME_VERSION := 2.7.12
```

## Apply patch

Default target:

```bash
make
```

Neutral target:

```bash
make neutral
```

## Apply patch without rewritten events

```bash
make replace-base
```

## Package files

```bash
make package
```

With a custom package version:

```bash
make package PACKAGE_VERSION=2.7.12b
```

