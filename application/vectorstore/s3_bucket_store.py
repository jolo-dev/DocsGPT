import logging
import os
import dotenv
from langchain.vectorstores import FAISS
from application.vectorstore.base import BaseVectorStore
from application.core.settings import settings
from langchain.document_loaders import S3DirectoryLoader
from application.aws.boto import init

logger = logging.getLogger(__name__)

dotenv.load_dotenv()

bucket = os.getenv("S3_BUCKET_NAME")
if not bucket:
    raise Exception("S3_BUCKET_NAME not set")

init()

class S3BucketStore(BaseVectorStore):

    def __init__(self, path, embeddings_key, docs_init=None):
        super().__init__()
        self.path = path
        embeddings = self._get_embeddings(settings.EMBEDDINGS_NAME, embeddings_key)

        loader = S3DirectoryLoader(bucket)
        documents = loader.load()

        if docs_init:
            self.docsearch = FAISS.from_documents(
                docs_init, embeddings
            )
        else:
            self.docsearch = FAISS.load(
                self.path, embeddings
            )
        self.assert_embedding_dimensions(embeddings)
