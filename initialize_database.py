from app.config.init_db import create_collections, create_indexes
print("Initializing Database...")
create_collections()
create_indexes()
print("Database Initialization completed successfully")