Custom main App settings
========================

You can set the environment variables to customize the main app settings before import charmy.

.. code-block:: python

   from os import environ

Disable auto create main app
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don`t want to create the main app automatically,
you can set the environment variable "AUTO_CREATE_MAIN_APP" to "False".

.. code-block:: python

   environ["AUTO_CREATE_MAIN_APP"] = "False"

   import charmy as cm

   app = cm.App(id_=cm.MAINAPP_ID)

   ...

   app.mainloop()

Switch UI framework
^^^^^^^^^^^^^^^^^^^

If you want to switch the ui framework,
you can set the environment variable "UI_FRAMEWORK" to "GLFW" or ...

.. code-block:: python

   environ["UI_FRAMEWORK"] = "GLFW"
