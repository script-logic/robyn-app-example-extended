# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

import warnings
from pathlib import Path

from pydantic import BaseModel, field_validator, model_validator


class FilesystemSettings(BaseModel):
    logs_dir: Path = Path("./logs")
    max_log_file_size_mb: int = 10
    log_backup_count: int = 5
    logs_file_name: Path = Path("logger.log")

    @field_validator("*", mode="after")
    @classmethod
    def ensure_absolute_paths[T](cls, v: T) -> Path | T:
        if isinstance(v, Path) and not v.is_absolute():
            return v.resolve()
        return v

    @model_validator(mode="after")
    def create_directories(self) -> FilesystemSettings:
        directories_to_create = [(self.logs_dir, "logs")]

        for directory, name in directories_to_create:
            try:
                if not directory.exists():
                    directory.mkdir(parents=True, exist_ok=True)
                    msg = f"Directory created: {name} -> {directory}"
                    warnings.warn(msg, stacklevel=1)
                else:
                    msg = f"Directory ready: {name} -> {directory}"
                    warnings.warn(msg, stacklevel=1)

                test_file = directory / ".permissions_test"
                try:
                    test_file.touch(exist_ok=True)
                    test_file.unlink(missing_ok=True)
                except PermissionError, OSError:
                    msg = (
                        f"No write permissions in directory: {directory}. "
                        "Some features may not work correctly."
                    )
                    warnings.warn(msg, stacklevel=1)

            except PermissionError as e:
                msg = (
                    f"Cannot create directory [{directory}] "
                    f"Check write permissions for the application."
                )
                warnings.warn(msg, stacklevel=1)
                raise PermissionError(msg) from e
            except Exception as e:
                msg = f"Failed to create required directory: {directory}"
                warnings.warn(msg, stacklevel=1)
                raise RuntimeError(msg) from e

        return self
