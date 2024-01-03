from typing import Any

from overhave.admin.views.base import ModelViewConfigured


class FeatureInWorkView(ModelViewConfigured):
    """View for :class:`FeatureView` table."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
