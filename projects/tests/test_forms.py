from projects.forms import EditOwnerNickname

from django.test import SimpleTestCase

class EditOwnerNicknameTest(SimpleTestCase):
    def test_edit_owner_nickname_field_label(self):
        form = EditOwnerNickname()
        self.assertTrue(form.fields['nickname'].label is None or form.fields['nickname'].label == 'nickname')

    def test_edit_owner_nickname_is_digit(self):
        form = EditOwnerNickname(data={'nickname': '222'})
        self.assertFalse(form.is_valid())