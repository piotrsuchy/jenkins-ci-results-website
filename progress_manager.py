class ProgressManager:
    def __init__(self):
        self._progress_state = {}
        
    def update_progress(self, setup_id, data):
        completed_tests = data.get('completed_tests', 0)
        total_tests = data.get('total_tests', 0)
        self._progress_state[setup_id] = f"{completed_tests}/{total_tests}"
        
    def get_progress_state(self):
        return self._progress_state
