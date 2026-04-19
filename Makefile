GAME_FOLDER := /mnt/c/Program Files (x86)/Steam/steamapps/common/YourChronicle/YourChronicle_Data
ASSETS_FILE := resources.assets

INPUTS := inputs
PROCESSED := processed
OUTPUTS := outputs

TARGET ?= feminine

PACKAGE_VERSION := 2.7.4


.PHONY: all feminine neutral masculine setup copy transform check backup replace clean

all: copy transform replace

feminine: TARGET := feminine
feminine: all

neutral: TARGET := neutral
neutral: all

masculine: TARGET := masculine
masculine: all

setup:
	mkdir -p $(INPUTS) $(PROCESSED) $(OUTPUTS)

copy: setup restore
	cp "$(GAME_FOLDER)/$(ASSETS_FILE)" "$(INPUTS)/"

transform:
	python 01_extract_assets.py
	python 02_add_templates.py
	python 03_replace_templates_with_text.py
	python 04_repack_assets.py
	python 05_additional_patch.py

check:
	@if diff -q "$(PROCESSED)/text_original.txt" "$(PROCESSED)/text_masculine.txt" > /dev/null; then \
		echo "Re-generated files are identical"; \
	else \
		echo "[!] Re-generated files differ"; \
		diff -u "$(PROCESSED)/text_original.txt" "$(PROCESSED)/text_masculine.txt"; \
		exit 1; \
	fi

backup:
	@if [ -f "$(GAME_FOLDER)/$(ASSETS_FILE)_backup" ]; then \
		echo "Backup already exists"; \
	else \
		cp "$(GAME_FOLDER)/$(ASSETS_FILE)" "$(GAME_FOLDER)/$(ASSETS_FILE)_backup"; \
		echo "Backup created"; \
	fi

restore:
	@if [ -f "$(GAME_FOLDER)/$(ASSETS_FILE)_backup" ]; then \
		cp "$(GAME_FOLDER)/$(ASSETS_FILE)_backup" "$(GAME_FOLDER)/$(ASSETS_FILE)"; \
		echo "Backup restored"; \
	else \
		echo "No backup found"; \
		exit 1; \
	fi

replace: backup check
	cp "$(OUTPUTS)/assets_$(TARGET)/$(ASSETS_FILE)" "$(GAME_FOLDER)/$(ASSETS_FILE)"

package:
	@for target in feminine neutral masculine; do \
		zip -j "yourchronicle_patch_$(PACKAGE_VERSION)_$$target.zip" \
		"outputs/assets_$$target/resources.assets"; \
	done

clean:
	rm -rf $(INPUTS) $(PROCESSED) $(OUTPUTS)
