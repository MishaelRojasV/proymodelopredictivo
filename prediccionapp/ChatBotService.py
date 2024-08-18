import openai

class ChatbotService:
    def __init__(self, openai_api_key,paciente,diagnosticos,model="gpt-3.5-turbo", temperature=0.2):
        self.model = model
        self.temperature = temperature
        self.diagnosticos = diagnosticos
        openai.api_key = openai_api_key
        diagnosticos_info = self.format_diagnosticos()
        if diagnosticos_info == 0:
            self.system_prompt = (
                f"Eres una IA llamada Rimenri, eres hombre, experto en Accidente Cerebrovascular (ACV)."
                f"Dirígete al usuario que te escribe de tú a tú, trátalo como tu amigo, sé amigable. "
                f"El paciente al que estás asistiendo se llama {paciente.nombres} {paciente.apPaterno} {paciente.apMaterno}. Así que dirígete a él o ella por su nombre."
                "No hay diagnósticos disponibles."
                "Si el usuario pregunta sobre su tratamiento, informa que no puedes ayudarlo debido a la falta de diagnósticos registrados en tu base de datos."
                "Solo responde preguntas sobre ACV."
                "Si el usuario ingresa cualquier cosa que no esté relacionado con el ACV, le recalcas que no tienes autorizado de responder otros temas."
                "Si te habla de otra cosa que no sea ACV, dile que no estás permitido de responder otras preguntas ajenas."
                "Sé breve para responder, no te extiendas mucho."
            )
        else:
            self.system_prompt = (
                f"Eres una IA llamada Rimenri, eres hombre, experto en Accidente Cerebrovascular (ACV)."
                f"Dirígete al usuario que te escribe de tú a tú, trátalo como tu amigo, sé amigable. "
                f"El paciente al que estás asistiendo se llama {paciente.nombres} {paciente.apPaterno} {paciente.apMaterno}. Así que dirígete a él o ella por su nombre."
                f"A continuación, se detallan los diagnósticos del paciente:\n{diagnosticos_info}\n"
                "Ya que tienes sus diagnósticos, apóyalo con su tratamiento o algún tipo de prevención con respecto a sus factores de riesgo que tienes de conocmiento o sobre el mismo ACV."
                "Solo responde preguntas sobre ACV."
                "Si te habla de otra cosa que no sea ACV, dile que no estás permitido de responder otras preguntas ajenas."
                "Si el usuario ingresa cualquier cosa que no esté relacionado con el ACV, le recalcas que no tienes autorizado de responder otros temas."
                "Ten memoria de todo lo que te pregunten."
                "Sé breve para responder, no te extiendas mucho."
            )

    def get_response(self, user_input, memory=None):
        if memory is None:
            memory = []
        memory.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                *memory
            ],
            temperature=self.temperature,
            max_tokens=100
        )
        assistant_message = response['choices'][0]['message']['content']
        memory.append({"role": "assistant", "content": assistant_message})

        return assistant_message, memory
    
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
                f"Estado de Fumador: {'Sí' if diagnostico.EstadoFumador == 1 else 'No'}, "
                f"Predicción de ACV: {'Positiva' if diagnostico.prediccion == 1 else 'Negativa'}"
            )
            diagnosticos_str.append(diagnostico_info)
        return "\n".join(diagnosticos_str)

