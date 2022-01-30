causes_list = {
    "fatal msg=Bootstrap failed to complete": "[OCP] Bootstrap failed to complete",
    "level=fatal msg=failed to initialize the cluster": "[OCP] failed to initialize the cluster",
    "failed to get CLI image: unable to wait for the 'cli' image in the stable stream to populate: timed out waiting for the condition": "[OCP-CI] failed to get CLI image",
    "pod \"e2e-azure-deploy-cnv-ipi-install-install\" failed": "[OCP] Bootstrap failure",
    "level=error msg=\"failed to list bundles\"": "[OCP-OLM]: failed to list bundles",
    "level=fatal msg=failed to fetch Cluster: failed to generate asset": "[Azure] Bootstrap failure - failed to fetch Cluster",
    "[Fail] [rfe_id:273]": "[CNV] KubeVirt Tests failure",
    "error: timed out waiting for the condition on pods/disks-images-provider": "[CNV] disks-images-provider timeout",
    "--- FAIL: TestTests ": "[CNV] KubeVirt Tests failure",
    "Process did not finish before 2h0m0s timeout": "[CNV] Deployment failure",
    "VM boot time could not be retrieved": "[CNV] VM boot time test failed",
    "send: spawn id exp5 not open": "[CNV] VM Uptime test failure",
    "-cnv-gather-extra failed after": "[OCP-CI-MG] cnv-gather-extra failed",
    "error: unable to read image registry.redhat.io/redhat/redhat-operator-index": "[Infra] registry.redhat.io Service Unavailable",
    "error: unable to read image brew.registry.redhat.io": "[Infra] brew.registry.redhat.io Unavailable",
    'level=error msg=Error: Error Deleting Network Security Rule "bootstrap_ssh_in"': "[OCP-Installer] Bootstrap resources destruction error",
    'level=error msg=Error: Unable to locate Storage Account': "[OCP-Installer] Bootstrap destruction error (Unable to locate Storage Account)",
    'ipi-deprovision-deprovision failed after': "[OCP-Installer] IPI Deprovision error",
    'Internal error occurred: admission plugin "LimitRanger" failed to complete mutation in': "[OCP] Internal Error"
}

advanced_causes_list = [
    ([
        'Error from server (NotFound): deployments.apps "hco-operator" not found',
        'failed with exit code 1, waiting 10 seconds to retry...',
        'cleanup'
    ], "[CNV] Deployment failure - hco-operator was not deployed"),
    ([
        "-n openshift-cnv --for delete",
        "WAIT_CSV_OUTPUT='error: timed out waiting for the condition on clusterserviceversions/kubevirt-hyperconverged-operator"
    ], "[CNV] Previous CSV removal failed"),
    ([
        "oc wait HyperConverged kubevirt-hyperconverged -n openshift-cnv --for condition=Available --timeout=30m",
        "error: timed out waiting for the condition on hyperconvergeds/kubevirt-hyperconverged"
    ], "[CNV] Deployment failure - CSV not available in time")
]