from backend.ingestion.embedder import embed_chunks, embed_single

sample_chunks = [
    "Ethics is about right and wrong behaviour.",
    "Cisco generated $46 billion in sales revenue.",
    "Moral philosophy deals with questions of right conduct."
]

embeddings = embed_chunks(sample_chunks)

print(f"Number of chunks embedded: {len(embeddings)}")
print(f"Vector size per chunk: {len(embeddings[0])}")
print(f"First 5 numbers of chunk 1: {embeddings[0][:5]}")
print(f"First 5 numbers of chunk 3: {embeddings[2][:5]}")