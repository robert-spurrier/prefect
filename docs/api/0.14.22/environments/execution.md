---
sidebarDepth: 2
editLink: false
---
# Execution Environments
---
Execution environments encapsulate the logic for where your Flow should execute in Prefect Cloud.

DEPRECATED: Environment based configuration is deprecated, please transition to
configuring `flow.run_config` instead of `flow.environment`. See [Flow configuration](/orchestration/flow_config/overview.html) for more info.
 ## DaskKubernetesEnvironment
 <div class='class-sig' id='prefect-environments-execution-dask-k8s-daskkubernetesenvironment'><p class="prefect-sig">class </p><p class="prefect-class">prefect.environments.execution.dask.k8s.DaskKubernetesEnvironment</p>(min_workers=1, max_workers=2, work_stealing=True, scheduler_logs=False, private_registry=False, docker_secret=None, labels=None, on_start=None, on_exit=None, metadata=None, scheduler_spec_file=None, worker_spec_file=None, image_pull_secret=None, log_k8s_errors=False)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/dask/k8s.py#L19">[source]</a></span></div>

DaskKubernetesEnvironment is an environment which deploys your flow on Kubernetes by spinning up a temporary Dask Cluster (using [dask-kubernetes](https://kubernetes.dask.org/en/latest/)) and running the Prefect `DaskExecutor` on this cluster.

DEPRECATED: Environment based configuration is deprecated, please transition to configuring `flow.run_config` instead of `flow.environment`. See [Flow configuration](/orchestration/flow_config/overview.html) for more info.

When running your flows that are registered with a private container registry, you should either specify the name of an `image_pull_secret` on the flow's `DaskKubernetesEnvironment` or directly set the `imagePullSecrets` on your custom worker/scheduler specs.

It is possible to provide a custom scheduler and worker spec YAML files through the `scheduler_spec_file` and `worker_spec_file` arguments. These specs (if provided) will be used in place of the defaults. Your spec files should be modeled after the job.yaml and worker_pod.yaml found [here](https://github.com/PrefectHQ/prefect/tree/master/src/prefect/environments/execution/dask). The main aspects to be aware of are the `command` and `args` on the container. The following environment variables, required for cloud, do not need to be included––they are automatically added and populated during execution:

- `PREFECT__CLOUD__GRAPHQL` - `PREFECT__CLOUD__AUTH_TOKEN` - `PREFECT__CONTEXT__FLOW_RUN_ID` - `PREFECT__CONTEXT__NAMESPACE` - `PREFECT__CONTEXT__IMAGE` - `PREFECT__CLOUD__USE_LOCAL_SECRETS` - `PREFECT__ENGINE__FLOW_RUNNER__DEFAULT_CLASS` - `PREFECT__ENGINE__TASK_RUNNER__DEFAULT_CLASS` - `PREFECT__ENGINE__EXECUTOR__DEFAULT_CLASS` - `PREFECT__LOGGING__LEVEL` - `PREFECT__CLOUD__SEND_FLOW_RUN_LOGS` - `PREFECT__LOGGING__EXTRA_LOGGERS`

Note: the logging attributes are only populated if they are not already provided.

**Args**:     <ul class="args"><li class="args">`min_workers (int, optional)`: the minimum allowed number of Dask worker pods; defaults to 1     </li><li class="args">`max_workers (int, optional)`: the maximum allowed number of Dask worker pods; defaults to 1     </li><li class="args">`work_stealing (bool, optional)`: toggle Dask Distributed scheduler work stealing;         defaults to False Only used when a custom scheduler spec is not provided. Enabling         this may cause ClientErrors to appear when multiple Dask workers try to run the         same Prefect Task.         `Warning`:  `work_stealing` if provided won't be appended to your custom         `scheduler_spec_file`. If wanted, don't forget to add it in your container env         (`DASK_DISTRIBUTED__SCHEDULER__WORK_STEALING`).     </li><li class="args">`scheduler_logs (bool, optional)`: log all Dask scheduler logs, defaults to False     </li><li class="args">`private_registry (bool, optional, DEPRECATED)`: a boolean specifying whether your         Flow's Docker container will be in a private Docker registry; if so, requires a         Prefect Secret containing your docker credentials to be set.  Defaults to `False`.     </li><li class="args">`docker_secret (str, optional, DEPRECATED)`: the name of the Prefect Secret containing         your Docker credentials; defaults to `"DOCKER_REGISTRY_CREDENTIALS"`.  This Secret         should be a dictionary containing the following keys: `"docker-server"`,         `"docker-username"`, `"docker-password"`, and `"docker-email"`.     </li><li class="args">`labels (List[str], optional)`: a list of labels, which are arbitrary string         identifiers used by Prefect Agents when polling for work     </li><li class="args">`on_start (Callable, optional)`: a function callback which will be called before the         flow begins to run     </li><li class="args">`on_exit (Callable, optional)`: a function callback which will be called after the flow         finishes its run     </li><li class="args">`metadata (dict, optional)`: extra metadata to be set and serialized on this environment     </li><li class="args">`scheduler_spec_file (str, optional)`: Path to a scheduler spec YAML file     </li><li class="args">`worker_spec_file (str, optional)`: Path to a worker spec YAML file     </li><li class="args">`image_pull_secret (str, optional)`: optional name of an `imagePullSecret` to use for         the scheduler and worker pods. To specify multiple image pull secrets, provide a comma         delimited string with no spaces, like `"some-secret,other-secret"`.         For more information go         [here](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).         `Warning`:  `image_pull_secret` if provided won't be appended to your custom         `worker_spec_file` or `scheduler_spec_file`. If you want it, don't forget to add it in         your spec files.     </li><li class="args">`log_k8s_errors (bool, optional)`: optional toggle to also log Kubernetes errors that may occur         using the Prefect logger. Defaults to `False`.</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-environments-execution-dask-k8s-daskkubernetesenvironment-execute'><p class="prefect-class">prefect.environments.execution.dask.k8s.DaskKubernetesEnvironment.execute</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/dask/k8s.py#L196">[source]</a></span></div>
<p class="methods">Create a single Kubernetes job that spins up a dask scheduler, dynamically creates worker pods, and runs the flow.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow object</li></ul> **Raises**:     <ul class="args"><li class="args">`Exception`: if the environment is unable to create the Kubernetes job</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-execution-dask-k8s-daskkubernetesenvironment-run'><p class="prefect-class">prefect.environments.execution.dask.k8s.DaskKubernetesEnvironment.run</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/dask/k8s.py#L287">[source]</a></span></div>
<p class="methods">Run the flow using a temporary dask-kubernetes cluster.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the flow to run.</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-execution-dask-k8s-daskkubernetesenvironment-setup'><p class="prefect-class">prefect.environments.execution.dask.k8s.DaskKubernetesEnvironment.setup</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/dask/k8s.py#L163">[source]</a></span></div>
<p class="methods">Sets up any infrastructure needed for this environment<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow object</li></ul></p>|

---
<br>

 ## DaskCloudProviderEnvironment
 <div class='class-sig' id='prefect-environments-execution-dask-cloud-provider-daskcloudproviderenvironment'><p class="prefect-sig">class </p><p class="prefect-class">prefect.environments.execution.dask.cloud_provider.DaskCloudProviderEnvironment</p>(provider_class, adaptive_min_workers=None, adaptive_max_workers=None, security=None, executor_kwargs=None, labels=None, on_execute=None, on_start=None, on_exit=None, metadata=None, **kwargs)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/dask/cloud_provider.py#L14">[source]</a></span></div>

DaskCloudProviderEnvironment creates Dask clusters using the Dask Cloud Provider project.

DEPRECATED: Environment based configuration is deprecated, please transition to configuring `flow.run_config` instead of `flow.environment`. See [Flow configuration](/orchestration/flow_config/overview.html) for more info.

For each flow run, a new Dask cluster will be dynamically created and the flow will run using a `DaskExecutor` with the Dask scheduler address from the newly created Dask cluster. You can specify the number of Dask workers manually (for example, passing the kwarg `n_workers`) or enable adaptive mode by passing `adaptive_min_workers` and, optionally, `adaptive_max_workers`. This environment aims to provide a very easy path to Dask scalability for users of cloud platforms, like AWS.

**NOTE:** AWS Fargate Task (not Prefect Task) startup time can be slow, depending on docker image size. Total startup time for a Dask scheduler and workers can be several minutes. This environment is a much better fit for production deployments of scheduled Flows where there's little sensitivity to startup time. `DaskCloudProviderEnvironment` is a particularly good fit for automated deployment of Flows in a CI/CD pipeline where the infrastructure for each Flow should be as independent as possible, e.g. each Flow could have its own docker image, dynamically create the Dask cluster to run on, etc. However, for development and interactive testing, creating a Dask cluster manually with Dask Cloud Provider and then using `LocalEnvironment` with a `DaskExecutor` will result in a much better development experience.

(Dask Cloud Provider currently only supports AWS using either Fargate or ECS. Support for AzureML is coming soon.)

*IMPORTANT* By default, Dask Cloud Provider may create a Dask cluster in some environments (e.g. Fargate) that is accessible via a public IP, without any authentication, and configured to NOT encrypt network traffic. Please be conscious of security issues if you test this environment. (Also see pull requests [85](https://github.com/dask/dask-cloudprovider/pull/85) and [91](https://github.com/dask/dask-cloudprovider/pull/91) in the Dask Cloud Provider project.)

**Args**:     <ul class="args"><li class="args">`provider_class (class)`: Class of a provider from the Dask Cloud Provider         projects. Current supported options are `ECSCluster` and `FargateCluster`.     </li><li class="args">`adaptive_min_workers (int, optional)`: Minimum number of workers for adaptive         mode. If this value is None, then adaptive mode will not be used and you         should pass `n_workers` or the appropriate kwarg for the provider class you         are using.     </li><li class="args">`adaptive_max_workers (int, optional)`: Maximum number of workers for adaptive         mode.     </li><li class="args">`security (Type[Security], optional)`: a Dask Security object from         `distributed.security.Security`.  Use this to connect to a Dask cluster that is         enabled with TLS encryption.  For more on using TLS with Dask see         https://distributed.dask.org/en/latest/tls.html     </li><li class="args">`executor_kwargs (dict, optional)`: a dictionary of kwargs to be passed to         the executor; defaults to an empty dictionary     </li><li class="args">`labels (List[str], optional)`: a list of labels, which are arbitrary string         identifiers used by Prefect Agents when polling for work     </li><li class="args">`on_execute (Callable[[Dict[str, Any], Dict[str, Any]], None], optional)`: a function         callback which will be called before the flow begins to run. The callback function         can examine the Flow run parameters and modify  kwargs to be passed to the Dask         Cloud Provider class's constructor prior to launching the Dask cluster for the Flow         run.  This allows for dynamically sizing the cluster based on the Flow run         parameters, e.g.  settings n_workers. The callback function's signature should be:         `on_execute(parameters: Dict[str, Any], provider_kwargs: Dict[str, Any]) -> None`         The callback function may modify provider_kwargs         (e.g.  `provider_kwargs["n_workers"] = 3`) and any relevant changes will be used when         creating the Dask cluster via a Dask Cloud Provider class.     </li><li class="args">`on_start (Callable, optional)`: a function callback which will be called before the         flow begins to run     </li><li class="args">`on_exit (Callable, optional)`: a function callback which will be called after the flow         finishes its run     </li><li class="args">`metadata (dict, optional)`: extra metadata to be set and serialized on this environment     </li><li class="args">`**kwargs (dict, optional)`: additional keyword arguments to pass to boto3 for         `register_task_definition` and `run_task`</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-environments-execution-dask-cloud-provider-daskcloudproviderenvironment-execute'><p class="prefect-class">prefect.environments.execution.dask.cloud_provider.DaskCloudProviderEnvironment.execute</p>(flow, **kwargs)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/dask/cloud_provider.py#L167">[source]</a></span></div>
<p class="methods">Execute a flow run on a dask-cloudprovider cluster.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow object     </li><li class="args">`**kwargs (Any)`: Unused</li></ul></p>|

---
<br>

 ## FargateTaskEnvironment
 <div class='class-sig' id='prefect-environments-execution-fargate-fargate-task-fargatetaskenvironment'><p class="prefect-sig">class </p><p class="prefect-class">prefect.environments.execution.fargate.fargate_task.FargateTaskEnvironment</p>(launch_type=&quot;FARGATE&quot;, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, region_name=None, executor=None, labels=None, on_start=None, on_exit=None, metadata=None, **kwargs)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/fargate/fargate_task.py#L32">[source]</a></span></div>

FargateTaskEnvironment is an environment which deploys your flow as a Fargate task.

DEPRECATED: Environment based configuration is deprecated, please transition to configuring `flow.run_config` instead of `flow.environment`. See [Flow configuration](/orchestration/flow_config/overview.html) for more info.

This environment requires AWS credentials and extra boto3 kwargs which are used in the creation and running of the Fargate task. When providing a custom container definition spec the first container in the spec must be the container that the flow runner will be executed on.

The following environment variables, required for cloud, do not need to be included––they are automatically added and populated during execution:

- `PREFECT__CLOUD__GRAPHQL` - `PREFECT__CLOUD__AUTH_TOKEN` - `PREFECT__CONTEXT__FLOW_RUN_ID` - `PREFECT__CONTEXT__IMAGE` - `PREFECT__CLOUD__USE_LOCAL_SECRETS` - `PREFECT__ENGINE__FLOW_RUNNER__DEFAULT_CLASS` - `PREFECT__ENGINE__TASK_RUNNER__DEFAULT_CLASS` - `PREFECT__CLOUD__SEND_FLOW_RUN_LOGS` - `PREFECT__LOGGING__EXTRA_LOGGERS`

Additionally, the following command will be applied to the first container:

`$ /bin/sh -c "python -c 'import prefect; prefect.environments.execution.load_and_run_flow()'"`

All `kwargs` are accepted that one would normally pass to boto3 for `register_task_definition` and `run_task`. For information on the kwargs supported visit the following links:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.register_task_definition

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.run_task

Note: You must provide `family` and `taskDefinition` with the same string so they match on run of the task.

The secrets and kwargs that are provided at initialization time of this environment are not serialized and will only ever exist on this object.

**Args**:     <ul class="args"><li class="args">`launch_type (str, optional)`: either FARGATE or EC2, defaults to FARGATE     </li><li class="args">`aws_access_key_id (str, optional)`: AWS access key id for connecting the boto3         client. Defaults to the value set in the environment variable         `AWS_ACCESS_KEY_ID` or `None`     </li><li class="args">`aws_access_key_id (str, optional)`: AWS access key id for connecting the boto3         client. Defaults to the value set in the environment variable         `AWS_ACCESS_KEY_ID` or `None`     </li><li class="args">`aws_secret_access_key (str, optional)`: AWS secret access key for connecting         the boto3 client. Defaults to the value set in the environment variable         `AWS_SECRET_ACCESS_KEY` or `None`     </li><li class="args">`aws_session_token (str, optional)`: AWS session key for connecting the boto3         client. Defaults to the value set in the environment variable         `AWS_SESSION_TOKEN` or `None`     </li><li class="args">`region_name (str, optional)`: AWS region name for connecting the boto3 client.         Defaults to the value set in the environment variable `REGION_NAME` or `None`     </li><li class="args">`executor (Executor, optional)`: the executor to run the flow with. If not provided, the         default executor will be used.     </li><li class="args">`labels (List[str], optional)`: a list of labels, which are arbitrary string         identifiers used by Prefect Agents when polling for work     </li><li class="args">`on_start (Callable, optional)`: a function callback which will be called before the         flow begins to run     </li><li class="args">`on_exit (Callable, optional)`: a function callback which will be called after the flow         finishes its run     </li><li class="args">`metadata (dict, optional)`: extra metadata to be set and serialized on this environment     </li><li class="args">`**kwargs (dict, optional)`: additional keyword arguments to pass to boto3 for         `register_task_definition` and `run_task`</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-environments-execution-fargate-fargate-task-fargatetaskenvironment-execute'><p class="prefect-class">prefect.environments.execution.fargate.fargate_task.FargateTaskEnvironment.execute</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/fargate/fargate_task.py#L409">[source]</a></span></div>
<p class="methods">Run the Fargate task that was defined for this flow.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow object</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-execution-fargate-fargate-task-fargatetaskenvironment-setup'><p class="prefect-class">prefect.environments.execution.fargate.fargate_task.FargateTaskEnvironment.setup</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/fargate/fargate_task.py#L379">[source]</a></span></div>
<p class="methods">Register the task definition if it does not already exist.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow object</li></ul></p>|

---
<br>

 ## KubernetesJobEnvironment
 <div class='class-sig' id='prefect-environments-execution-k8s-job-kubernetesjobenvironment'><p class="prefect-sig">class </p><p class="prefect-class">prefect.environments.execution.k8s.job.KubernetesJobEnvironment</p>(job_spec_file=None, unique_job_name=False, executor=None, labels=None, on_start=None, on_exit=None, metadata=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/k8s/job.py#L16">[source]</a></span></div>

KubernetesJobEnvironment is an environment which deploys your flow as a Kubernetes job. This environment allows (and requires) a custom job YAML spec to be provided.

DEPRECATED: Environment based configuration is deprecated, please transition to configuring `flow.run_config` instead of `flow.environment`. See [Flow configuration](/orchestration/flow_config/overview.html) for more info.

When providing a custom YAML job spec the first container in the spec must be the container that the flow runner will be executed on.

The following environment variables, required for cloud, do not need to be included––they are automatically added and populated during execution:

- `PREFECT__CLOUD__GRAPHQL` - `PREFECT__CLOUD__AUTH_TOKEN` - `PREFECT__CONTEXT__FLOW_RUN_ID` - `PREFECT__CONTEXT__NAMESPACE` - `PREFECT__CONTEXT__IMAGE` - `PREFECT__CLOUD__USE_LOCAL_SECRETS` - `PREFECT__ENGINE__FLOW_RUNNER__DEFAULT_CLASS` - `PREFECT__ENGINE__TASK_RUNNER__DEFAULT_CLASS` - `PREFECT__CLOUD__SEND_FLOW_RUN_LOGS` - `PREFECT__LOGGING__EXTRA_LOGGERS`

Additionally, the following command will be applied to the first container: `$ /bin/sh -c "python -c 'import prefect; prefect.environments.execution.load_and_run_flow()'"`

**Args**:     <ul class="args"><li class="args">`job_spec_file (str, optional)`: Path to a job spec YAML file. This path is only         used when the environment is built, so should refer to a file on the machine         used to build the flow.     </li><li class="args">`unique_job_name (bool, optional)`: whether to use a unique name for each job created         with this environment. Defaults to `False`     </li><li class="args">`executor (Executor, optional)`: the executor to run the flow with. If not provided, the         default executor will be used.     </li><li class="args">`labels (List[str], optional)`: a list of labels, which are arbitrary string         identifiers used by Prefect Agents when polling for work     </li><li class="args">`on_start (Callable, optional)`: a function callback which will be called before the         flow begins to run     </li><li class="args">`on_exit (Callable, optional)`: a function callback which will be called after the flow         finishes its run     </li><li class="args">`metadata (dict, optional)`: extra metadata to be set and serialized on this environment</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-environments-execution-k8s-job-kubernetesjobenvironment-execute'><p class="prefect-class">prefect.environments.execution.k8s.job.KubernetesJobEnvironment.execute</p>(flow, **kwargs)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/k8s/job.py#L113">[source]</a></span></div>
<p class="methods">Create a single Kubernetes job that runs the flow.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow object     </li><li class="args">`**kwargs (Any)`: additional keyword arguments to pass to the runner</li></ul> **Raises**:     <ul class="args"><li class="args">`Exception`: if the environment is unable to create the Kubernetes job</li></ul></p>|

---
<br>

 ## LocalEnvironment
 <div class='class-sig' id='prefect-environments-execution-local-localenvironment'><p class="prefect-sig">class </p><p class="prefect-class">prefect.environments.execution.local.LocalEnvironment</p>(executor=None, labels=None, on_start=None, on_exit=None, metadata=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/local.py#L10">[source]</a></span></div>

A LocalEnvironment class for executing a flow in the local process.

DEPRECATED: Environment based configuration is deprecated, please transition to configuring `flow.run_config` instead of `flow.environment`. See [Flow configuration](/orchestration/flow_config/overview.html) for more info.

**Args**:     <ul class="args"><li class="args">`executor (Executor, optional)`: the executor to run the flow with. If not provided, the         default executor will be used.     </li><li class="args">`labels (List[str], optional)`: a list of labels, which are arbitrary string         identifiers used by Prefect Agents when polling for work     </li><li class="args">`on_start (Callable, optional)`: a function callback which will be called before the         flow begins to run     </li><li class="args">`on_exit (Callable, optional)`: a function callback which will be called after the flow         finishes its run     </li><li class="args">`metadata (dict, optional)`: extra metadata to be set and serialized on this         environment</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-environments-execution-local-localenvironment-execute'><p class="prefect-class">prefect.environments.execution.local.LocalEnvironment.execute</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/execution/local.py#L54">[source]</a></span></div>
<p class="methods">Executes the flow in the local process.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow object</li></ul></p>|

---
<br>


<p class="auto-gen">This documentation was auto-generated from commit <a href='https://github.com/PrefectHQ/prefect/commit/n/a'>n/a</a> </br>on July 1, 2021 at 18:35 UTC</p>