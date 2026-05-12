import os

filepath = "/home/th3622/colloquy-2/stable-audio-tools/stable_audio_tools/interface/interfaces/diffusion_cond.py"

with open(filepath, "r") as f:
    lines = f.readlines()

# Find the start of create_diffusion_cond_ui block
start_line = -1
for i, line in enumerate(lines):
    if "with gr.Blocks(js=js, theme=gr.themes.Base()) as ui:" in line:
        start_line = i
        break

if start_line == -1:
    print("Could not find start line")
    exit(1)

# New content for the block
new_block = [
    '    with gr.Blocks(js=js, theme=gr.themes.Base()) as ui:\n',
    '        if gradio_title:\n',
    '            gr.Markdown("### %s" % gradio_title)\n',
    '        \n',
    '        with gr.Tab("Generation"):\n',
    '            create_sampling_ui(model_config) \n',
    '        \n',
    '        with gr.Tab("Dual Gen & Collection"):\n',
    '            with gr.Row():\n',
    '                with gr.Column(scale=6):\n',
    '                    dual_prompt_a = gr.Textbox(label="Prompt A (e.g. Neck Pickup)", placeholder="electric guitar neck pickup")\n',
    '                    dual_prompt_b = gr.Textbox(label="Prompt B (e.g. Bridge Pickup)", placeholder="electric guitar bridge pickup")\n',
    '                    dual_negative_prompt = gr.Textbox(label="Negative Prompt", placeholder="")\n',
    '                dual_generate_button = gr.Button("Generate Pair", variant=\'primary\', scale=1)\n',
    '\n',
    '            with gr.Row():\n',
    '                with gr.Column():\n',
    '                    gr.Markdown("### Result A")\n',
    '                    dual_audio_a = gr.Audio(label="Audio A", interactive=False)\n',
    '                    dual_spec_a = gr.Image(label="Spectrogram A", interactive=False)\n',
    '                    save_a_button = gr.Button("Add A to Collection")\n',
    '\n',
    '                with gr.Column():\n',
    '                    gr.Markdown("### Result B")\n',
    '                    dual_audio_b = gr.Audio(label="Audio B", interactive=False)\n',
    '                    dual_spec_b = gr.Image(label="Spectrogram B", interactive=False)\n',
    '                    save_b_button = gr.Button("Add B to Collection")\n',
    '\n',
    '            with gr.Accordion("Shared Parameters", open=False):\n',
    '                with gr.Row():\n',
    '                    dual_steps = gr.Slider(minimum=1, maximum=500, step=1, value=100, label="Steps")\n',
    '                    dual_cfg = gr.Slider(minimum=0.0, maximum=25.0, step=0.1, value=7.0, label="CFG scale")\n',
    '                    dual_seed = gr.Textbox(label="Seed (-1 for random)", value="-1")\n',
    '                \n',
    '                with gr.Row():\n',
    '                    dual_seconds_total = gr.Slider(minimum=0, maximum=512, step=1, value=30, label="Seconds total")\n',
    '                    dual_sampler = gr.Dropdown(["dpmpp-2m-sde", "dpmpp-3m-sde", "k-heun", "k-lms", "k-dpmpp-2s-ancestral"], label="Sampler type", value="dpmpp-3m-sde")\n',
    '\n',
    '            gr.Markdown("---")\n',
    '            gr.Markdown("## Audio Collection")\n',
    '            collection_files = gr.File(label="Saved Generations", value=get_collection_files, file_count="multiple", interactive=False)\n',
    '            with gr.Row():\n',
    '                refresh_collection_button = gr.Button("Refresh Collection")\n',
    '                clear_collection_button = gr.Button("Clear Collection", variant="stop")\n',
    '\n',
    '            # Dual generation click\n',
    '            dual_generate_button.click(\n',
    '                fn=generate_pair,\n',
    '                inputs=[\n',
    '                    dual_prompt_a, dual_prompt_b, dual_negative_prompt,\n',
    '                    gr.State(0), dual_seconds_total, dual_cfg, dual_steps,\n',
    '                    gr.State(None), dual_seed, dual_sampler\n',
    '                ],\n',
    '                outputs=[dual_audio_a, dual_spec_a, dual_audio_b, dual_spec_b, dual_seed]\n',
    '            )\n',
    '\n',
    '            # Collection actions\n',
    '            save_a_button.click(fn=add_to_collection, inputs=[dual_audio_a], outputs=[collection_files])\n',
    '            save_b_button.click(fn=add_to_collection, inputs=[dual_audio_b], outputs=[collection_files])\n',
    '            refresh_collection_button.click(fn=get_collection_files, outputs=[collection_files])\n',
    '            clear_collection_button.click(fn=clear_collection, outputs=[collection_files])\n',
    '\n',
    '    return ui\n'
]

# Find the end of the ui block (the 'return ui' line)
end_line = -1
for i in range(start_line, len(lines)):
    if "return ui" in lines[i]:
        end_line = i
        break

if end_line == -1:
    print("Could not find end line")
    exit(1)

# Replace the block
new_lines = lines[:start_line] + new_block + lines[end_line+1:]

with open(filepath, "w") as f:
    f.writelines(new_lines)

print("Successfully updated diffusion_cond.py")
