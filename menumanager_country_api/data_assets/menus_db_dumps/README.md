# NOTES

Filenames should be named like so: `XX_MM_YYYY.json`
`XX` is the ISO2 country code
`MM` is the month
`YYYY` is the year
Those should be placed in the `data_assets/menus_db_dumps` dir.

# Usage

1. Run `python menus_importer.py` from inside the country API container's shell in the project's base dir /most
   likely `/opt/app/menumanager_country_api`/
2. If needed, you might add a country to be proceeded only like `python menus_importer.py ke`, which is going to add
   only the menus for Kenya.
3. It is safe to import `import_menus` function in other scripts. Runs only with pure Python - if Django is initialized
   then this might not work.
4. Current local sqlite3 DB files will be backed up. 
5. Super-user is automatically created