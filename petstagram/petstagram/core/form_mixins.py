class DisabledFormMixin:
    disabled_fields = ()
    fields = None

    def _disable_fields(self):
        for field_name in self.disabled_fields:
            if field_name in self.fields:
                field = self.fields[field_name]
                # field.widget.attrs['disabled'] = 'disabled'
                field.widget.attrs['readonly'] = 'readonly'
