import ollama
import whisper
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

questions = {
    "EI": [
        "Você gosta de participar de eventos sociais com muitas pessoas?",
        "Você prefere passar tempo sozinho ou com um pequeno grupo de amigos próximos?",
        "Você se sente energizado quando interage com outras pessoas?",
        "Você costuma evitar grandes encontros e prefere atividades mais solitárias?"
    ],
    "SN": [
        "Você se concentra mais em fatos e detalhes do que em teorias ou ideias?",
        "Você prefere pensar no quadro geral e em conceitos abstratos, ao invés de se ater aos detalhes?",
        "Você confia mais em suas observações diretas do que em suas intuições?",
        "Você gosta de explorar possibilidades futuras em vez de se focar no que é concreto e tangível?"
    ],
    "TF": [
        "Você toma decisões com base na lógica e consistência, em vez de nas emoções pessoais?",
        "Você prioriza seus sentimentos e valores pessoais ao tomar decisões?",
        "Você acredita que as decisões devem ser objetivas e baseadas em fatos?",
        "Você tende a considerar como as decisões afetarão as pessoas ao seu redor?"
    ],
    "JP": [
        "Você prefere ter um plano e segui-lo rigorosamente?",
        "Você gosta de manter suas opções em aberto e ser flexível?",
        "Você se sente mais confortável quando tem um cronograma ou uma lista de tarefas?",
        "Você prefere reagir às circunstâncias à medida que elas surgem, em vez de planejar com antecedência?"
    ]
}

scores = {
    "EI": 0,  # Extroversão (E) vs. Introversão (I)
    "SN": 0,  # Sensação (S) vs. Intuição (N)
    "TF": 0,  # Pensamento (T) vs. Sentimento (F)
    "JP": 0   # Julgamento (J) vs. Percepção (P)
}

# Administramos o teste, e iteramos por cada categoria de perguntas.
for dimension, dimension_questions in questions.items():
    print(f"Responda as seguintes perguntas para {dimension}:")
    for i, question in enumerate(dimension_questions):
        print(f"Q{i+1}: {question} (1-5)")
        response = int(input("Avalie sua concordância em uma escala de 1 (Discordo Fortemente) a 5 (Concordo Fortemente): "))

        if response >= 4: 
            if i % 2 == 0: # basicamente, perguntas de numero par reforçam um perfil (extroversão)
                scores[dimension] += 1
            else:          # e perguntas de numero impar reforçam o anti-perfil (introversão)
                scores[dimension] -= 1

# calcular os percentuais, fonte: 16personalities
results = {
    "Extroversão (E)": max(0, scores["EI"] / len(questions["EI"]) * 100),
    "Introversão (I)": max(0, (-scores["EI"]) / len(questions["EI"]) * 100),
    "Sensação (S)": max(0, scores["SN"] / len(questions["SN"]) * 100),
    "Intuição (N)": max(0, (-scores["SN"]) / len(questions["SN"]) * 100),
    "Pensamento (T)": max(0, scores["TF"] / len(questions["TF"]) * 100),
    "Sentimento (F)": max(0, (-scores["TF"]) / len(questions["TF"]) * 100),
    "Julgamento (J)": max(0, scores["JP"] / len(questions["JP"]) * 100),
    "Percepção (P)": max(0, (-scores["JP"]) / len(questions["JP"]) * 100)
}

# mostrar o resultado em percentuais
print("\nResultados do MBTI (em percentuais):")
for trait, percentage in results.items():
    print(f"{trait}: {percentage:.2f}%")

mbti_profile = ", ".join([f"{trait}: {percentage:.2f}%" for trait, percentage in results.items()])
'''prompt = f"Analise o seguinte perfil MBTI com base nos percentuais: {mbti_profile}. Forneça insights sobre os traços de personalidade."

stream = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
)

print("\nAnálise Ollama do Perfil MBTI:")
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
'''

model = whisper.load_model("base") 
result = model.transcribe("C:/Users/PoderosoVitao/Downloads/UNSORTED/impossivel.mp3") # Depende de onde o úsuario enviou.
transcribed_text = result["text"]
#print("\nTranscricao: ", transcribed_text)

stream = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': ("Analise o sentimento do seguinte texto: " + transcribed_text)}],
    stream=True,
)

#print("\nAnálise de Sentimento:")
sentiment_analysis = ""
for chunk in stream:
    sentiment_analysis += chunk['message']['content']
#print(sentiment_analysis)

final_prompt = f"""
Forneça uma breve análise do perfil cultural do candidato com base nos seguintes resultados:

1. Perfil MBTI (percentuais):
{mbti_profile}

2. Transcrição da Entrevista:
{transcribed_text}

3. Análise de Sentimento:
{sentiment_analysis}

Leve em conta o perfil comportamental e o tom utilizado durante a entrevista para fornecer insights sobre o estilo de trabalho e adaptação cultural deste candidato.
"""

stream = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': final_prompt}],
    stream=True,
)

# Análise do perfil cultural. Ultima etapa da fase 2.
print("\nAnálise Final do Perfil Cultural:")

mensagemFinal = ""

for chunk in stream:
    mensagemFinal += chunk['message']['content']

# Agora basta passar a mensagemFinal para o recrutador, ou implementar uma heuristica para dar uma nota a essa avaliação.