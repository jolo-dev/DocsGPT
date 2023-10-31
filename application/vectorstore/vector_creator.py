from application.vectorstore.faiss import FaissStore
from application.vectorstore.elasticsearch import ElasticsearchStore
from application.vectorstore.s3_bucket_store import S3BucketStore


class VectorCreator:
    vectorstores = {
        'faiss': FaissStore,
        'elasticsearch':ElasticsearchStore,
        's3': S3BucketStore
    }

    @classmethod
    def create_vectorstore(cls, type, *args, **kwargs):
        vectorstore_class = cls.vectorstores.get(type.lower())
        if not vectorstore_class:
            raise ValueError(f"No vectorstore class found for type {type}")
        return vectorstore_class(*args, **kwargs)