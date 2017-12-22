class PanelAreaSetter:
    admin_area = ""

    def dispatch(self, request, *args, **kwargs):
        self.request.admin_area = self.admin_area
        return super().dispatch(request, *args, **kwargs)
