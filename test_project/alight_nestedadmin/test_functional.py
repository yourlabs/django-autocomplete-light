import json
import time

from dal.test import case, stories
from dal_alight.test import AlightStory

from .models import TModelOne


class AdminNestedLinkedDataTest(AlightStory,
                                case.AdminMixin,
                                case.OptionMixin,
                                case.AutocompleteTestCase):
    field_name = 'test'
    model = TModelOne

    def setUp(self):
        super(AdminNestedLinkedDataTest, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()

    def test_linked_value_is_forwarded_for_nested_admin(self):
        script = """
(function(XHR) {
    "use strict";

    var open = XHR.prototype.open;
    XHR.prototype.open = function(method, url, async, user, pass) {
        window.forward_val = new URL(
            window.location + url).searchParams.get("forward");
        open.call(this, method, url, async, user, pass);
      };
})(XMLHttpRequest);
            """

        self.browser.execute_script(script)

        story = stories.SelectOption(self)
        story.toggle_autocomplete()

        # The component debounces requests by 200ms; wait for the XHR to fire.
        forward_val = None
        tries = 30
        while tries and not forward_val:
            time.sleep(0.1)
            forward_val = self.browser.evaluate_script('window.forward_val')
            tries -= 1

        forward = json.loads(forward_val)
        self.assertEqual(forward, {'level_one': 'one', 'level_two': 'two'})
