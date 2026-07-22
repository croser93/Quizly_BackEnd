from google import genai


def gemini():
    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input="say hello world"
    )
    print(interaction.output_text)