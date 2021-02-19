## Changes in code
### bot.py:
* removed **.imtheadmin** command
    * instead: Admin Channel ID defined by env variable
* **on_ready()**: Unanswered requests from last session are now loaded
* **.whitelist**:
    * new arguments first name and (school) class (for private usage)
    * new field showing the admin the amount of whitelistet MC Accounts by the Dc User
    * added check if the user has already been whitelisted

### filemanager.py:
* after terminating session: requests are now saved as objects (pk1), not in JSON files
* completely switched the whitelist to a database
    * this works because we doesn't use the original whitelist.json in Minecraft, instead a plugin chekcks if the UUID is in the databse
* save_requests:
    * much simpler because the requests are saved as objects (with the _pickle module), not in a JSON anymore
* added **load_requests()** for loading the saved requests on startup
* **write_whitelist()**: added database support
* added **uuid_in_whitelist()** for checking the amount of the given UUID in the database
* added **dc_id_in_whitelist()** for checking the amount of the given Discord ID in the database

### request.py
* added two attributes *first_name* and *classs* (three 's' for a difference to the 'class' in python)

### Database table pattern

```
create table dc_users
(
    ID         int auto_increment
               primary key,
    uuid       varchar(64)  not null,
    dc_id      bigint       not null,
    first_name varchar(255) null,
    classs     varchar(255) null,
    date       datetime     not null
);
```
