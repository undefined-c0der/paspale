# Example Data Files

This directory contains example CSV files for testing.

## Expected Format

### Bar Charts (grouped)

```csv
label,method1,method2,method3
Workload A,1.0,1.5,2.0
Workload B,1.2,1.8,2.2
Workload C,0.9,1.4,1.9
```

- First column: group labels (shown on x-axis)
- Remaining columns: values for each bar in the group

### Stacked Charts

```csv
label,category1,category2,category3
Workload A,0.3,0.4,0.3
Workload B,0.25,0.45,0.3
Workload C,0.35,0.35,0.3
```

- Values should sum to 1.0 for normalized charts

### Line Charts

```csv
x,series1,series2
0,1.0,1.2
1,1.5,1.8
2,2.0,2.1
3,2.2,2.5
```

- First column: x-axis values
- Remaining columns: y values for each line
