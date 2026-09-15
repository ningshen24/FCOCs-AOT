# Prediction example

`mouse_qstr_example_input.csv` contains a real released descriptor row (PubChem CID 1017). Run:

```bash
python scripts/predict.py \
  --model mouse_qstr \
  --input examples/mouse_qstr_example_input.csv \
  --output examples/my_prediction.csv
```

The included `mouse_qstr_example_output.csv` shows the expected equation output. The same script supports all six released linear models; input columns must match the descriptor names in `models/specifications/models.json`.
