from typing import Any, Dict, List, Optional
from bson import ObjectId
from pymongo.collection import Collection
from decimal import Decimal
from bson.decimal128 import Decimal128

class BaseRepository:
    def __init__(self, collection: Collection):
        self.collection = collection
    
    def _serialize_document(self, document: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Convert MongoDB-specific types into Python types.
        """
        if document is None:
            return None
        serialized_document = self._convert_from_storage(document)
        serialized_document["_id"] = str(serialized_document["_id"])
        return serialized_document
    
    def _convert_from_storage(self, value: Any) -> Any:
        """
        Recursively convert MongoDB types into Python types.
        """
        if isinstance(value, Decimal128):
            return value.to_decimal()
        
        if isinstance(value, dict):
            return {
                key: self._convert_from_storage(val)
                for key, val in value.items()
            }
        
        if isinstance(value, list):
            return [
                self._convert_from_storage(item)
                for item in value
            ]
        return value
    
    def create(self, document: Dict[str, Any]) -> str:
        """
        Insert a new document into the collection
        Args:
            document: Dictionary containing the document data.
        Returns:
            The inserted document ID as a string
        """
        prepared_document = self._prepare_document_for_storage(document)
        result = self.collection.insert_one(prepared_document)
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
        prepared_update = self._prepare_document_for_storage(update_data)
        result  = self.collection.update_one(filters, {"$set": prepared_update})
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
    
    def _prepare_document_for_storage(self, value: Any) -> Any:
        """
        Recursively convert Python types into MongoDB-compatible types
        """
        if isinstance(value, Decimal):
            return Decimal128(value)
        if isinstance(value, dict):
            return {
                key: self._prepare_document_for_storage(val)
                for key, val in value.items()
            }
        if isinstance(value, list):
            return [
                self._prepare_document_for_storage(item)
                for item in value
            ]

        return value