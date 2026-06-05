from app.models.membership import UserRole
from app.schemas.base import CamelBase, CamelOrmSchema


class CreateOrUpdateMembershipDto(CamelBase):
    user_id: str
    role: UserRole = UserRole.REGULAR


class MemberResponse(CamelBase):
    """GET /members — user info + role (built manually from Membership + User)."""
    id: str
    first_name: str
    last_name: str
    email: str
    role: UserRole


class MembershipUpsertResponse(CamelOrmSchema):
    """POST /members/create-or-update — matches Node.js shape."""
    user_id: str
    gallery_id: str
    role: UserRole


class MembershipResponse(CamelOrmSchema):
    id: str
    user_id: str
    gallery_id: str
    role: UserRole
