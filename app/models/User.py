from app.database import ora as db 
from orator import SoftDeletes
from orator.orm import belongs_to_many
from app.models.UserProject import UserProject
from app.models.Project import Project
class User(SoftDeletes, db.Model):

    __dates__ = ["deleted_at", "created_at", "updated_at"]

    __fillable__ = ["id", 'name', 'email', "username", "access_token", "refresh_token","github_id", 'avatar_url','github_api_url','github_html_url']

    __table__ = "users"


    @belongs_to_many('user_projects', 'user_id', 'project_id')
    def projects(self):
        return Project
