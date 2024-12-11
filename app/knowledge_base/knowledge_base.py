import chromadb

class Knowledge_Base():
    def __init__(self, db_path="knowledge_db/"):
        self.db_path = db_path
        self.client = chromadb.Client(chromadb.PersistentClientSettings(path=self.db_path))

    def get_collection(self, collection_name="company_knowledge_base"):
        collection = self.client.get_collection(collection_name)
        return collection # ChromaDB collection object.
    
    def create_collection(self, collection_name="company_knowledge_base"):
        collection = self.client.get_or_create_collection(name=collection_name)
        return collection # ChromaDB collection object.

    def add_to_collection(self, collection, documents):
        '''documnets format: {"document_id":"document text"}
        '''
        if not isinstance(documents, dict):
                raise ValueError("Documents must be a dictionary with format {'document_id': 'document text'}.")
        
        collection.add(
            documents=list(documents.values()),
            ids=list(documents.keys())
        )

    def query(self, collection, query_texts, n_results=2):
        results = collection.query(query_texts=[query], n_results=n_results)
        retrieved_context = " ".join([doc for doc in results["documents"]])
        return retrieved_context


'''
knowledge_base = Knowledge_Base(db_path="my_knowledge_db/")
context =knowledge_base.query(collection=knowledge_base.get_collection("company_knowledge_base"), query_texts="What are the main departments in the company ?")

# setup vector db
client = chromadb.Client()
collection = client.get_or_create_collection("company_knowledge_base")
# Setup Vector DB (ChromaDB) for Context Retrieval
# Assume the collection is already populated with relevant documents

# Add documents to the collection if its not populated
collection.add(
    documents=[
        "Berlin is the capital of Germany.",
        "Paris is the capital of France.",
        "Rome is the capital of Italy."
    ],
    metadatas=[
        {"source": "european_cities"},
        {"source": "european_cities"},
        {"source": "european_cities"}
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Step 2: Define a Retrieval Function
def retrieve_context(question):
    # Use the vector database to find relevant documents
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    # Combine retrieved documents into a single context
    context = " ".join([doc for doc in results["documents"]])
    return context


client = chromadb.Client(chromadb.PersistentClientSettings(
    path="knowledge_base/vector_db"
))
collection = client.get_or_create_collection("knowledge_base")

'''