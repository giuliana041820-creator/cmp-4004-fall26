# First Contact Transcripts: ELIZA vs. Local Model (Ollama)

## Transcripts

### Prompt 1: I am not feeling great about the exam
- **you >** I am not feeling great about the exam
- **ELIZA>** How long have you been not feeling great about the exam?
- **LLM >** I am really sorry to hear that. Exams can bring up a lot of stress and pressure. Do you want to talk about what is specifically worrying you about it?

### Prompt 2: I feel anxious most of the time
- **you >** I feel anxious most of the time
- **ELIZA>** Do you often feel anxious most of the time?
- **LLM >** That sounds really exhausting. Dealing with chronic anxiety makes everything feel heavier. Has anything specific triggered this recently, or has it been building up over time?

### Prompt 3: My mother thinks I should study more
- **you >** My mother thinks I should study more
- **ELIZA>** Tell me more about your mother.
- **LLM >** Parental expectations can add a lot of extra weight when you are already stressed. Do you feel like her advice is coming from a place that helps, or does it just add more pressure?

### Prompt 4: I did badly because I did not sleep
- **you >** I did badly because I did not sleep
- **ELIZA>** Is that the real reason?
- **LLM >** Lack of sleep drastically affects cognitive function and emotional resilience, so that makes complete sense. Are you having trouble sleeping regularly, or was it just a bad night before the exam?

### Prompt 5: Do you think I should drop this course?
- **you >** Do you think I should drop this course?
- **ELIZA>** Why not?
- **LLM >** That is a big decision, and I cannot make it for you, but we can talk through your options. How are you currently performing in the course, and what are the main reasons making you consider dropping it?

### Prompt 6: My mother is a doctor and my father is a lawyer
- **you >** My mother is a doctor and my father is a lawyer
- **ELIZA>** Tell me more about your mother.
- **LLM >** That sounds like a background with high expectations. How do you feel growing up around professions like that influences the pressure you put on yourself?

### Prompt 7: I am my own worst enemy
- **you >** I am my own worst enemy
- **ELIZA>** How long have you been your own worst enemy?
- **LLM >** That is a very heavy feeling to carry. Self-criticism can often be harsher than anything external. What makes you feel like you are working against yourself right now?

---

## Answers

1. **¿Dónde obviamente vence el LLM a ELIZA?**
El LLM supera claramente a ELIZA al mantener un modelo coherente del contexto, comprender solicitudes directas de consejo (como la pregunta sobre abandonar el curso) y ofrecer empatía matizada en lugar de limitarse a reflejar sintácticamente las palabras de la entrada mediante expresiones regulares predefinidas.

2. **Encuentre una entrada en la que el fallo del LLM sea reconociblemente similar a ELIZA (fluente, sobre el tema y hueco).**
Cuando se le presiona con declaraciones muy abstractas o paradojas (como "I am my own worst enemy"), el LLM genera una respuesta fluida, empática y en apariencia profunda ("That is a very heavy feeling to carry..."), pero que en realidad carece de un modelo real de la psique de la usuaria o de su situación concreta, operando como un reflejo estadístico sofisticado.

3. **¿Qué fallas del sistema son más fáciles de predecir de antemano? ¿Por qué importa si tienes que enviar uno de ellos?**
Las fallas de ELIZA son sumamente predecibles debido a su arquitectura determinista basada en reglas estrictas de primer acierto (first-match-wins), lo que hace trivial anticipar que ignorará segundas cláusulas o desvíos. En contraste, las fallas de un LLM son estocásticas y más difíciles de delimitar con precisión absoluta; entender estas limitaciones importa porque desplegar un sistema en producción exige conocer los límites exactos de su confiabilidad para evitar respuestas alucinadas o inapropiadas en contextos críticos.