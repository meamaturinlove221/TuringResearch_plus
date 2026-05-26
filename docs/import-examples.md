# Import Examples

Status: namespace facade examples.

Round: 155.

The preferred long-term imports use the new namespace facade packages. The
existing `turing_research_plus` imports remain supported for compatibility.

## Core

```python
from turing_research_core import Workspace, load_workspace_registry
```

Compatible legacy import:

```python
from turing_research_plus.workspace import Workspace, load_workspace_registry
```

## Paper

```python
from turing_research_paper import PaperScaffold, build_vggt_paper_scaffold
```

Compatible legacy import:

```python
from turing_research_plus.paper_write import PaperScaffold, build_vggt_paper_scaffold
```

## Artifact

```python
from turing_research_artifact import ArtifactAuditReport, artifact_audit
```

Compatible legacy import:

```python
from turing_research_plus.artifact_audit import ArtifactAuditReport, artifact_audit
```

## Experiment

```python
from turing_research_experiment import ExperimentRouteSpec, compile_experiment_route
```

Compatible legacy import:

```python
from turing_research_plus.experiment_route import ExperimentRouteSpec, compile_experiment_route
```

## Dashboard / Export

```python
from turing_research_dashboard import DashboardCard, build_static_dashboard
```

Compatible legacy import:

```python
from turing_research_plus.ui import DashboardCard, build_static_dashboard
```

## Plugins

```python
from turing_research_plugins import PluginManifest, load_plugin_manifest
```

Compatible legacy import:

```python
from turing_research_plus.plugins import PluginManifest, load_plugin_manifest
```

## Cases

```python
from turing_research_cases import BenchmarkReport, run_benchmark_scenario
```

Compatible legacy import:

```python
from turing_research_plus.benchmark import BenchmarkReport, run_benchmark_scenario
```

## Compatibility Alias Registry

```python
from turing_research_plus.compat import legacy_module_for

legacy = legacy_module_for("turing_research_core", "workspace")
```

## Boundary

These examples are import examples only. They do not run live adapters, execute
plugins, read private project paths, or promote demo/planned material to
observed evidence.
