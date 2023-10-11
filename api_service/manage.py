# encoding: utf-8

import sqlite3
import click

MAIN_DB_PATH = "./api_service.sqlite3"

@click.group()
def cli():
    pass

@cli.command("init")
def init():
    click.echo("Creating admin user")

    conn = sqlite3.connect(MAIN_DB_PATH)
    cursor = conn.cursor()

    admin_user = ("admin", "admin@mail.com", "admin", True, "ADMIN")
    john_doe_user = ("johndoe", "johndoe@mail.com", "john", True, "USER")

    cursor.execute("INSERT INTO user (username, email, password, active, role) VALUES (?, ?, ?, ?, ?)", admin_user)
    cursor.execute("INSERT INTO user (username, email, password, active, role) VALUES (?, ?, ?, ?, ?)", john_doe_user)

    conn.commit()
    conn.close()

    click.echo("Created users.")

if __name__ == "__main__":
    cli()
