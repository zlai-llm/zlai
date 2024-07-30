import sys
import click
from streamlit.web import cli as stcli


@click.command()
@click.option('--port', default="8501", type=str, help='Port to run the server on')
def run_streamlit_app(
    port: str = "8501",
):
    """"""
    sys.argv = ["streamlit", "run", "./zlai/streamlit/web/app.py", f"--server.port={port}"]
    sys.exit(stcli.main())


if __name__ == '__main__':
    run_streamlit_app()
