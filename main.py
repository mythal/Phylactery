#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-or-later

import sys
import os
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1
from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str, timeout: int = 300
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
        This method will raise the exception received from
        `operation.exception()` or RuntimeError if there is no exception set,
        but there is an `error_code` set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to
        complete, a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]",
            f"{operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warn during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}",
                  file=sys.stderr, flush=True)

    return result


def start_instance(project_id: str, zone: str, instance_name: str) -> None:
    """
    Starts a stopped Google Compute Engine instance (with unencrypted disks).
    Args:
        project_id: project ID or project number of the Cloud project your
          instance belongs to.
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
        project_id: project ID or project number of the Cloud project your
          instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to stop.
    """
    instance_client = compute_v1.InstancesClient()

    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance stopping")
    return


port = int(os.getenv("PORT", "3000"))
project = os.environ["PROJECT"]
zone = os.environ["ZONE"]
instance = os.environ["INSTANCE"]
token = os.environ["TOKEN"]
# Use for endpoint. xxxx.xxx.moe/{secret}
secret = os.getenv("SECRET", "")
# Url to this bot.
self_endpoint = os.environ["ENDPOINT"]
group_id = int(os.environ["CHAT_ID"])
admin_id = os.getenv("ADMIN_ID") and int(os.getenv("ADMIN_ID"))


# bot
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id != group_id:
        context.bot.send_message(chat_id=chat_id, text="403")
        return

    context.bot.send_message(chat_id=chat_id, text=f"Starting {instance}...")
    start_instance(project, zone, instance)
    context.bot.send_message(chat_id=chat_id, text=f"{instance} is started")


def stop(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.effective_chat.id != group_id:
        context.bot.send_message(chat_id=chat_id, text="403")
        return

    if admin_id is not None and update.message.from_user.id != admin_id:
        context.bot.send_message(chat_id=chat_id, text="403")
        return

    context.bot.send_message(chat_id=chat_id, text=f"Stopping {instance}...")
    stop_instance(project, zone, instance)
    context.bot.send_message(chat_id=chat_id, text=f"{instance} is stopped")


# For test
def ping(update: Update, context: CallbackContext):
    if update.effective_chat.id != group_id:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"403 {update.effective_chat.id}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="pong")


if __name__ == "__main__":
    updater = Updater(token=token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("stop", stop))
    updater.dispatcher.add_handler(CommandHandler("ping", ping))
    updater.start_webhook(listen="0.0.0.0", port=port, url_path=secret,
                          webhook_url=f"{self_endpoint}/{secret}")
