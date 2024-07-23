# Analyzing Social Bias in Large Language Models (LLMs) in Legal Contexts

## Overview

This project investigates the extent of social bias in Large Language Models (LLMs) used for legal judgments. Using a dataset containing outputs from various LLMs on legal prompts, this analysis aims to uncover potential biases in the models related to social and identity terms, including religion, region, and gender.

## Dataset

The dataset includes legal prompts and verdicts for different cases, with each file corresponding to an LLM and containing:
- Law descriptions
- Legal situations involving various social and identity terms
- True verdicts
- Predicted verdicts by the LLM

The dataset is available in the folder linked [https://github.com/google-research-datasets/nlp-fairness-for-india](#). Each file in the folder represents the output of a specific LLM.

## Project Structure

- `data/` - Directory containing the dataset files.
- `notebooks/` - Jupyter notebooks for exploratory data analysis and bias analysis.
- `scripts/` - Python scripts for model evaluation and bias metrics calculation.
- `results/` - Output folder for results and analysis.

## Installation

To run the analysis, ensure you have the necessary libraries installed. You can set up the environment using `pip`:

```bash
pip install -r requirements.txt
