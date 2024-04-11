from langchain_community.document_loaders import PyPDFLoader
import tiktoken

loader = PyPDFLoader("./files/Achieving agility and quality in product development.pdf")
pages = loader.load()

print(len(pages))

tokenizer = tiktoken.get_encoding('cl100k_base')
def tiktoken_len(text):
    tokens = tokenizer.encode(
    text,
    disallowed_special=()
)
    return len(tokens)

tiktoken.encoding_for_model('gpt-3.5-turbo')

# create the length function
def get_token_count():
    token_counts = []
    for page in pages:
        token_counts.append(tiktoken_len(page.page_content))
    min_token_count = min(token_counts)
    avg_token_count = int(sum(token_counts) / len(token_counts))
    max_token_count = max(token_counts)

    # print token counts
    print(f"Min: {min_token_count}")
    print(f"Avg: {avg_token_count}")
    print(f"Max: {max_token_count}")