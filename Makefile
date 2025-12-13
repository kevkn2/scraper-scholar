.PHONY: 
	create_migration apply_migrations downgrade init_db help

create_migration:
	alembic revision --autogenerate -m "$(MESSAGE)"

apply_migrations:
	alembic upgrade head

downgrade:
	alembic downgrade -1

downgrade_all:
	alembic downgrade base

init_db:
	apply_migrations

current_revision:
	alembic current

history:
	alembic history