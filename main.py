#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-or-later

import sys
import os
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1
from flask import Flask


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    This method will wait for the extended (long-running) operation to
    complete. If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def start_instance(project_id: str, zone: str, instance_name: str) -> None:
    """
    Starts a stopped Google Compute Engine instance (with unencrypted disks).
    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to start.
    """
    instance_client = compute_v1.InstancesClient()

    operation = instance_client.start(
        project=project_id, zone=zone, instance=instance_name
    )

    wait_for_extended_operation(operation, "instance start")
    return

def stop_instance(project_id: str, zone: str, instance_name: str) -> None:
    """
    Stops a running Google Compute Engine instance.
    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to stop.
    """
    instance_client = compute_v1.InstancesClient()

    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance stopping")
    return

app = Flask(__name__)
project=os.environ["PROJECT"]
zone=os.environ["ZONE"]
instance=os.environ["INSTANCE"]

@app.route("/")
def hello_world():
    return "pong"

@app.route("/start")
def start():
    start_instance(project, zone, instance)
    return "done"

@app.route("/stop")
def stop():
    stop_instance(project, zone, instance)
    return "done"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
