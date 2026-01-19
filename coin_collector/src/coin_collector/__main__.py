import typer
from .game import run_game

app = typer.Typer()

@app.command()
def main(
    level: str = typer.Option("src/coin_collector/levels/level_example.json", help="Pfad zum Level"),
    fps: int = 60,
    debug: bool = False
):
    run_game(level, fps, debug)

if __name__ == "__main__":
    app()
