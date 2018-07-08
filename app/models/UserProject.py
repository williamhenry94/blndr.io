from app.database import ora as db 
from orator import SoftDeletes

class UserProject(db.Model):

    __dates__ = ["deleted_at", "created_at", "updated_at"]

    __fillable__ = ["user_id", 'project_id']

    __table__ = "user_projects"

    # __primary_key__ = "user_id"