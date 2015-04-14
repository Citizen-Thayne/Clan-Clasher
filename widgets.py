from itertools import chain
from django.forms.utils import flatatt
from django.forms.widgets import Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


# class ButtonDropdownWidget(Select):
#     custom_top = '''
#     <div class="dropdown">
#         <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-expanded="true">
#             {0}
#             <span class="caret"></span>
#         </button>
#     <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">'''
#
#     def render(self, name, value, attrs=None, choices=()):
#         if value is None:
#             value = ''
#         final_attrs = self.build_attrs(attrs, name=name)
#         output = [format_html('<select{0}>', flatatt(final_attrs))]
#         options = self.render_options(choices, [value])
#         if options:
#             output.append(options)
#         output.append('</select>')
#         return mark_safe('\n'.join(output))
#
#     def render_option(self, selected_choices, option_value, option_label):
#         if option_value is None:
#             option_value = ''
#         option_value = force_text(option_value)
#         if option_value in selected_choices:
#             selected_html = mark_safe(' selected="selected"')
#             if not self.allow_multiple_selected:
#                 # Only allow for a single selection.
#                 selected_choices.remove(option_value)
#         else:
#             selected_html = ''
#         return format_html('<option value="{0}"{1}>{2}</option>',
#         return format_html('<li role='presentation' value="{0}"{1}>{2}</option>',
#                            option_value,
#                            selected_html,
#                            force_text(option_label))
#
#     def render_options(self, choices, selected_choices):
#         # Normalize to strings.
#         selected_choices = set(force_text(v) for v in selected_choices)
#         output = []
#         for option_value, option_label in chain(self.choices, choices):
#             if isinstance(option_label, (list, tuple)):
#                 output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
#                 for option in option_label:
#                     output.append(self.render_option(selected_choices, *option))
#                 output.append('</optgroup>')
#             else:
#                 output.append(self.render_option(selected_choices, option_value, option_label))
#         return '\n'.join(output)