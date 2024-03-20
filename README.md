# SETUP

1. Create a copy of `.env_local` and change name to `.env`
2. Create a copy of `menumanager_country_api/settings/local_sample.py` and change name to `local.py`
3. Run the service
    1. Download contents of the `USSD-Country-API`
       from `https://dev.azure.com.mcas.ms/ICT-DevOps/USSD/_git/USSD-local-docker-services-run`
       /`USSD-local-docker-services-run` repo/ This will add files needed for local run like DBs
       and `docked-compose.yml`
    2. Copy downloaded contents in the base folder of this project
    3. Run `docker-compose up` for standalone run
    4. If you run all services refer to the base readme of `USSD-local-docker-services-run` REPO

# INIT menu DBs
You might initialize all subsidiaries DBs by running the `python menus_importer.py` in the project base folder.
This is going to read dumps in `data_assets` folder. For more info, check the comments in the `menus_importer.py` file.

# Some important environment variables

- SERVICE_BASE_PORT
    - DESCRIPTION: That port will be added to the country code to get the port that current country API is running on.
    - EXAMPLE: `20000+254 = 20254` Expected country API for Kenya to run on that port.
    - DEFAULT `20000`
- CACHE_MENU_KEY_PREFIX, default `menus`
    - DESCRIPTION: This will be used to store the menus key in redis.
    - EXAMPLE: `menus_254_247` - default for Kenya, 247 shortcode.
    - DEFAULT: `menus`
- CACHE_OMNI_KEY_PREFIX, default `OMNI`
    - DESCRIPTION: This will be used to store the OMNI services key in redis.
    - EXAMPLE: `OMNI_254_247` - default for Kenya, 247 shortcode.
    - DEFAULT: `OMNI`
- DATABASE_NAME and LOCAL_DATABASE_NAME names of the databases used for menus. This simulates multi country service -
  different database for different country. !NB always use local DB! Remote DB is used only when menus should be
  transferred from remote db to local DBs. More on that - in the readme of `USSD-local-docker-services-run` REPO

There are predefined .env files for each country in `USSD-local-docker-services-run`. Refer to those to get more info.

# Notes on menu editing

In Home page of menu admin there is button - `Rebuild menus`. That button will rebuild all menus and OMNI services keys
for all shortcodes for that country. Menu building could fail if menus are not correct. Wrong menus are bad thing
because they could make user journey impossible. For example - router screen w/o options or menu screen w/o options - If
menus are built with screens like that it will crash the entire user journey. That's why if one screen is not right then
the entire menu building process fails. Menu building is throwing a custom exception and tells you why menu building has
failed. When you do menu editing, always rebuild menus when you are ready and make sure that everything is building
correctly.# country-api
