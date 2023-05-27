{{ fullname | escape | underline}}

{{ dir({{ fullname }}) }}

.. automodule:: {{ fullname }}

   {% block attributes %}
   .. rubric:: Module Attributes

   {% for item in attributes %}
   .. autoattribute:: {{ fullname }}.{{ item }}
   {%- endfor %}
   {% endblock %}

   {% block classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :nosignatures:
      :toctree:
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endblock %}

   {% block functions %}
   .. rubric:: {{ _('Functions') }}

   {% for item in functions %}
   .. autofunction:: {{ item }}
   {%- endfor %}
   {% endblock %}

   {% block exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::
      :nosignatures:
      :toctree:
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endblock %}
