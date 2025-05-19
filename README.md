# Blender AI Script Assistant

The **Blender AI Script Assistant** is a Blender plugin that uses natural language prompts to generate executable Blender Python (`bpy`) scripts. It integrates with Hugging Face's language models to assist users in automating modeling and simulation tasks inside Blender.

## Features

- Accepts natural language input like “Add a red cube” or “Drop cloth on a sphere”
- Queries Hugging Face-hosted LLMs (e.g., Mixtral, OpenChat)
- Sanitizes code output to remove markdown and non-code responses
- Automatically writes generated code into Blender’s Text Editor
- Optional execution for supported scripts
- Includes a base version with fake response logic for offline testing

## Repository Contents

| File | Description |
|------|-------------|
| `blender_ai_plugin.py` | Main plugin that connects to Hugging Face API and queries live LLMs |
| `blender_ai_plugin_base.py` | Offline version with fake LLM response for demo or testing purposes |

## Installation Instructions

1. Open Blender.
2. Go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and select either `blender_ai_plugin.py` or `blender_ai_plugin_base.py`.
4. Enable the add-on via the checkbox.
5. Access the panel via `View3D > Sidebar (N) > BlenderAI`.

## Hugging Face API Setup (for `Blender_ai_plugin.py`)

To use the LLM version:
1. Create a Hugging Face account at https://huggingface.co/join
2. Generate an API token at https://huggingface.co/settings/tokens
3. Replace the value of `HF_TOKEN` in `blender_ai_plugin.py` with your token.

Note: Some models like `Mixtral` may require billing enabled.

## Example Prompt

`Add a sphere and place it at the world origin.`

The plugin will generate:

```python
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
```

## Known Limitations

- LLM responses can include unwanted markdown or explanation text (handled by `sanitize_script()`)
- Some hosted models require payment after limited use
- Plugin assumes user has a Text Editor area open in Blender for code preview

## Future Improvements

- Model switching (free/paid/local options)
- In-panel script editing
- Animation and rigging script generation
- Saving/exporting generated scripts
- Integration with Niloom.ai animation platform

## License

MIT License

## Related

- https://niloom.ai
- https://huggingface.co/docs/transformers/index

## Contributions

Pull requests are welcome. Feel free to open issues for improvements or ideas.
