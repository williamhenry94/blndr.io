from marshmallow import Schema, fields, validate


class Ratings(Schema):
    
   
    rating = fields.Integer(
        validate = [validate.Range(min=1, max=5,
            error="This input must be at least {min} and {max}.")],required=True )
   
    comment = fields.String(
        validate = [validate.Length(min=4,
            error="This input must be at least {min} characters.")],required=True )
    repo_id = fields.Integer(required=True)
    website = fields.URL(required=False )
    application_name = fields.String(validate = [validate.Length(min=3,
            error="This input must be at least {min} characters.")],required=True )
    platform = fields.String(required=True )