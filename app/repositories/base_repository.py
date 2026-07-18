from typing import Any, Dict, List, Optional
from bson import ObjectId
from pymongo.collection import Collection

class BaseRepository:
    def __init__(self, collection: Collection):
        self.collection = collection
    
    def _serialize_document(self, document: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Convert MongoDB ObjectId into string
        """
        if document is None:
            return None
        serialized_document = document.copy()
        serialized_document["_id"] = str(serialized_document["_id"])
        return serialized_document
    
    def create(self, document: Dict[str, Any]) -> str:
        """
        Insert a new document into the collection
        Args:
            document: Dictionary containing the document data.
        Returns:
            The inserted document ID as a string
        """
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
    
    def find_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a document by its MongoDB ObjectId.
        Args:
            document_id: The document ID as a string.
        
        Returns:
            The matching document if found, otherwise None.
        """
        if not ObjectId.is_valid(document_id):
            return None
        document = self.collection.find_one({"_id": self._object_id(document_id)})
        return self._serialize_document(document)
    
    def find_one(self, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a single document matching the given filters.
        """
        document = self.collection.find_one(filters)
        return self._serialize_document(document)
    
    def find_many(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find all documents matching the given filters.
        """
        documents = self.collection.find(filters)
        return [
            self._serialize_document(document)
            for document in documents
        ]
    
    def update_one(self, filters: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Update a single document.
        """
        result  = self.collection.update_one(filters, {"$set": update_data})
        return result.modified_count
    
    def delete_one(self, filters: Dict[str, Any]) -> int:
        """
        Delete a single document.
        """
        result = self.collection.delete_one(filters)
        return result.deleted_count
    
    def _object_id(self, document_id: str):
        """
        Convert a string ID to a MongoDB ObjectId.
        """
        return ObjectId(document_id)