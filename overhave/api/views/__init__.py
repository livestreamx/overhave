# flake8: noqa
from .auth_views import login_for_access_token
from .emulation_views import emulation_run_list_handler
from .extra_views import docs, favicon
from .feature_type_views import feature_types_list_handler
from .feature_views import get_features_handler
from .tags_views import tags_item_handler, tags_list_handler
from .testrun_views import get_test_run_handler, run_tests_by_tag_handler
from .testuser_views import (
    delete_testuser_handler,
    get_testuser_handler,
    testuser_get_spec_handler,
    testuser_list_handler,
    testuser_put_spec_handler,
)
