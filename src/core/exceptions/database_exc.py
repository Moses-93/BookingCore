class DatabaseError(Exception):
    """Base class for database errors"""


class DBIntegrityError(DatabaseError):
    """Integrity violation error (uniqueness, foreign key)"""


class DBCreateError(DatabaseError):
    """Error creating a record in the database"""


class DBReadError(DatabaseError):
    """Error reading from the database"""


class DBUpdateError(DatabaseError):
    """Error updating a record in the database"""


class DBDeleteError(DatabaseError):
    """Error deleting a record in the database"""
