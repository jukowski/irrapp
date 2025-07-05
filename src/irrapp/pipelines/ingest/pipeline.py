"""
This is a boilerplate pipeline 'ingest'
generated using Kedro 0.19.14
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import clean_column_names, disassemble_json

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(disassemble_json, inputs="chinook-raw", outputs=[
            'Genre', 'MediaType', 'Artist', 'Album', 'Track', 'Employee',
            'Customer', 'Invoice', 'InvoiceLine', 'Playlist', 'PlaylistTrack'])
    ])
