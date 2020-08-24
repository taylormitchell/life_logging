ankify_roam add --pageref-cloze=base_only ~/GitHub/roam_backup/json/second_brain.json
python -c "from ankify_roam import anki; anki._invoke('sync')"
