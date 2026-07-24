GAME_FOLDER := /mnt/c/Program Files (x86)/Steam/steamapps/common/YourChronicle/YourChronicle_Data
ASSETS_FILE := resources.assets
REWRITTEN_ASSETS_FILE := resources_with_rewritten_events.assets

INPUTS := inputs
PROCESSED := processed
OUTPUTS := outputs

TARGET ?= feminine

PACKAGE_VERSION ?= 2.7.13
GAME_VERSION := 2.7.13
BACKUP_FILE := $(GAME_FOLDER)/$(ASSETS_FILE)_backup_$(GAME_VERSION)


.PHONY: all feminine neutral masculine setup copy transform rewrite-events check backup replace replace-base package clean

all: copy transform rewrite-events replace

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

rewrite-events:
	python 06_rewrite_events.py

check:
	@for name in "[Translation]Upgrade_Action_Name" "[Translation]Dungeon_DungeonName" "[Translation]Title_Name" "[Translation]Routine_Name"; do \
		orig="$(PROCESSED)/$${name}_original.txt"; \
		gen="$(PROCESSED)/$${name}_masculine.txt"; \
		if diff "$$orig" "$$gen" > /dev/null; then \
			echo "$$name: OK (identical)"; \
		else \
			echo "[!] $$name: differs"; \
			diff -u "$$orig" "$$gen"; \
			exit 1; \
		fi; \
	done

backup:
	@if [ -f "$(BACKUP_FILE)" ]; then \
		echo "Backup already exists for $(GAME_VERSION)"; \
	else \
		cp "$(GAME_FOLDER)/$(ASSETS_FILE)" "$(BACKUP_FILE)"; \
		echo "Backup created for $(GAME_VERSION)"; \
	fi

restore:
	@if [ -f "$(BACKUP_FILE)" ]; then \
		cp "$(BACKUP_FILE)" "$(GAME_FOLDER)/$(ASSETS_FILE)"; \
		echo "Backup restored for $(GAME_VERSION)"; \
	else \
		echo "No backup found for $(GAME_VERSION), nothing restored"; \
	fi

replace: backup check rewrite-events
	cp "$(OUTPUTS)/assets_$(TARGET)/$(REWRITTEN_ASSETS_FILE)" "$(GAME_FOLDER)/$(ASSETS_FILE)"

replace-base: backup check
	cp "$(OUTPUTS)/assets_$(TARGET)/$(ASSETS_FILE)" "$(GAME_FOLDER)/$(ASSETS_FILE)"

package:
	@for target in feminine neutral masculine; do \
		echo "Creating yourchronicle_patch_$(PACKAGE_VERSION)_$$target.zip"; \
		zip -j "yourchronicle_patch_$(PACKAGE_VERSION)_$$target.zip" \
		"$(OUTPUTS)/assets_$$target/$(ASSETS_FILE)" \
		"$(OUTPUTS)/assets_$$target/$(REWRITTEN_ASSETS_FILE)"; \
	done

clean:
	rm -rf $(INPUTS) $(PROCESSED) $(OUTPUTS)
