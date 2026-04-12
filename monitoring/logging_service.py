import datetime

class LoggingService:
    def __init__(self, logging_collection):
        self.logging_collection = logging_collection

    def log_info(self, fetch_date, message):
        base_log = self.build_base(fetch_date)
        base_log['type'] = 'info'
        base_log['message'] = message

        self.logging_collection.insert_one(base_log)

    def log_error(self, fetch_date, exception):
        base_log = self.build_base(fetch_date)
        base_log['type'] = 'error'
        base_log['exception'] = repr(exception)

        self.logging_collection.insert_one(base_log)

    def build_base(self, fetch_date):
        return {
            'fetch_date': fetch_date,
            'timestamp': datetime.datetime.now().isoformat()
        }