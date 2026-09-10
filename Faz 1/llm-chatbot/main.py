import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()
client = genai.Client()  # GEMINI_API_KEY ortam değişkeninden otomatik okunur

# Alıştırma 5: Test — LLM Çıktısını Değil, Kendi Mantığını Test Et adımı için 
def append_user_message(contents: list[dict], text: str) -> list[dict]:
    return contents + [{"role": "user", "parts": [{"text": text}]}]



"""response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Merhaba, kısaca kendini tanıt.",
    #config=types.GenerateContentConfig(max_output_tokens=150), # max token ayarı
)
print(response.text)

print("finish_reason:", response.candidates[0].finish_reason)"""


# system_instruction ile Davranış Yönlendirme
# içerik üretiminde modelin davranışını yönlendirmek için system_instruction kullanılır.Farkı system_instruction'ı silerek görebilirsin.
""" response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="SSVEP nedir?",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Sen bir nörobilim kavramlarını lise seviyesinde sadeleştiren bir "
            "öğretmensin. Teknik terim kullanma, günlük hayattan örnekle anlat. "
            "Cevapların en fazla 3 cümle olsun."
        ),
        max_output_tokens=3000,
    ),
)
print(response.text) """ 


# Streaming Yanıt


"""Her chunk, o ana kadarki tüm metin değil, 
sadece o parçada üretilen yeni metindir (delta) — 
bu yüzden end="" ile art arda basıyoruz, aksi halde her chunk yeni satıra düşer
flush=True — Python çıktıyı buffer'da bekletmeden 
hemen ekrana basması için (flush olmazsa "streaming" olduğunu göremezsin, 
hepsi birden basılmış gibi görünür)""" 


"""for chunk in client.models.generate_content_stream(
    model="gemini-3.5-flash",
    contents="Nöroplastisite nedir?",
    config=types.GenerateContentConfig(
        system_instruction="Kısa ve öz cevap ver.",
        max_output_tokens=3000,
    ),
):
    print(chunk.text, end="", flush=True)
print()"""


# Konuşma Geçmişi (Hafıza) Yönetimi

MEMORY_ENABLED = True  # True: geçmiş turları hatırlar / False: her tur sıfırdan başlar (hafızasız)

def chat_loop(system_prompt: str = "Kısa ve yardımsever bir asistansın."):
    contents = []

    print("Çıkmak için 'exit' yaz.\n")
    print(f"Hafıza modu: {'AÇIK' if MEMORY_ENABLED else 'KAPALI'}\n")
    while True:
        user_input = input("Sen: ")
        if user_input.strip().lower() == "exit":
            break

        if not MEMORY_ENABLED:
            contents = []  # hafızasız modda önceki turları unut

        contents.append({"role": "user", "parts": [{"text": user_input}]})

        print("Asistan: ", end="")
        full_response_text = ""
        try:
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=3000,
                ),
            ):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response_text += chunk.text
            print()
        except errors.APIError as e:
            print(f"\n[Hata] API isteği başarısız oldu ({e.status}): {e.message}")
            continue  # bu turu hafızaya ekleme, kullanıcı tekrar deneyebilir

        if MEMORY_ENABLED:
            contents.append({"role": "model", "parts": [{"text": full_response_text}]})


BCI_SYSTEM_PROMPT = (
    "Sen SSVEP, P300 ve genel olarak Brain-Computer Interface (BCI) konularında "
    "uzmanlaşmış bir asistansın. Kullanıcı bir BCI/nörobilim terimi veya kavramı "
    "sorduğunda: 1) önce kısa ve teknik olarak doğru bir tanım ver, 2) ardından "
    "günlük hayattan somut bir benzetmeyle sadeleştir. Emin olmadığın veya "
    "tartışmalı olan noktaları açıkça belirt, uydurma bilgi verme. Cevapların en "
    "fazla 4-5 cümle olsun; kullanıcı devamını isterse detaylandır."
)

if __name__ == "__main__":
    chat_loop(BCI_SYSTEM_PROMPT)