from rest_framework.exceptions import ValidationError


class ValidatedUrl:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        curr_val = dict(value).get(self.field)
        if 'youtube.com' not in curr_val:
            raise ValidationError('Ссылки могут быть только на youtube.com')
