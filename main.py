import appointment_database as appdb
import llm_service
from nicegui import ui
import json

messages = []
username = "User"
llm=llm_service.LLMService()

@ui.page('/')
def chat_page():
    ui.label("THIS IS NOT A REAL CLINIC!").classes("w-full max-w-3xl mx-auto flex-grow text-2xl font-bold text-red-600")
    ui.label("This is a demo of an ai based chat system.").classes("w-full max-w-3xl mx-auto flex-grow text-lg text-gray-700 mb-4")

    async def send_message():
        api_url = input_box_url.value
        api_key = input_box_key.value
        text = input_box.value.strip()
        username = input_box_username.value.strip() or "User"
        
        if not text:
            return

        messages.append((username, text))
        refresh_chat()

        answer = await ask_llm(api_url, api_key, messages)

        messages.append(("assistant", answer))
        refresh_chat()

    def _parse_json(response):

        try:
            # Attempt to parse the response as JSON
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            # If parsing fails, return an empty dictionary
            return {}

    async def ask_llm(api_url, api_key, messages):
        prompt = messages[-1][1] + "\n\nIf he is making an appointment with date and time, please return a JSON object with the following format. IMPORTANT: JSON Output Format Required. You MUST respond with ONLY a valid JSON object (no markdown, no extra text). The JSON must strictly follow this schema:: {\"phone\": \"123-456-7890\", \"doctor\": \"Dr. Someone\", \"date\": \"YYYY-MM-DD\", \"time\": \"HH:MM:SS\"}. If not, return an empty JSON object: {}."
        response = await llm(
            api_key=api_key,
            base_url=api_url,
            prompt=prompt,
            temperature=0.8,
            max_tokens=2000
        )
        print(f"LLM response: {response}")  # Debugging line to print the raw response

        if(response):
            # Parse JSON
            result = _parse_json(response)
            print(result)  # Debugging line to print the parsed result
            print(messages[-1][0])  # Debugging line to print the last message's role
            if result and all(key in result for key in ["phone", "doctor", "date", "time"]) and messages[-1][0] != "User":
                # If the result is not empty, create an appointment
                appointment_id = appdb.create_appointment(
                    patient_name=messages[-1][0],
                    phone=result.get("phone", ""),
                    doctor=result.get("doctor", ""),
                    appointment_time=f"{result.get('date', '')} {result.get('time', '')}"
                )
                return f"Appointment created with ID: {appointment_id}. \n\nLast message: {messages[-1][1]}. This is a simulated response from the AI."

        return f"Error: Failed to create appointment. Last message: {messages[-1][1]}. This is a simulated response from the AI."

    def refresh_chat():
        chat.clear()

        with chat:
            for role, text in messages:
                if role == "assistant":
                    ui.chat_message(
                        text,
                        name="AI"
                    )
                else:
                    ui.chat_message(
                        text,
                        name=username,
                        sent=True
                    )


    chat = ui.column().classes(
        "w-full max-w-3xl mx-auto flex-grow"
    )

    ui.label("AI chatbot URL").classes("w-full max-w-3xl mx-auto")
    input_box_url = ui.input().classes("w-full max-w-3xl mx-auto").props("autofocus")

    ui.label("AI chatbot key").classes("w-full max-w-3xl mx-auto")
    input_box_key = ui.input().classes("w-full max-w-3xl mx-auto")

    with ui.row().classes(
        "w-full max-w-3xl mx-auto"
    ):
        ui.label("Username").classes("w-1/6")
        input_box_username = ui.input().classes("w-1/6").props("placeholder=User").on("input", lambda e: setattr(username, 'value', e.args['value']))

    with ui.row().classes(
        "w-full max-w-3xl mx-auto"
    ):
        input_box = ui.textarea(
            placeholder="Chat here..."
        ).classes("flex-grow").props("autofocus")

        input_box.on(
            'keydown',
            lambda e: send_message() if (
                e.args['key'] == 'Enter'
                and not e.args.get('shiftKey', False)
            ) else None
        )

        ui.button(
            "send",
            on_click=send_message
        )

    ui.link("Staff only", "/admin")

@ui.page('/admin')
def admin_page():

    def postpone_appointment(appointment_id):
        appdb.postpone_appointment(appointment_id)
        ui.navigate.reload()

    def delete_appointment(appointment_id):
        appdb.delete_appointment(appointment_id)
        ui.navigate.reload()

    ui.label('Appointment Management').classes('text-2xl font-bold mb-4')
    appointments = appdb.get_appointments()

    for appointment in appointments:
        print(appointment)  # Debugging line to print each appointment
        with ui.row():
            ui.label(
                f"{appointment['doctor']} "
                f"{appointment['appointment_time']} "
                f"{appointment['patient_name']}"
            )

            ui.button(
                'Delay 1 hour',
                on_click=lambda a=appointment:
                    postpone_appointment(a['id'])
            )

            ui.button(
                'Delete',
                on_click=lambda a=appointment:
                    delete_appointment(a['id'])
            )
    ui.button('Return to Chat', on_click=lambda: ui.navigate.to('/'))
appdb.init_db()
ui.run()