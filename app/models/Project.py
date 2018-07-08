from app.database import ora as db 
from orator import SoftDeletes

class Project(SoftDeletes, db.Model):

    __dates__ = ["deleted_at", "created_at", "updated_at"]

    __fillable__ = ["id", 'project_name', 'project_description', "owner_id", "repo_id", "repo_name", "repo_full_name","private"]

    __table__ = "projects"
