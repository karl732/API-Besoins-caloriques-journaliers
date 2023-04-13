"""Description.

Application ligne de commande pour la librairie du menu alimentaire.
"""
from .data import Donnees

from serde.json import from_json, to_json
import typer
from rich import print