class FormMixin(object):
    def get_errors(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key, error_dicts in errors.items():
                messages = []
                for error_dict in error_dicts:
                    message = error_dict.get('message')
                    messages.append(message)
                new_errors[key] = messages
            return new_errors
        else:
            return {}