from pydantic import BaseModel
from app.models.membership import UserRole

class CreateOrUpdateMembershipDto(BaseModel):
    user_id: str
    role: UserRole = UserRole.REGULAR

class MembershipResponse(BaseModel):
    id: str
    user_id: str
    gallery_id: str
    role: UserRole
    
    model_config = {"from_attributes": True}