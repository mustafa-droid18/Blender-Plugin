bl_info = {
    "name": "Niloom AI Script Assistant",
    "author": "Your Name",
    "version": (2, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > NiloomAI",
    "description": "Queries Hugging Face LLM and previews generated bpy scripts",
    "category": "3D View",
}

import bpy
import requests
import re

HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN"  # Replace with your Hugging Face token
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
processing_llm = False

def query_llm(prompt: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": f"Write only valid bpy Python code for: {prompt}",
        "parameters": {
            "max_new_tokens": 1024,
            "temperature": 0.7
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    if isinstance(result, list) and 'generated_text' in result[0]:
        return result[0]['generated_text']
    elif isinstance(result, dict) and 'generated_text' in result:
        return result['generated_text']
    else:
        return str(result)

def sanitize_script(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"```(python)?", "", raw)
    raw = raw.replace("```", "")

    lines = raw.splitlines()
    capturing = False
    code_lines = []

    for line in lines:
        line = line.strip()

        if "import bpy" in line or "bpy." in line:
            capturing = True

        if capturing:
            if line.lower().startswith("explanation") or line.lower().startswith("note"):
                break
            if line and not line.startswith("*"):
                code_lines.append(line)

    return "\n".join(code_lines).strip()

class NiloomProperties(bpy.types.PropertyGroup):
    user_prompt: bpy.props.StringProperty(
        name="Prompt",
        description="Describe what you want Blender to do",
        default=""
    )

class NILOOM_OT_GenerateScript(bpy.types.Operator):
    bl_idname = "niloom.generate_script"
    bl_label = "Query and Preview Script"

    def execute(self, context):
        global processing_llm
        if processing_llm:
            self.report({'WARNING'}, "Still querying, please wait.")
            return {'CANCELLED'}

        props = context.scene.niloom_props
        prompt = props.user_prompt.strip()
        if not prompt:
            self.report({'ERROR'}, "Prompt is empty.")
            return {'CANCELLED'}

        processing_llm = True
        try:
            self.report({'INFO'}, "Querying Hugging Face...")
            raw = query_llm(prompt)

            print("=== RAW LLM RESPONSE ===")
            print(raw)
            print("========================")

            script = sanitize_script(raw)

            if not script:
                self.report({'ERROR'}, "LLM returned no usable code.")
                return {'CANCELLED'}

            # Show in Blender Text Editor
            text_name = "NiloomGeneratedScript"
            if text_name in bpy.data.texts:
                bpy.data.texts[text_name].clear()
            else:
                bpy.data.texts.new(text_name)
            bpy.data.texts[text_name].write(script)

            self.report({'INFO'}, f"Script previewed in Text Editor: {text_name}")

        except Exception as e:
            self.report({'ERROR'}, f"Query failed: {e}")
        finally:
            processing_llm = False

        return {'FINISHED'}

class NILOOM_PT_MainPanel(bpy.types.Panel):
    bl_label = "Niloom AI"
    bl_idname = "NILOOM_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NiloomAI"

    def draw(self, context):
        layout = self.layout
        props = context.scene.niloom_props
        layout.prop(props, "user_prompt")
        layout.operator("niloom.generate_script", text="Generate Script")

classes = [NiloomProperties, NILOOM_OT_GenerateScript, NILOOM_PT_MainPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.niloom_props = bpy.props.PointerProperty(type=NiloomProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.niloom_props

if __name__ == "__main__":
    register()
