import click
from app import create_app, db
from app.models import User


@click.group()
def cli():
    pass


@click.command()
def createsuperuser():
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)

    admin = User(username=username, password=password, is_admin=True)

    app = create_app()
    with app.app_context():
        try:
            db.session.add(admin)
            db.session.commit()
            click.echo('Superuser created successfully.')
        except Exception as e:
            db.session.rollback()
            click.echo(f"Error creating superuser: {e}")


cli.add_command(createsuperuser)

if __name__ == '__main__':
    cli()
