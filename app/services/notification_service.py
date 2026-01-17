from app import db
from app.models import Notification

class NotificationService:
    @staticmethod
    def create_notification(user_id, title, message, notification_type):
        """Create a new notification for a user"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark a notification as read"""
        notification = Notification.query.filter_by(
            id=notification_id, user_id=user_id).first()
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for a user"""
        return Notification.query.filter_by(
            user_id=user_id, is_read=False).count()
    
    @staticmethod
    def get_user_notifications(user_id, limit=20):
        """Get recent notifications for a user"""
        return Notification.query.filter_by(user_id=user_id)\
            .order_by(Notification.created_at.desc())\
            .limit(limit).all()