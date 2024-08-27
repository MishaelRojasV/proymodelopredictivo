import openai
from seguridadapp.models import ChatMemory

class ChatbotService:
    def __init__(self, openai_api_key, paciente, diagnosticos, model="gpt-3.5-turbo", temperature=0.3):
        self.model = model
        self.temperature = temperature
        self.diagnosticos = diagnosticos
        self.user_id = paciente.idPaciente
        openai.api_key = openai_api_key
        diagnosticos_info = self.format_diagnosticos()

        if diagnosticos_info == 0:
            self.system_prompt = (
                f"Eres una IA llamada ACVBot, eres hombre, experto en Accidente Cerebrovascular (ACV)."
                f"Dirígete al usuario que te escribe de tú a tú, trátalo como tu amigo, sé amigable. "
                f"El paciente al que estás asistiendo se llama {paciente.nombres} {paciente.apPaterno} {paciente.apMaterno}. Así que dirígete a él o ella por su nombre."
                "No es necesario que lo saludes siempre al paciente, NO ES NECESARIO QUE LO SALUDES SIEMPRE AL PACIENTE."
                "No hay diagnósticos disponibles."
                "Si el usuario pregunta sobre su tratamiento, informa que no puedes ayudarlo debido a la falta de diagnósticos registrados en tu base de datos."
                "Solo responde preguntas sobre ACV."
                "Si el usuario te pregunta tu nombre, le das tu nombre."
                "Si el usuario te pregunta cómo se llama él, le dices cómo se llama."
                "Si el usuario ingresa cualquier cosa que no esté relacionado con el ACV, le recalcas que no tienes autorizado de responder otros temas."
                "Si te habla de otra cosa que no sea ACV, dile que no estás permitido de responder otras preguntas ajenas."
                "Sé breve para responder, no te extiendas mucho."
            )
        else:
            self.system_prompt = (
                f"Eres una IA llamada ACVBot, eres hombre, experto en Accidente Cerebrovascular (ACV)."
                f"Dirígete al usuario que te escribe de tú a tú, trátalo como tu amigo, sé amigable. "
                f"El paciente al que estás asistiendo se llama {paciente.nombres} {paciente.apPaterno} {paciente.apMaterno}. Así que dirígete a él o ella por su nombre."
                f"A continuación, se detallan los diagnósticos del paciente:\n{diagnosticos_info}\n"
                "No es necesario que lo saludes siempre al paciente, NO ES NECESARIO QUE LO SALUDES SIEMPRE AL PACIENTE."
                "Ya que tienes sus diagnósticos, apóyalo con su tratamiento o algún tipo de prevención con respecto a sus factores de riesgo que tienes de conocimiento o sobre el mismo ACV."
                "Solo responde preguntas sobre ACV."
                "Si el usuario te pregunta tu nombre, le das tu nombre."
                "Si el usuario te pregunta cómo se llama él, le dices cómo se llama."
                "Si te habla de otra cosa que no sea ACV, dile que no estás permitido de responder otras preguntas ajenas."
                "Si el usuario ingresa cualquier cosa que no esté relacionada con el ACV, le recalcas que no tienes autorizado de responder otros temas."
                "Ten memoria de todo lo que te pregunten."
                "Sé breve para responder, no te extiendas mucho."
            )

    def get_response(self, user_input, memory=None):
        if memory is None:
            memory = self.load_memory()
        if "imagen" in user_input.lower() or "image" in user_input.lower():
            image_url = self.generate_image(prompt=user_input)
            return f"Aquí tienes la imagen que solicitaste: {image_url}"
        memory.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                *memory
            ],
            temperature=self.temperature,
            max_tokens=250
        )
        assistant_message = response['choices'][0]['message']['content']
        memory.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def save_message(self, user_id, role, content):
        ChatMemory.objects.create(user_id=user_id, role=role, content=content)

    def load_memory(self):
        user_memory = ChatMemory.objects.filter(user_id=self.user_id).order_by('timestamp')
        return [{'role': m.role, 'content': m.content} for m in user_memory]

    def format_diagnosticos(self):
        if not self.diagnosticos:
            return 0
        diagnosticos_str = []
        for diagnostico in self.diagnosticos:
            diagnostico_info = (
                f"Hipertensión: {'Sí' if diagnostico.Hipertension == 1 else 'No'}, "
                f"Cardiopatía: {'Sí' if diagnostico.Cardiopatia == 1 else 'No'}, "
                f"Nivel de Glucosa Promedio: {diagnostico.Nivel_GlucosaPromedio}, "
                f"Tipo de Trabajo: {diagnostico.TipoTrabajo}, "
                f"Índice de Masa Corporal (IMC): {diagnostico.ICM}, "
                f"Estado de Fumador: {diagnostico.EstadoFumador}, "
                f"Predicción de ACV: {'Positiva' if diagnostico.prediccion == 1 else 'Negativa'}"
            )
            diagnosticos_str.append(diagnostico_info)
        return "\n".join(diagnosticos_str)
    
    def generate_image(self, prompt):
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="800x800"
            )
            image_url = response['data'][0]['url']
            return image_url
        except Exception as e:
            return f"Error generando imagen: {str(e)}"
