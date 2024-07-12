import gradio as gr
import httpx


class GradioUI:
    def __init__(self):
        self.api_url = "http://localhost:8000/upload"

    def upload_and_process_file(self, file):
        try:
            with open(file.name, "rb") as f:
                files = {'file': (file.name, f, 'multipart/form-data')}
                data = {'bucket_name': 'your-bucket-name'}

                response = httpx.post(self.api_url, files=files, data=data)

            if response.status_code == 200:
                response_data = response.json()
                task_id = response_data.get("task_id")
                return "Upload and processing completed successfully.", task_id
            else:
                return f"Error: {response.status_code} - {response.text}", None
        except Exception as e:
            return f"Error: {str(e)}", None

    def download(self, task_id: int):
        response = httpx.get(f"{self.api_url}/download/{task_id}")
        if response.status_code == 200:
            with open(f"downloaded_{task_id}.txt", "wb") as f:
                f.write(response.content)
            return f"Downloaded file for task {task_id} as downloaded_{task_id}.txt"
        else:
            return f"Error: {response.status_code} - {response.text}"

    def launch_interface(self):
        with gr.Blocks() as interface:
            task_id_state = gr.State()

            upload_button = gr.File(label="Upload File")
            submit_button = gr.Button("Submit")
            download_button = gr.Button(label="Download Result")

            upload_result = gr.Textbox(label="Upload Result")
            download_result = gr.Textbox(label="Download Result")

            submit_button.click(
                fn=self.upload_and_process_file,
                inputs=[upload_button],
                outputs=[upload_result, task_id_state]
            )

            download_button.click(
                fn=self.download,
                inputs=[task_id_state],
                outputs=download_result
            )

        interface.launch()


if __name__ == "__main__":
    ui = GradioUI()
    ui.launch_interface()