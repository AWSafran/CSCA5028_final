import datetime

class LoggingService:
    def __init__(self, logging_collection):
        self.logging_collection = logging_collection

    def log_info(self, requested_date, message):
        base_log = self.build_base(requested_date)
        base_log['type'] = 'info'
        base_log['message'] = message

        self.logging_collection.insert_one(base_log)

    def log_error(self, requested_date, exception):
        base_log = self.build_base(requested_date)
        base_log['type'] = 'error'
        base_log['exception'] = repr(exception)

        self.logging_collection.insert_one(base_log)

    def log_handled_error(self, requested_date, message):
        base_log = self.build_base(requested_date)
        base_log['type'] = 'handled_error'
        base_log['message'] = message

        self.logging_collection.insert_one(base_log)


    def build_base(self, requested_date):
        return {
            'requested_date': requested_date,
            'timestamp': datetime.datetime.now().isoformat(),
            'application': 'rest_api'
        }