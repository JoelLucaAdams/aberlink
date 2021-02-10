# Spike work for PostgreSQL database

After a discussion with CS-Support we came to the conclusion that there were two options for hosting PostgreSQL. The first being that it would be hosted directly in my container and the second being that it would be hosted remotely on db.dcs.aber.ac.uk. I've decided in the end to use the second option as keeping the database separate from my container makes it a lot less prone to attacks as it is located elsewhere. It also means that I no longer have to setup my own database each time. The details to access the container are as follows:  

Server: `db.dcs.aber.ac.uk` \
PostgreSQL Account: `joa38` \
Database: `cs39440_20_21_joa38` \
Password: `Stored on Lasspass` (reset: <https://impacs-inter.dcs.aber.ac.uk/mypgpw/Postgres/>)

link to connect from command line: `psql -h db.dcs.aber.ac.uk -U joa38 -d cs39440_20_21_joa38`

Thank you to Sandy Spence [axs] for setting up access the database.

## migrating database

`python3 manage.py makemigrations <app>` \
`python3 manage.py sqlmigrate <app> <migration_id>` \
`python3 manage.py migrate`

Use `python3 manage.py migrate --fake-initial` if it breaks.

To rollback to a previous migration use `python3 manage.py migrate <app> <migration_id>`

## Error `django.db.migrations.exceptions.InconsistentMigrationHistory`

This error usually pops up when the database has to be updated and the tables need to be rewritten. Currently my workaround is to delete and recreate the daatabse to fix any issues using the following commands: \
`psql -h db.dcs.aber.ac.uk -U joa38 -d cs39440_20_21_joa38` \
`DROP SCHEMA joa38 CASCADE;` \
`CREATE SCHEMA joa38;` \
`python3 manage.py migrate`
