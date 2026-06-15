"""
Placeholder tests — fill in as the project grows.
Run with: pytest tests/ -v
"""
import os
import pytest


def test_model_file_exists():
    """Fails until you complete Checkpoint 1 and promote the weights."""
    model_path = os.path.join("models", "base", "best.pt")
    assert os.path.exists(model_path), (
        "Model not found. Complete Checkpoint 1: train and run 'make promote'."
    )


def test_config_files_exist():
    assert os.path.exists(os.path.join("configs", "train.yaml"))
    assert os.path.exists(os.path.join("configs", "inference.yaml"))


def test_data_structure_exists():
    assert os.path.exists(os.path.join("data", "processed", "train"))
    assert os.path.exists(os.path.join("data", "processed", "val"))
