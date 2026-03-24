def build_context(docs, max_length=3000):
    context = ""
    sources = []

    for i, doc in enumerate(docs):
        chunk = f"[Doc {i}] {str(doc)}"

        if len(context) + len(chunk) > max_length:
            break

        context += chunk + "\n\n"
        sources.append(f"Doc {i}")

    return context, sources