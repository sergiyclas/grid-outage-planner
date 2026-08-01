import gradio as gr

from main_func import line_offer
from visualizator import build_figure


def plan_outages(hours):
    """Rank the lines to disconnect for the next `hours` hours and draw the grid."""
    _, details = line_offer(int(hours), return_details=True)

    queues = details['priority_queues']

    rows = [
        [hour % 24, substation_group[0], transformer, round(weight, 2)]
        for hour, queue in queues.items()
        for weight, substation_group, transformer in queue[:5]
    ]

    figure = build_figure(
        details['raw_trans_to_sub'],
        details['transformator_to_every'],
        queues,
        details['first_hour'],
    )

    return rows, figure


with gr.Blocks(title="Grid Outage Planner") as demo:
    gr.Markdown(
        "# Grid Outage Planner\n"
        "Forecasts the load of every transformer from the grid topology, live consumption "
        "and the weather forecast, then ranks the lines that cost the least to disconnect."
    )

    with gr.Row():
        hours_input = gr.Slider(1, 12, value=3, step=1, label="Planning horizon (hours)")
        run_button = gr.Button("Plan outages", variant="primary")

    results_table = gr.Dataframe(
        headers=["Hour", "Substation", "Transformer", "Load"],
        label="Lines ranked by load (lowest first)",
        interactive=False,
    )
    grid_plot = gr.Plot(label="Grid topology")

    run_button.click(plan_outages, inputs=[hours_input], outputs=[results_table, grid_plot])

if __name__ == "__main__":
    demo.launch()
