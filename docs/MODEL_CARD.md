# Model card

## Intended use

FCOCs-AOT provides in-silico estimates of acute oral toxicity (`pLD50`) for PAE- and BP-related food-contact organic chemicals in mouse and rat. It is intended for screening, prioritization, hypothesis generation and support of chemical-safety assessment.

It is **not** a replacement for regulatory testing requirements or expert toxicological evaluation.

## Endpoints

`pLD50 = -log10(LD50 [mol/kg])`

Higher pLD50 corresponds to lower LD50 and therefore greater acute oral toxicity.

## Mouse QSTR

- n = 63 (48 training / 15 test)
- QSARINS 2.2.4, MLR/OLS, Rnd split
- 6 descriptors
- Reported: R² = 0.8626; Q²_LOO = 0.8137; external R² = 0.9223; external RMSE = 0.3377; CCC = 0.9008
- Leverage warning threshold h* = 0.4375

## Rat QSTR

- n = 67 (51 training / 16 test)
- QSARINS 2.2.4, MLR/OLS, Rnd split
- 5 descriptors
- Reported: R² = 0.8567; Q²_LOO = 0.8254; external R² = 0.8456; external RMSE = 0.2843; CCC = 0.9160
- h* = 0.3529

## Mouse q-RASTR

- Read-across: GK, 6 close source compounds, sigma = 0.5
- Final 6-variable MLR
- Reported: R² = 0.8873; Q²_LOO = 0.8518; external R² = 0.7919; external RMSE = 0.4430; CCC = 0.8595

## Rat q-RASTR

- Read-across: LK, 3 close source compounds, gamma = 0.75
- Final 5-variable MLR
- Reported: R² = 0.8399; **Q²_LOO = 0.8057**; external R² = 0.8219; external RMSE = 0.3077; CCC = 0.8954

## Mouse→Rat iQTTR

```text
rat_pLD50 = -0.2465756098 + 1.0618214544 * mouse_pLD50
```

20 training / 7 test; reported external R² = 0.7743, external RMSE = 0.3325.

## Rat→Mouse iQTTR

```text
mouse_pLD50 = 0.6421132156 + 0.7264473617 * rat_pLD50
```

20 training / 7 test; reported external R² = 0.9101, external RMSE = 0.1884.

## Applicability domain

The QSTR/q-RASTR models use leverage-based applicability-domain analysis together with residual diagnostics. Predictions outside the structural domain or with lower PRI should be interpreted cautiously.

## Limitations

- Chemical domain focuses on PAE/BP-related FCOCs.
- Descriptor-generation software dependencies are partly third-party/restricted.
- Revised Orange workflows are included and the previously conflicting NN/SVM settings now match Table S6; the exact Orange3 package/add-on version still needs authoritative recording for strict environment reproduction.
- Cleaned merged descriptor matrices are released, but the raw separate PaDEL and alvaDesc exports are not included; alvaDesc itself is proprietary/commercial.
- Models estimate acute lethality and do not characterize chronic, endocrine, reproductive, developmental or other toxicity endpoints.
