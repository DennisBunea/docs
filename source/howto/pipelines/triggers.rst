.. meta::
    :description: What are Valohai pipelines? They allow you to standardize how your machine learning project is ran.

.. _pipeline-triggers:

Schedule pipelines
################################

Valohai triggers allow you to launch a copy of an existing pipeline on a time-based trigger. For example, running a pipeline weekly on Mondays at 09:00.

.. note::

    You can create a trigger after you've ran at least one succesfully completed pipeline.
    You can either schedule a specific (commit) version of a pipeline to run or schedule a pipeline run that always uses the latest version of the pipeline.

..

1. Go to project settings
2. Navigate to the Triggers tab
3. Set your trigger title (e.g. Daily retraining, every 4 hours)
4. Select Scheduled (Cron) as the condition, as click Add
5. Open the condition and set the schedule you want.
  ●	You can either use one of the options or select Custom
  ●	For example a custom value: 0 0/4 * * 1-7 would run the pipeline every 4 hours on every day of the week.
6. On the Actions column select the right action and click Add
   ● Copy Pipeline reruns always the same pipeline version
     ● Select the Source Pipeline that you want to run
   ●Run Pipeline runs a pipeline with whatever is the newest version fetched to Valohai
     ●Source Commit Reference, could be for example main to always run with the latest pipeline from your main branch
     ●Pipeline Name is the name of the pipeline in your valohai.yaml
     ●Pipeline Title is the title used in the UI and API results
7. Click on Create trigger


.. warning::

    Note that all times are expressed in UTC time.

..

.. image:: /_images/pipeline-trigger.png
    :alt: Create a pipeline trigger

..

.. admonition:: Name your pipelines
    :class: tip

    Open the Pipelines tab and name your pipeline by editing the pipeline title. This will make it easier to find the right pipeline when setting up the triggers.

..
