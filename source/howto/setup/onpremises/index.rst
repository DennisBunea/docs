.. meta::
    :description: How to manually deploy Valohai resources in your on-premise environment

.. _onpremises:


Deploy on-premise
#################

.. warning::

    Valohai agents can be installed on a on-premises machines running Linux, preferably Ubuntu 20.04.

The Compute and Data Layer of Valohai can be deployed to your on-premise environment. This enables you to:

* Use your own on-premises machines to run machine learning jobs.
* Use your own cloud storage for storing training artefacts, like trained models, preprocessed datasets, visualizations, etc.
* Mount local data to your on-premises workers.
* Access databases and date warehouses directly from the workers, which are inside your network.

Valohai doesn't have direct access to the on-premises machine that executes the machine learning jobs. Instead it communicates with a separate static virtual machine in your on-premise environment that's responsible for storing the job queue, job states, and short-term logs.

.. image:: /_images/valohai_environment.png
    :width: 700
    :alt: Valohai Components


Installing the Valohai worker
-----------------------------

The Valohai agent (Peon) is responsible for fetching new jobs, writing logs, and updating the job states for Valohai.

You'll need to have ``Python 3.6+`` installed on the machines by default. The ``peon-bringup`` (bup) will install other dependencies, like ``docker`` and if needed ``nvidia-docker``.

.. warning::

    Before running the template you'll need the following information from Valohai:

    * ``name`` the queue name that this on-premises machine will use.
    * ``queue-address`` will be assigned for the queue in your subscription.
    * ``redis-password`` that your queue uses. This is usually stored in your cloud providers Secret Manager.
    * ``url`` download URL for the Valohai worker agent.

.. code-block:: bash

    sudo su
    apt-get update -y && apt-get install -y python3 python3-distutils
    
    TEMPDIR=$(mktemp -d)
    pushd $TEMPDIR

    export NAME=<queue-name>
    export QUEUE_ADDRESS=<queue-address>
    export PASSWORD=<redis-password>
    export URL=<bup-url>

    curl $URL --output bup.pex
    chmod u+x bup.pex
    env "CLOUD=none" "ALLOW_MOUNTS=true" "INSTALLATION_TYPE=private-worker" "REDIS_URL=rediss://:$PASSWORD@$QUEUE_ADDRESS:63790"  "QUEUES=$NAME" ./bup.pex

    popd

Frequently Asked Questions
--------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :stub-columns: 1

   * - Question
     - Answer
   * - Can I run multiple jobs in parallel on the same on-premise machine?
     - Yes. You can add ``SINGLE_GPU_PER_PEON=true`` in the peon configuration file (``/etc/peon.config``) to Valohai to run multiple jobs in parallel. Each job will have access to one GPU and will take up as much memory/CPU as it needs.
   * - Can I define per execution how many GPUs I want to use?
     - No. The ``SINGLE_GPU_PER_PEON`` inside ``/etc/peon.config`` defines if Valohai will always use all the GPUs for a job, or run one job per GPU.
   * - I have just one GPU on my machine. Can I run multiple jobs on the same GPU?
     - Yes. You'll need to udpate your the peon service file.
      
       * Rename ``/etc/systemd/system/peon.service`` to ``/etc/systemd/system/peon@.service``
       * Run ``systemctl daemon-reload`` read the new service file
       * Enable multiple peons:
       
         * ``systemctl enable --now peon@1``
         * ``systemctl enable --now peon@2``
         * ``systemctl enable --now peon@3``

