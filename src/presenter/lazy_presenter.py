class LazyPresenter:
    def __init__(self, presenter_class, *args, **kwargs):
        self.presenter_class = presenter_class
        self.args = args
        self.kwargs = kwargs
        self._instance = None

    def __getattr__(self, name):
        if self._instance is None:
            self._instance = self.presenter_class(*self.args, **self.kwargs)
        return getattr(self._instance, name)
