""" 
The reason why we need to settup some stuff related to Clerk is because Clerk is going to handle all of the authentication and authorization for us in the frontend.
So we need to create a Clerk instance that we can use to make requests to the Clerk API.
 """
from clerk_backend_api import Clerk
from app.core.config import settings

clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)