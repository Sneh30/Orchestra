import json
from pathlib import Path
from typing import Annotated

import typer

from research_orchestrator.evaluation.metrics import aggregate_evaluation

app = typer.Typer(help="Evaluate generated research reports.")


@app.command()
def report(
    report_path: Annotated[Path, typer.Argument(help="Path to a JSON report payload.")],
) -> None:
    payload = json.loads(report_path.read_text())
    results = aggregate_evaluation(payload)
    typer.echo(
        json.dumps(
            [{"metric": item.metric, "score": item.score, "details": item.details} for item in results],
            indent=2,
        )
    )


if __name__ == "__main__":
    app()

