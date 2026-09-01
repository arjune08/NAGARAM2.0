"""
NAGARAM — Issue Management Models
Unified issue tracking for civic and agricultural problems.
"""
from datetime import datetime, timezone
from app.extensions import db


class IssueCategory(db.Model):
    """Categories for issues (civic and agricultural)."""
    __tablename__ = 'issue_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    issue_type = db.Column(db.String(20), nullable=False)  # 'civic' or 'agricultural'
    description = db.Column(db.String(300))
    icon = db.Column(db.String(50))  # Icon identifier
    is_active = db.Column(db.Boolean, default=True)

    @classmethod
    def seed_default_categories(cls):
        """Seed default civic and agricultural categories."""
        civic_cats = [
            ('Roads & Potholes', 'Road damage, potholes, missing signs'),
            ('Sanitation & Garbage', 'Uncollected garbage, overflowing bins'),
            ('Water Supply', 'Pipe leaks, water shortage, dirty water'),
            ('Drainage & Sewage', 'Blocked drains, sewage overflow'),
            ('Street Lighting', 'Non-functional streetlights'),
            ('Public Parks', 'Park maintenance, broken equipment'),
            ('Stray Animals', 'Stray cattle or animal nuisance'),
            ('Encroachment', 'Illegal construction or road blockage'),
        ]
        agri_cats = [
            ('Pest Attack', 'Insect infestation, pest damage'),
            ('Crop Disease', 'Fungal, bacterial, or viral plant disease'),
            ('Soil Health', 'Soil degradation, nutrient deficiency'),
            ('Water & Irrigation', 'Irrigation scarcity, canal breach'),
            ('Weather Impact', 'Hail, flood, drought damage'),
            ('Fertilizer Issue', 'Supply shortage, adulteration'),
            ('Seed Quality', 'Poor germination, fake seeds'),
            ('Market Access', 'Transport issue, price exploitation'),
        ]

        created = []
        for name, desc in civic_cats:
            cat = cls.query.filter_by(name=name, issue_type='civic').first()
            if not cat:
                cat = cls(name=name, issue_type='civic', description=desc)
                db.session.add(cat)
                created.append(cat)

        for name, desc in agri_cats:
            cat = cls.query.filter_by(name=name, issue_type='agricultural').first()
            if not cat:
                cat = cls(name=name, issue_type='agricultural', description=desc)
                db.session.add(cat)
                created.append(cat)

        db.session.commit()
        return created

    def __repr__(self):
        return f'<IssueCategory {self.name} ({self.issue_type})>'


class Issue(db.Model):
    """Unified issue model for civic and agricultural problems."""
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    # Format: NG-XXXX (civic) or AG-XXXX (agricultural)

    issue_type = db.Column(db.String(20), nullable=False, index=True)  # 'civic' or 'agricultural'
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('issue_categories.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reporter_type = db.Column(db.String(20), nullable=False)  # citizen, farmer

    # Location
    location = db.Column(db.String(300))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Status & Priority
    status = db.Column(db.String(30), default='Submitted', nullable=False, index=True)
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High, Critical

    # Assignment
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id],
                                  backref='assigned_issues')

    # Agricultural-specific
    crop_name = db.Column(db.String(100))
    affected_area = db.Column(db.Float)  # Acres
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'))

    # Resolution
    resolution = db.Column(db.Text)
    resolved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_by = db.relationship('User', foreign_keys=[resolved_by_id])

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    resolved_at = db.Column(db.DateTime)

    # Relationships
    updates = db.relationship('IssueUpdate', backref='issue', lazy='dynamic',
                              order_by='IssueUpdate.created_at.desc()')
    assignments = db.relationship('IssueAssignment', backref='issue', lazy='dynamic')
    comments = db.relationship('IssueComment', backref='issue', lazy='dynamic',
                               order_by='IssueComment.created_at')
    images = db.relationship('IssueImage', backref='issue', lazy='dynamic')

    # Valid statuses
    STATUSES = [
        'Submitted', 'Under Review', 'Assigned', 'In Progress',
        'Waiting for Information', 'Resolved', 'Closed'
    ]
    PRIORITIES = ['Low', 'Medium', 'High', 'Critical']

    def __repr__(self):
        return f'<Issue {self.issue_id}: {self.title[:40]}>'


class IssueUpdate(db.Model):
    """Status updates and activity log for issues."""
    __tablename__ = 'issue_updates'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')

    old_status = db.Column(db.String(30))
    new_status = db.Column(db.String(30))
    message = db.Column(db.Text)
    update_type = db.Column(db.String(30), default='status_change')
    # status_change, comment, assignment, resolution, escalation

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<IssueUpdate issue={self.issue_id} {self.update_type}>'


class IssueAssignment(db.Model):
    """Track issue assignments to users/organizations."""
    __tablename__ = 'issue_assignments'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])
    assigned_by = db.relationship('User', foreign_keys=[assigned_by_id])
    role_type = db.Column(db.String(20))  # expert, ngo, volunteer
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<IssueAssignment issue={self.issue_id} to={self.assigned_to_id}>'


class IssueComment(db.Model):
    """Comments/discussion on issues."""
    __tablename__ = 'issue_comments'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')
    content = db.Column(db.Text, nullable=False)
    is_internal = db.Column(db.Boolean, default=False)  # Admin/expert only
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<IssueComment issue={self.issue_id} by={self.user_id}>'


class IssueImage(db.Model):
    """Images/evidence attached to issues."""
    __tablename__ = 'issue_images'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    original_filename = db.Column(db.String(300))
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    caption = db.Column(db.String(300))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploaded_by = db.relationship('User')
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<IssueImage {self.filename}>'
