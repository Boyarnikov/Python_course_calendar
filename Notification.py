import csv

class NotificationManager:
    file_notify = 'backend_data_notification.csv'
    
    def __init__(self):
        self._notifications = []
        
    def get_notifications(self):
        return self._notifications

    def notification_add_part(self, organizer, added_user, remove_user, events):
        self._notifications.append({"Organizer": organizer.get_id(), "AddedUser": added_user.get_id(),"RemoveUser": None, "Events": events})

    def notification_remove_part(self, organizer,added_user, remove_user, events):
        self._notifications.append({"Organizer": organizer.get_id(),"AddedUser": None, "RemoveUser": remove_user.get_id(), "Events": events})
        
    def save_notifications(self):
        with open(self.file_notify, 'w', newline='') as file:
            fieldnames = ['Organizer', 'AddedUser', 'RemoveUser', 'Events']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for notification in self._notifications:
                writer.writerow(notification)

    def load_notifications(self):
        try:
            with open(self.file_notify, 'r', newline='') as file:
                reader = csv.DictReader(file)
                self._notifications = [row for row in reader]
        except FileNotFoundError:
            self._notifications = []
 
    def notify_added_to_event(self, organizer, added_user, remove_user,  event):
        event_title = event.get_title()
        self.notification_add_part(organizer, added_user, remove_user, [event_title])
    
    def notify_remove_from_event(self, organizer, added_user, remove_user, event):
        event_title = event.get_title()
        self.notification_remove_part(organizer, added_user, remove_user, [event_title])
    
    def remove_notifications(self, user_id):
        self._notifications = [notification for notification in self._notifications if
                               notification.get('AddedUser') != user_id and notification.get('RemoveUser') != user_id]
        
    
    