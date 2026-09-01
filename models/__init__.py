"""
NAGARAM — Models Package
Import all models so SQLAlchemy can discover them.
"""
from app.models.user import User, Role
from app.models.profile import (
    CitizenProfile, FarmerProfile, ExpertProfile,
    NGOProfile, VolunteerProfile
)
from app.models.issue import (
    Issue, IssueCategory, IssueUpdate,
    IssueAssignment, IssueComment, IssueImage
)
from app.models.notification import Notification
from app.models.farm import (
    Farm, Crop, SoilRecord, HarvestRecord,
    FarmDocument, FarmInput
)
from app.models.market import MarketPrice, BuyerListing, TransportListing
from app.models.scheme import GovernmentScheme
from app.models.consultation import Consultation

__all__ = [
    'User', 'Role',
    'CitizenProfile', 'FarmerProfile', 'ExpertProfile',
    'NGOProfile', 'VolunteerProfile',
    'Issue', 'IssueCategory', 'IssueUpdate',
    'IssueAssignment', 'IssueComment', 'IssueImage',
    'Notification',
    'Farm', 'Crop', 'SoilRecord', 'HarvestRecord',
    'FarmDocument', 'FarmInput',
    'MarketPrice', 'BuyerListing', 'TransportListing',
    'GovernmentScheme',
    'Consultation',
]
