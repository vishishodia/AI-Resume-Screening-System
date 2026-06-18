from sentence_transformers import SentenceTransformer

print("loading Model..")

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence = "Python developer"

embedding = model.encode(sentence)

print(type(embedding))
print(f"embedding length: {len(embedding)}")
print("\nfirst 10 values...")
print(embedding[:10])


