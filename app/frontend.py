import gradio as gr
import requests
import pandas as pd
import json

REQUEST_URL = 'http://127.0.0.1:8000/items/'


def byte_to_json(response):
    decoded_string = response.content.decode('utf-8')
    return json.loads(decoded_string)


def gradio_interface():
    def create(name, description):
        # TODO: Create an item, 
        item = {"name": name, "description": description}
        
        # Send POST request to create the item
        response = requests.post(REQUEST_URL, json=item)
        
        # Handle response errors
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.reason}"
        
        return byte_to_json(response), update_table()

    def read(item_id):
        # TODO: Get an item given its id,
        response = requests.get(f"{REQUEST_URL}{item_id}")
        return byte_to_json(response)

    def update(item_id, name, description):
        # TODO: Update an item's name and description given its id, 
        item = {"name": name, "description": description}
        response = requests.put(f"{REQUEST_URL}{item_id}", json=item)
        return byte_to_json(response), update_table()

    def delete(item_id):
        # TODO: Delete an item given its id,
        response = requests.delete(f"{REQUEST_URL}{item_id}")
        return byte_to_json(response), update_table()

    def update_table():
        # TODO: Get all items in the database,
        response = requests.get(REQUEST_URL)
        items = byte_to_json(response)

        if isinstance(items, dict):  # If single item, convert to list of one item
            items = [items]

        if not items:  # In case the response is empty
            items = []

        return pd.DataFrame(items)

    with gr.Blocks() as app:
        gr.Markdown("### CRUD Application")
        table_output = gr.DataFrame(label="Current Items", interactive=False, 
                                    value=update_table(), height=200, 
                                    wrap=True, column_widths=['20%','30%','50%'])

        # Use as reference for TODO tasks below
        with gr.Tab("Create Item"):
            name = gr.Textbox(label="Name")
            description = gr.Textbox(label="Description")
            create_btn = gr.Button("Create")
            output = gr.Textbox(label="Output", interactive=False)
            create_btn.click(
                create, inputs=[name, description], outputs=[output, table_output])

        with gr.Tab("Read Item"):
            # TODO: Given a valid item id as input, 
            item_id = gr.Textbox(label="Item ID")
            read_btn = gr.Button("Read")
            output = gr.Textbox(label="Output", interactive=False)
            read_btn.click(read, inputs=[item_id], outputs=[output])

        with gr.Tab("Update Item"):
            # TODO: Given a valid item id, new name, and new description as input,
            item_id = gr.Textbox(label="Item ID")
            name = gr.Textbox(label="New Name")
            description = gr.Textbox(label="New Description")
            update_btn = gr.Button("Update")
            output = gr.Textbox(label="Output", interactive=False)
            update_btn.click(update, inputs=[item_id, name, description], outputs=[output, table_output])

        with gr.Tab("Delete Item"):
            # TODO: Given a valid item id as input,
            item_id = gr.Textbox(label="Item ID")
            delete_btn = gr.Button("Delete")
            output = gr.Textbox(label="Output", interactive=False)
            delete_btn.click(delete, inputs=[item_id], outputs=[output, table_output])

    return app


gradio_app = gradio_interface()


def start_gradio():
    gradio_app.launch()


if __name__ == "__main__":
    start_gradio()
